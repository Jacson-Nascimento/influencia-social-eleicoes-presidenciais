#!/usr/bin/env python3
"""Inferência espacial complementar: bootstrap de 27 UFs e HAC por distância.

Retoma EXATAMENTE a variável do segundo turno e as covariáveis dos scripts 16/18.
Amostra: 5.565 municípios; validação por UFs, sem efeitos fixos estaduais.
Não produz inferência causal. Conley e clusters não eliminam confundimento.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix, eye
from scipy.stats import chi2, f

HERE=Path(__file__).resolve().parent
def imp(n,fn):
    spec=importlib.util.spec_from_file_location(n,HERE/fn)
    t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t);return t

prep=imp("preparacao_20","16_modelos_competitividade.py")
ols=imp("controles_20","13_modelos_controles_socioeconomicos.py")
pweights=imp("pesos_20","17_sensibilidade_ponderacao_eleitoral.py")
spatial=imp("spatial_20","10_espacial_municipal.py")
FEATS=ols.COVARS
OUTCOMES=prep.OUTCOMES

def xyz_da_latlon(d):
    lat=np.radians(d.latitude.to_numpy(dtype=float))
    lon=np.radians(d.longitude.to_numpy(dtype=float))
    xyz=np.column_stack([np.cos(lat)*np.cos(lon),np.cos(lat)*np.sin(lon),np.sin(lat)])
    if not np.isfinite(xyz).all():raise ValueError("Coordenadas não finitas.")
    return xyz

def kernel_conley(xyz,km):
    """Kernel Bartlett em distâncias arco de grande círculo; simétrico e diagonal 1."""
    raio=6371.0088
    chord=2*np.sin(km/(2*raio))
    pares=cKDTree(xyz).query_pairs(chord,output_type="ndarray")
    if len(pares):
        dif=np.linalg.norm(xyz[pares[:,0]]-xyz[pares[:,1]],axis=1)
        dist=2*raio*np.arcsin(np.clip(dif/2,0,1))
        w=np.clip(1-dist/km,0,1)
        ii=np.concatenate([pares[:,0],pares[:,1]])
        jj=np.concatenate([pares[:,1],pares[:,0]])
        vals=np.concatenate([w,w])
        K=coo_matrix((vals,(ii,jj)),shape=(len(xyz),len(xyz))).tocsr()
    else:
        K=coo_matrix((len(xyz),len(xyz))).tocsr()
    K+=eye(len(xyz),format="csr")
    return K,int(len(pares))

def fit_inferencia(X,y,w,groups,kernels):
    sqrt=np.sqrt(w)
    A=X*sqrt[:,None]
    b=y*sqrt
    q=A.shape[1];n=A.shape[0]
    if np.linalg.matrix_rank(A)!=q:raise ValueError("Matriz de regressão singular.")
    inv=np.linalg.inv(A.T@A)
    coef=inv@(A.T@b)
    resid=b-A@coef
    scores=A*resid[:,None]
    fields={}
    theta=coef[-4:]
    group=pd.Series(groups).to_numpy()
    distinct=np.unique(group)
    G=len(distinct)
    meat=np.zeros((q,q))
    for g in distinct:
        v=scores[group==g].sum(axis=0)
        meat+=np.outer(v,v)
    corr=(G/(G-1))*((n-1)/(n-q))
    cov=inv@meat@inv*corr
    cov=(cov+cov.T)/2
    c=cov[-4:,-4:]
    test=float(theta@np.linalg.pinv(c)@theta/4)
    fields["uf_cluster_F4"]=test
    fields["uf_cluster_p_F4_"+str(G-1)]=float(f.sf(max(test,0),4,G-1))
    for km,(K,npairs) in kernels.items():
        meat=scores.T@(K@scores)
        cc=(inv@meat@inv)
        cc=(cc+cc.T)/2
        v=cc[-4:,-4:]
        stat=float(theta@np.linalg.pinv(v)@theta)
        fields["conley_"+str(km)+"km_wald_chi2_4"]=stat
        fields["conley_"+str(km)+"km_p_qui2_4"]=float(chi2.sf(max(stat,0),4))
        fields["conley_"+str(km)+"km_pares"]=npairs
    fields["coef_contexto_padronizado"]=[float(x) for x in theta]
    return fields

def estado_cv(d,features,contexto,y,w):
    ufs=np.sort(d.SG_UF.unique())
    grupo=d.SG_UF.to_numpy()
    full=np.column_stack([features,contexto])
    saida=[]
    for fold in range(5):
        test=np.isin(grupo,ufs[fold::5])
        train=~test
        x0=pweights.padronizar(features,train)
        x1=pweights.padronizar(full,train)
        b0=pweights.wls(np.c_[np.ones(train.sum()),x0[train]],y[train],w[train])["beta"]
        b1=pweights.wls(np.c_[np.ones(train.sum()),x1[train]],y[train],w[train])["beta"]
        e0=y[test]-np.c_[np.ones(test.sum()),x0[test]]@b0
        e1=y[test]-np.c_[np.ones(test.sum()),x1[test]]@b1
        tes_uf=grupo[test];wt=w[test]
        for uf in np.unique(tes_uf):
            mask=tes_uf==uf
            saida.append({"UF":str(uf),"fold":fold+1,"n":int(mask.sum()),
              "peso_total":float(wt[mask].sum()),
              "sse_local":float(np.sum(wt[mask]*e0[mask]**2)),
              "sse_contexto":float(np.sum(wt[mask]*e1[mask]**2))})
    return saida

def bootstrap_estados(arr,nrep,seed):
    rng=np.random.default_rng(seed)
    w=arr[:,0];a=arr[:,1];b=arr[:,2]
    if (w<=0).any():raise ValueError("UF com peso nulo.")
    def ganho(idx):
        ws=w[idx].sum()
        return 100*(1-np.sqrt(b[idx].sum()/ws)/np.sqrt(a[idx].sum()/ws))
    obs=ganho(np.arange(len(w)))
    smp=rng.integers(0,len(w),size=(nrep,len(w)))
    vals=np.empty(nrep)
    for j in range(nrep): vals[j]=ganho(smp[j])
    low,high=np.quantile(vals,[.025,.975])
    return {"ganho_rmse_observado_pct":float(obs),
      "ic_bootstrap_ufs_percentil_95_inf":float(low),
      "ic_bootstrap_ufs_percentil_95_sup":float(high),
      "fracao_bootstrap_ganho_positivo":float((vals>0).mean()),
      "n_replicacoes":nrep,"n_ufs":len(w),"semente":seed,
      "advertencia":"IC de reamostragem de UFs tratadas como blocos; não corrige dependência entre UFs vizinhas e não implica inferência causal."}

def executar(panel,nrep=4999):
    out=[];ufs_data=[];inference=[]
    for ano in (2018,2022):
        d=ols.especificacao_modelo(panel.loc[panel.ano.eq(ano)].copy(),ano)
        d=d.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
        n=len(d)
        if n!=5565 or d.SG_UF.nunique()!=27:
            raise ValueError("Amostra de referência alterada.")
        xx=d[FEATS].to_numpy(dtype=float)
        nn=spatial.knn(d,8)
        lag=xx[nn].mean(axis=1)
        z=np.column_stack([xx,lag])
        z=(z-z.mean(axis=0))/z.std(axis=0)
        fu=pd.get_dummies(d.SG_UF,drop_first=True,dtype=float).to_numpy()
        X=np.column_stack([np.ones(n),fu,z])
        xyz=xyz_da_latlon(d)
        kernels={km:kernel_conley(xyz,km) for km in (100,250)}
        for label,col in OUTCOMES.items():
            y=d[col].to_numpy(dtype=float)
            for scheme in ("igual","populacao_anterior"):
                w=np.ones(n) if scheme=="igual" else d["pop_2017" if ano==2018 else "pop_2021"].to_numpy(dtype=float)
                peruf=estado_cv(d,xx,lag,y,w)
                if len(peruf)!=27 or len(set(x["UF"] for x in peruf))!=27:
                    raise ValueError("Ausência de UF na validação.")
                arr=np.array([[x["peso_total"],x["sse_local"],x["sse_contexto"]] for x in peruf])
                bs=bootstrap_estados(arr,nrep,seed=20261010+ano*100+(label=="direcao_pt13")*10+(scheme!="igual"))
                base={"ano":ano,"desfecho":label,"peso":scheme,"k":8,"n":n}
                out.append({**base,**bs})
                ufs_data.extend([{**base,**r} for r in peruf])
                res=fit_inferencia(X,y,w,d.SG_UF.to_numpy(),kernels)
                inference.append({**base,**res})
    return pd.DataFrame(out),pd.DataFrame(ufs_data),inference

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for nm in ("mapa","hhi","ibge","competitividade","pasta"):
        p.add_argument("--"+nm,type=Path,required=True)
    p.add_argument("--replicacoes",type=int,default=4999)
    a=p.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):
        raise SystemExit("Saída anterior preservada.")
    if a.replicacoes<999:raise ValueError("Reamostragens insuficientes.")
    panel,exc=prep.preparar(a.mapa,a.hhi,a.ibge,a.competitividade)
    ci,ufs,coef=executar(panel,a.replicacoes)
    a.pasta.mkdir(parents=True,exist_ok=True)
    ci.to_csv(a.pasta/"incerteza_rmse_bootstrap_uf.csv",index=False,float_format="%.10f")
    ufs.to_csv(a.pasta/"erros_validacao_por_uf.csv",index=False,float_format="%.10f")
    (a.pasta/"wald_contexto_cluster_e_conley.json").write_text(json.dumps(coef,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest={"tipo":"Inferência descritiva para modelos com características de vizinhos, NÃO causal",
      "data":"10/10/2026","n_municipios":5565,"unidades_cluster":27,
      "bootstrap":"UF inteira, reamostra de contribuições fora da amostra; percentis 2.5% e 97.5%; estado no fold nunca participa do treino; folds compartilham treinos",
      "wald_uf":"OLS/WLS com covariância cluster robusta CR1 pela UF; F Wald 4 regressoras de contexto, gl denominador=26",
      "conley":"HAC espacial com Bartlett e distâncias entre centroides municipais; raios 100 e 250 km, WLS transformado por raiz da ponderação; qui-quadrado Wald aproximado",
      "cautelas":["UFs próximas podem continuar correlacionadas, logo IC bootstrap estadual pode subestimar incerteza.",
        "Conley HAC assume regularidade espacial/assintótica e não resolve variáveis omitidas.",
        "Os resultados são sensíveis a pesos, controles e definição de vizinhança.",
        "Os valores de 2018/2022 são históricos; nenhuma alegação de previsão ex ante ou transmissão social individual.",
        "O primeiro turno de 2018 mantém ressalva documental de 76 votos e não integra o desfecho principal."],
      "excluidos_censo2010":exc}
    (a.pasta/"manifesto.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(ci.to_string(index=False))
    print(pd.DataFrame([{k:v for k,v in z.items() if k!="coef_contexto_padronizado"} for z in coef]).to_string(index=False))
if __name__=="__main__":main()
