#!/usr/bin/env python3
"""Sondagem de viabilidade histórica SIDRA, sem estimar nem imputar variáveis."""
import hashlib,json,requests
from datetime import datetime,timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
TESTS={
 "censo_1991":"/t/202/n6/1100015/v/93/p/1991/c1/0,1/c2/0,5?formato=json",
 "censo_2000":"/t/202/n6/1100015/v/93/p/2000/c1/0,1/c2/0,5?formato=json",
 "pop_1997":"/t/6579/n6/1100015/v/9324/p/1997?formato=json",
 "pop_2001":"/t/6579/n6/1100015/v/9324/p/2001?formato=json",
 "pop_2005":"/t/6579/n6/1100015/v/9324/p/2005?formato=json",
 "pop_2009":"/t/6579/n6/1100015/v/9324/p/2009?formato=json",
 "pib_1999":"/t/5938/n6/1100015/v/37/p/1999?formato=json",
 "pib_2000":"/t/5938/n6/1100015/v/37/p/2000?formato=json",
 "pib_2004":"/t/5938/n6/1100015/v/37/p/2004?formato=json",
 "pib_2008":"/t/5938/n6/1100015/v/37/p/2008?formato=json"
}
def run(item):
 name,path=item
 url="https://apisidra.ibge.gov.br/values"+path
 result={"serie":name,"url":url}
 try:
  r=requests.get(url,headers={"User-Agent":"pesquisa-academica-temporal-eleicoes/1.0"},timeout=75)
  result.update({"status_http":r.status_code,"sha256_resposta":hashlib.sha256(r.content).hexdigest(),"bytes":len(r.content)})
  data=r.json()
  result["tipo"]=type(data).__name__
  if isinstance(data,list):
   result["n_linhas"]=len(data)
   result["cabecalho"]=data[0] if data else {}
   result["amostra"]=data[1:3] if len(data)>1 else []
   result["valido"]=len(data)>1 and all(row.get("V") not in ("...","..","X","-","") for row in data[1:])
  else:
   result["erro_api"]=str(data)[:600];result["valido"]=False
 except Exception as exc:
  result["erro"]=repr(exc);result["valido"]=False
 return result
def main():
 p=Path("outputs/viabilidade_historica_ibge_v01")
 if p.exists() and any(p.iterdir()):raise SystemExit("Não alterar relatório já existente.")
 p.mkdir(parents=True,exist_ok=True)
 with ThreadPoolExecutor(max_workers=5) as ex:
  rows=list(ex.map(run,TESTS.items()))
 result={"criado_em":datetime.now(timezone.utc).isoformat(),
    "limite":"Testes para um único município (1100015), NÃO garantem cobertura nacional",
    "resultados":rows,"dados_salvos":"Somente resumo e hash do retorno, nenhum dado imputado."}
 (p/"consulta_serie_historica_sidra.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps([{k:r.get(k) for k in ("serie","status_http","valido","n_linhas","erro_api","erro")} for r in rows],ensure_ascii=False,indent=2))
if __name__=="__main__":main()
