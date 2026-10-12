#!/usr/bin/env python3
"""Examinar fonte alternativa TSE por seção 1998 sem pressupor completude."""
import csv,hashlib,json,tempfile,zipfile
from pathlib import Path
from urllib.request import urlopen,Request
from datetime import datetime,timezone
URL="https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_1998_BR.zip"
OUT=Path("outputs/alternativa_tse_1998_secao_v01")
def main():
 if OUT.exists() and any(OUT.iterdir()):raise SystemExit("Arquivos anteriores preservados")
 OUT.mkdir(parents=True,exist_ok=True)
 report={"fonte_url":URL,"coleta_utc":datetime.now(timezone.utc).isoformat(),"objetivo":"Identificar alternativa válida ao arquivo nominal 1998 com votos zerados."}
 try:
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"1998_secao.zip";h=hashlib.sha256()
   with urlopen(Request(URL,headers={"User-Agent":"pesquisa-eleitoral-1998/1.0"}),timeout=240) as r,p.open("wb") as f:
    while b:=r.read(2*1024*1024):h.update(b);f.write(b)
   report["sha256_zip"]=h.hexdigest();report["bytes_zip"]=p.stat().st_size
   with zipfile.ZipFile(p) as z:
    report["zip_ok"]=z.testzip() is None
    report["arquivos"]=[{"nome":v.filename,"bytes":v.file_size} for v in z.infolist()]
    csvs=[v.filename for v in z.infolist() if v.filename.lower().endswith((".csv",".txt"))]
    samples=[]
    for name in csvs[:6]:
     with z.open(name) as raw:
      import io
      rd=csv.reader(io.TextIOWrapper(raw,encoding="latin1",errors="replace"),delimiter=";")
      hd=next(rd,None)
      first=[next(rd,None) for i in range(5)]
      samples.append({"arquivo":name,"colunas":hd,
              "primeiros_registros":first})
    report["amostras_csv"]=samples
   report["status"]="SCHEMA_IDENTIFICADO_SEM_VALIDACAO_COMPLETUDE"
 except Exception as e:
  report["status"]="NAO_ACESSIVEL";report["erro"]=str(e)
 (OUT/"inventario_alternativa_1998.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(report,ensure_ascii=False,indent=2)[:10000])
if __name__=="__main__":main()
