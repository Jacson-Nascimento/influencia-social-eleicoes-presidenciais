#!/usr/bin/env python3
"""Reconstruir a votação presidencial de 1998 a partir de seção/municipio.

Fontes TSE: votação seção 1998 BR (TXT sem cabeçalho, separado por ponto-e-vírgula).
Esta reconstrução é EXPLORATÓRIA pois TSE adverte que 1998 é incompleto.
Não confundir índice de primeiro turno com índice de segundo turno de outros anos.
"""
from collections import defaultdict
from datetime import datetime,timezone
import hashlib,json,tempfile,zipfile
from pathlib import Path
from urllib.request import urlopen,Request
import numpy as np,pandas as pd
URL="https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_1998_BR.zip"
NAMES=["geracao_data","geracao_hora","ano","turno","eleicao","abrangencia",
       "campo6","cod_municipio","municipio_nome","zona","secao",
       "cargo_cod","cargo_nome","cod_votavel","n_votos"]
OUT=Path("outputs/reconstrucao_1998_secao_v01")
def main():
 if OUT.exists() and any(OUT.iterdir()): raise SystemExit("Saída ocupada, preservar versões.")
 OUT.mkdir(parents=True,exist_ok=True)
 meta={"origem":URL,"criado_em":datetime.now(timezone.utc).isoformat(),
       "status":"NAO_VALIDADO","advertencia":"TSE reconhece incompletude dos resultados de 1998."}
 try:
  with tempfile.TemporaryDirectory() as td:
   file=Path(td)/"secoes.zip"
   sha=hashlib.sha256()
   with urlopen(Request(URL,headers={"User-Agent":"pesquisa-painel-eleitoral-1998/1.0"}),timeout=180) as r,file.open("wb") as f:
    while block:=r.read(1024*1024):sha.update(block);f.write(block)
   meta["sha256_arquivo_tse"]=sha.hexdigest()
   merged=defaultdict(int)
   seen=set();labels=set();cargos=set();cods=set()
   rows=0;incoerente=0;campo_equal=0
   with zipfile.ZipFile(file) as zip_:
    members=[n for n in zip_.namelist() if n.endswith("votacao_secao_1998_BR.txt")]
    if len(members)!=1:raise ValueError("ZIP TSE não possui TXT único reconhecido")
    with zip_.open(members[0]) as f:
     for ch in pd.read_csv(f,sep=";",header=None,names=NAMES,encoding="latin1",dtype=str,chunksize=60000):
      rows+=len(ch)
      if ch.shape[1]!=len(NAMES):raise ValueError("Número inesperado de colunas")
      cargos.update(ch.cargo_nome.dropna().unique().tolist())
      labels.update(ch.abrangencia.dropna().unique().tolist())
      if not ch.ano.eq("1998").all() or not ch.turno.eq("1").all():
       raise ValueError("Ano e turno inválidos no TXT")
      if not ch.cargo_nome.eq("PRESIDENTE").all():
       raise ValueError("TXT contém outros cargos sem identificação")
      campo_equal+=int(ch.campo6.eq(ch.cod_municipio).sum())
      ch["n_votos"]=pd.to_numeric(ch.n_votos,errors="raise").astype("int64")
      ch["cod_votavel"]=pd.to_numeric(ch.cod_votavel,errors="raise").astype(int)
      if ch.n_votos.lt(0).any():raise ValueError("Votos negativos")
      v=ch.groupby(["cod_municipio","cod_votavel"],dropna=False).n_votos.sum()
      for pair,value in v.items():merged[pair]+=int(value)
      cods.update(ch.cod_votavel.unique().tolist())
      seen.update(ch.cod_municipio.unique().tolist())
   meta.update({"linhas_lidas":rows,"campo6_igual_cod_municipio_linhas":campo_equal,
         "abrangencias":sorted(labels),"cargos":sorted(cargos),
         "votaveis":sorted(map(int,cods)),
         "municipios_unicos":len(seen)})
  d=pd.DataFrame([(code,cand,v) for (code,cand),v in merged.items()],
                columns=["CD_MUNICIPIO","NR_CANDIDATO","QT_VOTOS"])
  if d.empty:raise ValueError("Dados agregados vazios")
  codes=pd.to_numeric(d.CD_MUNICIPIO,errors="raise").astype("int64")
  d["CD_MUNICIPIO"]=codes
  map_=pd.read_csv("outputs/municipal_v01/chaves_tse_ibge_5570_centroides.csv",dtype={"SG_UF":str,"CD_MUNICIPIO_IBGE":str})
  map_["CD_MUNICIPIO"]=pd.to_numeric(map_.CD_MUNICIPIO).astype(int)
  if map_.CD_MUNICIPIO.duplicated().any():
   raise ValueError("CD_MUNICIPIO não identifica UF de forma única em 2018")
  d=d.merge(map_[["CD_MUNICIPIO","SG_UF","CD_MUNICIPIO_IBGE"]],on="CD_MUNICIPIO",how="left",validate="many_to_one")
  meta["n_sem_chave_tse_atual"]=int(d.loc[d.SG_UF.isna(),"CD_MUNICIPIO"].nunique())
  meta["codigo_nao_correspondente_exemplos"]=d.loc[d.SG_UF.isna(),"CD_MUNICIPIO"].drop_duplicates().tolist()[:30]
  national=d.groupby("NR_CANDIDATO").QT_VOTOS.sum().sort_values(ascending=False)
  meta["total_por_numero_votavel"]={str(k):int(v) for k,v in national.items()}
  meta["votacao_PT13"]=int(national.get(13,0))
  meta["votacao_PSDB45"]=int(national.get(45,0))
  meta["total_todos_codigos_inclui_nao_candidatos"]=int(d.QT_VOTOS.sum())
  meta["n_cidades_com_registro_na_malha_atual"]=int(d.loc[d.SG_UF.notna(),"CD_MUNICIPIO"].nunique())
  d.to_csv(OUT/"votacao_por_municipio_candidatura_1998.csv",index=False)
  meta["status"]="AGREGADO_COM_RESSALVA_DOCUMENTAL_1998_NAO_CONCILIADO"
  meta["saida_sha256"]=hashlib.sha256((OUT/"votacao_por_municipio_candidatura_1998.csv").read_bytes()).hexdigest()
 except Exception as e:
  meta["status"]="BLOQUEADO";meta["erro"]=repr(e)
  (OUT/"manifesto.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
  raise
 (OUT/"manifesto.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(meta,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
