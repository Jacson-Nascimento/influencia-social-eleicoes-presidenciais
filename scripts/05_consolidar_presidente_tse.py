#!/usr/bin/env python3
"""Consolidação presidencial por município a partir do ZIP nominal oficial do TSE.

Escolhe somente o arquivo nacional BRASIL ou BR. Os demais arquivos por UF,
quando presentes, não são somados novamente, evitando duplicação de votos.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from pathlib import Path
import zipfile

import pandas as pd

COLS = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO",
        "DS_CARGO", "NR_CANDIDATO", "QT_VOTOS_NOMINAIS"]
KEY = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_CANDIDATO"]


def escolher_csv(nomes, ano):
    nomes = [n for n in nomes if n.lower().endswith(".csv") and
             "votacao_candidato_munzona" in Path(n).name.lower() and
             not n.startswith("__MACOSX/")]
    correspondencias = []
    for suffix in ("BRASIL", "BR"):
        encontrados = [n for n in nomes if Path(n).name.lower() ==
                       f"votacao_candidato_munzona_{ano}_{suffix.lower()}.csv"]
        if len(encontrados) == 1:
            correspondencias.append(encontrados[0])
        elif len(encontrados) > 1:
            raise ValueError("Nomes nacionais repetidos no ZIP.")
    if len(correspondencias) == 1:
        return correspondencias[0]
    if len(correspondencias) > 1:
        raise ValueError("Há arquivos BR e BRASIL simultaneamente: requer auditoria.")
    if len(nomes) == 1:
        return nomes[0]
    raise ValueError("Não foi identificado um CSV nacional único e inequívoco: " +
                     repr([Path(n).name for n in nomes[:35]]))


def consolidar_zip(caminho, ano, chunksize=100000):
    caminho = Path(caminho)
    if not zipfile.is_zipfile(caminho):
        raise ValueError("O arquivo de origem não é um ZIP válido.")
    votos = defaultdict(int)
    lidos = 0
    presidenciais = 0
    with zipfile.ZipFile(caminho) as z:
        selected = escolher_csv(z.namelist(), ano)
        with z.open(selected) as stream:
            chunks = pd.read_csv(stream, sep=";", encoding="latin1", dtype=str,
                                 usecols=lambda c: c in COLS, chunksize=chunksize,
                                 low_memory=False)
            for chunk in chunks:
                ausentes = set(COLS).difference(chunk.columns)
                if ausentes:
                    raise ValueError("Campos obrigatórios ausentes: " + repr(sorted(ausentes)))
                lidos += len(chunk)
                parte = chunk.loc[chunk["DS_CARGO"].str.strip().str.upper() == "PRESIDENTE"].copy()
                if parte.empty:
                    continue
                presidenciais += len(parte)
                if not parte["ANO_ELEICAO"].eq(str(ano)).all():
                    raise ValueError("Ano encontrado não coincide com o especificado.")
                for c in ("NR_TURNO", "CD_MUNICIPIO", "NR_CANDIDATO", "QT_VOTOS_NOMINAIS"):
                    parte[c] = pd.to_numeric(parte[c], errors="raise").astype("int64")
                if parte["QT_VOTOS_NOMINAIS"].lt(0).any():
                    raise ValueError("Votos negativos.")
                if not parte["NR_TURNO"].isin([1, 2]).all():
                    raise ValueError("Turno diferente de 1 e 2.")
                parte["SG_UF"] = parte["SG_UF"].str.strip().str.upper()
                if parte["SG_UF"].isna().any() or (parte["SG_UF"] == "").any():
                    raise ValueError("Sigla UF ausente.")
                parte["ANO_ELEICAO"] = ano
                agrupado = parte.groupby(KEY, dropna=False)["QT_VOTOS_NOMINAIS"].sum()
                for chave, qtd in agrupado.items():
                    votos[chave] += int(qtd)
    if not votos:
        raise ValueError("Não foram encontrados registros de presidente.")
    df = pd.DataFrame([(*k, v) for k, v in votos.items()], columns=KEY + ["QT_VOTOS_NOMINAIS"])
    df.sort_values(KEY, inplace=True)
    df.reset_index(drop=True, inplace=True)
    if df.duplicated(KEY).any():
        raise AssertionError("Chave consolidada duplicada.")
    auditoria = {
        "arquivo_csv_no_zip": selected, "linhas_csv_lidas": lidos,
        "linhas_presidenciais_lidas": presidenciais,
        "linhas_consolidadas": len(df), "votos_nominais_somados_ambos_turnos":
        int(df["QT_VOTOS_NOMINAIS"].sum()), "unidades_uf": sorted(df["SG_UF"].unique().tolist()),
        "turnos": sorted(map(int, df["NR_TURNO"].unique().tolist()))
    }
    return df, auditoria


def main():
    import json
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--arquivo", required=True, type=Path)
    ap.add_argument("--ano", type=int, choices=(2018, 2022), required=True)
    ap.add_argument("--saida", required=True, type=Path)
    ap.add_argument("--relatorio", required=True, type=Path)
    a = ap.parse_args()
    if a.saida.exists() or a.relatorio.exists():
        raise SystemExit("Saída já existente. Arquivos anteriores preservados.")
    df, info = consolidar_zip(a.arquivo, a.ano)
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    a.relatorio.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.saida, index=False, encoding="utf-8")
    a.relatorio.write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
