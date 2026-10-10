#!/usr/bin/env python3
"""Indicadores descritivos de composição de votos nominais por município/turno."""
import argparse
from pathlib import Path
import math
import pandas as pd

GROUP = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO"]
REQ = set(GROUP + ["NR_CANDIDATO", "QT_VOTOS_NOMINAIS"])

def calcular(df):
    faltantes = REQ - set(df.columns)
    if faltantes:
        raise ValueError("Colunas ausentes: " + str(sorted(faltantes)))
    if df.duplicated(GROUP + ["NR_CANDIDATO"]).any():
        raise ValueError("Candidatura repetida na mesma unidade. Agregue a fonte primeiro.")
    df = df.copy()
    df["QT_VOTOS_NOMINAIS"] = pd.to_numeric(df["QT_VOTOS_NOMINAIS"], errors="raise")
    if df["QT_VOTOS_NOMINAIS"].lt(0).any():
        raise ValueError("Votos negativos são inválidos.")
    records = []
    for idx, subset in df.groupby(GROUP, dropna=False, sort=True):
        positive = subset.loc[subset.QT_VOTOS_NOMINAIS > 0, "QT_VOTOS_NOMINAIS"]
        total = int(positive.sum())
        if total == 0:
            continue
        p = (positive / total).to_numpy(dtype=float)
        hhi = float((p * p).sum())
        entropia = -sum(float(x) * math.log(float(x)) for x in p)
        records.append(dict(zip(GROUP, idx),
            total_votos_nominais=total,
            candidaturas_com_votos=len(p),
            hhi=hhi,
            numero_efetivo_candidaturas=1 / hhi,
            entropia_shannon=entropia,
            maior_fatia_nominal=float(max(p)),
        ))
    return pd.DataFrame.from_records(records, columns=GROUP + [
        "total_votos_nominais", "candidaturas_com_votos", "hhi",
        "numero_efetivo_candidaturas", "entropia_shannon", "maior_fatia_nominal"
    ])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arquivo", type=Path, required=True)
    parser.add_argument("--saida", type=Path, required=True)
    args = parser.parse_args()
    if args.saida.exists():
        raise SystemExit("Saída existente não sobreposta: " + str(args.saida))
    df = pd.read_csv(args.arquivo)
    out = calcular(df)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.saida, index=False, encoding="utf-8")
    print("Territórios/turnos:", len(out))
    print("Indicadores meramente descritivos: HHI muda mecanicamente com o número de candidaturas.")

if __name__ == "__main__":
    main()
