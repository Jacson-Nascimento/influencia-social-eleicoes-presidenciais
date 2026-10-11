#!/usr/bin/env python3
"""Padroniza em 4.999 os bootstrap UFs da validação geográfica regional.

Reutiliza exclusivamente os SSE por UF do benchmark regional v02;
não recalcula resultados eleitorais, regressores, dobras nem RMSE.
Preserva v01 e v02 para rastreabilidade.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bench",type=Path,required=True)
    p.add_argument("--sse",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    if a.out.exists() and any(a.out.iterdir()):
        raise SystemExit("Não substituir resultados existentes.")
    bench=pd.read_csv(a.bench)
    sse=pd.read_csv(a.sse)
    records=[]
    for _,r in bench.iterrows():
        choose=((sse.ano==r.ano)&(sse.desfecho==r.desfecho)&
                (sse.ponderacao==r.ponderacao)&(sse.benchmark==r.benchmark)&
                (sse.familia==r.familia))
        arr=sse.loc[choose].sort_values("UF")[["sse_baseline","sse_contexto"]].to_numpy(dtype=float)
        assert len(arr)==27
        seed=20261011+int(r.ano)*11+len(r.benchmark)+len(r.desfecho)+len(r.ponderacao)+len(r.familia)
        rng=np.random.default_rng(seed)
        draws=rng.integers(0,27,size=(4999,27))
        sums=arr[draws].sum(axis=1)
        gains=100*(1-np.sqrt(sums[:,1]/sums[:,0]))
        obs=100*(1-np.sqrt(arr[:,1].sum()/arr[:,0].sum()))
        assert abs(obs-r.reducao_rmse_pct)<1e-5
        rr=r.copy()
        rr["bootstrap_uf_ci95_inf"],rr["bootstrap_uf_ci95_sup"]=np.quantile(gains,[.025,.975])
        records.append(rr)
    df=pd.DataFrame(records)
    assert len(df)==48 and len(sse)==48*27
    a.out.mkdir(parents=True)
    df.to_csv(a.out/"comparacao_benchmarks_uf_bootstrap_4999.csv",index=False,float_format="%.10f")
    meta={"versao":"v03","repeticoes_uf":4999,"n_ufs":27,
        "origem":"outputs/benchmark_geografico_v02/sse_por_uf_e_modelo.csv",
        "modificacao":"somente limites de bootstrap de 95%, pontos estimados preservados",
        "nota":"A rotina original de inferência espacial usa 4.999 repetições; a rodada benchmark v02 usava 1.999. v03 padroniza ambas em 4.999.",
        "ressalva":"UFs limítrofes não necessariamente independentes; intervalos exploratórios."}
    (a.out/"manifesto.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
    print(df[["ano","desfecho","ponderacao","benchmark","familia","reducao_rmse_pct","bootstrap_uf_ci95_inf","bootstrap_uf_ci95_sup"]].to_string(index=False))
if __name__=="__main__":main()
