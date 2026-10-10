#!/usr/bin/env python3
"""Estatística territorial descritiva a partir de bases presidenciais oficiais consolidadas.

2018 é uma base sob ressalva: 76 votos a mais no primeiro turno que a
totalização histórica publicada, sem qualquer ajuste artificial nos microdados.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd


def analisar(arquivos):
    nacional, estadual, variacoes = [], [], {}
    for ano, caminho in arquivos:
        df = pd.read_csv(caminho, dtype={"SG_UF": "string"})
        if not df["ANO_ELEICAO"].eq(ano).all():
            raise ValueError("Ano divergente no arquivo: " + str(ano))
        chave = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_CANDIDATO"]
        if df.duplicated(chave).any():
            raise ValueError("Chave municipal/candidatura repetida.")
        if df["QT_VOTOS_NOMINAIS"].lt(0).any():
            raise ValueError("Contagens negativas.")
        finalistas = {2018: [17, 13], 2022: [13, 22]}[ano]
        df["VOTOS_FINALISTAS"] = df["QT_VOTOS_NOMINAIS"].where(df["NR_CANDIDATO"].isin(finalistas), 0)
        grupos = []
        for (turno, uf, muni), part in df.groupby(["NR_TURNO", "SG_UF", "CD_MUNICIPIO"],
                                                   observed=True, sort=True):
            votos = part["QT_VOTOS_NOMINAIS"].astype("float64").to_numpy()
            total = int(votos.sum())
            # Contar também localidades eleitorais sem votos nominais válidos.
            # Excluí-las reduziria artificialmente a cobertura da UF ZZ.
            p = votos[votos > 0] / total if total > 0 else np.array([])
            grupos.append({"ano": ano, "turno": int(turno), "uf": uf,
                           "municipio_tse": int(muni), "validos": total,
                           "finalistas": int(part["VOTOS_FINALISTAS"].sum()),
                           "hhi": float((p * p).sum())})
        tab = pd.DataFrame(grupos)
        if set(tab.turno.unique()) != {1, 2}:
            raise ValueError("Ambos os turnos são necessários.")
        dentro = tab[tab.uf != "ZZ"]
        fora = tab[tab.uf == "ZZ"]
        for turno in (1, 2):
            todos = tab[tab.turno == turno]
            munis = dentro[dentro.turno == turno]
            exterior = fora[fora.turno == turno]
            nacional.append({
                "ano": ano, "turno": turno, "votos_validos": int(todos.validos.sum()),
                "municipios_brasil": len(munis), "localidades_exterior": len(exterior),
                "localidades_exterior_com_votos": int((exterior.validos > 0).sum()),
                "votos_validos_exterior": int(exterior.validos.sum()),
                "mediana_hhi_brasil": float(munis.hhi.median()),
                "media_hhi_ponderada_brasil": float(np.average(munis.hhi, weights=munis.validos)),
                "participacao_finalistas_total": float(todos.finalistas.sum() / todos.validos.sum())
            })
        for (uf, turno), munis in dentro.groupby(["uf", "turno"], sort=True):
            estadual.append({"ano": ano, "uf": uf, "turno": turno,
                "n_municipios": len(munis),
                "votos_validos": int(munis.validos.sum()),
                "mediana_hhi": float(munis.hhi.median()),
                "hhi_ponderado": float(np.average(munis.hhi, weights=munis.validos)),
                "participacao_finalistas": float(munis.finalistas.sum() / munis.validos.sum())})
        pv = dentro.pivot(index=["uf", "municipio_tse"], columns="turno", values="validos")
        if pv.isna().any().any():
            raise ValueError("Há municípios sem correspondência entre turnos.")
        crescimento = pv[2] - pv[1]
        variacoes[str(ano)] = {
            "municipios_pareados": len(pv),
            "frac_municipios_aumento_validos": float((crescimento > 0).mean()),
            "frac_municipios_reducao_validos": float((crescimento < 0).mean()),
            "mediana_variacao_absoluta": float(crescimento.median()),
            "mediana_variacao_percentual": float(((pv[2] / pv[1]) - 1).median()*100),
            "condicao": "ressalva documentada de 76 votos no 1º turno" if ano == 2018 else "totalização nacional conciliada"
        }
    return pd.DataFrame(nacional), pd.DataFrame(estadual), variacoes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base2018", required=True, type=Path)
    ap.add_argument("--base2022", required=True, type=Path)
    ap.add_argument("--pasta", required=True, type=Path)
    a = ap.parse_args()
    a.pasta.mkdir(parents=True, exist_ok=True)
    destinos = [a.pasta / n for n in
                ("resumo_nacional_2018_2022.csv", "resumo_uf_2018_2022.csv",
                 "comparativo_municipal_2018_2022.json")]
    if any(p.exists() for p in destinos):
        raise SystemExit("Há saída anterior. Preservada, não sobrescrita.")
    n, e, v = analisar([(2018, a.base2018), (2022, a.base2022)])
    n.to_csv(destinos[0], index=False, float_format="%.10f")
    e.to_csv(destinos[1], index=False, float_format="%.10f")
    destinos[2].write_text(json.dumps(v, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(n.to_string(index=False))
    print(json.dumps(v, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
