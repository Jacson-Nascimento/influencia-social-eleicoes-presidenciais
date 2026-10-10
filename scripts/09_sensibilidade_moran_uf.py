#!/usr/bin/env python3
"""Sensibilidade do índice Moran I para k=3,4,5,6 e correção Holm.

Reutiliza funções auditadas do script 08; quatro testes de referência
são ajustados para multiplicidade sobre k=4.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import pandas as pd
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("moran_uf", HERE / "08_autocorrelacao_uf.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def holm_quatro(pvals):
    ordem = np.argsort(pvals)
    saida = [None] * len(pvals)
    acumulado = 0.0
    for pos, i in enumerate(ordem):
        acumulado = max(acumulado, float((len(pvals)-pos)*pvals[i]))
        saida[int(i)] = min(1.0, acumulado)
    return saida


def avaliar(geo, meta, arquivos):
    pos = base.malha_estadual(geo, meta)
    ufs = sorted(pos)
    rows = []
    for ano, arquivo in arquivos:
        df = pd.read_csv(arquivo)
        df = df[(df["SG_UF"] != "ZZ") & df["SG_UF"].isin(ufs)]
        agg = df.groupby(["NR_TURNO", "SG_UF", "NR_CANDIDATO"], as_index=False)["QT_VOTOS_NOMINAIS"].sum()
        for turno in (1, 2):
            sub = agg[agg.NR_TURNO == turno]
            hhi = {}
            for uf, x in sub.groupby("SG_UF"):
                v = x["QT_VOTOS_NOMINAIS"].to_numpy(dtype=float)
                p = v/v.sum()
                hhi[uf] = float((p*p).sum())
            if sorted(hhi) != ufs:
                raise ValueError("Cobertura incompleta para " + str((ano, turno)))
            vetor = [hhi[uf] for uf in ufs]
            for k in (3, 4, 5, 6):
                W = base.pesos_knn(pos, ufs, vizinhos=k)
                resultado = base.permutacao(vetor, W, rep=9999, seed=20261010)
                rows.append({"ano": ano, "turno": turno, "k_vizinhos": k,
                             "I": resultado["I"],
                             "p_permutacional": resultado["p_permutacional_bicaudal"]})
    df = pd.DataFrame(rows).sort_values(["ano", "turno", "k_vizinhos"]).reset_index(drop=True)
    ref = df[df.k_vizinhos == 4].copy()
    ref["p_ajustado_holm"] = holm_quatro(ref.p_permutacional.to_numpy(dtype=float))
    return df, ref


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("geo", "metadata", "votos2018", "votos2022", "pasta"):
        p.add_argument("--"+name, type=Path, required=True)
    a = p.parse_args()
    destino_csv = a.pasta / "sensibilidade_knn_moran.csv"
    destino_json = a.pasta / "holm_quatro_testes.json"
    if destino_csv.exists() or destino_json.exists():
        raise SystemExit("Saídas existentes preservadas.")
    df, ref = avaliar(json.loads(a.geo.read_text()), json.loads(a.metadata.read_text()),
                      [(2018, a.votos2018), (2022, a.votos2022)])
    a.pasta.mkdir(parents=True, exist_ok=True)
    df.to_csv(destino_csv, index=False, float_format="%.10f")
    saida = {"aviso": "p ajustado somente entre os quatro testes fixados em k=4; k=3,5,6 são sensibilidades descritivas",
             "metodo": "Holm, bicaudal, 9999 permutações por teste e seed 20261010",
             "resultados": ref.to_dict(orient="records")}
    destino_json.write_text(json.dumps(saida, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(df.to_string(index=False))
    print(json.dumps(saida, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
