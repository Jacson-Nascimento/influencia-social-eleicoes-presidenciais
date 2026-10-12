#!/usr/bin/env python3
"""Inventário independente dos arquivos presidenciais TSE 1998/2002/2006/2010.

Não incorpora 1998 a modelos do segundo turno e não altera v14/v15.
Downloads ZIP oficiais TSE para arquivo temporário, checksums e resultados
agregados por UF/município/candidato/turno. Não infere municípios ausentes.
"""
import argparse, hashlib, json, tempfile
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import urlopen,Request
import pandas as pd
import numpy as np
import importlib.util

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("tse_historico",HERE/"05_consolidar_presidente_tse.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
URL="https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{year}.zip"

def main():
    arg=argparse.ArgumentParser(description=__doc__)
    arg.add_argument("--ano",required=True,type=int,choices=[1998,2002,2006,2010])
    arg.add_argument("--mapa",required=True,type=Path)
    arg.add_argument("--saida",required=True,type=Path)
    a=arg.parse_args()
    if a.saida.exists() and any(a.saida.iterdir()):
        raise SystemExit("Pasta ocupada, preservar originais.")
    a.saida.mkdir(parents=True,exist_ok=True)
    manifest={"ano":a.ano,"origem_url":URL.format(year=a.ano),
       "consulta_utc":datetime.now(timezone.utc).isoformat(),
       "observacoes":["Dados 1998 declarados incompletos pelo TSE, não imputar ausências.",
                      "1998: sem segundo turno presidencial; resultado em primeiro turno somente.",
                      "Exterior identificado como UF ZZ, excluído de atributos municipais.",
                      "Código TSE igual em anos distintos não prova estabilidade das fronteiras municipais.",
                      "Registros e valores brutos não alterados."]}
    try:
        with tempfile.TemporaryDirectory() as td:
            file=Path(td)/f"votacao_candidato_munzona_{a.ano}.zip"
            h=hashlib.sha256()
            with urlopen(Request(manifest["origem_url"],headers={"User-Agent":"artigo-academico-dados-eleitorais-publicos/1.0"}),timeout=240) as f, file.open("wb") as out:
                while b:=f.read(1024*1024):
                    h.update(b);out.write(b)
            manifest["sha256_zip_original"]=h.hexdigest()
            manifest["bytes_zip"]=file.stat().st_size
            data,info=mod.consolidar_zip(file,a.ano)
            manifest["consolidacao"]=info
        data=data[data.DS_CARGO.eq("PRESIDENTE")] if "DS_CARGO" in data else data
        data.to_csv(a.saida/f"votos_presidenciais_municipais_{a.ano}.csv",index=False)
        tab=[]
        for turno in sorted(data.NR_TURNO.unique()):
            part=data[data.NR_TURNO==turno]
            per=part.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum().sort_values(ascending=False)
            local=part[part.SG_UF.ne("ZZ")]
            foreign=part[part.SG_UF.eq("ZZ")]
            m=local[["SG_UF","CD_MUNICIPIO"]].drop_duplicates()
            tab.append({"turno":int(turno),
                "total_votos_nominais":int(per.sum()),
                "municipios_distintos_sem_exterior":int(len(m)),
                "ufs_territoriais":int(m.SG_UF.nunique()),
                "votos_municipais":int(local.QT_VOTOS_NOMINAIS.sum()),
                "votos_exterior":int(foreign.QT_VOTOS_NOMINAIS.sum()),
                "n_candidaturas_registradas":int(len(per)),
                "candidatos_votos":{str(k):int(v) for k,v in per.items()},
                "numero_13_votos":int(per.get(13,0))})
        manifest["turnos"]=tab
        mapa=pd.read_csv(a.mapa,dtype={"SG_UF":str})
        mapkey=set(zip(mapa.SG_UF,mapa.CD_MUNICIPIO.astype(int)))
        local=data[data.SG_UF.ne("ZZ")][["SG_UF","CD_MUNICIPIO"]].drop_duplicates()
        keys=set(zip(local.SG_UF,local.CD_MUNICIPIO.astype(int)))
        manifest["municipios_distintos_total_arquivo"]=len(keys)
        manifest["chaves_com_mapa_atual"]=len(keys & mapkey)
        manifest["chaves_sem_mapa_atual"]=len(keys - mapkey)
        manifest["municipios_mais_recentes_ausentes_no_ano"]=len(mapkey - keys)
        manifest["exemplos_sem_correspondencia"]=sorted(str(x) for x in keys - mapkey)[:20]
        manifest["total_nao_implicado_validacao"]=(
          "Os totais lidos precisam ser confrontados com totalização oficial de cada eleição e condições dos arquivos.")
        if a.ano==1998:
            manifest["tratamento_pesquisa"]="SOMENTE PRIMEIRO TURNO, COM COBERTURA TSE POTENCIALMENTE INCOMPLETA"
            if 2 in data.NR_TURNO.unique(): raise ValueError("Arquivo 1998 inesperadamente contém turno 2, verificar cargo")
        else:
            manifest["tratamento_pesquisa"]="CANDIDATO_13_VS_FINALISTA_NO_SEGUNDO_TURNO_APOS_IDENTIFICAR_VENCEDORES"
            if 2 not in data.NR_TURNO.unique(): raise ValueError("Segundo turno ausente no arquivo")
        manifest["status"]="INVENTARIADO_NAO_CONCILIADO_COM_TOTAL_TSE"
    except Exception as ex:
        manifest["status"]="FALHA_INVENTARIO"
        manifest["erro"]=str(ex)
        (a.saida/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
        raise
    (a.saida/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:manifest[k] for k in ("ano","status","turnos","chaves_com_mapa_atual","chaves_sem_mapa_atual","municipios_mais_recentes_ausentes_no_ano")},indent=2,ensure_ascii=False))
if __name__=="__main__":main()
