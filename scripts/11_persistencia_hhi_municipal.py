#!/usr/bin/env python3
"""Persistência territorial e variação de HHI. Descritivo, não causal."""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd

path=Path(__file__).resolve().parent/"10_espacial_municipal.py"
spec=importlib.util.spec_from_file_location("mun",path)
mun=importlib.util.module_from_spec(spec);spec.loader.exec_module(mun)

def analisar(mapa_path, indicadores_path, reps=1999):
    mapa=pd.read_csv(mapa_path,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
    df=pd.read_csv(indicadores_path,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
    if len(mapa)!=5570 or mapa.CD_MUNICIPIO_IBGE.duplicated().any():
        raise ValueError("Correspondência municipal incompleta.")
    cols=["CD_MUNICIPIO_IBGE","ano","NR_TURNO"]
    if df.duplicated(cols).any() or len(df)!=4*5570:raise ValueError("HHI contém lacunas ou duplicidades.")
    pivot=df.pivot(index="CD_MUNICIPIO_IBGE",columns=["ano","NR_TURNO"],values="hhi")
    pivot=pivot.reindex(mapa.CD_MUNICIPIO_IBGE)
    if pivot.shape!=(5570,4) or pivot.isna().any().any():raise ValueError("Painel municipal não balanceado.")
    results={"n_municipios":5570,"comparacoes_temporais":[],"mudancas_entre_turnos":[]}
    uf=mapa.SG_UF.to_numpy()
    nei=mun.knn(mapa,8)
    for t in (1,2):
        a=pivot[(2018,t)].to_numpy();b=pivot[(2022,t)].to_numpy()
        ra=np.argsort(np.argsort(a,kind="stable"),kind="stable")
        rb=np.argsort(np.argsort(b,kind="stable"),kind="stable")
        # A avaliação definitiva de Spearman usa scipy.stats para tratar empates.
        from scipy.stats import spearmanr
        residual_a=a.copy(); residual_b=b.copy()
        for u in np.unique(uf):
            idx=(uf==u)
            residual_a[idx]-=a[idx].mean()
            residual_b[idx]-=b[idx].mean()
        results["comparacoes_temporais"].append({
            "turno":t,"pearson_bruto":float(np.corrcoef(a,b)[0,1]),
            "spearman_bruto":float(spearmanr(a,b).statistic),
            "pearson_apos_media_uf":float(np.corrcoef(residual_a,residual_b)[0,1]),
            "n":5570
        })
    for ano in (2018,2022):
        d=pivot[(ano,2)].to_numpy()-pivot[(ano,1)].to_numpy()
        raw=mun.permutar(d,nei,uf,reps,seed=20261010+ano*100,estratificada=False)
        control=mun.permutar(d,nei,uf,reps,seed=20261010+ano*100+1,estratificada=True)
        results["mudancas_entre_turnos"].append({
            "ano":ano,
            "mediana_delta_hhi":float(np.median(d)),
            "media_delta_hhi":float(np.mean(d)),
            "proporcao_municipios_delta_hhi_positivo":float((d>0).mean()),
            "moran_k8_bruto_delta_hhi":raw,
            "moran_k8_apos_media_uf_delta_hhi":control
        })
    results["advertencia"]="A correlação temporal e o agrupamento de variações não identificam contágio entre eleitores nem mudança individual de votos. Diferença de 76 votos na base de 2018 sob ressalva."
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mapa",type=Path,required=True)
    p.add_argument("--hhi",type=Path,required=True)
    p.add_argument("--saida",type=Path,required=True)
    p.add_argument("--reps",type=int,default=1999)
    a=p.parse_args()
    if a.saida.exists():raise SystemExit("Arquivo anterior preservado.")
    out=analisar(a.mapa,a.hhi,a.reps)
    a.saida.parent.mkdir(parents=True,exist_ok=True)
    a.saida.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
