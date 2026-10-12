#!/usr/bin/env python3
"""Coletar histórico pré-eleitoral IBGE para 2002/2006/2010.

Censo 2000 pop por sexo e situação, estimações 2001 2005 2009, PIB
2004 2008: anos anteriores a pleitos 2006/2010.
PIB 2000 não existe na série SIDRA 5938: NÃO imputar para 2002.
Estruturas posteriores são apenas aproximações; 2010 com Censo 2000.
"""
import argparse,hashlib,json,time,requests,numpy as np,pandas as pd
from pathlib import Path
from datetime import datetime,timezone
URL="https://apisidra.ibge.gov.br/values"
PATHS={
"censo2000":"/t/202/n6/all/v/93/p/2000/c1/0,1/c2/0,5?formato=json",
"pop2001":"/t/6579/n6/all/v/9324/p/2001?formato=json",
"pop2005":"/t/6579/n6/all/v/9324/p/2005?formato=json",
"pop2009":"/t/6579/n6/all/v/9324/p/2009?formato=json",
"pib2004":"/t/5938/n6/all/v/37/p/2004?formato=json",
"pib2008":"/t/5938/n6/all/v/37/p/2008?formato=json"}
BAD={"...","..","X","x","-","","null"}

def download(name):
 url=URL+PATHS[name]
 for step in range(4):
  try:
   r=requests.get(url,timeout=(35,210),headers={"User-Agent":"estudo-academico-eleicoes-historico/1.0"})
   r.raise_for_status()
   t=r.json()
   if not isinstance(t,list) or len(t)<5000:raise ValueError(f"IBGE retornou {len(t)} registros em {name}")
   d=pd.DataFrame(t[1:])
   if not {"D1C","D2C","D3C","V"}.issubset(d.columns):
    raise ValueError("Campos SIDRA ausentes: "+repr(d.columns.tolist()))
   d["CD_MUNICIPIO_IBGE"]=d.D1C.astype(str)
   d["valor"]=pd.to_numeric(d.V.where(~d.V.isin(BAD)),errors="coerce")
   if not d.CD_MUNICIPIO_IBGE.str.fullmatch(r"\d{7}").all():
    raise ValueError("Codigo IBGE irregular")
   return d,{"url":url,"status_http":r.status_code,"sha256_resposta":hashlib.sha256(r.content).hexdigest(),
         "n_registros":len(d),"obtido_em":datetime.now(timezone.utc).isoformat()}
  except Exception:
   if step==3:raise
   time.sleep(3*(step+1))

def pick(d,variable,year,fn):
 s=d[(d.D2C==str(variable))&(d.D3C==str(year))].copy()
 if fn:s=s[fn(s)]
 if s.CD_MUNICIPIO_IBGE.duplicated().any() or len(s)<5400:
  raise ValueError(f"Serie insuficiente {year}: {len(s)}")
 return s[["CD_MUNICIPIO_IBGE","valor"]]

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--mapa",required=True,type=Path)
 ap.add_argument("--saida",required=True,type=Path)
 ap.add_argument("--manifesto",required=True,type=Path)
 a=ap.parse_args()
 if a.saida.exists() or a.manifesto.exists():raise SystemExit("Saída existe, manter original.")
 base=pd.read_csv(a.mapa,dtype={"CD_MUNICIPIO_IBGE":str})
 if len(base)!=5570:raise ValueError("Mapa deve conter 5570 códigos")
 base=base[["CD_MUNICIPIO_IBGE"]]
 info={}
 for key in PATHS:
  d,record=download(key)
  info[key]=record
  if key=="censo2000":
   for field,fn in {
      "total2000":lambda x:x.D4C.eq("0")&x.D5C.eq("0"),
      "urbanos2000":lambda x:x.D4C.eq("1")&x.D5C.eq("0"),
      "mulheres2000":lambda x:x.D4C.eq("0")&x.D5C.eq("5")}.items():
    p=pick(d,93,2000,fn).rename(columns={"valor":field})
    base=base.merge(p,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
  else:
   field=key.replace("pop","pop_").replace("pib","pib_mil_")
   yy=int(key[-4:])
   var=9324 if key.startswith("pop") else 37
   p=pick(d,var,yy,None).rename(columns={"valor":field})
   base=base.merge(p,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
 base["urbanizacao_2000"]=base.urbanos2000/base.total2000
 base["fracao_feminina_2000"]=base.mulheres2000/base.total2000
 for year,popyear,pibyear in [(2002,2001,None),(2006,2005,2004),(2010,2009,2008)]:
  p=base[f"pop_{popyear}"]
  base[f"log_pop_{year}"]=np.log(p.where(p>0))
  if pibyear:
   pib=base[f"pib_mil_{pibyear}"]
   base[f"pibpc_proxy_{year}"]=pib*1000/p
   base[f"log_pibpc_proxy_{year}"]=np.log(base[f"pibpc_proxy_{year}"].where(base[f"pibpc_proxy_{year}"]>0))
  cols=[f"log_pop_{year}","urbanizacao_2000","fracao_feminina_2000"]
  if pibyear:cols.append(f"log_pibpc_proxy_{year}")
  info[f"n_controles_completos_{year}"]=int(base[cols].notna().all(axis=1).sum())
 for col in ("urbanizacao_2000","fracao_feminina_2000"):
  if not base[col].dropna().between(0,1).all():raise ValueError("Proporção inválida")
 if len(base)!=5570 or base.CD_MUNICIPIO_IBGE.duplicated().any():
  raise ValueError("base inconsistente")
 a.saida.parent.mkdir(parents=True,exist_ok=True)
 base.to_csv(a.saida,index=False,float_format="%.12f")
 info.update({"censo":2000,"pop_ref":[2001,2005,2009],"pib_ref":[2004,2008],
  "pib_2000":"Indisponível no SIDRA5938, não imputado",
  "efeito":"Para 2002 estimar modelo demográfico reduzido com três regressores; 2006/2010 comportam quatro",
  "ressalva":"Base revisada retrospectivamente pode não refletir valores publicados antes de cada eleição",
  "arquivo_sha256":hashlib.sha256(a.saida.read_bytes()).hexdigest()})
 a.manifesto.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(info,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
