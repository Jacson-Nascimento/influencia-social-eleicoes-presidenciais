#!/usr/bin/env python3
"""Sensibilidade com 3 vs 4 regressores e ruptura 2000/2010.

Usar interseção completa do PIB para cinco eleições, sem imputar.
Janela 2006–2022 com PIB nominal prévio existente para todos os pleitos.
2014 recalculado em duas versões censitárias, somente como DIAGNÓSTICO:
Censo 2000 vs. Censo 2010 (principal).
Não usar Censo 2010 para resultados anteriores a 2010.
Não alterar os resultados do artigo v15 ou a base v01 dos seis pleitos.
"""
import argparse,importlib.util,json
from pathlib import Path
import numpy as np,pandas as pd

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("historic_6_elections",HERE/"36_modelos_seis_eleicoes_censo_anterior.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
g=m.g
Y=m.OUTCOMES
YEARS=(2006,2010,2014,2018,2022)

def enhanced(panel,args):
    h=pd.read_csv(args.ibge_historico,dtype={"CD_MUNICIPIO_IBGE":str})
    ib14=pd.read_csv(args.ibge_2014,dtype={"CD_MUNICIPIO_IBGE":str})
    ib18=pd.read_csv(args.ibge_2018_2022,dtype={"CD_MUNICIPIO_IBGE":str})
    lookup_hist=h.set_index("CD_MUNICIPIO_IBGE")
    ib14=ib14.set_index("CD_MUNICIPIO_IBGE")
    ib18=ib18.set_index("CD_MUNICIPIO_IBGE")
    p=panel[panel.ano.isin(YEARS)].copy()
    result=[]
    for year in YEARS:
        d=p[p.ano==year].copy()
        ids=d.CD_MUNICIPIO_IBGE.tolist()
        if year<=2010:
            d["log_pibpc_proxy"]=lookup_hist.loc[ids,f"log_pibpc_proxy_{year}"].to_numpy(float)
        elif year==2014:
            d["log_pibpc_proxy"]=ib14.loc[ids,"log_pibpc_proxy"].to_numpy(float)
        else:
            pop="pop_2017" if year==2018 else "pop_2021"
            pib="pibpc_proxy_2016_2017_reais" if year==2018 else "pibpc_proxy_2020_2021_reais"
            d["log_pibpc_proxy"]=np.log(ib18.loc[ids,pib].to_numpy(float))
        result.append(d)
    combined=pd.concat(result,ignore_index=True)
    # A amostra de seis eleições (5506) contém uma cidade sem PIB comparável.
    # Excluí-la de TODOS os anos 2006-2022; não imputar.
    eligibility=combined.groupby("CD_MUNICIPIO_IBGE").log_pibpc_proxy.apply(
        lambda v: len(v)==5 and np.isfinite(v).all())
    valid_ids=set(eligibility[eligibility].index)
    combined=combined[combined.CD_MUNICIPIO_IBGE.isin(valid_ids)].copy()
    if len(valid_ids)<5400 or len(combined)!=5*len(valid_ids):
        raise ValueError(f"Amostra 2006–2022 com PIB insuficiente: {len(valid_ids)}.")
    if not np.isfinite(combined.log_pibpc_proxy).all():
        raise ValueError("Valores econômicos não finitos.")
    return combined,lookup_hist

def mats(frame,fields):
    d=frame.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
    x=d[fields].to_numpy(float)
    loc=pd.Categorical(d.SG_UF.map(g.uf_region),categories=["S","SE","CO","NE","N"])
    region=pd.get_dummies(loc,drop_first=True,dtype=float).to_numpy()
    base=np.column_stack([x,region])
    near=g.sp.knn(d,8)
    return d,base,np.column_stack([base,x[near].mean(axis=1)])

def predict_errors(train_years,target,data,outcome,weight,logit):
    source=pd.concat([data[y][0] for y in train_years],ignore_index=True)
    x0tr=np.vstack([data[y][1] for y in train_years])
    x1tr=np.vstack([data[y][2] for y in train_years])
    d,x0te,x1te=data[target]
    ycol=Y[outcome]
    trainy=source[ycol].to_numpy(float);y=d[ycol].to_numpy(float)
    trainw=np.ones(len(source)) if weight=="uniforme" else source.pop_previa.to_numpy(float)
    w=np.ones(len(d)) if weight=="uniforme" else d.pop_previa.to_numpy(float)
    p0=g.predict(x0tr,x0te,trainy,trainw,logit=logit)
    p1=g.predict(x1tr,x1te,trainy,trainw,logit=logit)
    rec=[]
    for u in np.sort(d.SG_UF.unique()):
        idx=d.SG_UF.eq(u).to_numpy()
        rec.append({"UF":u,"weight_sum":float(w[idx].sum()),
                    "sse_baseline":float(np.sum(w[idx]*(y[idx]-p0[idx])**2)),
                    "sse_contexto":float(np.sum(w[idx]*(y[idx]-p1[idx])**2))})
    return rec

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    for name in ("mapa","ibge_historico","ibge_2014","ibge_2018_2022","votos_2002","votos_2006","votos_2010","votos_2014","votos_2018_2022","saida"):
        pa.add_argument("--"+name,required=True,type=Path)
    a=pa.parse_args()
    if a.saida.exists() and any(a.saida.iterdir()):raise SystemExit("Não alterar saída anterior")
    allpanel,coverage=m.build_panel(a)
    if coverage["amostra_comum_seis_eleicoes"]!=5506:raise ValueError("Amostra balanceada mudou.")
    enriched,lookup_hist=enhanced(allpanel,a)
    n_keep=enriched.CD_MUNICIPIO_IBGE.nunique()
    assert 5400<=n_keep<=5506
    fields={"tres_controles":["log_pop","urbanizacao","fracao_feminina"],
            "quatro_controles":["log_pop","log_pibpc_proxy","urbanizacao","fracao_feminina"]}
    geo=[];time=[];vintage=[]
    for variant,cols in fields.items():
        data={year:mats(enriched[enriched.ano==year].copy(),cols) for year in YEARS}
        for year in YEARS:
            d,x0,x1=data[year]
            for outcome in Y:
                y=d[Y[outcome]].to_numpy(float)
                for weight in ("uniforme","populacao_anterior"):
                    w=np.ones(len(d)) if weight=="uniforme" else d.pop_previa.to_numpy(float)
                    for logit in ([False,True] if outcome=="competitividade" else [False]):
                        records=m.uf_holdout(d,x0,x1,y,w,logit)
                        b=m.bootstrap(records,seed=20022022+year*7+(len(cols)*7)+int(logit)*5+(weight=="populacao_anterior")*11+(outcome=="direcao_pt13")*13)
                        geo.append({"ano":year,"especificacao":variant,"desfecho":outcome,
                            "ponderacao":weight,"familia":"logit_fracionario" if logit else "linear","n":len(d),**b})
        for ix,target in enumerate(YEARS[1:]):
            train=YEARS[:ix+1]
            for outcome in Y:
                for weight in ("uniforme","populacao_anterior"):
                    for logit in ([False,True] if outcome=="competitividade" else [False]):
                        records=predict_errors(train,target,data,outcome,weight,logit)
                        b=m.bootstrap(records,seed=20022022+target*13+len(cols)*4+int(logit)*11+(weight=="populacao_anterior")*17+(outcome=="direcao_pt13")*23)
                        time.append({"teste_ano":target,"treino_anos":"+".join(map(str,train)),
                            "especificacao":variant,"desfecho":outcome,"ponderacao":weight,
                            "familia":"logit_fracionario" if logit else "linear",
                            "n_treino":len(train)*n_keep,"n_teste":n_keep,**b})
        # 2014 counterfactual vintage diagnostic: compare old vs contemporary census for test
        old=enriched[enriched.ano==2014].copy()
        ids=old.CD_MUNICIPIO_IBGE.tolist()
        old["urbanizacao"]=lookup_hist.loc[ids,"urbanizacao_2000"].to_numpy(float)
        old["fracao_feminina"]=lookup_hist.loc[ids,"fracao_feminina_2000"].to_numpy(float)
        alternatives={
           "censo2000_fixado_ate_2014":old,
           "censo2010_anterior_2014":enriched[enriched.ano==2014].copy()}
        for label,testframe in alternatives.items():
            orig_data=data.copy()
            orig_data[2014]=mats(testframe,cols)
            # within 2014 geographic UF validation
            d,x0,x1=orig_data[2014]
            for outcome in Y:
                y=d[Y[outcome]].to_numpy(float)
                for weight in ("uniforme","populacao_anterior"):
                    w=np.ones(len(d)) if weight=="uniforme" else d.pop_previa.to_numpy(float)
                    for logit in ([False,True] if outcome=="competitividade" else [False]):
                        records=m.uf_holdout(d,x0,x1,y,w,logit)
                        b=m.bootstrap(records,seed=234344+len(cols)*5+int(logit)*13+(weight=="populacao_anterior")*23+(outcome=="direcao_pt13")*7)
                        vintage.append({"teste":"UF_2014","censo2014":label,"especificacao":variant,
                          "desfecho":outcome,"ponderacao":weight,"familia":"logit_fracionario" if logit else "linear",**b})
                        temporal=predict_errors((2006,2010),2014,orig_data,outcome,weight,logit)
                        t=m.bootstrap(temporal,seed=346633+len(cols)*5+int(logit)*13+(weight=="populacao_anterior")*23+(outcome=="direcao_pt13")*7)
                        vintage.append({"teste":"2006_2010_para_2014","censo2014":label,"especificacao":variant,
                          "desfecho":outcome,"ponderacao":weight,"familia":"logit_fracionario" if logit else "linear",**t})
    if len(geo)!=60 or len(time)!=48 or len(vintage)!=48:
        raise AssertionError((len(geo),len(time),len(vintage)))
    a.saida.mkdir(parents=True)
    pd.DataFrame(geo).to_csv(a.saida/"geo_tres_quatro_controles.csv",index=False,float_format="%.10f")
    pd.DataFrame(time).to_csv(a.saida/"temporal_tres_quatro_controles.csv",index=False,float_format="%.10f")
    pd.DataFrame(vintage).to_csv(a.saida/"censo_vintage_2014.csv",index=False,float_format="%.10f")
    manifest={"autor":"Jacson Cruz do Nascimento",
      "anos":[2006,2010,2014,2018,2022],
      "amostra_municipios_fixa":n_keep,
      "objetivo":"isolar efeito da inclusão do PIB vs três controles e efeito dos Censos 2000/2010 na validação de 2014",
      "regras":[
        "Os resultados 2002–2022 usam censo anterior 2000/2010; 1998 foi excluído.",
        "Modelos com 4 controles não incluem 2002; série PIB em vintage homogêneo ausente para pleito de 2002.",
        "Para 2014 o uso alternativo do Censo 2000 é apenas sensibilidade, não especificação preferida.",
        "Mesmo universo após exclusão completa do PIB faltante para todos os anos 2006–2022; comparação interna três vs quatro controles.",
        "PIB 2004 2008 2012 2016 2020 dividido por estimativa de população do ano seguinte são proxies, não PIB per capita oficial.",
        "Treino de validação temporal só tem votos de pleitos anteriores.",
        "UF bootstrap 4999 condicionais, não corrigem correlação espacial entre UFs limítrofes.",
        "Nenhum resultado identifica causalidade ou contágio social."],
      "pontos_de_sensibilidade":["quebra no ano 2014 de variáveis censitárias",
        "diferença entre modelos com três e quatro regressores",
        "comparabilidade temporal das eleições com candidatos distintos"]}
    (a.saida/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print("GEO",pd.DataFrame(geo)[["ano","especificacao","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
    print("VINTAGE",pd.DataFrame(vintage)[["teste","censo2014","especificacao","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
if __name__=="__main__":main()
