#!/usr/bin/env python3
"""Modelos descritivos de associação HHI e controles demográficos/econômicos.

Os coeficientes, o ajuste e o Moran residual são diagnósticos de associação.
Nenhuma especificação identifica contágio eleitoral ou efeito causal.
"""
import argparse, importlib.util, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

p=Path(__file__).resolve().parent/"10_espacial_municipal.py"
spec=importlib.util.spec_from_file_location("mun",p)
mun=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mun)
COVARS=["log_pop","log_pibpc_proxy","urbanizacao_2010","fracao_feminina_2010"]

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def preparar(mapa_path,hhi_path,ibge_path):
    mapa=pd.read_csv(mapa_path,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
    hhi=pd.read_csv(hhi_path,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
    ibge=pd.read_csv(ibge_path,dtype={"CD_MUNICIPIO_IBGE":str})
    for nm,t in (("mapa",mapa),("controles",ibge)):
        if t.CD_MUNICIPIO_IBGE.duplicated().any():raise ValueError(nm+" tem código duplicado.")
    if len(mapa)!=5570 or len(hhi)!=5570*4:
        raise ValueError("Painel de votação inesperado.")
    cols=["CD_MUNICIPIO_IBGE","ano","NR_TURNO"]
    if hhi.duplicated(cols).any():raise ValueError("HHI repetido por município/ano/turno.")
    a=mapa.merge(ibge,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one",indicator=True)
    faltas_chave=a.loc[a._merge.ne("both"),"CD_MUNICIPIO_IBGE"].tolist()
    a=a.drop(columns="_merge")
    fontes=["pop_2017","pop_2021","pibpc_proxy_2016_2017_reais","pibpc_proxy_2020_2021_reais","urbanizacao_2010","fracao_feminina_2010"]
    if not set(fontes).issubset(a):raise ValueError("Faltam colunas oficiais IBGE.")
    for col in fontes[:4]:
        a.loc[a[col]<=0,col]=np.nan
    for col in fontes[4:]:
        a.loc[(a[col]<0)|(a[col]>1),col]=np.nan
    complete=a[fontes].notna().all(axis=1)
    retained=a.loc[complete].copy()
    excluded=a.loc[~complete,["SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE"]].to_dict(orient="records")
    if not 5500<=len(retained)<=5570:raise ValueError("Amostra após junção incompleta: "+str(len(retained)))
    d=retained.merge(hhi[cols+["hhi"]],on="CD_MUNICIPIO_IBGE",validate="one_to_many",how="left")
    if len(d)!=4*len(retained) or d.hhi.isna().any():raise ValueError("Painel controlado tem HHI faltante.")
    return d,excluded,faltas_chave

def especificacao_modelo(d,ano):
    x=d.copy()
    if ano==2018:
        pop="pop_2017"; pib="pibpc_proxy_2016_2017_reais"
    elif ano==2022:
        pop="pop_2021";pib="pibpc_proxy_2020_2021_reais"
    else:raise ValueError("Ano inválido")
    x["log_pop"]=np.log(x[pop].astype(float))
    x["log_pibpc_proxy"]=np.log(x[pib].astype(float))
    if not np.isfinite(x[COVARS].to_numpy(dtype=float)).all():raise ValueError("Controles não finitos.")
    return x

def fit(x,y):
    beta, *_=np.linalg.lstsq(x,y,rcond=None)
    predicted=x@beta
    residual=y-predicted
    sse=float(residual@residual)
    centered=y-y.mean()
    sst=float(centered@centered)
    n,p=x.shape
    if n<=p or sst<=0:raise ValueError("Matriz de desenho não estimável.")
    rank=int(np.linalg.matrix_rank(x))
    if rank!=p:raise ValueError("Regressores colineares.")
    r2=1-sse/sst
    return {"beta":beta,"resid":residual,"r2":r2,
            "r2_ajustado":1-(1-r2)*(n-1)/(n-p),
            "rmse_treino":float(np.sqrt(np.mean(residual**2))),
            "n":n,"n_coef":p}

def matrizes(d):
    vals=d[COVARS].to_numpy(dtype=float)
    mu=vals.mean(axis=0);sd=vals.std(axis=0)
    if (sd<=0).any():raise ValueError("Controles constantes.")
    z=(vals-mu)/sd
    uf=pd.get_dummies(d.SG_UF,drop_first=True,dtype=float)
    c=np.c_[np.ones(len(d)),uf.to_numpy()]
    full=np.c_[c,z]
    return c,full,mu,sd

def validacao_externa_uf(d):
    # Grupo de UFs inteiras fora da amostra. SEM efeitos fixos de UF,
    # pois não podem ser previstos para UFs ausentes do treino.
    y=d.hhi.to_numpy(dtype=float)
    raw=d[COVARS].to_numpy(dtype=float)
    grupos=d.SG_UF.astype(str).to_numpy()
    ufs=np.sort(np.unique(grupos))
    erros=[]
    for fold in range(5):
        teste=np.isin(grupos,ufs[fold::5]);treino=~teste
        if teste.sum()==0 or treino.sum()==0:raise ValueError("Partição inválida.")
        mean=raw[treino].mean(axis=0);sd=raw[treino].std(axis=0)
        if (sd<=0).any():raise ValueError("Feature constante no treino.")
        ztre=(raw[treino]-mean)/sd
        ztes=(raw[teste]-mean)/sd
        xb=np.ones((treino.sum(),1))
        xf=np.c_[np.ones(treino.sum()),ztre]
        by=np.linalg.lstsq(xb,y[treino],rcond=None)[0]
        fy=np.linalg.lstsq(xf,y[treino],rcond=None)[0]
        pb=np.ones((teste.sum(),1))@by
        pf=np.c_[np.ones(teste.sum()),ztes]@fy
        erros.append({"fold":fold+1,"ufs_teste":ufs[fold::5].tolist(),
          "n_teste":int(teste.sum()),"sse_baseline_media":float(np.sum((y[teste]-pb)**2)),
          "sse_controles":float(np.sum((y[teste]-pf)**2))})
    return {
       "criterio":"UF totalmente excluída do treino; nenhum efeito fixo de UF em ambos os modelos CV",
       "n_folds":5,
       "rmse_global_medio":float(np.sqrt(sum(e["sse_baseline_media"] for e in erros)/sum(e["n_teste"] for e in erros))),
       "rmse_controles":float(np.sqrt(sum(e["sse_controles"] for e in erros)/sum(e["n_teste"] for e in erros))),
       "folds":erros}

def executar(d,reps=999):
    if reps<199:raise ValueError("Permutações insuficientes.")
    rows=[]; cvs=[]; beta=[]
    total=int(d.CD_MUNICIPIO_IBGE.nunique())
    if len(d)!=total*4:raise ValueError("Painel não balanceado.")
    mapa=d.loc[(d.ano==2018)&(d.NR_TURNO==1)].sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
    near={k:mun.knn(mapa,k) for k in (4,8,12)}
    order=mapa.CD_MUNICIPIO_IBGE.astype(str).to_numpy()
    for ano in (2018,2022):
        for turno in (1,2):
            df=d.loc[(d.ano==ano)&(d.NR_TURNO==turno)].copy()
            df=especificacao_modelo(df,ano)
            df=df.set_index("CD_MUNICIPIO_IBGE").loc[order].reset_index()
            if len(df)!=total:raise ValueError("Incompatibilidade na junção por período.")
            y=df.hhi.to_numpy(dtype=float)
            X0,X1,mu,sd=matrizes(df)
            base=fit(X0,y);full=fit(X1,y)
            groups=df.SG_UF.to_numpy()
            row={"ano":ano,"turno":turno,"n_municipios":total,
                 "r2_uf":base["r2"],"r2_uf_mais_controles":full["r2"],
                 "delta_r2":full["r2"]-base["r2"],
                 "r2_ajustado_uf":base["r2_ajustado"],
                 "r2_ajustado_com_controles":full["r2_ajustado"],
                 "rmse_in_sample_uf":base["rmse_treino"],
                 "rmse_in_sample_controles":full["rmse_treino"]}
            for label,model in (("uf",base),("controles",full)):
                p=mun.permutar(model["resid"],near[8],groups,reps,20261010+ano*13+turno*100+int(label=="controles"),True)
                for name,value in p.items():row["residuo_"+label+"_"+name]=value
                if label=="controles":
                    for k in (4,12):row["residuo_controles_moran_k"+str(k)]=mun.moran(model["resid"],near[k])
            rows.append(row)
            cv=validacao_externa_uf(df);cvs.append({"ano":ano,"turno":turno,**cv})
            for name,coeff in zip(COVARS,full["beta"][-4:]):
                beta.append({"ano":ano,"turno":turno,"controle":name,"beta_padronizado_descritivo":float(coeff)})
    results=pd.DataFrame(rows)
    results["p_holm_moran_controles"]=mun.holm(results["residuo_controles_p_bicaudal"].to_numpy())
    return results,cvs,pd.DataFrame(beta)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("mapa","hhi","ibge","pasta"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--permutacoes",type=int,default=999)
    a=p.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):raise SystemExit("Preservar diretório de resultados anterior.")
    data,excluded,no_id=preparar(a.mapa,a.hhi,a.ibge)
    tab,cv,betas=executar(data,a.permutacoes)
    a.pasta.mkdir(parents=True,exist_ok=True)
    tab.to_csv(a.pasta/"modelos_e_moran_residual.csv",index=False,float_format="%.10f")
    betas.to_csv(a.pasta/"coeficientes_padronizados_descritivos.csv",index=False,float_format="%.10f")
    (a.pasta/"cv_ufs.json").write_text(json.dumps(cv,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    manifest={"n_municipios_completos":int(data.CD_MUNICIPIO_IBGE.nunique()),
        "n_municipios_excluidos":len(excluded),"municipios_excluidos":excluded,
        "sem_chave_entre_ibge_e_tse":no_id,
        "controles":["log população estimada anterior","log PIB/população proxy de anos distintos","fração urbana Censo 2010","fração mulheres Censo 2010"],
        "fontes":{"ibge":str(a.ibge),"mapa":str(a.mapa),"hhi":str(a.hhi)},
        "sha256_insumos":{"ibge":sha(a.ibge),"mapa":sha(a.mapa),"hhi":sha(a.hhi)},
        "especificacoes":"OLS UF fixo versus UF fixo + controles; Moran residual centrado por UF, permutações restritas, k=8 primário e k=4/12 sensibilidades; CV separado por UF sem efeitos fixos",
        "permutacoes":a.permutacoes,
        "advertencia":"Modelos não causais, coeficientes sem interpretação de mudança individual de voto. Moran residual e sua permutação são diagnósticos aproximados após ajuste de regressão; valores-p não equivalem a testes causais formais. As proxies PIB/pop estão em anos diferentes.",
        "vintage":"Dados IBGE consultados em 2026, eventualmente revisados; não se alega conjunto informacional disponível ex ante."}
    (a.pasta/"manifesto_controles_e_modelos.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(tab.to_string(index=False))
    print(json.dumps({"municipios":manifest["n_municipios_completos"],"excluidos":excluded,"cv":cv},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
