#!/usr/bin/env python3
"""Validação espacial com exclusão de uma faixa de treinamento próxima às UFs de teste.

Reestima a generalização por cinco folds de UFs inteiras omitidas, porém
exclui adicionalmente observações de TREINO com centroides a menos de
100/250 quilômetros do centroide de qualquer município de TESTE.
Recalcula os dois modelos em idêntica amostra de treino em cada fold.
Contexto WX usa exclusivamente indicadores IBGE (sem voto), com k=8
fixado antes da partição. Dados IBGE 2026: análise retrospectiva.
"""
import argparse, json, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

HERE=Path(__file__).resolve().parent
def load(name,file):
    sp=importlib.util.spec_from_file_location(name,HERE/file)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
g=load("geo_buff","22_benchmark_geografico_competitividade.py")
s=load("inference_buff","20_inferencia_espacial_validacao.py")

def mask_training(d,fold,km):
    ufs=np.sort(d.SG_UF.unique())
    test=d.SG_UF.isin(ufs[fold::5]).to_numpy()
    training=~test
    if km>0:
        xyz=s.xyz_da_latlon(d)
        rad=km/6371.0088
        chord=2*np.sin(rad/2)
        nearest=cKDTree(xyz[test]).query(xyz[training],k=1)[0]
        trainids=np.flatnonzero(training)
        training[trainids[nearest<=chord]]=False
    assert not np.any(test & training)
    assert test.sum()>250 and training.sum()>1000
    return training,test

