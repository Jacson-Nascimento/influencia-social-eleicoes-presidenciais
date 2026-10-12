#!/usr/bin/env python3
"""Exploração C/M presidencial 2014–2018–2022 com amostra municipal comum.

Experimentos separados da publicação v14:
(1) 5 dobras por UF por ano; (2) validação temporal 2014=>2018,
2018=>2022 e 2014+2018=>2022. Todos os estimadores são treinados de novo.
Controles IBGE usam PIB/popolação pré-pleito; WX de k=8 usa apenas IBGE.
Importante: reuso da mesma cidade em anos diferentes é intencional nos
testes temporais; não se trata de previsão em tempo real.
"""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import importlib.util

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("geo30",HERE/"22_benchmark_geografico_competitividade.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

Y={"competitividade":"competitividade_2t","direcao_pt13":"margem_assinada_pt13"}
X=["log_pop","log_pibpc_proxy","urbanizacao_2010","fracao_feminina_2010"]
UFKEY=["SG_UF","CD_MUNICIPIO"]
def load_data(a):
    v14=pd.read_csv(a.votos2014,dtype={"CD_MUNICIPIO_IBGE":str})
    c14=pd.read_csv(a.controles2014,dtype={"CD_MUNICIPIO_IBGE":str})
    map_=pd.read_csv(a.mapa,dtype={"CD_MUNICIPIO_IBGE":str})
    old=pd.read_csv(a.votos2018_2022)
    ibge=pd.read_csv(a.controles2018_2022,dtype={"CD_MUNICIPIO_IBGE":str})
    assert len(v14)==5570 and len(map_)==5570 and len(old)==11140
    assert set(old.ano)=={2018,2022}
    assert len(c14)==5570
    v14=v14.merge(c14[["CD_MUNICIPIO_IBGE"]+X+["pop_2013"]],on="CD_MUNICIPIO_IBGE",validate="one_to_one")
    v14["pop_antes"]=v14.pop_2013
    all_=[v14[["ano","CD_MUNICIPIO_IBGE","SG_UF","CD_MUNICIPIO","latitude","longitude","pop_antes"]+X+list(Y.values())]]
    old=old.merge(map_[["SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude"]],
        how="left",on=UFKEY,validate="many_to_one")
    old=old.merge(ibge,on="CD_MUNICIPIO_IBGE",validate="many_to_one",how="left")
    for ano in (2018,2022):
        d=old[old.ano==ano].copy()
        pop="pop_2017" if ano==2018 else "pop_2021"
        pib="pibpc_proxy_2016_2017_reais" if ano==2018 else "pibpc_proxy_2020_2021_reais"
        d["pop_antes"]=d[pop]
        d["log_pop"]=np.log(d[pop].where(d[pop]>0))
        d["log_pibpc_proxy"]=np.log(d[pib].where(d[pib]>0))
        all_.append(d[["ano","CD_MUNICIPIO_IBGE","SG_UF","CD_MUNICIPIO","latitude","longitude","pop_antes"]+X+list(Y.values())])
    combined=pd.concat(all_,ignore_index=True)
    if len(combined)!=5570*3:raise AssertionError("Painel não contém os três pleitos")
    essential=X+["pop_antes"]+list(Y.values())+["latitude","longitude"]
    complete=combined[essential].notna().all(axis=1)
    common=combined.loc[complete].groupby("CD_MUNICIPIO_IBGE").ano.nunique()
    common=sorted(common[common==3].index)
    p=combined[combined.CD_MUNICIPIO_IBGE.isin(common)].copy()
    if len(common)!=5564 or len(p)!=3*len(common):
        raise ValueError(f"Amostra comum inesperada: {len(common)}")
    if (p.pop_antes<=0).any() or not p.competitividade_2t.between(0,1).all():
        raise ValueError("Indicadores inválidos")
    if not np.allclose(p.competitividade_2t,1-p.margem_assinada_pt13.abs()):
        raise ValueError("C e M não conciliados")
    return p,common,combined

def matrices(panel,year):
    d=panel[panel.ano==year].copy().sort_values(UFKEY).reset_index(drop=True)
    if len(d)!=5564 or d.SG_UF.nunique()!=27:raise ValueError("Cobertura inesperada")
    x=d[X].to_numpy(float)
    reg=d.SG_UF.map(g.uf_region)
    cats=pd.Categorical(reg,categories=["S","SE","CO","NE","N"])
    mac=pd.get_dummies(cats,drop_first=True,dtype=float).to_numpy()
    if mac.shape!=(len(d),4):raise ValueError("Regiões inconsistentes")
    b=np.column_stack([x,mac])
    k=g.sp.knn(d,8)
    wx=x[k].mean(axis=1)
    return d,b,np.column_stack([b,wx])

def bootstrap(records,seed,n=4999):
    z=np.array([[r["weight_sum"],r["sse_local"],r["sse_contexto"]] for r in records],float)
    if len(z)!=27 or z[:,0].min()<=0: raise ValueError("UF omitida da validação.")
    a=np.sqrt(z[:,1].sum()/z[:,0].sum())
    b=np.sqrt(z[:,2].sum()/z[:,0].sum())
    rng=np.random.default_rng(seed)
    dr=rng.integers(0,27,size=(n,27))
    sums=z[dr].sum(axis=1)
    sim=100*(1-np.sqrt(sums[:,2]/sums[:,1]))
    return {"rmse_local":float(a),"rmse_contexto":float(b),
        "ganho_rmse_pct":float(100*(1-b/a)),
        "ic95_uf_inf":float(np.quantile(sim,.025)),
        "ic95_uf_sup":float(np.quantile(sim,.975)),
        "ufs_com_piora":int((z[:,2]>z[:,1]).sum())}

def temporal(train_years,test_year,frames,feat,outcome,weight,logit=False,seed=0):
    d=pd.concat([frames[y] for y in train_years],ignore_index=True)
    test=frames[test_year]
    base_tr=np.concatenate([feat[y][0] for y in train_years])
    full_tr=np.concatenate([feat[y][1] for y in train_years])
    base_te,full_te=feat[test_year]
    col=Y[outcome]
    ytr=d[col].to_numpy(float); yte=test[col].to_numpy(float)
    wtr=np.ones(len(d)) if weight=="uniforme" else d.pop_antes.to_numpy(float)
    wte=np.ones(len(test)) if weight=="uniforme" else test.pop_antes.to_numpy(float)
    p0=g.predict(base_tr,base_te,ytr,wtr,logit=logit)
    p1=g.predict(full_tr,full_te,ytr,wtr,logit=logit)
    uf=test.SG_UF.to_numpy()
    records=[]
    for u in sorted(set(uf)):
        loc=uf==u
        records.append({"UF":u,"weight_sum":float(wte[loc].sum()),
            "sse_local":float(np.sum(wte[loc]*(yte[loc]-p0[loc])**2)),
            "sse_contexto":float(np.sum(wte[loc]*(yte[loc]-p1[loc])**2))})
    return bootstrap(records,seed),records

def main():
    pa=argparse.ArgumentParser()
    for item in ("votos2014","controles2014","votos2018_2022","controles2018_2022","mapa","out"):
        pa.add_argument("--"+item,type=Path,required=True)
    args=pa.parse_args()
    if args.out.exists() and any(args.out.iterdir()):raise SystemExit("Resultados anteriores preservados.")
    p,common,all_=load_data(args)
    frames={}; feat={}
    for year in (2014,2018,2022):
        d,b,allx=matrices(p,year)
        frames[year]=d; feat[year]=(b,allx)
    cross=[]; temporal_results=[]; uf_results=[]; descriptive=[]
    for year in (2014,2018,2022):
        d=frames[year];b,full=feat[year]
        basecount=all_[(all_.ano==year)].notna().all(axis=1).sum()
        descriptive.append({"ano":year,"n_municipios_base_comum":len(d),
            "media_c_municipios":float(d.competitividade_2t.mean()),
            "media_m_municipios":float(d.margem_assinada_pt13.mean()),
            "proporcao_municipios_maioria_pt13":float(d.margem_assinada_pt13.gt(0).mean()),
            "populacao_ponderada_c":float(np.average(d.competitividade_2t,weights=d.pop_antes)),
            "populacao_ponderada_m":float(np.average(d.margem_assinada_pt13,weights=d.pop_antes))})
        for outcome,col in Y.items():
            y=d[col].to_numpy(float)
            for weight in ("uniforme","populacao_anterior"):
                w=np.ones(len(d)) if weight=="uniforme" else d.pop_antes.to_numpy(float)
                for logit in (False,True) if outcome=="competitividade" else (False,):
                    typ="logit_fracionario" if logit else "linear"
                    row,ufs=g.cv_uf(d,b,full[:,b.shape[1]:],y,w,logit=logit)
                    rec=[{"UF":v["UF"],"weight_sum":v["weight_sum"],"sse_local":v["sse_baseline"],"sse_contexto":v["sse_contexto"]} for v in ufs]
                    check=bootstrap(rec,seed=20261012+year*10+(outcome=="direcao_pt13")*4+(weight=="populacao_anterior")*2+int(logit))
                    if abs(check["ganho_rmse_pct"]-row["reducao_rmse_pct"])>1e-7:raise ValueError("Conferência CV por UF falhou.")
                    cross.append({"ano":year,"desfecho":outcome,"ponderacao":weight,"familia":typ,"n":len(d),**check})
    scenarios=[([2014],2018),([2018],2022),([2014,2018],2022)]
    for i,(years,test_year) in enumerate(scenarios):
        for outcome in Y:
            for weight in ("uniforme","populacao_anterior"):
                for logit in (False,True) if outcome=="competitividade" else (False,):
                    typ="logit_fracionario" if logit else "linear"
                    k=2030333+test_year*17+i*170+(outcome=="direcao_pt13")*50+(weight=="populacao_anterior")*10+int(logit)
                    vals,peruf=temporal(years,test_year,frames,feat,outcome,weight,logit,seed=k)
                    case="+".join(str(y) for y in years)+"=>"+str(test_year)
                    temporal_results.append({"treino_anos":"+".join(map(str,years)),"teste_ano":test_year,"caso":case,
                     "desfecho":outcome,"ponderacao":weight,"familia":typ,
                     "n_treino":5564*len(years),"n_teste":5564,**vals})
                    uf_results.extend([{**{"caso":case,"desfecho":outcome,"ponderacao":weight,"familia":typ},**r} for r in peruf])
    cr=pd.DataFrame(cross); tm=pd.DataFrame(temporal_results)
    if len(cr)!=18 or len(tm)!=18 or len(uf_results)!=18*27:
        raise ValueError("Número de resultados inesperado.")
    args.out.mkdir(parents=True)
    cr.to_csv(args.out/"validacao_geografica_por_eleicao_2014_2018_2022.csv",index=False,float_format="%.10f")
    tm.to_csv(args.out/"validacao_temporal_out_of_time.csv",index=False,float_format="%.10f")
    pd.DataFrame(uf_results).to_csv(args.out/"sse_por_uf_validacao_temporal.csv",index=False,float_format="%.10f")
    pd.DataFrame(descriptive).to_csv(args.out/"perfil_municipal_3_eleicoes.csv",index=False,float_format="%.10f")
    meta={"autor":"Jacson Cruz do Nascimento","status":"ESTUDO_EXPLORATORIO_2014_SEM_ALTERAR_ARTIGO_V14",
     "anos":[2014,2018,2022],"amostra_municipal_comum":len(common),"n_observacoes":len(p),
     "controle_2014":{"PIB":2012,"populacao":2013,"demografia_censitaria":2010},
     "controle_2018":{"PIB":2016,"populacao":2017,"demografia_censitaria":2010},
     "controle_2022":{"PIB":2020,"populacao":2021,"demografia_censitaria":2010},
     "geografia":"centroides IBGE2022 e 8 vizinhos mais próximos",
     "familias":["OLS/WLS linear C e M","logit fracionario para C"],
     "modelos":"quatro controles locais + quatro dummies macrorregião vs adição de WX(k8)",
     "tempo":"2014=>2018, 2018=>2022, 2014+2018=>2022; treino contém apenas eleições anteriores.",
     "variavel_M":"candidatura do PT número13 menos candidatura adversária: Dilma (2014), Haddad (2018), Lula (2022); identidade partidária não implica a mesma candidatura",
     "regras":["Mesmos 5564 municípios presentes nas três eleições: 2014 possui um PIB 2012 adicionalmente ausente.",
               "WX de IBGE está disponível para todos os municípios no ano de referência; abordagem transdutiva somente para covariáveis, não desfechos.",
               "Nenhum treino incorpora votos de eleições cronologicamente posteriores ao teste temporal.",
               "Testes temporais não garantem previsão eleitoral em tempo real, pois IBGE publicado pode ser revisado a posteriori.",
               "Nacional 2014 inclui votos no exterior, não atribuídos a municípios brasileiros.",
               "Ganhos percentuais de RMSE são comparáveis apenas dentro do mesmo desfecho, ponderação e teste.",
               "Treino de 2014+2018 reusa municipios em dois anos e não equivale a independência entre unidades.",
               "Inferência por UF por bootstrap 4999 é exploratória: UFs vizinhas podem ser dependentes.",
               "Resultados não identificam causalidade nem contágio social."],
     "fontes":["outputs/piloto_2014_v01","outputs/piloto_2014_ibge_v01",
               "outputs/competitividade_v02","data/ibge_tratados/controles_pre_eleitorais_v02.csv"]}
    (args.out/"manifesto.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
    print("\n---VALIDACAO UF---")
    print(cr[["ano","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
    print("\n---VALIDACAO TEMPORAL---")
    print(tm[["caso","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
if __name__=="__main__":main()
