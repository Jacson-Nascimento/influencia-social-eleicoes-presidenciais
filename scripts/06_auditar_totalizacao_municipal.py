#!/usr/bin/env python3
"""Audita votos presidenciais municipais frente aos totais nacionais do TSE."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd


def auditar(votos, controles, ano):
    df = votos.loc[votos["ANO_ELEICAO"] == ano].copy()
    if df.empty:
        raise ValueError("Ano não encontrado.")
    key = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_CANDIDATO"]
    if df.duplicated(key).any():
        raise ValueError("Chaves de votos duplicadas.")
    if df["QT_VOTOS_NOMINAIS"].lt(0).any():
        raise ValueError("Votos negativos.")
    if sorted(df["NR_TURNO"].unique().tolist()) != [1, 2]:
        raise ValueError("Ambos os turnos são obrigatórios.")
    expected = controles.loc[controles["ANO_ELEICAO"] == ano]
    if len(expected) != 2:
        raise ValueError("Controles nacionais incompletos.")
    reports = []
    for t in (1, 2):
        sub = df.loc[df["NR_TURNO"] == t]
        total = int(sub["QT_VOTOS_NOMINAIS"].sum())
        check = expected.loc[expected["NR_TURNO"] == t].iloc[0]
        esperado = int(check["TOTAL_VALIDOS"])
        por_candidato = (sub.groupby("NR_CANDIDATO")["QT_VOTOS_NOMINAIS"].sum()
                         .astype("int64").to_dict())
        verificacoes = {}
        for codigo in ("CANDIDATO_1", "CANDIDATO_2"):
            candidate = int(check[codigo])
            observado = int(por_candidato.get(candidate, 0))
            referencia = int(check["VOTOS_" + codigo])
            verificacoes[str(candidate)] = {"observado": observado, "referencia": referencia,
                                           "diferenca": observado - referencia}
        outros = total - sum(int(por_candidato.get(int(check[c]), 0))
                             for c in ("CANDIDATO_1", "CANDIDATO_2"))
        outros_ref = int(check["VOTOS_OUTROS"])
        ok = total == esperado and outros == outros_ref and all(
            x["diferenca"] == 0 for x in verificacoes.values())
        reports.append({
            "turno": t, "votos_validos_observados": total,
            "votos_validos_referencia": esperado, "residuo_total": total - esperado,
            "outros_observados": outros, "outros_referencia": outros_ref,
            "candidatos": verificacoes, "uf_inclui_exterior":
            "ZZ" in set(sub["SG_UF"].tolist()),
            "uf_quantidade": int(sub["SG_UF"].nunique()),
            "municipios_uf_distintos": int(sub[["SG_UF", "CD_MUNICIPIO"]].drop_duplicates().shape[0]),
            "aprovado": ok,
        })
    return {"ano": ano, "aprovado": all(r["aprovado"] for r in reports),
            "turnos": reports,
            "limites": "Agregação territorial não identifica transferência individual ou influência causal."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--arquivo", required=True, type=Path)
    p.add_argument("--controles", required=True, type=Path)
    p.add_argument("--ano", required=True, type=int, choices=(2018, 2022))
    p.add_argument("--saida", required=True, type=Path)
    a = p.parse_args()
    if a.saida.exists():
        raise SystemExit("Relatório já existe, não sobrescrever.")
    df = pd.read_csv(a.arquivo, dtype={"SG_UF": str})
    ctr = pd.read_csv(a.controles)
    report = auditar(df, ctr, a.ano)
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    a.saida.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["aprovado"]:
        raise SystemExit("Divergência com totalização oficial; resultados não aprovados.")


if __name__ == "__main__":
    main()