def cv_buffer(d,x,wx,y,w,buffer_km,year,outcome,weightname,logit):
    rec=[];fold_rows=[]
    full=np.column_stack([x,wx])
    for fold in range(5):
        train,test=mask_training(d,fold,buffer_km)
        p0=g.predict(x[train],x[test],y[train],w[train],logit=logit)
        p1=g.predict(full[train],full[test],y[train],w[train],logit=logit)
        gtest=d.SG_UF.to_numpy()[test];yt=y[test];wt=w[test]
        for uf in np.unique(gtest):
            chosen=gtest==uf
            rec.append({"UF":str(uf),"fold":fold+1,"n_test":int(chosen.sum()),
                        "weight_sum":float(wt[chosen].sum()),
                        "sse_local":float(np.sum(wt[chosen]*(yt[chosen]-p0[chosen])**2)),
                        "sse_contextual":float(np.sum(wt[chosen]*(yt[chosen]-p1[chosen])**2)),
                        "n_train":int(train.sum()),
                        "n_buffer_excluded":int((~train & ~test).sum())})
        fold_rows.append({"ano":year,"desfecho":outcome,"ponderacao":weightname,
                          "familia":"logit_fracionario" if logit else "linear",
                          "buffer_km":buffer_km,"fold":fold+1,
                          "n_train":int(train.sum()),"n_test":int(test.sum()),
                          "n_buffer_excluded":int((~train & ~test).sum())})
    vals=np.array([[r["weight_sum"],r["sse_local"],r["sse_contextual"]] for r in rec],float)
    assert len(rec)==27 and vals[:,0].sum()>0
    rmse_local=np.sqrt(vals[:,1].sum()/vals[:,0].sum())
    rmse_context=np.sqrt(vals[:,2].sum()/vals[:,0].sum())
    gain=100*(rmse_local-rmse_context)/rmse_local
    seed=20261011+year*21+buffer_km*17+(outcome=="direcao_pt13")*4+(weightname=="populacao_anterior")*3+int(logit)
    rng=np.random.default_rng(seed)
    draws=rng.integers(0,27,size=(4999,27))
    sums=vals[draws].sum(axis=1)
    gains=100*(1-np.sqrt(sums[:,2]/sums[:,1]))
    return {
        "ano":year,"desfecho":outcome,"ponderacao":weightname,
        "benchmark":"socio_mais_macrorregiao",
        "familia":"logit_fracionario" if logit else "linear",
        "buffer_km":buffer_km,"rmse_local":float(rmse_local),"rmse_contextual":float(rmse_context),
        "ganho_rmse_pct":float(gain),"ic_uf_inf":float(np.quantile(gains,.025)),
        "ic_uf_sup":float(np.quantile(gains,.975)),
        "ufs_com_piora":int(np.count_nonzero(vals[:,2]>vals[:,1])),
        "municipios_teste_total":int(sum(v["n_test"] for v in fold_rows)),
        "n_train_min":int(min(v["n_train"] for v in fold_rows)),
        "n_train_max":int(max(v["n_train"] for v in fold_rows)),
        "excluidos_buffer_min":int(min(v["n_buffer_excluded"] for v in fold_rows)),
        "excluidos_buffer_max":int(max(v["n_buffer_excluded"] for v in fold_rows))
    },rec,fold_rows

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    for k in ("mapa","hhi","ibge","competitividade","out"): pa.add_argument("--"+k,type=Path,required=True)
    a=pa.parse_args()
    if a.out.exists() and any(a.out.iterdir()):
        raise SystemExit("Preservar saídas anteriores.")
    panel,excluded=g.base.preparar(a.mapa,a.hhi,a.ibge,a.competitividade)
    results=[];peruf=[];folds=[]
    for ano in (2018,2022):
        d,bench,wx=g.data_year(panel,ano)
        x=bench["socio_mais_macrorregiao"]
        for outcome,col in g.OUTCOMES.items():
            y=d[col].to_numpy(float)
            for typ in ("uniforme","populacao_anterior"):
                w=np.ones(len(d)) if typ=="uniforme" else d["pop_2017" if ano==2018 else "pop_2021"].to_numpy(float)
                for km in (0,100,250):
                    for logit in (False,True) if outcome=="competitividade" else (False,):
                        item,records,foldrecs=cv_buffer(d,x,wx,y,w,km,ano,outcome,typ,logit)
                        results.append(item)
                        peruf.extend([{**{k:item[k] for k in ("ano","desfecho","ponderacao","familia","buffer_km")},**r} for r in records])
                        folds.extend(foldrecs)
    a.out.mkdir(parents=True,exist_ok=True)
    t=pd.DataFrame(results)
    if len(t)!=36 or t.municipios_teste_total.ne(5565).any():
        raise ValueError("Tabela de 36 comparações inválida")
    # 0 km deve reproduzir benchmark v02 a partir das mesmas cinco dobras.
    benchmark=pd.read_csv("outputs/benchmark_geografico_v02/comparacao_benchmarks_regionais.csv")
    for _,r in t[t.buffer_km.eq(0)].iterrows():
        ref=benchmark[(benchmark.ano==r.ano)&(benchmark.desfecho==r.desfecho)&
             (benchmark.ponderacao==r.ponderacao)&
             (benchmark.benchmark.eq("socio_mais_macrorregiao"))&
             (benchmark.familia==r.familia)]
        if len(ref)!=1 or abs(ref.iloc[0].reducao_rmse_pct-r.ganho_rmse_pct)>1e-6:
            raise ValueError("Benchmark 0 km não reproduziu: "+r.to_json())
    t.to_csv(a.out/"validacao_uf_buffer_espacial.csv",index=False,float_format="%.10f")
    pd.DataFrame(peruf).to_csv(a.out/"sse_por_uf_buffer_espacial.csv",index=False,float_format="%.10f")
    pd.DataFrame(folds).to_csv(a.out/"folds_buffer_espacial.csv",index=False)
    manifest={"autor":"Jacson Cruz do Nascimento","universo":5565,"anos":[2018,2022],
      "buffer_km":[0,100,250],"folds":5,"amostra_teste":"mesmas cinco dobras de UFs de origem, um estado sempre totalmente excluído do treino",
      "amostra_treino":"UFs não testadas, excetuando município com centroide a <= raio de município de teste",
      "modelo":"Controles locais + quatro dummies macrorregionais; comparar com adição de médias de k8 municípios",
      "familia":"OLS/WLS linear; logit fracionario somente para competitividade",
      "usos_do_contexto":"WX de IBGE pode incluir covariáveis de UFs testadas; não há vazamento do DESFECHO eleitoral; sensibilidade transdutiva",
      "inferencias":["Buffer geométrico não assegura independência residual entre UFs remotas.","Número de municípios de treino diminui com raio do buffer.","Bootstrap UF de 4999 repetições sobre SSE observado em folds fixos; IC exploratório.","Testes de 2018 e 2022 são retrospectivos, com dados de vintages revisados.","Mudança de buffer modifica o conjunto de treino; não isola impacto causal."],
      "benchmark_reproduzido":"outputs/benchmark_geografico_v02/comparacao_benchmarks_regionais.csv",
      "municipios_excluidos_IBGE":excluded}
    (a.out/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(t[["ano","desfecho","ponderacao","familia","buffer_km","ganho_rmse_pct","ic_uf_inf","ic_uf_sup","n_train_min"]].to_string(index=False))
if __name__=="__main__":main()
