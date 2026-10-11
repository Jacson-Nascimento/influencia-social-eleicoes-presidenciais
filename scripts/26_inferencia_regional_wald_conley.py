#!/usr/bin/env python3
"""Inferência conjunta com benchmark de macrorregiões — C e M, 2018/2022.

X: constante, quatro características municipais padronizadas, quatro dummies
de macrorregião e quatro médias socioeconômicas dos oito vizinhos.
Não usar efeitos fixos de UF simultaneamente com dummies macrorregionais:
haveria colinearidade perfeita. A UF é o agrupamento de covariância CR1.
Conley: kernel espacial Bartlett com 100 e 250 km entre centroides IBGE 2022.
Resultados descritivos, não causais; valores-p exploratórios.
"""
import argparse, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent

def imp(n,p):
    spec=importlib.util.spec_from_file_location(n,HERE/p)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

original=imp("spatial_inference_v20","20_inferencia_espacial_validacao.py")
geo=imp("geographic_bench_v22","22_benchmark_geografico_competitividade.py")
comp=imp("comp_v16","16_modelos_competitividade.py")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ("mapa","hhi","ibge","competitividade","out"):
        ap.add_argument("--"+name,required=True,type=Path)
    args=ap.parse_args()
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit("Saída anterior preservada; selecione nova pasta.")
    panel,excluded=comp.preparar(args.mapa,args.hhi,args.ibge,args.competitividade)
    records=[]
    for ano in (2018,2022):
        d,arr,wx=geo.data_year(panel,ano)
        B=arr["socio_mais_macrorregiao"]
        # Preservar as dummies macroregionais: apenas colunas contínuas normalizadas.
        X0=np.column_stack([B,wx]).astype(float)
        mu=X0.mean(axis=0); sd=X0.std(axis=0)
        if (sd<1e-12).any(): raise ValueError("Coluna sem variação nos controles.")
        X=np.column_stack([np.ones(len(d)),(X0-mu)/sd])
        if X.shape!=(5565,13) or np.linalg.matrix_rank(X)!=13:
            raise ValueError("Posto/forma inválidos no modelo regional.")
        xyz=original.xyz_da_latlon(d)
        kernels={km:original.kernel_conley(xyz,km) for km in (100,250)}
        for desfecho,col in comp.OUTCOMES.items():
            y=d[col].to_numpy(dtype=float)
            for peso in ("uniforme","populacao_anterior"):
                w=np.ones(len(d)) if peso=="uniforme" else d["pop_2017" if ano==2018 else "pop_2021"].to_numpy(dtype=float)
                r=original.fit_inferencia(X,y,w,d.SG_UF.to_numpy(),kernels)
                records.append({
                    "ano":ano,"desfecho":desfecho,"ponderacao":peso,
                    "benchmark":"socio_mais_macrorregiao",
                    "n":len(d),"n_uf_cluster":d.SG_UF.nunique(),
                    "regressores_contextuais":4,
                    "wald_F4_uf":r["uf_cluster_F4"],
                    "p_uf_CR1_26gl":r["uf_cluster_p_F4_26"],
                    "wald_chi2_conley_100km":r["conley_100km_wald_chi2_4"],
                    "p_conley_100km":r["conley_100km_p_qui2_4"],
                    "wald_chi2_conley_250km":r["conley_250km_wald_chi2_4"],
                    "p_conley_250km":r["conley_250km_p_qui2_4"],
                    "pares_conley_100km":r["conley_100km_pares"],
                    "pares_conley_250km":r["conley_250km_pares"],
                    "coeficientes_contextuais":json.dumps(r["coef_contexto_padronizado"])
                })
    t=pd.DataFrame(records)
    if len(t)!=8 or t.duplicated(["ano","desfecho","ponderacao"]).any():
        raise AssertionError("Esperadas 8 combinações únicas.")
    for c in ("p_uf_CR1_26gl","p_conley_100km","p_conley_250km"):
        if not t[c].between(0,1).all():raise AssertionError("Valor-p fora de [0,1].")
    args.out.mkdir(parents=True)
    t.to_csv(args.out/"wald_conley_com_macrorregiao.csv",index=False,float_format="%.12g")
    manifest={
        "metodo":"OLS/WLS, regressoras socioeconômicas locais + macrorregiões + WX(k8)",
        "diferenca_para_A2_original":"A tabela A2 original usa efeitos fixos de UF e não inclui a macrorregião como controle distinto. Esta nova tabela usa quatro dummies regionais no modelo e UF somente para agrupamento dos erros.",
        "n":5565,"unidades_uf":27,"anos":[2018,2022],
        "familia":"linear OLS/WLS; testes Wald dos quatro parâmetros de WX",
        "inferencias":"CR1 cluster UF com F(4,26); HAC Conley Bartlett 100 e 250 km com Qui-quadrado(4)",
        "peso":"uniforme ou IBGE população anterior, versões recuperadas em 2026",
        "restricoes":["Não interpretar valores-p como ganho fora da amostra.",
                      "UFs vizinhas continuam dependentes apesar de cluster UF.",
                      "Distância por centroides e dois anos eleitorais apenas.",
                      "Resultados não estabelecem causalidade, difusão ou contágio."],
        "excluidos":excluded}
    (args.out/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(t.drop(columns=["coeficientes_contextuais"]).to_string(index=False))
if __name__=="__main__":main()
