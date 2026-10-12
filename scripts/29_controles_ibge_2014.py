#!/usr/bin/env python3
"""Preparar controles municipais anteriores a 2014 com fontes IBGE/SIDRA.

2012 PIB nominal em milhares de reais: SIDRA tab5938 v37;
2013 estimativa de população residente: SIDRA tab6579 v9324.
Usa controles de urbanização e fração feminina do Censo 2010 previamente
tratados no projeto, sem substituir/sobrescrever arquivos anteriores.
Conserva hashes e URLs, inclusive dos dados recuperados posteriormente.
"""
import argparse, hashlib, json, time
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import pandas as pd
import requests
BASE="https://apisidra.ibge.gov.br/values"
ENDPOINTS={
 "pib_2012":"/t/5938/n6/all/v/37/p/2012?formato=json",
 "pop_2013":"/t/6579/n6/all/v/9324/p/2013?formato=json"}
SENTINELS={"","X","x","..","...","-","null"}

def fetch(label,path):
    u=BASE+ENDPOINTS[label]
    r=None
    for retry in range(4):
        try:
            r=requests.get(u,timeout=(30,180),headers={"User-Agent":"research-eleicoes-municipais-public-open-data/1.0"})
            r.raise_for_status()
            data=r.json()
            if not isinstance(data,list) or len(data)<5500:raise ValueError("resposta SIDRA incompleta")
            raw=r.content
            sha=hashlib.sha256(raw).hexdigest()
            h=data[0]
            rows=data[1:]
            if not {"D1C","D2C","D3C","V"}.issubset(h.keys()):
                raise ValueError("campo SIDRA ausente: "+str(h))
            d=pd.DataFrame(rows)
            if not d.D1C.astype(str).str.fullmatch(r"\d{7}").all():
                raise ValueError("Código IBGE não possui sete dígitos")
            yr=2012 if label=="pib_2012" else 2013
            var="37" if label=="pib_2012" else "9324"
            d=d[(d.D3C.astype(str)==str(yr))&(d.D2C.astype(str)==var)]
            if d.D1C.duplicated().any() or len(d)<5500:
                raise ValueError("Municípios duplicados ou ausentes nos dados IBGE")
            v=pd.to_numeric(d.V.where(~d.V.isin(SENTINELS)),errors="coerce")
            out=pd.DataFrame({"CD_MUNICIPIO_IBGE":d.D1C.astype(str),
                              label:v}).reset_index(drop=True)
            if out[label].notna().sum()<5500:
                raise ValueError("Valores insuficientes "+label)
            return out,{"url":u,"sha256_resposta_http":sha,"n_linhas_recebidas":len(rows),
                        "municipios_com_valor":int(out[label].notna().sum()),
                        "coleta_utc":datetime.now(timezone.utc).isoformat()}
        except Exception:
            if retry==3:raise
            time.sleep(5*(retry+1))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--controles",required=True,type=Path)
    p.add_argument("--mapa",required=True,type=Path)
    p.add_argument("--saida",required=True,type=Path)
    p.add_argument("--manifesto",required=True,type=Path)
    args=p.parse_args()
    if args.saida.exists() or args.manifesto.exists():raise SystemExit("Pasta de saída já contém arquivo.")
    ctrl=pd.read_csv(args.controles,dtype={"CD_MUNICIPIO_IBGE":str})
    mapa=pd.read_csv(args.mapa,dtype={"CD_MUNICIPIO_IBGE":str})
    if len(mapa)!=5570 or mapa.CD_MUNICIPIO_IBGE.duplicated().any():
        raise ValueError("Geocódigos base inconsistentes")
    cols=["CD_MUNICIPIO_IBGE","urbanizacao_2010","fracao_feminina_2010"]
    if not set(cols).issubset(ctrl):raise ValueError("Controles históricos 2010 ausentes")
    joined=mapa[["CD_MUNICIPIO_IBGE"]].merge(ctrl[cols],on="CD_MUNICIPIO_IBGE",validate="one_to_one",how="left")
    meta={}
    for name in ENDPOINTS:
        vals,rec=fetch(name,args.saida.parent)
        joined=joined.merge(vals,on="CD_MUNICIPIO_IBGE",validate="one_to_one",how="left")
        meta[name]=rec
    joined["pibpc_proxy_2012_2013_reais"]=joined.pib_2012*1000/joined.pop_2013
    joined["log_pop"]=np.log(joined.pop_2013.where(joined.pop_2013.gt(0)))
    joined["log_pibpc_proxy"]=np.log(joined.pibpc_proxy_2012_2013_reais.where(joined.pibpc_proxy_2012_2013_reais.gt(0)))
    required=["log_pop","log_pibpc_proxy","urbanizacao_2010","fracao_feminina_2010"]
    complete=joined[required].notna().all(axis=1)
    if joined.CD_MUNICIPIO_IBGE.duplicated().any() or len(joined)!=5570 or complete.sum()<5500:
        raise ValueError("Insuficiência de dados limpos: "+str(complete.sum()))
    args.saida.parent.mkdir(parents=True,exist_ok=True)
    joined.to_csv(args.saida,index=False,float_format="%.12f")
    info={"escopo":"Dados anteriores ao ano eleitoral para exercício exploratório 2014",
        "fontes_sidra":meta,"controle_censo2010":"fonte já tratada no repositório (dados/ibge_tratados/controles_pre_eleitorais_v02.csv)",
        "n_municipios":5570,"controles_completos":int(complete.sum()),
        "sem_controles_completos":joined.loc[~complete,"CD_MUNICIPIO_IBGE"].tolist(),
        "defasagem":{"2014":{"pib":2012,"pop":2013,"censo":2010}},
        "proxy_pib_per_capita":"PIB nominal 2012 R$ / população estimada 2013; NÃO é PIB per capita oficial",
        "cautela":"Séries recuperadas em 2026 podem ter sido revisadas; nenhum desempenho preditivo em tempo real.",
        "arquivo_saida_sha256":hashlib.sha256(args.saida.read_bytes()).hexdigest()}
    args.manifesto.write_text(json.dumps(info,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(info,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
