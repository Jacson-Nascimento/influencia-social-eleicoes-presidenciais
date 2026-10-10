#!/usr/bin/env python3
"""Moran municipal do HHI eleitoral: 2018 e 2022, TSE + IBGE, teste não causal."""
import argparse, hashlib, json, tempfile, zipfile, shutil
from pathlib import Path
import numpy as np
import pandas as pd

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""): h.update(b)
    return h.hexdigest()

def crosswalk(path):
    with zipfile.ZipFile(path) as z:
        names=[x for x in z.namelist() if x.lower().endswith(".csv")]
        if len(names)!=1: raise ValueError("CSV TSE-IBGE ambíguo.")
        with z.open(names[0]) as f: d=pd.read_csv(f,sep=";",encoding="latin1",dtype=str)
    col=["SG_UF","CD_MUNICIPIO_TSE","CD_MUNICIPIO_IBGE"]
    if not set(col).issubset(d.columns): raise ValueError("Dicionário TSE-IBGE incompleto.")
    d=d.loc[d.SG_UF.ne("ZZ"),col].dropna().drop_duplicates()
    d["CD_MUNICIPIO_TSE"]=pd.to_numeric(d.CD_MUNICIPIO_TSE,errors="raise").astype(int)
    d["CD_MUNICIPIO_IBGE"]=d.CD_MUNICIPIO_IBGE.str.strip()
    if not d.CD_MUNICIPIO_IBGE.str.fullmatch(r"\d{7}").all(): raise ValueError("Geocódigos IBGE inválidos.")
    if d.duplicated(["SG_UF","CD_MUNICIPIO_TSE"]).any() or d.CD_MUNICIPIO_IBGE.duplicated().any():
        raise ValueError("Correspondência TSE-IBGE não bijetiva.")
    return d

def geo_ibge(path):
    import pyogrio, shapely
    with zipfile.ZipFile(path) as z, tempfile.TemporaryDirectory() as td:
        names=[x for x in z.namelist() if Path(x).suffix.lower() in (".shp",".dbf",".shx",".prj",".cpg")]
        shp=[n for n in names if n.lower().endswith(".shp")]
        if len(shp)!=1: raise ValueError("Shapefile IBGE não identificado unicamente.")
        for n in names:
            with z.open(n) as f, open(Path(td)/Path(n).name,"wb") as o: shutil.copyfileobj(f,o)
        d=pyogrio.read_dataframe(str(Path(td)/Path(shp[0]).name),columns=["CD_MUN"])
        if "CD_MUN" not in d.columns or d.geometry.isna().any(): raise ValueError("Geometrias IBGE incompletas.")
        c=shapely.centroid(d.geometry.values)
        out=pd.DataFrame({"CD_MUNICIPIO_IBGE":d.CD_MUN.astype(str).str.strip(),
                          "latitude":shapely.get_y(c),"longitude":shapely.get_x(c)})
    if out.CD_MUNICIPIO_IBGE.duplicated().any(): raise ValueError("Geocódigos duplicados na malha.")
    return out

