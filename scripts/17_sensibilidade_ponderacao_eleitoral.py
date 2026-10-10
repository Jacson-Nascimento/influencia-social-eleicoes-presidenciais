#!/usr/bin/env python3
"""Sensibilidade ponderada por votos válidos do segundo turno.

A observação segue sendo município, mas o peso é o número de votos válidos
dos finalistas. Comparar a especificação não ponderada para avaliar se
grandes centros alteram as conclusões. Não inferir comportamentos individuais.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
def importar(nome,path):
    spec=importlib.util.spec_from_file_location(nome,HERE/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod
prep=importar("prep_comp","16_modelos_competitividade.py")
spatial=importar("spatial_comp","10_espacial_municipal.py")
controls=importar("controls_comp","13_modelos_controles_socioeconomicos.py")

def wls(x,y,w):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float);w=np.asarray(w,dtype=float)
    if x.shape[0]!=len(y) or len(y)!=len(w) or (w<=0).any() or not np.isfinite(w).all():
        raise ValueError("Dimensões e pesos inválidos.")
    root=np.sqrt(w)
    beta=np.linalg.lstsq(x*root[:,None],y*root,rcond=None)[0]
    resid=y-x@beta
    ss=float(np.sum(w*resid**2))
    sst=float(np.sum(w*(y-np.average(y,weights=w))**2))
    if sst<=0:raise ValueError("Variância ponderada nula.")
    return {"r2_ponderado":float(1-ss/sst),"rmse_ponderado":float(np.sqrt(ss/w.sum())),
            "beta":beta,"residuos":resid}

def padronizar(x,train):
    mu=x[train].mean(axis=0);sd=x[train].std(axis=0)
    if (sd<=0).any():raise ValueError("Controle sem variação.")
    return (x-mu)/sd

def cv_uf_ponderado(frame,x,vizinhos,y,w):
    u=frame.SG_UF.to_numpy();siglas=np.sort(np.unique(u))
    full=np.column_stack([x,vizinhos])
    folds=[]
    for fold in range(5):
        mask=np.isin(u,siglas[fold::5]);tr=~mask
        x0=padronizar(x,tr);x1=padronizar(full,tr)
        p0=wls(np.c_[np.ones(tr.sum()),x0[tr]],y[tr],w[tr])["beta"]
        p1=wls(np.c_[np.ones(tr.sum()),x1[tr]],y[tr],w[tr])["beta"]
        e0=y[mask]-np.c_[np.ones(mask.sum()),x0[mask]]@p0
        e1=y[mask]-np.c_[np.ones(mask.sum()),x1[mask]]@p1
        folds.append({"fold":fold+1,"n":int(mask.sum()),"ufs":siglas[fold::5].tolist(),
           "sse_local":float(np.sum(w[mask]*e0**2)),
           "sse_contexto":float(np.sum(w[mask]*e1**2)),
           "peso_votos_validos":int(w[mask].sum())})
    total=sum(f["peso_votos_validos"] for f in folds)
    a=float(np.sqrt(sum(f["sse_local"] for f in folds)/total))
    b=float(np.sqrt(sum(f["sse_contexto"] for f in folds)/total))
    return {"rmse_local":a,"rmse_contexto":b,
       "reducao_rmse_pct":float(100*(a-b)/a),
       "dobras_com_piora":int(sum(f["sse_contexto"]>f["sse_local"] for f in folds)),
       "folds":folds}

def executar(data):
    records=[];cv=[]
    for ano in (2018,2022):
        d=data[data.ano.eq(ano)].copy()
        d=controls.especificacao_modelo(d,ano)
        d=d.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
        assert len(d)==5565
        w=d.total_validos.to_numpy(dtype=float)
        U=pd.get_dummies(d.SG_UF,drop_first=True,dtype=float).to_numpy()
        fix=np.c_[np.ones(len(d)),U]
        x=d[controls.COVARS].to_numpy(dtype=float)
        for k in (4,8,12):
            nbr=spatial.knn(d,k)
            v=x[nbr].mean(axis=1)
            z0=(x-x.mean(0))/x.std(0)
            xv=np.column_stack([x,v])
            z1=(xv-xv.mean(0))/xv.std(0)
            for label,col in prep.OUTCOMES.items():
                y=d[col].to_numpy(dtype=float)
                b0=wls(np.c_[fix,z0],y,w)
                b1=wls(np.c_[fix,z1],y,w)
                val=cv_uf_ponderado(d,x,v,y,w)
                records.append({"ano":ano,"desfecho":label,"k":k,"n":len(d),
                   "peso_total_votos_validos":int(w.sum()),
                   "r2_ponderado_local":b0["r2_ponderado"],
                   "r2_ponderado_contexto":b1["r2_ponderado"],
                   "delta_r2_ponderado":b1["r2_ponderado"]-b0["r2_ponderado"],
                   "rmse_cv_ponderado_local":val["rmse_local"],
                   "rmse_cv_ponderado_contexto":val["rmse_contexto"],
                   "reducao_rmse_cv_ponderado_pct":val["reducao_rmse_pct"],
                   "dobras_com_piora":val["dobras_com_piora"]})
                cv.append({"ano":ano,"desfecho":label,"k":k,"detalhes":val})
    return pd.DataFrame(records),cv

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for nm in ("mapa","hhi","ibge","competitividade","pasta"):
        p.add_argument("--"+nm,type=Path,required=True)
    a=p.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):
        raise SystemExit("Resultados anteriores preservados.")
    d,excluded=prep.preparar(a.mapa,a.hhi,a.ibge,a.competitividade)
    summary,cv=executar(d)
    a.pasta.mkdir(parents=True,exist_ok=True)
    summary.to_csv(a.pasta/"modelos_ponderados_competitividade_e_direcao.csv",
                   index=False,float_format="%.10f")
    (a.pasta/"validacao_ponderada_ufs.json").write_text(json.dumps(cv,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    metadata={"objeto":"Sensibilidade descritiva, não causal",
        "pesos":"Votos nominais válidos totais no segundo turno por município, constantes por desfecho de cada eleição.",
        "amostra":5565,"n_excluidos":len(excluded),
        "contraste":"Mesma amostra e mesmos atributos dos modelos não ponderados; a ponderação dá peso relativo maior aos municípios com mais votos válidos.",
        "aviso":"Validação geográfica não equivale a previsão ex ante; votos observados do segundo turno só são usados como pesos de avaliação, não como variáveis de previsão ou informação disponível antes da eleição.",
        "restricao":"Ponderação usa tamanho eleitoral observado ex post. Não utilizar resultado como evidência de desempenho prospectivo.",
        "script":"scripts/17_sensibilidade_ponderacao_eleitoral.py"}
    (a.pasta/"manifesto.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(summary.to_string(index=False))
if __name__=="__main__":main()
