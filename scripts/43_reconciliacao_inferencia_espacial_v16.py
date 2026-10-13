#!/usr/bin/env python3
"""Reavaliacao de inferencia espacial da v16 em 5506 municipios, sem alterar saidas.

OLS/WLS por pleito: 3 controles locais + 4 dummies de macrorregiao +
3 medias de atributos locais nos oito vizinhos. Teste conjunto de WX(3)
com CR1/UF (F[3,26]) e HAC Conley-Bartlett 100 e 250 km (chi2[3]).
Buffers de exclusao de treino de 0, 100 e 250 km, 2018/2022, C/M e
pesos uniforme/populacional; cinco folds com UFs inteiras no teste.
O arquivo de entrada principal e reconstruido a partir dos insumos
versionados no repositorio, SEM nova coleta.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import chi2, f

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"scripts"
OUT=ROOT/"outputs/reconciliacao_inferencia_espacial_v16_v01"
BASEPATH=ROOT/"outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_geografica_2002_2022.csv"

def imp(name,filename):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

m=imp("modelos_v16_43","36_modelos_seis_eleicoes_censo_anterior.py")
geo=imp("conley_original_43","20_inferencia_espacial_validacao.py")

SOURCE={
    "mapa":"outputs/municipal_v01/chaves_tse_ibge_5570_centroides.csv",
    "ibge_historico":"outputs/controles_ibge_historicos_v01/controles_2002_2006_2010.csv",
    "ibge_2014":"outputs/piloto_2014_ibge_v01/controles_IBGE_para_eleicao_2014.csv",
    "ibge_2018_2022":"data/ibge_tratados/controles_pre_eleitorais_v02.csv",
    "votos_2002":"outputs/inventario_tse_historico_v01/2002/votos_presidenciais_municipais_2002.csv",
    "votos_2006":"outputs/inventario_tse_historico_v01/2006/votos_presidenciais_municipais_2006.csv",
    "votos_2010":"outputs/inventario_tse_historico_v01/2010/votos_presidenciais_municipais_2010.csv",
    "votos_2014":"outputs/piloto_2014_v01/votos_2014_segundo_turno_municipios.csv",
    "votos_2018_2022":"outputs/competitividade_v02/competitividade_e_margem_assinada_segundo_turno.csv",
}
YEARS=m.YEARS
COLUMNS={"competitividade":"competitividade_2t","direcao_pt13":"margem_assinada_pt13"}

def fit_spatial(x,y,w,groups,kernels):
    """Replica CR1/Conley do script 20, trocando q_contexto=4 por 3."""
    n=x.shape[0]
    q=x.shape[1]
    mu=x.mean(axis=0)
    sd=x.std(axis=0)
    if np.any(sd<1e-12):raise ValueError("Preditor constante")
    X=np.column_stack([np.ones(n),(x-mu)/sd])
    q=X.shape[1]
    if np.linalg.matrix_rank(X)!=q:raise ValueError("Matriz singular")
    sw=np.sqrt(w)
    A=X*sw[:,None]
    b=y*sw
    inv=np.linalg.inv(A.T@A)
    beta=inv@(A.T@b)
    resid=b-A@beta
    scores=A*resid[:,None]
    theta=beta[-3:]
    unique=np.sort(np.unique(groups))
    G=len(unique)
    if G!=27:raise ValueError("UFs diferentes de 27")
    meat=np.zeros((q,q))
    for state in unique:
        v=scores[groups==state].sum(axis=0)
        meat+=np.outer(v,v)
    corr=(G/(G-1))*((n-1)/(n-q))
    cov=inv@meat@inv*corr
    cov=(cov+cov.T)/2
    q3=cov[-3:,-3:]
    F=float(theta@np.linalg.pinv(q3)@theta/3)
    result={"wald_F3_CR1":F,"p_uf_CR1":float(f.sf(max(F,0),3,G-1))}
    for km,(K,n_pairs) in kernels.items():
        meat=scores.T@(K@scores)
        C=inv@meat@inv
        C=(C+C.T)/2
        chi=float(theta@np.linalg.pinv(C[-3:,-3:])@theta)
        result[f"wald_chi2_conley_{km}"]=chi
        result[f"p_conley_{km}"]=float(chi2.sf(max(chi,0),3))
        result[f"n_pares_conley_{km}"]=n_pairs
    result["coef_contexto_3"]=json.dumps([float(v) for v in theta])
    return result

def buffered_cv(d,x0,x1,y,w,xyz,km,year,outcome,weight):
    group=d.SG_UF.to_numpy()
    ufs=np.sort(np.unique(group))
    states=[]
    folds=[]
    threshold=2*np.sin(km/(2*6371.0088))
    for fold in range(5):
        test=np.isin(group,ufs[fold::5])
        train=~test
        if km:
            dist=cKDTree(xyz[test]).query(xyz[train],k=1)[0]
            ids=np.flatnonzero(train)
            train[ids[dist<=threshold]]=False
        if np.any(train&test) or train.sum()<1000 or test.sum()<250:
            raise ValueError("Treino ou teste invalido")
        p0=m.g.predict(x0[train],x0[test],y[train],w[train],logit=False)
        p1=m.g.predict(x1[train],x1[test],y[train],w[train],logit=False)
        observed=y[test]
        wt=w[test]
        for uf in np.unique(group[test]):
            ix=group[test]==uf
            states.append({"UF":uf,
                "fold":fold+1,
                "weight_sum":float(wt[ix].sum()),
                "sse_baseline":float(np.sum(wt[ix]*(observed[ix]-p0[ix])**2)),
                "sse_contexto":float(np.sum(wt[ix]*(observed[ix]-p1[ix])**2))})
        folds.append({"ano":year,"desfecho":outcome,"ponderacao":weight,
            "buffer_km":km,"fold":fold+1,
            "n_train":int(train.sum()),"n_test":int(test.sum()),
            "n_excluido_buffer":int((~train&~test).sum())})
    if len(states)!=27:raise ValueError("UF duplicada/ausente")
    seed=20261012+year*13+int(outcome=="direcao_pt13")*10+int(weight=="populacao_anterior")*5+km*1009
    stats=m.bootstrap(states,seed)
    return stats,states,folds

def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise SystemExit("Saida existente, abortando para preservar originais")
    for file in SOURCE.values():
        if not (ROOT/file).is_file():raise FileNotFoundError(file)
    args=SimpleNamespace(**{key:ROOT/value for key,value in SOURCE.items()})
    panel,coverage=m.build_panel(args)
    if len(panel)!=33036 or len(panel.CD_MUNICIPIO_IBGE.unique())!=5506:
        raise AssertionError("Panel diferente da v16")
    if panel.groupby("ano").size().to_dict()!={int(yr):5506 for yr in YEARS}:
        raise AssertionError("Distribuicao de anos inesperada")
    data={yr:m.year_data(panel,yr) for yr in YEARS}
    ref=pd.read_csv(BASEPATH)
    infer=[]
    buffers=[]
    sse=[]
    folds=[]
    # Cria UMA matriz de kernel por coordenada; a amostra balanceada repete geometria.
    d0=data[2002][0]
    xyz=geo.xyz_da_latlon(d0)
    kernels={km:geo.kernel_conley(xyz,km) for km in (100,250)}
    ids0=d0.CD_MUNICIPIO_IBGE.astype(str).to_numpy()
    for year in YEARS:
        d,x0,x1=data[year]
        ids=d.CD_MUNICIPIO_IBGE.astype(str).to_numpy()
        if not np.array_equal(ids,ids0):
            raise ValueError("Ordem/geometria muda entre eleicoes")
        if not np.allclose(geo.xyz_da_latlon(d),xyz):
            raise ValueError("Coordenadas inconsistentes")
        for outcome,col in COLUMNS.items():
            y=d[col].to_numpy(float)
            for weight in ("uniforme","populacao_anterior"):
                w=np.ones(len(d)) if weight=="uniforme" else d.pop_previa.to_numpy(float)
                r=fit_spatial(x1,y,w,d.SG_UF.to_numpy(),kernels)
                infer.append({"ano":year,"desfecho":outcome,"ponderacao":weight,
                    "n":len(d),"n_uf":27,"n_contextuais":3,**r})
                # Buffers analisados especificamente para a divergencia v12 x v16.
                if year not in (2018,2022):
                    continue
                for km in (0,100,250):
                    gain,recs,parts=buffered_cv(d,x0,x1,y,w,xyz,km,year,outcome,weight)
                    if km==0:
                        match=ref[(ref.ano==year)&(ref.desfecho==outcome)&
                            (ref.ponderacao==weight)&(ref.familia=="linear")]
                        if len(match)!=1:
                            raise AssertionError("Benchmark da v16 nao localizado")
                        err=abs(float(match.iloc[0].ganho_rmse_pct)-gain["ganho_rmse_pct"])
                        if err>2e-6:
                            raise AssertionError(f"Benchmark 0 km nao reproduzido: {year} {outcome} {weight} {err}")
                    buffers.append({"ano":year,"desfecho":outcome,"ponderacao":weight,
                        "familia":"linear","buffer_km":km,"n_teste":len(d),
                        "n_train_min":min(v["n_train"] for v in parts),
                        "n_train_max":max(v["n_train"] for v in parts),
                        "n_buffer_min":min(v["n_excluido_buffer"] for v in parts),
                        "n_buffer_max":max(v["n_excluido_buffer"] for v in parts),
                        "ganho_rmse_pct":gain["ganho_rmse_pct"],
                        "rmse_baseline":gain["rmse_baseline"],
                        "rmse_contexto":gain["rmse_contexto"],
                        "ic95_inf":gain["ic95_uf_inf"],
                        "ic95_sup":gain["ic95_uf_sup"],
                        "ufs_piora":gain["ufs_piora"]})
                    sse.extend([{"ano":year,"desfecho":outcome,"ponderacao":weight,
                        "buffer_km":km,**v} for v in recs])
                    folds.extend(parts)
    a=pd.DataFrame(infer)
    b=pd.DataFrame(buffers)
    if len(a)!=24 or len(b)!=24 or len(sse)!=24*27 or len(folds)!=24*5:
        raise ValueError(f"Contagens incorretas infer={len(a)} buffer={len(b)}")
    for field in ("p_uf_CR1","p_conley_100","p_conley_250"):
        if not a[field].between(0,1).all():raise ValueError("p fora [0,1]")
    OUT.mkdir(parents=True,exist_ok=False)
    a.to_csv(OUT/"wald_cr1_conley_v16.csv",index=False,float_format="%.10f")
    b.to_csv(OUT/"buffer_geografico_v16.csv",index=False,float_format="%.10f")
    pd.DataFrame(sse).to_csv(OUT/"sse_uf_buffer_v16.csv",index=False,float_format="%.10f")
    pd.DataFrame(folds).to_csv(OUT/"folds_buffer_v16.csv",index=False)
    manifest={
        "autor":"Jacson Cruz do Nascimento",
        "tipo":"Reavaliacao da inferencia espacial: v16 de 2002-2022, sem 1998",
        "n_municipios":5506,"n_obs":33036,"n_uf":27,
        "anos":list(YEARS),"anos_buffer":[2018,2022],
        "outcomes":["competitividade","direcao_pt13"],
        "censo":"2000 para 2002/2006/2010; 2010 para 2014/2018/2022",
        "regressoras":"3 locais + 4 macrorregiao + 3 medias k8",
        "contraste":"teste conjunto de 3 medias contextuais, nao causal",
        "infer_CR1":"WLS transformado, cluster UF (27), correcao CR1, F(3,26)",
        "infer_Conley":"Bartlett arco grande circulo com centroides IBGE 2022, 100/250km; Wald chi2(3) assintotico",
        "cv_espacial":"5 folds fixos por UF; buffer 0/100/250 km no treino; todas as UFs de teste fora",
        "bootstrap":"4.999 reamostragens condicionais das 27 contribuicoes estaduais com folds fixos",
        "integridade":"Buffer 0km cotejado com outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_geografica_2002_2022.csv",
        "vintage":"Atributos IBGE do repositorio recuperados retrospectivamente; nenhuma previsao ex ante",
        "entradas_sha256":{k:hashlib.sha256((ROOT/v).read_bytes()).hexdigest() for k,v in SOURCE.items()},
        "limitacoes":[
            "CR1 pressupoe independencia entre estados distintos",
            "Conley depende do raio e nao corrige endogeneidade, seletividade ou unidade territorial",
            "A mesma cidade aparece em eleicoes diferentes, mas inferencia aplicada POR PLEITO",
            "WX usa covariaveis IBGE de UFs de teste (informacao transdutiva), nunca os votos dessas UFs",
            "1998 excluido, nenhum voto externo ou VT imputado, sem causalidade social",
            "Multiplos testes sao exploratorios sem correcao por multiplicidade",
            "Conley nao corrige sozinho inferencia dos ganhos fora da amostra"
        ]}
    (OUT/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("INFERENCIA ESPACIAL")
    print(a[["ano","desfecho","ponderacao","wald_F3_CR1","p_uf_CR1","p_conley_100","p_conley_250"]].to_string(index=False))
    print("VALIDACAO BUFFER")
    print(b[["ano","desfecho","ponderacao","buffer_km","ganho_rmse_pct","ic95_inf","ic95_sup"]].to_string(index=False))

if __name__=="__main__":
    main()
