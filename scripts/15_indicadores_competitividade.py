#!/usr/bin/env python3
"""Competitividade presidencial municipal (2º turno) e análises do 1º turno.

Fonte: votos nominais municipais do TSE já auditados no repositório.
Não alterar bases de votos/HHI originais. Nunca inferir escolha individual.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

FINALISTAS = {
    2018: {13: "Fernando Haddad (PT)", 17: "Jair Bolsonaro (PSL)"},
    2022: {13: "Luiz Inácio Lula da Silva (PT)", 22: "Jair Bolsonaro (PL)"},
}
CHAVE = ["ANO_ELEICAO", "NR_TURNO", "SG_UF", "CD_MUNICIPIO"]


def sha256(arquivo):
    h = hashlib.sha256()
    with Path(arquivo).open("rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def calcular_eleicao(votos, ano):
    necessarias = set(CHAVE + ["NR_CANDIDATO", "QT_VOTOS_NOMINAIS"])
    if not necessarias.issubset(votos.columns):
        raise ValueError("Ausência de campos eleitorais: " + str(sorted(necessarias - set(votos.columns))))
    v = votos.copy()
    if len(v) and not v.ANO_ELEICAO.eq(ano).all():
        raise ValueError("Ano eleitoral incorreto.")
    if v.duplicated(CHAVE + ["NR_CANDIDATO"]).any():
        raise ValueError("Chaves de candidaturas duplicadas.")
    if v.QT_VOTOS_NOMINAIS.isna().any() or (v.QT_VOTOS_NOMINAIS < 0).any():
        raise ValueError("Contagens inválidas de votos.")
    v = v.loc[v.SG_UF.ne("ZZ")].copy()
    if set(v.NR_TURNO.unique()) != {1, 2}:
        raise ValueError("São necessários os dois turnos.")
    for turno in (1, 2):
        n = v.loc[v.NR_TURNO.eq(turno), ["SG_UF", "CD_MUNICIPIO"]].drop_duplicates().shape[0]
        if n != 5570:
            raise ValueError(f"Cobertura de municípios {ano}, turno {turno}: {n}, esperado 5.570.")

    # Turno 2: dois finalistas nacionais explicitamente identificados.
    t2 = v[v.NR_TURNO.eq(2)]
    ids = set(FINALISTAS[ano])
    if set(t2.NR_CANDIDATO.unique()) != ids:
        raise ValueError("Segundo turno contém candidatos diferentes dos finalistas históricos.")
    t2 = t2.pivot(index=["SG_UF", "CD_MUNICIPIO"],
                  columns="NR_CANDIDATO", values="QT_VOTOS_NOMINAIS")
    if t2.isna().any().any():
        raise ValueError("Finalista sem registro em município; não imputar zero.")
    oponente = next(x for x in ids if x != 13)
    a = t2[13].astype("int64")
    b = t2[oponente].astype("int64")
    total = a + b
    if (total <= 0).any():
        raise ValueError("Município sem votos válidos no 2º turno.")
    segundo = pd.DataFrame({
        "ano": ano,
        "SG_UF": t2.index.get_level_values("SG_UF"),
        "CD_MUNICIPIO": t2.index.get_level_values("CD_MUNICIPIO"),
        "votos_pt13": a.to_numpy(),
        "votos_oponente": b.to_numpy(),
        "numero_oponente": oponente,
        "total_validos": total.to_numpy(),
        "parcela_pt13": (a / total).to_numpy(),
        "parcela_oponente": (b / total).to_numpy(),
        # Índice principal: 1 para empate, 0 para monopólio da votação.
        "competitividade_2t": (1.0 - (a - b).abs() / total).to_numpy(),
        # Direção: positivo para maior votação de candidatura 13, negativo para oponente.
        "margem_assinada_pt13": ((a - b) / total).to_numpy(),
    })
    if len(segundo) != 5570 or not segundo.competitividade_2t.between(0, 1).all():
        raise AssertionError("Indicador de segundo turno incorreto.")
    if not np.allclose(segundo.competitividade_2t, 1.0 - np.abs(segundo.margem_assinada_pt13)):
        raise AssertionError("Identidade de competitividade não fecha.")
    if not np.allclose(segundo.parcela_pt13 + segundo.parcela_oponente, 1.0):
        raise AssertionError("Parcelas de segundo turno não somam 100%.")
    if segundo.total_validos.sum() != int(total.sum()):
        raise AssertionError("Total da votação alterado.")

    # Turno 1: indicador condicional entre as duas candidaturas mais votadas
    # DENTRO de cada município (não necessariamente finalistas nacionais).
    t1 = v.loc[v.NR_TURNO.eq(1)].copy()
    registros = []
    for (uf, municipio), grupo in t1.groupby(["SG_UF", "CD_MUNICIPIO"], sort=True):
        qtd = grupo.QT_VOTOS_NOMINAIS.to_numpy(dtype=np.int64)
        cod = grupo.NR_CANDIDATO.to_numpy(dtype=int)
        validos = int(qtd.sum())
        if validos <= 0:
            raise ValueError("Município sem votos válidos no primeiro turno.")
        pos = np.argsort(-qtd, kind="stable")
        top1, top2 = int(qtd[pos[0]]), int(qtd[pos[1]])
        cobertura = (top1 + top2) / validos
        p = qtd / validos
        hhi = float(np.sum(p*p))
        mp = dict(zip(cod, qtd))
        dir_pt = (int(mp.get(13, 0)) - int(mp.get(oponente, 0))) / validos
        registros.append({
            "ano": ano, "SG_UF": uf, "CD_MUNICIPIO": int(municipio),
            "total_validos": validos,
            "codigo_primeiro": int(cod[pos[0]]),
            "codigo_segundo": int(cod[pos[1]]),
            "votos_primeiro": top1, "votos_segundo": top2,
            "cobertura_top2": cobertura,
            "competitividade_top2_condicional": 1 - abs(top1 - top2) / (top1 + top2),
            "hhi_primeiro_turno": hhi,
            "numero_efetivo_candidaturas": 1 / hhi,
            "margem_pt13_vs_oponente_nacional_sobre_validos": dir_pt,
            "votos_outras_candidaturas": validos - (top1 + top2),
        })
    primeiro = pd.DataFrame(registros)
    if len(primeiro) != 5570:
        raise AssertionError("Número de municípios incorreto no primeiro turno.")
    if not primeiro.cobertura_top2.between(0,1).all():
        raise AssertionError("Cobertura das duas principais candidaturas inválida.")
    if not primeiro.competitividade_top2_condicional.between(0,1).all():
        raise AssertionError("Competitividade condicionada inválida.")
    if not np.allclose(primeiro.votos_outras_candidaturas + primeiro.votos_primeiro +
                       primeiro.votos_segundo, primeiro.total_validos):
        raise AssertionError("Conciliação das candidaturas no primeiro turno falhou.")
    return primeiro, segundo


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base2018",required=True,type=Path)
    p.add_argument("--base2022",required=True,type=Path)
    p.add_argument("--pasta",required=True,type=Path)
    a=p.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):
        raise SystemExit("Resultados anteriores preservados. Escolha diretório novo.")
    a.pasta.mkdir(parents=True,exist_ok=True)
    a2018=pd.read_csv(a.base2018, dtype={"SG_UF":str})
    a2022=pd.read_csv(a.base2022, dtype={"SG_UF":str})
    p18,s18=calcular_eleicao(a2018,2018)
    p22,s22=calcular_eleicao(a2022,2022)
    first=pd.concat([p18,p22],ignore_index=True).sort_values(["ano","SG_UF","CD_MUNICIPIO"])
    second=pd.concat([s18,s22],ignore_index=True).sort_values(["ano","SG_UF","CD_MUNICIPIO"])
    first.to_csv(a.pasta/"indicadores_complementares_primeiro_turno.csv",index=False,float_format="%.12f")
    second.to_csv(a.pasta/"competitividade_e_margem_assinada_segundo_turno.csv",index=False,float_format="%.12f")
    summary=[]
    for ano in (2018,2022):
        x=second[second.ano.eq(ano)]
        y=first[first.ano.eq(ano)]
        summary.append({
            "ano":ano,"municipios":len(x),
            "mediana_competitividade_segundo_turno":float(x.competitividade_2t.median()),
            "media_competitividade_segundo_turno_nao_ponderada":float(x.competitividade_2t.mean()),
            "competitividade_nacional_ponderada_pela_votacao":float(1 - abs(x.votos_pt13.sum()-x.votos_oponente.sum())/x.total_validos.sum()),
            "fracao_municipios_vantagem_pt13":float((x.margem_assinada_pt13>0).mean()),
            "frac_municipios_margem_zero":float((x.margem_assinada_pt13==0).mean()),
            "mediana_cobertura_top2_primeiro_turno":float(y.cobertura_top2.median()),
            "mediana_competitividade_top2_condicional_primeiro":float(y.competitividade_top2_condicional.median()),
            "n_cidades_primeiro_turno_top2_diferentes_finalistas":int(
                (~y.apply(lambda r: {r.codigo_primeiro,r.codigo_segundo} == set(FINALISTAS[ano]),axis=1)).sum()
            ),
            "votos_nacionais_segundo_turno":int(x.total_validos.sum()),
        })
    info={"autor":"Jacson Cruz do Nascimento",
          "indicador_principal":"C2=1-abs(v13-voponente)/(v13+voponente)=1-abs(margem_assinada_pt13), apenas 2º turno.",
          "indice_secundario":"Top2 municipal condicional e sua cobertura sobre votos válidos; HHI e número efetivo de candidaturas no 1º turno.",
          "indice_direcao":"(v13-voponente)/(v13+voponente), 2º turno, com identificação de candidatos por ano.",
          "candidaturas":FINALISTAS,
          "avisos":["Mesma legenda PT/número 13, candidatos diferentes 2018/2022.",
                    "C2 mede competitividade municipal, não eleição competitiva entre partidos em geral.",
                    "Empate municipal C2=1, votação integral para um candidato C2=0.",
                    "Sem inferência individual, causal ou preditiva.",
                    "2018 permanece sob ressalva de 76 votos no primeiro turno comparado com notícia histórica do TSE."],
          "sha256_insumos":{"2018":sha256(a.base2018),"2022":sha256(a.base2022)},
          "resumo":summary}
    (a.pasta/"manifesto_e_resumo.json").write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(info,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
