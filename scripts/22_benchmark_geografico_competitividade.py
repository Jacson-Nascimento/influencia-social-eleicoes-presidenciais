#!/usr/bin/env python3
"""Benchmarks regionais mais fortes para competitividade e margem eleitoral.

Modelo principal de validação deixa UFs completas fora do treino.
Comparações aninhadas usam IDÊNTICA amostra, mesmas dobras e ponderação.
As variáveis dos vizinhos são exclusivamente IBGE, nunca votos ou desfechos.
"""
import argparse,importlib.util,json,hashlib
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
def module(name,path):
    s=importlib.util.spec_from_file_location(name,HERE/path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
base=module("comp22","16_modelos_competitividade.py")
soc=module("soc22","13_modelos_controles_socioeconomicos.py")
sp=module("sp22","10_espacial_municipal.py")
macro={
"N":set("AC AM AP PA RO RR TO".split()),"NE":set("AL BA CE MA PB PE PI RN SE".split()),
"CO":set("DF GO MT MS".split()),"SE":set("ES MG RJ SP".split()),
"S":set("PR RS SC".split())}
uf_region={u:r for r,units in macro.items() for u in units}
assert len(uf_region)==27
FEATURES=soc.COVARS
OUTCOMES=base.OUTCOMES

def data_year(panel,ano):
    d=soc.especificacao_modelo(panel.loc[panel.ano.eq(ano)].copy(),ano)
    d=d.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
    if len(d)!=5565 or d.SG_UF.nunique()!=27: raise ValueError("Amostra inválida.")
    r=d.SG_UF.map(uf_region)
    if r.isna().any():raise ValueError("UF sem região.")
    # Dummy de 5 macrorregiões com Sul como referência, 4 colunas.
    cats=pd.Categorical(r,categories=["S","SE","CO","NE","N"])
    region=pd.get_dummies(cats,drop_first=True,dtype=float).to_numpy()
    lat=d.latitude.to_numpy(dtype=float)/10.0
    lon=d.longitude.to_numpy(dtype=float)/10.0
    geo=np.column_stack([lat,lon,lat*lat,lon*lon,lat*lon])
    x=d[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(np.column_stack([x,geo])).all():raise ValueError("Atributos geográficos inválidos.")
    neighbor=sp.knn(d,8)
    wx=x[neighbor].mean(axis=1)
    arrays={
      "socio_local":x,
      "socio_mais_macrorregiao":np.column_stack([x,region]),
      "socio_mais_coordenadas":np.column_stack([x,geo]),
      "socio_macro_coordenadas":np.column_stack([x,region,geo])
    }
    return d,arrays,wx

def predict(xtrain,xtest,ytrain,wtrain,logit=False):
    # Normalização calculada EXCLUSIVAMENTE no treino.
    mu=xtrain.mean(0);sd=xtrain.std(0)
    sd=np.where(sd<1e-10,1.0,sd)
    xt=np.column_stack([np.ones(len(xtrain)),(xtrain-mu)/sd])
    xv=np.column_stack([np.ones(len(xtest)),(xtest-mu)/sd])
    if logit:
        from scipy.optimize import minimize
        from scipy.special import expit
        def fun(coef):
            eta=xt@coef
            pred=expit(eta)
            eps=1e-12
            val=-np.sum(wtrain*(ytrain*np.log(np.clip(pred,eps,1))+
                                 (1-ytrain)*np.log(np.clip(1-pred,eps,1))))
            grad=xt.T@(wtrain*(pred-ytrain))
            return float(val),grad
        init=np.zeros(xt.shape[1]);avg=np.average(ytrain,weights=wtrain)
        init[0]=np.log(np.clip(avg,1e-4,1-1e-4)/(1-np.clip(avg,1e-4,1-1e-4)))
        r=minimize(fun,init,jac=True,method="L-BFGS-B",
                   options={"maxiter":450,"ftol":1e-10})
        if not r.success and np.linalg.norm(r.jac)>1e-4:
            raise RuntimeError("Fractional logit falhou: "+str(r.message))
        return expit(xv@r.x)
    sw=np.sqrt(wtrain)
    coef=np.linalg.lstsq(xt*sw[:,None],ytrain*sw,rcond=None)[0]
    return xv@coef

def cv_uf(d,bas,wx,y,w,logit=False):
    groups=d.SG_UF.to_numpy()
    unique=np.sort(np.unique(groups))
    rec=[]
    for fold in range(5):
        tr=~np.isin(groups,unique[fold::5]);te=~tr
        pb=predict(bas[tr],bas[te],y[tr],w[tr],logit=logit)
        pc=predict(np.column_stack([bas,wx])[tr],np.column_stack([bas,wx])[te],
                   y[tr],w[tr],logit=logit)
        ufs=groups[te];actual=y[te];weight=w[te]
        for uf in np.unique(ufs):
            loc=(ufs==uf)
            rec.append({"UF":uf,"fold":fold+1,"n":int(loc.sum()),
                        "weight_sum":float(weight[loc].sum()),
                        "sse_baseline":float(np.sum(weight[loc]*(actual[loc]-pb[loc])**2)),
                        "sse_contexto":float(np.sum(weight[loc]*(actual[loc]-pc[loc])**2))})
    denom=sum(v["weight_sum"] for v in rec)
    a=np.sqrt(sum(v["sse_baseline"] for v in rec)/denom)
    b=np.sqrt(sum(v["sse_contexto"] for v in rec)/denom)
    return {"rmse_local":float(a),"rmse_com_contexto":float(b),
      "reducao_rmse_pct":float(100*(a-b)/a),"ufs_piora":int(sum(z["sse_contexto"]>z["sse_baseline"] for z in rec)),
      "folds_piora":int(sum(sum(q["sse_contexto"] for q in rec if q["fold"]==i)>sum(q["sse_baseline"] for q in rec if q["fold"]==i) for i in range(1,6)))},rec

def bootstrapUF(records,repetitions,seed):
    arr=np.asarray([[r["weight_sum"],r["sse_baseline"],r["sse_contexto"]] for r in records],dtype=float)
    n=len(arr);assert n==27
    rng=np.random.default_rng(seed)
    draws=rng.integers(0,n,size=(repetitions,n))
    sums=arr[draws].sum(axis=1)
    gains=100*(1-np.sqrt(sums[:,2]/sums[:,1]))
    return float(np.quantile(gains,.025)),float(np.quantile(gains,.975))

def main():
    p=argparse.ArgumentParser()
    for n in ("mapa","hhi","ibge","competitividade","output"):p.add_argument("--"+n,required=True,type=Path)
    p.add_argument("--bootstrap",type=int,default=1999)
    a=p.parse_args()
    if a.output.exists() and any(a.output.iterdir()):raise SystemExit("Saída v01 preservada, escolher nova.")
    panel,excluded=base.preparar(a.mapa,a.hhi,a.ibge,a.competitividade)
    rows,ufrows=[],[]
    for year in (2018,2022):
        d,bench,wx=data_year(panel,year)
        for target,col in OUTCOMES.items():
            y=d[col].to_numpy(dtype=float)
            for weights in ("uniforme","populacao_anterior"):
                w=np.ones(len(d)) if weights=="uniforme" else d["pop_2017" if year==2018 else "pop_2021"].to_numpy(dtype=float)
                for name,x in bench.items():
                    for functional in (("linear","logit_fracionario") if target=="competitividade" else ("linear",)):
                        out,records=cv_uf(d,x,wx,y,w,logit=functional=="logit_fracionario")
                        low,high=bootstrapUF(records,a.bootstrap,20261011+year*11+len(name)+len(target)+len(weights)+len(functional))
                        rows.append({"ano":year,"desfecho":target,"ponderacao":weights,
                          "benchmark":name,"familia":functional,"n_municipios":len(d),
                          **out,"bootstrap_uf_ci95_inf":low,"bootstrap_uf_ci95_sup":high})
                        ufrows.extend([{"ano":year,"desfecho":target,"ponderacao":weights,
                            "benchmark":name,"familia":functional,**r} for r in records])
    a.output.mkdir(parents=True,exist_ok=True)
    table=pd.DataFrame(rows)
    table.to_csv(a.output/"comparacao_benchmarks_regionais.csv",index=False,float_format="%.9f")
    pd.DataFrame(ufrows).to_csv(a.output/"sse_por_uf_e_modelo.csv",index=False,float_format="%.9f")
    manifest={"n_municipios":5565,"anos":[2018,2022],"vizinhos":8,
      "covariaveis_ibge":FEATURES,
      "benchmark":["quatro controles locais","controles + dummies cinco macrorregioes",
                   "controles + latitude longitude e termos quadraticos",
                   "controles + macrorregiao + polinomio de latitude longitude"],
      "geografia_projecao":"centroides IBGE 2022, graus decimais, sem uso de votos como feature",
      "pesos":["iguais por municipio","estimativa IBGE anterior (2017/2021) obtida em 2026"],
      "modelos":["OLS/WLS com mesmo k folds de UF completa","fractional logit quase-verossimilhança apenas para competitividade em [0,1]"],
      "bootstrap":"UF reamostrada após CV, IC percentil exploratorio, nem UFs vizinhas independentes nem temporal",
      "importante":"Comparar RMSE apenas dentro do MESMO desfecho/ano/ponderação, nunca C e M diretamente.",
      "disclaimer":"Sem resultados eleitorais dos vizinhos como regressores; sem causalidade; region e coordenadas são controles observados; locacional não equivale a transmissão social.",
      "municipios_excluidos":excluded}
    (a.output/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(table.to_string(index=False))
if __name__=="__main__":main()
