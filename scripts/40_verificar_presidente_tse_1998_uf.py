#!/usr/bin/env python3
"""Ler CSV por UF de 1998 com schema oficial de 23 colunas e testar cobertura PRESIDENCIAL.

Esta sondagem não faz estimação, não altera dados de 2002–2022 e
não considera totais como conciliados sem confrontá-los com o TSE.
"""
import argparse,hashlib,json,tempfile,zipfile
from pathlib import Path
from urllib.request import urlopen,Request
from collections import Counter,defaultdict
from datetime import datetime,timezone
import pandas as pd
FIELDS=["ANO_ELEICAO","NR_TURNO","SG_UF","CD_MUNICIPIO","DS_CARGO","NR_VOTAVEL","QT_VOTOS"]
def main():
 p=argparse.ArgumentParser();p.add_argument("--uf",choices=["AC","RS","SP"],required=True);p.add_argument("--out",type=Path,required=True)
 a=p.parse_args()
 if a.out.exists():raise FileExistsError("Preservar relatório anterior")
 a.out.parent.mkdir(parents=True,exist_ok=True)
 url=f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_1998_{a.uf}.zip"
 res={"uf":a.uf,"url":url,"coleta_utc":datetime.now(timezone.utc).isoformat(),"status":"NAO_CONCILIADO"}
 try:
  with tempfile.TemporaryDirectory() as td:
   zpath=Path(td)/"votacao1998.zip"
   h=hashlib.sha256()
   with urlopen(Request(url,headers={"User-Agent":"academic-presidential-1998-tse/1.0"}),timeout=210) as resp,zpath.open("wb") as f:
    while block:=resp.read(2*1024*1024):h.update(block);f.write(block)
   res["zip_sha256"]=h.hexdigest()
   n=0;pres=0;cargos=Counter();municipios=set();votacoes=defaultdict(int);turnos=set()
   with zipfile.ZipFile(zpath) as z:
    fs=[x for x in z.namelist() if x.endswith(".csv")]
    if len(fs)!=1:raise ValueError("CSV unico nao identificado")
    with z.open(fs[0]) as src:
     for chunk in pd.read_csv(src,sep=";",encoding="latin1",dtype=str,usecols=FIELDS,chunksize=150000):
      if not set(FIELDS).issubset(chunk.columns):raise ValueError("Colunas ausentes")
      n+=len(chunk)
      grupos=chunk.DS_CARGO.value_counts()
      for k,v in grupos.items():cargos[str(k)]+=int(v)
      ele=chunk[chunk.DS_CARGO.fillna("").str.upper().str.strip().eq("PRESIDENTE")]
      pres+=len(ele)
      if ele.empty:continue
      if not ele.ANO_ELEICAO.eq("1998").all():raise ValueError("Ano incorreto")
      turnos.update(ele.NR_TURNO.unique().tolist())
      municipios.update(zip(ele.SG_UF,ele.CD_MUNICIPIO))
      ele=ele.copy()
      ele["QT_VOTOS"]=pd.to_numeric(ele.QT_VOTOS,errors="raise")
      for k,v in ele.groupby("NR_VOTAVEL").QT_VOTOS.sum().items():votacoes[str(k)]+=int(v)
   res.update({"n_linhas":n,"cargos":dict(cargos),"n_linhas_presidente":pres,
      "municipios_presidente_distintos":len(municipios),"turnos_presidente":sorted(turnos),
      "total_votos_por_numero":dict(sorted(votacoes.items())),
      "votos_presidente_cod13":votacoes.get("13",0),
      "votos_presidente_cod45":votacoes.get("45",0),
      "status":"PRESIDENTE_IDENTIFICADO_SEM_CONCILIACAO_TSE" if pres else "AUSENCIA_PRESIDENTE_NO_ARQUIVO_UF"})
 except Exception as err:res.update({"status":"ERRO_SONDAGEM","erro":repr(err)})
 a.out.write_text(json.dumps(res,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({k:res[k] for k in ("uf","status","n_linhas","n_linhas_presidente","municipios_presidente_distintos","turnos_presidente") if k in res},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
