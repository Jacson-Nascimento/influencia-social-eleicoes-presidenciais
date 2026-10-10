#!/usr/bin/env python3
"""Consolida votos nominais presidenciais de arquivos TSE de município-zona."""
import argparse
from pathlib import Path
import zipfile
import pandas as pd

REQUIRED = {
    "ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO", "DS_CARGO",
    "NR_CANDIDATO", "QT_VOTOS_NOMINAIS",
}
KEY = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_CANDIDATO"]

def ler_chunks(path, chunksize=100_000):
    path = Path(path)
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            nomes = [n for n in archive.namelist() if n.lower().endswith(".csv") and not n.startswith("__MACOSX/")]
            candidatos = [n for n in nomes if "votacao_candidato_munzona" in n.lower()]
            if len(candidatos) != 1:
                raise ValueError("ZIP exige exatamente um CSV votação_candidato_munzona; encontrados: " + str(candidatos))
            with archive.open(candidatos[0]) as data:
                yield from pd.read_csv(data, sep=";", encoding="latin1", dtype=str, chunksize=chunksize, low_memory=False)
    elif path.suffix.lower() == ".csv":
        yield from pd.read_csv(path, sep=";", encoding="latin1", dtype=str, chunksize=chunksize, low_memory=False)
    else:
        raise ValueError("Formato não aceito. Use ZIP ou CSV do TSE.")

def consolidar(chunks, ano):
    acumulados = []
    for chunk in chunks:
        missing = REQUIRED.difference(chunk.columns)
        if missing:
            raise ValueError("Campos obrigatórios ausentes: " + str(sorted(missing)))
        pres = chunk[chunk["DS_CARGO"].str.strip().str.upper().eq("PRESIDENTE")].copy()
        if pres.empty:
            continue
        if not pres["ANO_ELEICAO"].eq(str(ano)).all():
            raise ValueError("Ano no arquivo não coincide com o solicitado.")
        for col in ["NR_TURNO", "CD_MUNICIPIO", "NR_CANDIDATO", "QT_VOTOS_NOMINAIS"]:
            pres[col] = pd.to_numeric(pres[col], errors="raise").astype("int64")
        if pres["QT_VOTOS_NOMINAIS"].lt(0).any():
            raise ValueError("Contagem de votos negativa.")
        pres["ANO_ELEICAO"] = int(ano)
        totals = pres.groupby(KEY, dropna=False, as_index=False)["QT_VOTOS_NOMINAIS"].sum()
        acumulados.append(totals)
    if not acumulados:
        raise ValueError("Nenhuma observação presidencial encontrada.")
    all_rows = pd.concat(acumulados, ignore_index=True)
    totals = all_rows.groupby(KEY, dropna=False, as_index=False)["QT_VOTOS_NOMINAIS"].sum()
    totals = totals.sort_values(KEY).reset_index(drop=True)
    if totals.duplicated(KEY).any():
        raise AssertionError("Chave repetida após agregação.")
    if totals["QT_VOTOS_NOMINAIS"].lt(0).any():
        raise AssertionError("Votos negativos após agregação.")
    return totals

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arquivo", type=Path, required=True)
    parser.add_argument("--ano", type=int, required=True, choices=(2018, 2022, 2026))
    parser.add_argument("--saida", type=Path, required=True)
    args = parser.parse_args()
    if not args.arquivo.is_file():
        raise SystemExit("Arquivo-fonte inexistente: " + str(args.arquivo))
    out = consolidar(ler_chunks(args.arquivo), args.ano)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    if args.saida.exists():
        raise SystemExit("Saída já existe; não sobreposta: " + str(args.saida))
    out.to_csv(args.saida, index=False, encoding="utf-8")
    print("Linhas consolidadas:", len(out), "Votos nominais:", int(out["QT_VOTOS_NOMINAIS"].sum()))
    print("ATENÇÃO: confira contra totais oficiais antes de interpretar.")

if __name__ == "__main__":
    main()
