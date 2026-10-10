#!/usr/bin/env python3
"""Coleta auditável do SIDRA/IBGE para controles antecedentes às eleições.

Censo 2010: composição sexo e urbanização. PIB 2016/2020 e população
estimada 2017/2021: proxies de renda municipal, sem dados posteriores à
eleição correspondente. Os valores têm atribuição ao IBGE.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import requests
import pandas as pd
import numpy as np

BASE="https://apisidra.ibge.gov.br/values"
SOURCES={
  "censo2010": "/t/202/n6/all/v/93/p/2010/c1/0,5/c2/0,1?formato=json",
  "pib2016_2020": "/t/5938/n6/all/v/37/p/2016,2020?formato=json",
  "pop2017_2021": "/t/6579/n6/all/v/9324/p/2017,2021?formato=json",
}
MISSING={"","X","x","..","...","-","- ","null"}

def fetch(name, root):
    url=BASE+SOURCES[name]
    path=root/(name+".json.gz")
    if path.exists(): raise FileExistsError("Arquivo já existe, preservado: "+str(path))
    session=requests.Session()
    exc=None
    for i in range(4):
        try:
            response=session.get(url,timeout=(25,210),headers={"User-Agent":"pesquisa-academica-eleicoes/1.0"})
            response.raise_for_status()
            data=response.json()
            if not isinstance(data,list) or len(data)<5000:
                raise ValueError("IBGE devolveu dados incompletos/erro: "+str(data)[:350])
            required={"D1C","D2C","D3C","V"}
            if not required.issubset(data[0]):
                raise ValueError("Cabeçalho SIDRA inesperado: "+str(data[0])[:400])
            values=data[1:]
            if len(values)<5000:raise ValueError("Amostra incompleta.")
            encoded=json.dumps(data,ensure_ascii=False,separators=(",",":")).encode("utf-8")
            root.mkdir(parents=True,exist_ok=True)
            with gzip.open(path,"wb",compresslevel=9) as f:f.write(encoded)
            return {"recurso":name,"url":url,"sha256_gzip":hashlib.sha256(path.read_bytes()).hexdigest(),
                    "n_registros":len(values),"bytes_comprimidos":path.stat().st_size,
                    "baixado_utc":datetime.now(timezone.utc).isoformat()}
        except (ValueError,requests.RequestException) as err:
            exc=err
    raise RuntimeError("Falha de consulta ao SIDRA "+name+": "+str(exc))

def read(name, root):
    with gzip.open(root/(name+".json.gz"),"rt",encoding="utf-8") as f:
        obj=json.load(f)
    d=pd.DataFrame(obj[1:])
    for c in ("D1C","D2C","D3C","V"):
        if c not in d:raise ValueError("Coluna SIDRA ausente "+c)
    d["CD_MUNICIPIO_IBGE"]=d.D1C.astype(str).str.strip()
    if not d.CD_MUNICIPIO_IBGE.str.fullmatch(r"\d{7}").all():
        raise ValueError("IDs municipais SIDRA inválidos.")
    d["ano"]=pd.to_numeric(d.D3C,errors="raise").astype(int)
    d["valor"]=pd.to_numeric(d.V.where(~d.V.isin(MISSING)),errors="coerce")
    return d

def series(d, ano, variable, output, filter_expression=None):
    x=d[(d.ano==ano)&d.D2C.eq(str(variable))].copy()
    if filter_expression is not None:x=x[filter_expression(x)]
    if x.CD_MUNICIPIO_IBGE.duplicated().any():
        raise ValueError("SIDRA: município duplicado na série "+output)
    return x[["CD_MUNICIPIO_IBGE","valor"]].rename(columns={"valor":output})

def transformar(root):
    census=read("censo2010",root)
    if not {"D4C","D5C"}.issubset(census.columns):
        raise ValueError("Censo 2010 sem dimensões de sexo e situação de domicílio.")
    total=series(census,2010,93,"pop_2010",lambda d:d.D4C.eq("0")&d.D5C.eq("0"))
    urban=series(census,2010,93,"urb_2010",lambda d:d.D4C.eq("0")&d.D5C.eq("1"))
    women=series(census,2010,93,"mulheres_2010",lambda d:d.D4C.eq("5")&d.D5C.eq("0"))
    pib=read("pib2016_2020",root)
    pop=read("pop2017_2021",root)
    a=total
    for series_ in (urban,women,
                    series(pib,2016,37,"pib_mil_reais_2016"),
                    series(pib,2020,37,"pib_mil_reais_2020"),
                    series(pop,2017,9324,"pop_2017"),
                    series(pop,2021,9324,"pop_2021")):
        a=a.merge(series_,how="outer",on="CD_MUNICIPIO_IBGE",validate="one_to_one")
    a["urbanizacao_2010"]=a.urb_2010/a.pop_2010
    a["fracao_feminina_2010"]=a.mulheres_2010/a.pop_2010
    a["pibpc_proxy_2016_2017_reais"]=a.pib_mil_reais_2016*1000/a.pop_2017
    a["pibpc_proxy_2020_2021_reais"]=a.pib_mil_reais_2020*1000/a.pop_2021
    a["pop_2017"]=pd.to_numeric(a.pop_2017)
    a["pop_2021"]=pd.to_numeric(a.pop_2021)
    if a.CD_MUNICIPIO_IBGE.duplicated().any():raise ValueError("Geocódigos duplicados no painel IBGE.")
    if len(a)<5560 or len(a)>5590:raise ValueError("Cobertura inesperada IBGE: "+str(len(a)))
    for c in ("urbanizacao_2010","fracao_feminina_2010"):
        if a[c].dropna().lt(0).any() or a[c].dropna().gt(1).any():
            raise ValueError("Proporção fora do intervalo: "+c)
    for c in ("pibpc_proxy_2016_2017_reais","pibpc_proxy_2020_2021_reais","pop_2017","pop_2021"):
        if a[c].dropna().le(0).any():raise ValueError("Indicador não positivo: "+c)
    a.sort_values("CD_MUNICIPIO_IBGE",inplace=True)
    return a

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pasta",type=Path,required=True)
    p.add_argument("--saida",type=Path,required=True)
    p.add_argument("--manifesto",type=Path,required=True)
    args=p.parse_args()
    if args.saida.exists() or args.manifesto.exists():
        raise SystemExit("Saída prévia existe; preservar versões.")
    entries=[fetch(name,args.pasta) for name in SOURCES]
    result=transformar(args.pasta)
    args.saida.parent.mkdir(parents=True,exist_ok=True)
    result.to_csv(args.saida,index=False,float_format="%.10f")
    info={"escopo":"Controles socioeconômicos e demográficos municipais antecedentes",
      "fontes":entries,
      "n_municipios_uniao":len(result),
      "completos_censo2010":int(result[["pop_2010","urbanizacao_2010","fracao_feminina_2010"]].notna().all(axis=1).sum()),
      "completos_2018":int(result[["urbanizacao_2010","fracao_feminina_2010","pop_2017","pibpc_proxy_2016_2017_reais"]].notna().all(axis=1).sum()),
      "completos_2022":int(result[["urbanizacao_2010","fracao_feminina_2010","pop_2021","pibpc_proxy_2020_2021_reais"]].notna().all(axis=1).sum()),
      "descricao":"PIB per capita proxy combina PIB em milhares de reais do ano anterior ao denominador estimado de população do ano posterior. NÃO equivale ao indicador oficial de PIB per capita; anos distintos e preços correntes.",
      "defasagem": {"eleicao_2018":{"pib":2016,"pop":2017,"censo":2010},
                     "eleicao_2022":{"pib":2020,"pop":2021,"censo":2010}},
      "limites":"Séries oficiais podem ter revisão retrospectiva. Dados com ano de referência anterior à eleição não implicam que a edição atualmente publicada já estivesse disponível na época; evitar afirmação de validação preditiva em tempo real.",
      "sha256_saida":hashlib.sha256(args.saida.read_bytes()).hexdigest()}
    args.manifesto.parent.mkdir(parents=True,exist_ok=True)
    args.manifesto.write_text(json.dumps(info,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(info,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
