#!/usr/bin/env python3
"""Autocorrelação exploratória da concentração de votos por UF.

Vizinhança: quatro UFs mais próximas dos centroides geométricos da malha do IBGE.
Não equivale à contiguidade municipal nem identifica influência causal.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from shapely.geometry import shape


def malha_estadual(geo, metadata):
    estados = {int(item["id"]): item["sigla"] for item in metadata}
    features = geo.get("features", [])
    positions = {}
    for feature in features:
        props = feature.get("properties", {})
        keys = [feature.get("id")] + [props.get(k) for k in
               ("id", "codarea", "CD_UF", "codigo", "codigo_ibge")]
        codes = []
        for key in keys:
            if key is not None:
                try:
                    codes.append(int(key))
                except (ValueError, TypeError):
                    pass
        ids = sorted(set(codes).intersection(estados))
        if len(ids) != 1:
            raise ValueError("IBGE GeoJSON contém feature sem UF identificável de forma única: " +
                             json.dumps({"id": feature.get("id"), "properties": props}, ensure_ascii=False)[:1000])
        sigla = estados[ids[0]]
        if sigla in positions:
            raise ValueError("UF duplicada na malha geográfica.")
        geom = shape(feature["geometry"])
        if geom.is_empty:
            raise ValueError("Geometria vazia: " + sigla)
        centroid = geom.centroid
        positions[sigla] = (centroid.y, centroid.x)
    if len(positions) != 27:
        raise ValueError("Malha deve conter exatamente 27 UFs; contém " + str(len(positions)))
    return positions


def haversine_radians(latlon):
    lat = np.radians(latlon[:, 0])[:, None]
    lon = np.radians(latlon[:, 1])[:, None]
    dlat = lat-lat.T
    dlon = lon-lon.T
    h = np.sin(dlat/2)**2 + np.cos(lat)*np.cos(lat.T)*np.sin(dlon/2)**2
    return 2 * np.arcsin(np.sqrt(np.maximum(0, np.minimum(1, h))))


def pesos_knn(positions, ufs, vizinhos=4):
    a = np.array([positions[uf] for uf in ufs], dtype=float)
    d = haversine_radians(a)
    np.fill_diagonal(d, np.inf)
    w = np.zeros_like(d)
    for i in range(len(ufs)):
        neighbors = np.argsort(d[i])[:vizinhos]
        w[i, neighbors] = 1 / vizinhos
    return w


def moran(x, w):
    x = np.asarray(x, dtype=float)
    z = x - x.mean()
    if len(x) != w.shape[0] or np.sum(z*z) <= 1e-25:
        raise ValueError("Dimensão inválida ou variância insuficiente.")
    return float((len(x) / w.sum()) * (z @ w @ z) / (z @ z))


def permutacao(x, w, rep=9999, seed=20261010):
    rng = np.random.default_rng(seed)
    observado = moran(x, w)
    perm = np.array([moran(rng.permutation(x), w) for _ in range(rep)])
    centro = perm.mean()
    extremos = (np.abs(perm-centro) >= np.abs(observado-centro)).sum()
    return {"I": observado, "p_permutacional_bicaudal": float((extremos+1)/(rep+1)),
            "valor_medio_nulo": float(centro), "repeticoes": rep, "seed": seed}


def calcular(votos2018, votos2022, positions):
    ufs = sorted(positions)
    w = pesos_knn(positions, ufs, vizinhos=4)
    outcomes = []
    for ano, arquivo in ((2018, votos2018), (2022, votos2022)):
        df = pd.read_csv(arquivo)
        df = df[(df["SG_UF"] != "ZZ") & df["SG_UF"].isin(ufs)]
        sums = df.groupby(["NR_TURNO", "SG_UF", "NR_CANDIDATO"], as_index=False)["QT_VOTOS_NOMINAIS"].sum()
        for turno, sub in sums.groupby("NR_TURNO"):
            reg = []
            for uf, g in sub.groupby("SG_UF"):
                v = g["QT_VOTOS_NOMINAIS"].to_numpy(dtype=float)
                p = v / v.sum()
                reg.append((uf, float(np.sum(p*p))))
            values = dict(reg)
            if sorted(values) != ufs:
                raise ValueError("Cobertura estadual incompleta para " + str((ano, turno)))
            outcome = {"ano": ano, "turno": int(turno),
                       "medida": "HHI da composição de votos presidenciais válidos por UF",
                       "n_ufs": len(ufs),
                       "vizinhos_knn": 4,
                       **permutacao([values[uf] for uf in ufs], w)}
            outcomes.append(outcome)
    return outcomes, w


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for nm in ("votos2018", "votos2022", "geo", "metadata", "saida"):
        p.add_argument("--"+nm, required=True, type=Path)
    a=p.parse_args()
    if a.saida.exists():
        raise SystemExit("Resultado preexistente preservado.")
    geostr=a.geo.read_bytes()
    metastr=a.metadata.read_bytes()
    pos=malha_estadual(json.loads(geostr), json.loads(metastr))
    resultados, W=calcular(a.votos2018, a.votos2022, pos)
    report={
        "natureza": "exploratória descritiva, não causal e não preditiva",
        "escala": "27 unidades da federação",
        "pesos": "k=4 vizinhos mais próximos pela distância de Haversine entre centroides da malha IBGE; matriz dirigida e normalizada por linha",
        "referencia_geojson": "https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?intrarregiao=UF&formato=application/vnd.geo%2Bjson&qualidade=minima",
        "referencia_metadata": "https://servicodados.ibge.gov.br/api/v1/localidades/estados",
        "sha256_geojson": hashlib.sha256(geostr).hexdigest(),
        "sha256_metadata": hashlib.sha256(metastr).hexdigest(),
        "ressalva_2018": "diferença de +76 votos em 2018, turno 1, entre ZIP público e notícia histórica; não ajustada",
        "resultados": resultados,
        "limitacoes": "Dependência territorial da concentração não equivale a contágio social. Amostra de apenas 27 UFs, geometria contemporânea e múltiplas comparações; interpretar p-valores como exploratórios."
    }
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    a.saida.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
