#!/usr/bin/env python3
"""Inspecionar formato CSV por UF 1998: sem forçar leiaute do ZIP BR."""
import argparse,csv,hashlib,io,json,tempfile,zipfile
from pathlib import Path
from collections import Counter
from urllib.request import urlopen,Request
from datetime import datetime,timezone
def main():
 p=argparse.ArgumentParser();p.add_argument("--uf",choices=["AC","RS"],required=True);p.add_argument("--out",type=Path,required=True)
 a=p.parse_args()
 if a.out.exists():raise FileExistsError("Versão já existe")
 a.out.parent.mkdir(parents=True,exist_ok=True)
 URL=f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_1998_{a.uf}.zip"
 meta={"url":URL,"uf":a.uf,"criacao_utc":datetime.now(timezone.utc).isoformat(),"status":"NAO_APURADO"}
 try:
  with tempfile.TemporaryDirectory() as td:
   zipp=Path(td)/"z.zip"
   with urlopen(Request(URL,headers={"User-Agent":"pesquisa-eleicoes-1998-leiaute/1.0"}),timeout=180) as r,zipp.open("wb") as w:
    while b:=r.read(1024*1024):w.write(b)
   with zipfile.ZipFile(zipp) as z:
    files=[f for f in z.namelist() if f.endswith(".csv")]
    if len(files)!=1:raise ValueError("Arquivos CSV inesperados: "+repr(files))
    with z.open(files[0]) as b:
     sample=b.read(14000)
    meta["primeiros_bytes_txt"]=sample[:1700].decode("latin1",errors="replace")
    meta["primeira_linha_bytes_hex"]=sample.splitlines()[0][:250].hex()
    meta["n_linhas_amostradas"]=len(sample.splitlines())
    for sep in (";",",","\t","|"):
     sample_lines=sample.decode("latin1",errors="replace").splitlines()[:5]
     parsed=list(csv.reader(sample_lines,delimiter=sep))
     meta["possivel_delimitador_"+repr(sep)]={"campos":list(map(len,parsed)),"linhas":parsed[:2]}
    meta["status"]="ESQUEMA_AMOSTRADO_SEM_TOTALIZACAO"
 except Exception as exc:meta["status"]="ERRO";meta["erro"]=repr(exc)
 a.out.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({"uf":a.uf,"status":meta["status"],"sample":meta.get("primeiros_bytes_txt","")[:700]},ensure_ascii=False))
if __name__=="__main__":main()
