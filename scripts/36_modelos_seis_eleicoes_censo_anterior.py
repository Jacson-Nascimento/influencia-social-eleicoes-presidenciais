#!/usr/bin/env python3
"""Painel presidencial 2002-2022 com Censo anterior ao pleito (6 eleições).

Convenção documental baseada em CRUZ (2019, UnB, tese): o censo mais recente
anterior ao ano da eleição. Portanto: Censo 2000 para 2002/06/10; Censo 2010
para 2014/18/22. 1998 EXCLUÍDO.
Principal: três atributos disponíveis para os seis pleitos (log população
anterior, urbanização do censo anterior, proporção feminina do censo anterior).
SENSIBILIDADE FUTURA: PIB histórico 2002 não coberto pelo mesmo SIDRA e não
imputado; NÃO combinar 4 variáveis 2006+ com 3 em 2002 numa comparação limpa.
Comparação do baseline local+4 dummies macro com adição de médias k8 IBGE.
Validação UF-omitida por pleito e temporal expanding-window consecutiva.
Não usar TSE de 1998 nem covariáveis pós-pleito.
"""
import argparse,json,hashlib,importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("benchmark_historico",HERE/"22_benchmark_geografico_competitividade.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
OUTCOMES={"competitividade":"competitividade_2t","direcao_pt13":"margem_assinada_pt13"}
YEARS=(2002,2006,2010,2014,2018,2022)
BASECOLS=["log_pop","urbanizacao","fracao_feminina"]
K=("SG_UF","CD_MUNICIPIO")
FINALISTAS={2002:{13,45},2006:{13,45},2010:{13,45},2014:{13,45},2018:{13,17},2022:{13,22}}

def history_votes(path,year):
    x=pd.read_csv(path,dtype={"SG_UF":str})
    x=x[(x.NR_TURNO==2)&(x.SG_UF.isin(g.uf_region))].copy()
    x["NR_CANDIDATO"]=x.NR_CANDIDATO.astype(int)
    candidates=set(x.NR_CANDIDATO.unique())
    if candidates!=FINALISTAS[year]:raise ValueError(f"{year}: finalistas inesperados {candidates}")
    if x.duplicated(list(K)+["NR_CANDIDATO"]).any():raise ValueError(f"{year}: voto duplo")
    x=x.pivot(index=list(K),columns="NR_CANDIDATO",values="QT_VOTOS_NOMINAIS")
    other=next(iter(FINALISTAS[year]-{13}))
    x=x.dropna(subset=[13,other])
    v13=x[13].astype("int64"); vother=x[other].astype("int64")
    den=v13+vother
    if (den<=0).any():raise ValueError("Município sem votos válidos")
    result=x.reset_index()[list(K)].copy()
    result["ano"]=year
    result["votos_pt13"]=v13.to_numpy()
    result["votos_oponente"]=vother.to_numpy()
    result["total_validos"]=den.to_numpy()
    result["competitividade_2t"]=(1-abs(v13-vother)/den).to_numpy()
    result["margem_assinada_pt13"]=((v13-vother)/den).to_numpy()
    return result

def build_panel(a):
    mapa=pd.read_csv(a.mapa,dtype={"SG_UF":str,"CD_MUNICIPIO_IBGE":str})
    if len(mapa)!=5570:raise ValueError("malha atual diferente de 5570")
    h=pd.read_csv(a.ibge_historico,dtype={"CD_MUNICIPIO_IBGE":str})
    i=pd.read_csv(a.ibge_2014,dtype={"CD_MUNICIPIO_IBGE":str})
    late=pd.read_csv(a.ibge_2018_2022,dtype={"CD_MUNICIPIO_IBGE":str})
    first=pd.read_csv(a.votos_2014,dtype={"CD_MUNICIPIO_IBGE":str})
    last=pd.read_csv(a.votos_2018_2022,dtype={"SG_UF":str})
    for f in (mapa,h,i,late):
        if f.CD_MUNICIPIO_IBGE.duplicated().any():raise ValueError("código IBGE duplicado nos insumos")
    p=[]
    oldcover={}
    for year in YEARS:
        if year<2014:
            d=history_votes(getattr(a,f"votos_{year}"),year)
        elif year==2014:
            d=first.copy()
        else:
            d=last[last.ano==year].copy()
        # Join by year-specific TSE municipality and modern IBGE key; missing
        # historical keys are excluded, not allocated to modern cities by guess.
        if year!=2014:
            d=d.merge(mapa[list(K)+["CD_MUNICIPIO_IBGE","latitude","longitude"]],
                      on=list(K),how="left",validate="one_to_one",indicator=True)
        oldcover[str(year)]={
          "votos_municipios_antes_da_correspondencia":int(len(d)),
          "municipios_sem_chave_atual":int(d.CD_MUNICIPIO_IBGE.isna().sum()),
          "exemplos_sem_chave":d.loc[d.CD_MUNICIPIO_IBGE.isna(),list(K)].head(15).to_dict("records")}
        d=d[d.CD_MUNICIPIO_IBGE.notna()].copy()
        if year<=2010:
            d=d.merge(h,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
            d["urbanizacao"]=d.urbanizacao_2000
            d["fracao_feminina"]=d.fracao_feminina_2000
            d["log_pop"]=d[f"log_pop_{year}"]
            d["pop_previa"]=d[f"pop_{year-1}"]
            d["censo_ano"]=2000
        elif year==2014:
            d=d.merge(i,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one",suffixes=("","_ibge"))
            d["urbanizacao"]=d.urbanizacao_2010
            d["fracao_feminina"]=d.fracao_feminina_2010
            d["log_pop"]=np.log(d.pop_2013)
            d["pop_previa"]=d.pop_2013
            d["censo_ano"]=2010
        else:
            d=d.merge(late,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
            d["urbanizacao"]=d.urbanizacao_2010
            d["fracao_feminina"]=d.fracao_feminina_2010
            pop=d["pop_2017" if year==2018 else "pop_2021"]
            d["log_pop"]=np.log(pop.where(pop>0))
            d["pop_previa"]=pop
            d["censo_ano"]=2010
        select=["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE",
          "latitude","longitude","pop_previa","censo_ano"]+BASECOLS+list(OUTCOMES.values())
        p.append(d[select].copy())
    big=pd.concat(p,ignore_index=True)
    valid=big[BASECOLS+["pop_previa","latitude","longitude"]+list(OUTCOMES.values())].notna().all(axis=1)
    for feat in BASECOLS+["pop_previa"]:
        if feat in ["pop_previa"]:valid&=big[feat]>0
    candidates=big.loc[valid].groupby("CD_MUNICIPIO_IBGE").ano.nunique()
    common=sorted(candidates[candidates==6].index)
    panel=big[big.CD_MUNICIPIO_IBGE.isin(common)].copy()
    if not (5400<=len(common)<=5570):
        raise ValueError("Amostra comum implausível: "+str(len(common)))
    if len(panel)!=len(common)*6 or panel.groupby("ano").size().nunique()!=1:
        raise ValueError("Painel não balanceado")
    if panel.duplicated(["ano","CD_MUNICIPIO_IBGE"]).any():raise ValueError("duplicatas")
    if not np.allclose(panel.competitividade_2t,1-np.abs(panel.margem_assinada_pt13)):
        raise ValueError("Indicadores C/M inconsistentes")
    oldcover["amostra_comum_seis_eleicoes"]=len(common)
    oldcover["observacoes_balanceadas"]=len(panel)
    oldcover["excluidos_sem_amostra_comum"]=sorted(set(mapa.CD_MUNICIPIO_IBGE)-set(common))
    return panel,oldcover

def year_data(panel,year):
    d=panel[panel.ano==year].sort_values(list(K)).reset_index(drop=True)
    x=d[BASECOLS].to_numpy(dtype=float)
    region=pd.Categorical(d.SG_UF.map(g.uf_region),categories=["S","SE","CO","NE","N"])
    reg=pd.get_dummies(region,drop_first=True,dtype=float).to_numpy()
    if reg.shape!=(len(d),4):raise ValueError("Macrorregiões inválidas")
    b=np.column_stack([x,reg])
    nearest=g.sp.knn(d,8)
    contextual=np.column_stack([b,x[nearest].mean(axis=1)])
    return d,b,contextual

def bootstrap(vals,seed):
    a=np.array([[q["weight_sum"],q["sse_baseline"],q["sse_contexto"]] for q in vals],float)
    if len(a)!=27 or (a[:,0]<=0).any(): raise ValueError("Sem todas 27 UFs")
    rmse0=np.sqrt(a[:,1].sum()/a[:,0].sum());rmse1=np.sqrt(a[:,2].sum()/a[:,0].sum())
    rng=np.random.default_rng(seed)
    sims=a[rng.integers(0,27,size=(4999,27))].sum(axis=1)
    gains=100*(1-np.sqrt(sims[:,2]/sims[:,1]))
    return {"rmse_baseline":float(rmse0),"rmse_contexto":float(rmse1),
       "ganho_rmse_pct":float(100*(1-rmse1/rmse0)),
       "ic95_uf_inf":float(np.quantile(gains,.025)),
       "ic95_uf_sup":float(np.quantile(gains,.975)),
       "ufs_piora":int(sum(a[:,2]>a[:,1]))}

def uf_holdout(d,x0,x1,y,w,logit):
    rec=[];ufs=np.sort(d.SG_UF.unique())
    for fold in range(5):
        train=~d.SG_UF.isin(ufs[fold::5]).to_numpy()
        test=~train
        p0=g.predict(x0[train],x0[test],y[train],w[train],logit=logit)
        p1=g.predict(x1[train],x1[test],y[train],w[train],logit=logit)
        t=d.SG_UF.to_numpy()[test];wtest=w[test];actual=y[test]
        for state in np.unique(t):
            ix=t==state
            rec.append({"UF":state,"fold":fold+1,
                "weight_sum":float(wtest[ix].sum()),
                "sse_baseline":float(np.sum(wtest[ix]*(actual[ix]-p0[ix])**2)),
                "sse_contexto":float(np.sum(wtest[ix]*(actual[ix]-p1[ix])**2))})
    return rec

def temporal(trainyears,testyear,data,outcome,weight,logit):
    dv=pd.concat([data[t][0] for t in trainyears],ignore_index=True)
    x0tr=np.vstack([data[t][1] for t in trainyears]);x1tr=np.vstack([data[t][2] for t in trainyears])
    te,x0te,x1te=data[testyear]
    target=OUTCOMES[outcome]
    wtr=np.ones(len(dv)) if weight=="uniforme" else dv.pop_previa.to_numpy(float)
    wt=np.ones(len(te)) if weight=="uniforme" else te.pop_previa.to_numpy(float)
    ytr=dv[target].to_numpy(float);yte=te[target].to_numpy(float)
    p0=g.predict(x0tr,x0te,ytr,wtr,logit=logit)
    p1=g.predict(x1tr,x1te,ytr,wtr,logit=logit)
    rec=[]
    for state in np.sort(te.SG_UF.unique()):
        ix=te.SG_UF.eq(state).to_numpy()
        rec.append({"UF":state,"weight_sum":float(wt[ix].sum()),
          "sse_baseline":float(np.sum(wt[ix]*(yte[ix]-p0[ix])**2)),
          "sse_contexto":float(np.sum(wt[ix]*(yte[ix]-p1[ix])**2))})
    return rec

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ("mapa","ibge_historico","ibge_2014","ibge_2018_2022","votos_2002","votos_2006","votos_2010","votos_2014","votos_2018_2022","saida"):
        p.add_argument("--"+flag,required=True,type=Path)
    a=p.parse_args()
    if a.saida.exists() and any(a.saida.iterdir()):raise SystemExit("Não substituir resultados")
    panel,coverage=build_panel(a)
    pdata={year:year_data(panel,year) for year in YEARS}
    if any(len(pdata[y][0])!=coverage["amostra_comum_seis_eleicoes"] for y in YEARS):raise ValueError("Amostras diferentes")
    geo=[];tim=[];sse=[]
    for year in YEARS:
        d,x0,x1=pdata[year]
        for outcome in OUTCOMES:
            y=d[OUTCOMES[outcome]].to_numpy(float)
            for weight in ("uniforme","populacao_anterior"):
                w=np.ones(len(d)) if weight=="uniforme" else d.pop_previa.to_numpy(float)
                for logit in ([False,True] if outcome=="competitividade" else [False]):
                    vals=uf_holdout(d,x0,x1,y,w,logit)
                    result=bootstrap(vals,seed=20261012+year*13+int(outcome=="direcao_pt13")*10+int(weight=="populacao_anterior")*5+int(logit))
                    geo.append({"ano":year,"desfecho":outcome,"ponderacao":weight,
                      "familia":"logit_fracionario" if logit else "linear","n":len(d),**result})
    for i,testyear in enumerate(YEARS[1:]):
        training=list(YEARS[:i+1])
        for outcome in OUTCOMES:
            for weight in ("uniforme","populacao_anterior"):
                for logit in ([False,True] if outcome=="competitividade" else [False]):
                    vals=temporal(training,testyear,pdata,outcome,weight,logit)
                    stats=bootstrap(vals,seed=20500212+testyear*17+int(outcome=="direcao_pt13")*10+int(weight=="populacao_anterior")*5+int(logit))
                    scenario="+".join(map(str,training))+"=>"+str(testyear)
                    tim.append({"cenario":scenario,"treino_anos":"+".join(map(str,training)),
                     "teste_ano":testyear,"desfecho":outcome,"ponderacao":weight,
                     "familia":"logit_fracionario" if logit else "linear",
                     "n_treino":len(training)*len(pdata[testyear][0]),"n_teste":len(pdata[testyear][0]),**stats})
                    sse.extend([{"cenario":scenario,"desfecho":outcome,"ponderacao":weight,
                      "familia":"logit_fracionario" if logit else "linear",**v} for v in vals])
    if len(geo)!=36 or len(tim)!=30 or len(sse)!=30*27:
        raise ValueError(f"Contagem errada {len(geo)} {len(tim)} {len(sse)}")
    a.saida.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(geo).to_csv(a.saida/"validacao_geografica_2002_2022.csv",index=False,float_format="%.10f")
    pd.DataFrame(tim).to_csv(a.saida/"validacao_temporal_2002_2022.csv",index=False,float_format="%.10f")
    pd.DataFrame(sse).to_csv(a.saida/"sse_uf_validacao_temporal.csv",index=False,float_format="%.10f")
    pd.DataFrame({"CD_MUNICIPIO_IBGE":sorted(panel.CD_MUNICIPIO_IBGE.unique())}).to_csv(a.saida/"municipios_amostra_comum.csv",index=False)
    summary={"autor":"Jacson Cruz do Nascimento",
      "carater":"ESTUDO EXPLORATORIO 2002-2022, 1998 EXCLUIDO, SEM SUBMISSAO",
      "referencia_metodologica":"CRUZ, Rafael Georges da (2019), UnB, escolha do Censo anterior ao pleito",
      "anos":list(YEARS),"censo_por_ano":{str(k):(2000 if k<=2010 else 2010) for k in YEARS},
      "n_municipios":coverage["amostra_comum_seis_eleicoes"],
      "n_observacoes":coverage["observacoes_balanceadas"],
      "total_cenarios_validacao_geografica":len(geo),
      "total_cenarios_validacao_temporal":len(tim),
      "controles":"log população anterior, proporção urbana Censo anterior e proporção feminina Censo anterior",
      "pib":"Sem PIB no modelo principal comum a seis pleitos, devido à ausência de mesma série oficial para 2002. Não imputado.",
      "benchmark":"3 controles locais + 4 indicadores macrorregionais; alternativa acrescenta médias IBGE de 8 vizinhos",
      "variavel_dependente":"C=1−|M| e M=(votos_PT13−votos_outro_finalista)/votos_validos",
      "cinco_folds_uf":True,"bootstrap_uf":4999,
      "cautelas":["Municípios do passado sem correspondência atual são excluídos, sem imputação.",
        "M representa candidaturas diferentes do PT ao longo dos anos.",
        "Troca 2000/2010 cria quebra de vintage dos indicadores demográficos.",
        "Populações e contas retrospectivamente recuperadas em 2026, não previsão em tempo real.",
        "UFs limítrofes podem ter dependência espacial residual.",
        "Unidades repetidas em anos distintos não são independentes.",
        "O estudo não demonstra causalidade ou contágio social."],
      "cobertura_por_eleicao":coverage}
    (a.saida/"manifesto.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"n_municipios":summary["n_municipios"],"n_obs":summary["n_observacoes"],"cobertura":coverage},ensure_ascii=False)[:3500])
    print("GEOGRAFICO",pd.DataFrame(geo)[["ano","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
    print("TEMPORAL",pd.DataFrame(tim)[["cenario","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
if __name__=="__main__":main()
