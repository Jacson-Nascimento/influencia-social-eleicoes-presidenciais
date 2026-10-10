#!/usr/bin/env python3
"""Comparação incremental de contexto socioeconômico espacial, sem votos dos vizinhos.

Os atributos de municípios próximos são conhecidos sem consultar HHI/votos
em qualquer município. O experimento descreve distribuição de concentração,
não identifica transmissão social ou prevê resultados eleitorais.
"""
import argparse, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
def importar(nome,arquivo):
    spec=importlib.util.spec_from_file_location(nome,HERE/arquivo)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

mund=importar("municipal","10_espacial_municipal.py")
base=importar("controles","13_modelos_controles_socioeconomicos.py")

FEATURES=base.COVARS

def preparar_features(df, vizinhos):
    arr=df[FEATURES].to_numpy(dtype=float)
    viz=arr[vizinhos].mean(axis=1)
    if not np.isfinite(viz).all():raise ValueError("Médias dos vizinhos não finitas.")
    return arr,viz

def padronizar_treino(x,train,test):
    media=x[train].mean(axis=0)
    desvio=x[train].std(axis=0)
    if (desvio<=1e-14).any():raise ValueError("Covariável constante na dobra.")
    return (x[train]-media)/desvio,(x[test]-media)/desvio

def crossval_uf(df,proprios,vizinhos):
    y=df.hhi.to_numpy(dtype=float)
    uf=df.SG_UF.astype(str).to_numpy()
    ufs=np.sort(np.unique(uf))
    folds=[]
    for f in range(5):
        teste=np.isin(uf,ufs[f::5]);train=~teste
        if min(teste.sum(),train.sum())<10:raise ValueError("Amostra de validação insuficiente.")
        xb_tr,xb_te=padronizar_treino(proprios,train,teste)
        xf_tr,xf_te=padronizar_treino(np.column_stack([proprios,vizinhos]),train,teste)
        beta0=np.linalg.lstsq(np.c_[np.ones(train.sum()),xb_tr],y[train],rcond=None)[0]
        beta1=np.linalg.lstsq(np.c_[np.ones(train.sum()),xf_tr],y[train],rcond=None)[0]
        p0=np.c_[np.ones(teste.sum()),xb_te]@beta0
        p1=np.c_[np.ones(teste.sum()),xf_te]@beta1
        folds.append({"fold":f+1,"ufs_teste":ufs[f::5].tolist(),
           "n_teste":int(teste.sum()),
           "sse_controles_locais":float(np.sum((y[teste]-p0)**2)),
           "sse_controles_mais_contexto":float(np.sum((y[teste]-p1)**2))})
    total=sum(x["n_teste"] for x in folds)
    rmse0=np.sqrt(sum(x["sse_controles_locais"] for x in folds)/total)
    rmse1=np.sqrt(sum(x["sse_controles_mais_contexto"] for x in folds)/total)
    return {"rmse_controles_locais":float(rmse0),
            "rmse_controles_mais_contexto":float(rmse1),
            "mudanca_relativa_rmse_pct":float((rmse0-rmse1)/rmse0*100),
            "dobras_com_piora":sum(x["sse_controles_mais_contexto"]>x["sse_controles_locais"] for x in folds),
            "n_folds":5,"folds":folds}

def comparar(d):
    original=d[(d.ano==2018)&(d.NR_TURNO==1)].sort_values(["SG_UF","CD_MUNICIPIO"])
    ids=original.CD_MUNICIPIO_IBGE.astype(str).to_numpy()
    vizinhancas={k:mund.knn(original,k) for k in (4,8,12)}
    outputs=[]
    for ano in (2018,2022):
        for turno in (1,2):
            df=d[(d.ano==ano)&(d.NR_TURNO==turno)].copy()
            df=base.especificacao_modelo(df,ano).set_index("CD_MUNICIPIO_IBGE").loc[ids].reset_index()
            if len(df)!=len(ids):raise ValueError("Chaves não balanceadas.")
            uf=pd.get_dummies(df.SG_UF,drop_first=True,dtype=float).to_numpy()
            Xfix=np.c_[np.ones(len(df)),uf]
            y=df.hhi.to_numpy(dtype=float)
            for k,nn in vizinhancas.items():
                x,lag=preparar_features(df,nn)
                xpad=(x-x.mean(axis=0))/x.std(axis=0)
                lagpad=(lag-lag.mean(axis=0))/lag.std(axis=0)
                reg0=base.fit(np.c_[Xfix,xpad],y)
                reg1=base.fit(np.c_[Xfix,xpad,lagpad],y)
                cv=crossval_uf(df,x,lag)
                outputs.append({"ano":ano,"turno":turno,"k":k,"n_municipios":len(df),
                  "r2_uf_locais":float(reg0["r2"]),
                  "r2_uf_locais_e_vizinhos":float(reg1["r2"]),
                  "incremento_r2":float(reg1["r2"]-reg0["r2"]),
                  "moran_residuo_local":float(mund.moran(reg0["resid"],nn)),
                  "moran_residuo_com_contexto":float(mund.moran(reg1["resid"],nn)),
                  "rmse_cv_local":cv["rmse_controles_locais"],
                  "rmse_cv_contexto":cv["rmse_controles_mais_contexto"],
                  "reduz_rmse_cv_pct":cv["mudanca_relativa_rmse_pct"],
                  "dobras_com_piora":cv["dobras_com_piora"],"detalhe_cv":cv})
    return outputs

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ("mapa","hhi","ibge","pasta"):p.add_argument("--"+n,type=Path,required=True)
    a=p.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):raise SystemExit("Não sobrepor resultados anteriores.")
    df,excluded,miss=base.preparar(a.mapa,a.hhi,a.ibge)
    vals=comparar(df)
    a.pasta.mkdir(parents=True,exist_ok=True)
    small=pd.DataFrame([{k:v for k,v in o.items() if k!="detalhe_cv"} for o in vals])
    small.to_csv(a.pasta/"comparacao_contexto_espacial_k4_k8_k12.csv",index=False,float_format="%.10f")
    (a.pasta/"validacao_ufs_detalhada.json").write_text(json.dumps(vals,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report={"objeto":"HHI municipal observado 2018/2022, não votos individuais",
       "amostra_municipios":len(df)//4,"municipios_excluidos":excluded,
       "comparacao":"UF + covariáveis locais versus UF + covariáveis locais + médias de covariáveis dos k vizinhos (in-sample); CV excluindo UF completa sem efeitos fixos estaduais",
       "k_primario":8,"k_sensibilidade":[4,12],
       "vizinhos":"Médias de quatro covariáveis IBGE nos k centroides mais próximos, não incluem valores de HHI, votos, identidade ou escolha de candidaturas vizinhas.",
       "sem_uso_de_rotulos_vizinhos":True,
       "observacao_transducao":"Atributos IBGE dos municípios de teste entram nas médias dos vizinhos, mas a votação/HHI dos municípios de teste nunca é usada para treinar parâmetros. Cenário de covariáveis públicas observadas, não predição eleitoral estrita em tempo real.",
       "interpretacao":"Associação e extrapolação geográfica descritivas, não manada causal. Vintages IBGE 2026 revisáveis; contiguidade territorial, outras matrizes e identificação social não testadas."}
    (a.pasta/"metodologia.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(small.to_string(index=False))
if __name__=="__main__":main()
