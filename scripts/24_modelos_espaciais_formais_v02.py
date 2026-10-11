#!/usr/bin/env python3
"""Robustez descritiva por modelos formais de erro espacial e defasagem espacial.

GM_Error: erro espacial estimado por GMM; GM_Lag: defasagem espacial
endógena estimada por IV/2SLS. A matriz de oito vizinhos foi calculada
com centroides IBGE 2022, pesos normalizados por linha. Não são modelos
de previsão ex ante; não demonstram interação individual ou contágio.
"""
import argparse,importlib.util,json
from pathlib import Path
import numpy as np
import pandas as pd
from libpysal.weights import W
import spreg

HERE=Path(__file__).resolve().parent
def module(name,path):
  t=importlib.util.spec_from_file_location(name,HERE/path)
  m=importlib.util.module_from_spec(t);t.loader.exec_module(m);return m
base=module("base23","16_modelos_competitividade.py")
soc=module("soc23","13_modelos_controles_socioeconomicos.py")
sp=module("sp23","10_espacial_municipal.py")
region={**{u:"N" for u in "AC AM AP PA RO RR TO".split()},
**{u:"NE" for u in "AL BA CE MA PB PE PI RN SE".split()},
**{u:"CO" for u in "DF GO MT MS".split()},
**{u:"SE" for u in "ES MG RJ SP".split()},
**{u:"S" for u in "PR RS SC".split()}}
def build(df,year):
    d=soc.especificacao_modelo(df[df.ano==year].copy(),year)
    d=d.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
    n=len(d)
    if n!=5565:raise ValueError("Amostra inesperada.")
    nn=sp.knn(d,8)
    w=W({i:[int(j) for j in nn[i]] for i in range(n)},id_order=list(range(n)),silence_warnings=True)
    w.transform="r"
    x=d[soc.COVARS].to_numpy(dtype=float)
    lag=x[nn].mean(axis=1)
    rg=pd.get_dummies(pd.Categorical(d.SG_UF.map(region),categories=["S","SE","CO","NE","N"]),drop_first=True,dtype=float).to_numpy()
    lat=d.latitude.to_numpy(dtype=float)/10
    lon=d.longitude.to_numpy(dtype=float)/10
    ge=np.column_stack([lat,lon,lat**2,lon**2,lat*lon])
    z=np.column_stack([x,rg,ge,lag])
    z=(z-z.mean(0))/np.where(z.std(0)>0,z.std(0),1)
    return d,z,w,nn

def sar_iv(y,z,nn):
    # SAR: y = rho * W y + X beta + erro.
    # 2SLS, H=[X,W^2 X]; W y é endógena; instrumentos espaciais
    # assumem exogeneidade de X e especificação suficiente.
    n=len(y)
    arr=y.reshape(-1)
    wy=arr[nn].mean(axis=1)
    X=np.column_stack([np.ones(n),z])
    wz=z[nn].mean(axis=1)
    w2z=wz[nn].mean(axis=1)
    H=np.column_stack([X,w2z])
    Z=np.column_stack([X,wy])
    zhat=H@np.linalg.lstsq(H,Z,rcond=None)[0]
    coeff=np.linalg.lstsq(zhat,arr,rcond=None)[0]
    resid=arr-Z@coeff
    base_resid=wy-X@np.linalg.lstsq(X,wy,rcond=None)[0]
    full_resid=wy-H@np.linalg.lstsq(H,wy,rcond=None)[0]
    first_stage_partial_r2=1-float(full_resid@full_resid)/float(base_resid@base_resid)
    if not np.isfinite(coeff).all() or not np.isfinite(first_stage_partial_r2):
        raise ValueError("Instrumentos SAR inválidos.")
    return float(coeff[-1]),resid,float(first_stage_partial_r2)

def run(panel):
    rows=[]
    for year in (2018,2022):
        d,z,w,nn=build(panel,year)
        for target,column in base.OUTCOMES.items():
            y=d[column].to_numpy(dtype=float).reshape(-1,1)
            for method in ("GM_Error","SAR_IV_2SLS"):
                try:
                    if method=="GM_Error":
                        mod=spreg.GM_Error(y,z,w,name_y=target,name_x=[f"x{i}" for i in range(z.shape[1])])
                        beta=np.asarray(mod.betas).reshape(-1)
                        param=float(beta[-1])
                        res=np.asarray(mod.u).reshape(-1)
                        first_stage=float("nan")
                        pseudo=float(getattr(mod,"pr2",float("nan")))
                    else:
                        param,res,first_stage=sar_iv(y,z,nn)
                        pseudo=float("nan")
                    rows.append({"ano":year,"desfecho":target,"metodo":method,
                        "n":len(y),"n_regressores":z.shape[1],
                        "coeficiente_espacial":param,
                        "nome_coeficiente": "lambda" if method=="GM_Error" else "rho",
                        "pseudo_r2":pseudo,"iv_primeiro_estagio_r2_parcial":first_stage,
                        "moran_residual_k8":sp.moran(res,nn),
                        "tipo_analise":"in_sample exploratoria, não CV, não causal",
                        "status":"concluido"})
                except Exception as ex:
                    rows.append({"ano":year,"desfecho":target,"metodo":method,"n":len(y),
                        "n_regressores":z.shape[1],"coeficiente_espacial":float("nan"),
                        "nome_coeficiente":"lambda" if method=="GM_Error" else "rho",
                        "pseudo_r2":float("nan"),"iv_primeiro_estagio_r2_parcial":float("nan"),"moran_residual_k8":float("nan"),
                        "tipo_analise":"in_sample exploratoria, não CV, não causal",
                        "status":"erro_"+type(ex).__name__+":"+str(ex)[:160]})
    return pd.DataFrame(rows)

def main():
    p=argparse.ArgumentParser()
    for n in ("mapa","hhi","ibge","competitividade","output"):p.add_argument("--"+n,required=True,type=Path)
    a=p.parse_args()
    if a.output.exists() and any(a.output.iterdir()):raise SystemExit("Saída anterior preservada.")
    panel,_=base.preparar(a.mapa,a.hhi,a.ibge,a.competitividade)
    results=run(panel)
    a.output.mkdir(parents=True,exist_ok=True)
    results.to_csv(a.output/"modelos_espaciais_gmm.csv",index=False)
    manifest={
      "amostra":"5.565 municipios para cada eleicao", "anos":[2018,2022],
      "metodos":"spreg.GM_Error GMM e SAR_IV_2SLS instrumentando Wy com W²X, Matriz kNN8 por centroides IBGE2022",
      "covariaveis":"4 controles socioeconomicos + 4 dummies macroregionais + polinomio de coordenadas (5) + 4 médias de vizinhança",
      "restricoes":["SAR_IV_2SLS depende de restrições de exclusão e instrumentos que não foram validados causalmente; observar força parcial de primeiro estágio.","GMM espacial não equivale a experimento causal.","Lag espacial do desfecho não pode servir de regressor de previsão ex ante em UF de teste.",
                    "Pseudo-R2 do spreg não comparar diretamente ao R2 convencional ou ao RMSE de validação.",
                    "Coeficientes espaciais refletem especificações associativas e possível estrutura não observada.",
                    "Registros com status erro sinalizam execução incompleta e não podem ser tratados como evidência positiva."]}
    (a.output/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(results.to_string(index=False))
    if not results.status.eq("concluido").all():raise SystemExit("Alguma especificação espacial falhou: não divulgar como validada.")
if __name__=="__main__":main()
