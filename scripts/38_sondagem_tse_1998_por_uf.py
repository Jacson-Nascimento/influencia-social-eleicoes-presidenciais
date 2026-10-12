#!/usr/bin/env python3
"""Avaliação de completude dos arquivos TSE por UF de 1998.

Apenas inventaria membros ZIP e agrega campos territoriais da votação
por seção de Presidente (TXT com 15 colunas sem cabeçalho, conforme
votacao_secao_1998_BR.txt). Não altera nem preenche resultados nacionais.
"""
import argparse,csv,hashlib,io,json,tempfile,zipfile
from pathlib import Path
from urllib.request import urlopen,Request
from datetime import datetime,timezone
from collections import defaultdict

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--uf",required=True,choices=["AC","RS","SP"])
 p.add_argument("--out",required=True,type=Path)
 a=p.parse_args()
 if a.out.exists():raise FileExistsError("Relatório pré-existente intocado.")
 a.out.parent.mkdir(parents=True,exist_ok=True)
 url=f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_1998_{a.uf}.zip"
 meta={"UF":a.uf,"origem":url,"acesso_utc":datetime.now(timezone.utc).isoformat(),
       "status":"SEM_COLETA_VALIDADA"}
 try:
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/f"1998_{a.uf}.zip"
   sha=hashlib.sha256();maxbytes=350*1024*1024
   with urlopen(Request(url,headers={"User-Agent":"academic-1998-tse-coverage/1.0"}),timeout=240) as r,path.open("wb") as f:
    downloaded=0
    while block:=r.read(2*1024*1024):
     downloaded+=len(block)
     if downloaded>maxbytes:raise ValueError("Arquivo excedeu 350MB, interromper análise")
     sha.update(block);f.write(block)
   meta.update({"sha256":sha.hexdigest(),"bytes_zip":downloaded})
   n=0;count=0;cities=set();names=set();turns=set();votes=defaultdict(int);bad=0
   with zipfile.ZipFile(path) as z:
    meta["arquivos_zip"]=[{"name":x.filename,"bytes":x.file_size} for x in z.infolist()]
    txts=[x.filename for x in z.infolist() if x.filename.lower().endswith((".txt",".csv")) and "votacao_secao" in x.filename.lower()]
    if not txts:raise ValueError("Não há dados por seção")
    for f in txts:
     with z.open(f) as handle:
      reader=csv.reader(io.TextIOWrapper(handle,encoding="latin1",errors="replace"),delimiter=";")
      for record in reader:
       n+=1
       if len(record)!=15:
        bad+=1
        continue
       if record[2]=="1998" and record[12]=="PRESIDENTE":
        turns.add(record[3]);cities.add(record[7]);names.add(record[8])
        try:votes[record[13]]+=int(record[14])
        except ValueError:bad+=1
        count+=1
   meta.update({"n_linhas":n,"n_linhas_presidente":count,
      "municipios_codigo_distintos":len(cities),"municipios_nome_distintos":len(names),
      "turnos":sorted(turns),"municipios_exemplos":sorted(names)[:20],
      "votos_cod13":votes.get("13",0),"votos_cod45":votes.get("45",0),
      "total_todos_codigos":sum(votes.values()),"codigos_votaveis":len(votes),
      "linhas_incompletas_ou_erro":bad,
      "status":"COBERTURA_UF_EXPLORATORIA_SEM_TOTALIZACAO_OFICIAL"})
 except Exception as exc:
  meta["status"]="INVENTARIO_NAO_CONCLUIDO";meta["erro"]=str(exc)
 a.out.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(meta,ensure_ascii=False,indent=2)[:8000])
if __name__=="__main__":main()