def join_bases(cross,geo,files):
    base={}; keys=[]
    for ano,path in files:
        d=pd.read_csv(path,dtype={"SG_UF":str})
        d=d[d.SG_UF.ne("ZZ")].copy()
        chave=["ANO_ELEICAO","NR_TURNO","SG_UF","CD_MUNICIPIO","NR_CANDIDATO"]
        if not d.ANO_ELEICAO.eq(ano).all() or d.duplicated(chave).any(): raise ValueError("Chaves eleitorais inválidas.")
        if d.QT_VOTOS_NOMINAIS.lt(0).any(): raise ValueError("Votos negativos.")
        k=d[["SG_UF","CD_MUNICIPIO"]].drop_duplicates()
        if len(k)!=5570: raise ValueError(f"Cobertura municipal {ano}: {len(k)}")
        for turno in (1,2):
            if len(d[d.NR_TURNO.eq(turno)][["SG_UF","CD_MUNICIPIO"]].drop_duplicates())!=5570:
                raise ValueError("Turno com cobertura incompleta.")
        base[ano]=d;keys.append(k)
    todas=pd.concat(keys).drop_duplicates()
    if len(todas)!=5570: raise ValueError("Unidades eleitorais mudam entre 2018 e 2022.")
    m=todas.merge(cross,left_on=["SG_UF","CD_MUNICIPIO"],
                  right_on=["SG_UF","CD_MUNICIPIO_TSE"],how="left",validate="one_to_one",indicator=True)
    if not m._merge.eq("both").all(): raise ValueError("Municípios sem correspondência TSE-IBGE: "+m.loc[m._merge.ne("both")].head(5).to_json())
    m=m.drop(columns=["_merge","CD_MUNICIPIO_TSE"])
    m=m.merge(geo,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one",indicator=True)
    if not m._merge.eq("both").all() or len(m)!=5570: raise ValueError("Municípios sem geometria IBGE.")
    m=m.drop(columns="_merge").sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
    if m.isna().any().any(): raise ValueError("Coordenadas ausentes.")
    return m,base

def knn(m,k):
    from scipy.spatial import cKDTree
    lat=np.radians(m.latitude.to_numpy());lon=np.radians(m.longitude.to_numpy())
    xyz=np.c_[np.cos(lat)*np.cos(lon),np.cos(lat)*np.sin(lon),np.sin(lat)]
    v=cKDTree(xyz).query(xyz,k=k+1)[1]
    return np.asarray([row[row!=i][:k] for i,row in enumerate(v)],dtype=np.int32)

def moran(x,n):
    z=np.asarray(x,dtype=float)
    z=z-z.mean()
    d=float(z@z)
    if d<=1e-18: raise ValueError("Variância nula.")
    return float((z*np.mean(z[n],axis=1)).sum()/d)

def permutar(x,n,uf,reps,seed,estratificada):
    rng=np.random.default_rng(seed)
    v=np.asarray(x,dtype=float).copy()
    groups=[np.flatnonzero(uf==u) for u in np.unique(uf)] if estratificada else []
    if estratificada:
        for ids in groups: v[ids]-=v[ids].mean()
    observado=moran(v,n);res=np.empty(reps)
    for j in range(reps):
        if estratificada:
            t=v.copy()
            for ids in groups: t[ids]=rng.permutation(v[ids])
        else: t=rng.permutation(v)
        res[j]=moran(t,n)
    c=float(res.mean())
    return {"moran_i":observado,"p_bicaudal":float((1+np.sum(abs(res-c)>=abs(observado-c)))/(reps+1)),
            "media_nula":c}

def holm(p):
    p=np.asarray(p,dtype=float);out=np.empty(len(p));cum=0
    for i,j in enumerate(np.argsort(p)):
        cum=max(cum,(len(p)-i)*p[j]);out[j]=min(1.,cum)
    return out

def estatisticas(map_,data,ano):
    cols=["SG_UF","CD_MUNICIPIO","NR_TURNO"]
    total=data.groupby(cols,as_index=False).QT_VOTOS_NOMINAIS.sum().rename(columns={"QT_VOTOS_NOMINAIS":"validos"})
    if (total.validos<=0).any(): raise ValueError("Total válido não positivo.")
    d=data.merge(total,on=cols,validate="many_to_one")
    d["sq"]=(d.QT_VOTOS_NOMINAIS/d.validos)**2
    h=d.groupby(cols,as_index=False).sq.sum().rename(columns={"sq":"hhi"})
    res=map_.merge(h,on=["SG_UF","CD_MUNICIPIO"],validate="one_to_many",how="left")
    if len(res)!=11140 or res.hhi.isna().any(): raise ValueError("HHI municipal incompleto.")
    if ((res.hhi<=0)|(res.hhi>1.0000000001)).any():raise ValueError("HHI fora de 0-1.")
    return res.assign(ano=ano)

def executar(mapa,bases,reps):
    nei={k:knn(mapa,k) for k in (4,8,12)}
    registros=[];all_hhi=[]
    for ano in (2018,2022):
        d=estatisticas(mapa,bases[ano],ano)
        all_hhi.append(d[["ano","NR_TURNO","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","hhi"]])
        for turno in (1,2):
            t=d.loc[d.NR_TURNO.eq(turno)].sort_values(["SG_UF","CD_MUNICIPIO"])
            if len(t)!=5570:raise ValueError("Unidades incompletas.")
            for k in (4,8,12):
                for tipo in ("bruto","centrado_uf"):
                    seed=20261010 + ano*13 + turno*1000 + k*10 + (tipo=="centrado_uf")
                    result=permutar(t.hhi.to_numpy(),nei[k],t.SG_UF.to_numpy(),
                                   reps,seed,tipo=="centrado_uf")
                    registros.append({"ano":ano,"turno":turno,"k":k,"ajuste":tipo,
                                      "seed":seed,"n_municipios":5570,**result})
    out=pd.DataFrame(registros);out["p_holm_k8"]=np.nan
    for tipo in ("bruto","centrado_uf"):
        idx=out.ajuste.eq(tipo)&out.k.eq(8)
        out.loc[idx,"p_holm_k8"]=holm(out.loc[idx,"p_bicaudal"].to_numpy())
    return out,pd.concat(all_hhi,ignore_index=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for nm in ("crosswalk","malha","base2018","base2022","saida"):
        p.add_argument("--"+nm,required=True,type=Path)
    p.add_argument("--reps",type=int,default=1999)
    a=p.parse_args()
    if a.reps<99:raise ValueError("Número baixo de permutações.")
    if a.saida.exists() and any(a.saida.iterdir()):raise SystemExit("Saída anterior preservada.")
    mapa,bases=join_bases(crosswalk(a.crosswalk),geo_ibge(a.malha),
                          [(2018,a.base2018),(2022,a.base2022)])
    res,hhi=executar(mapa,bases,a.reps)
    a.saida.mkdir(parents=True,exist_ok=True)
    mapa.to_csv(a.saida/"chaves_tse_ibge_5570_centroides.csv",index=False)
    hhi.to_csv(a.saida/"hhi_municipal_2018_2022.csv",index=False)
    res.to_csv(a.saida/"moran_municipal_sensibilidade.csv",index=False,float_format="%.10f")
    manifest={"n_municipios":len(mapa),"periodos":[2018,2022],"malha_ano":2022,
        "origem_crosswalk":"https://dadosabertos.tse.jus.br/dataset/codigos-oficiais-de-uf-e-municipios-segundo-o-tse-e-o-ibge",
        "sha256_crosswalk":sha(a.crosswalk),"sha256_malha":sha(a.malha),
        "sha256_votos2018":sha(a.base2018),"sha256_votos2022":sha(a.base2022),
        "metodo":"Moran I por kNN de centroides IBGE; k=8 primário, k=4/12 sensibilidade; permutações globais ou por UF",
        "reps":a.reps,"holms":"4 testes por família bruto/centrado UF para k=8",
        "ressalva_2018":"76 votos de divergência no primeiro turno frente à notícia histórica; dados inalterados",
        "limite":"Associação espacial não demonstra influência interpessoal nem causalidade."}
    (a.saida/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(res.to_string(index=False))
if __name__=="__main__":main()
