#!/usr/bin/env python3
"""Conciliação inicial da votação PRESIDENTE segundo turno 2014 no TSE.

Executar SOMENTE sobre ZIP nominal TSE oficial (BR/BRASIL) após download.
Não altera os scripts, votos, saídas ou manuscrito de 2018/2022.
Só publica o CSV final se cobrir 5570 municípios, casar códigos TSE/IBGE
e conciliar exatamente o resultado definitivo do segundo turno.
"""
import argparse, hashlib, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"scripts"/"05_consolidar_presidente_tse.py"
spec=importlib.util.spec_from_file_location("consolidar_TSE_2014",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
DILMA=54501118
AECIO=51041155
TOTAL=DILMA+AECIO

def main():
    q=argparse.ArgumentParser(description=__doc__)
    q.add_argument("--arquivo",required=True,type=Path)
    q.add_argument("--mapa",required=True,type=Path)
    q.add_argument("--saida",required=True,type=Path)
    q.add_argument("--manifesto",required=True,type=Path)
    a=q.parse_args()
    if a.saida.exists() or a.manifesto.exists():
        raise SystemExit("Saídas anteriores intocadas; use nova pasta.")
    checksum=hashlib.sha256(a.arquivo.read_bytes()).hexdigest()
    frame,meta=mod.consolidar_zip(a.arquivo,2014)
    nacional=frame.loc[frame.NR_TURNO.eq(2)].copy()
    nacional["NR_CANDIDATO"]=nacional.NR_CANDIDATO.astype(int)
    totais_nacionais={int(k):int(v) for k,v in nacional.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum().items()}
    exterior=nacional.loc[nacional.SG_UF.eq("ZZ")]
    totais_exterior={int(k):int(v) for k,v in exterior.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum().items()}
    t=nacional.loc[nacional.SG_UF.ne("ZZ")].copy()
    ids=set(t.NR_CANDIDATO.unique())
    if ids!={13,45}:raise ValueError("Candidaturas segundo turno inválidas: "+str(ids))
    key=["SG_UF","CD_MUNICIPIO"]
    if t.duplicated(key+["NR_CANDIDATO"]).any():raise ValueError("Chaves duplicadas")
    x=t.pivot(index=key,columns="NR_CANDIDATO",values="QT_VOTOS_NOMINAIS")
    totals={13:int(x[13].sum()),45:int(x[45].sum())}
    notes={"ano":2014,"fonte_oficial":"https://dadosabertos.tse.jus.br/dataset/resultados-2014",
      "arquivo_url":"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2014.zip",
      "arquivo_zip_sha256":checksum,"colunas_pivot":sorted(ids),
      "auditoria_arquivo":meta,"votos_municipios_brasil_sem_exterior":totals,
      "votos_exterior_ZZ":totais_exterior,
      "votos_nacionais_incluindo_exterior":totais_nacionais,
      "referencia_TSE_definitivo":{13:DILMA,45:AECIO,"total":TOTAL},
      "municipios_votos":int(len(x))}
    a.manifesto.parent.mkdir(parents=True,exist_ok=True)
    if len(x)!=5570 or x.isna().any().any() or totais_nacionais!={13:DILMA,45:AECIO} or sum(totals.values())+sum(totais_exterior.values())!=TOTAL:
        notes["status"]="BLOQUEADO_DIVERGENCIA_TSE"
        a.manifesto.write_text(json.dumps(notes,ensure_ascii=False,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else str(x))+"\n")
        raise ValueError("Conciliação 2014 rejeitada; conferência: "+json.dumps(notes,ensure_ascii=False,default=lambda x:int(x) if isinstance(x,np.integer) else str(x))[:2400])
    x=x.reset_index()
    mapa=pd.read_csv(a.mapa,dtype={"SG_UF":str,"CD_MUNICIPIO":str,"CD_MUNICIPIO_IBGE":str})
    mapa["CD_MUNICIPIO"]=pd.to_numeric(mapa.CD_MUNICIPIO,errors="raise").astype("int64")
    d=x.merge(mapa,on=key,how="left",indicator=True,validate="one_to_one")
    missing=d.loc[d._merge.ne("both"),key]
    notes["sem_correspondencia_mapa"]=int(len(missing))
    if len(d)!=5570 or len(missing) or d.CD_MUNICIPIO_IBGE.duplicated().any():
        notes["status"]="BLOQUEADO_CHAVES_GEOGRAFICAS"
        notes["exemplos_sem_chave"]=missing.head(20).to_dict("records")
        a.manifesto.write_text(json.dumps(notes,ensure_ascii=False,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else str(x))+"\n")
        raise ValueError("Falha na correspondência 2014/2018 dos códigos TSE")
    n13=d[13].astype("int64");n45=d[45].astype("int64")
    validos=n13+n45
    out=pd.DataFrame({
      "ano":2014,"SG_UF":d.SG_UF,"CD_MUNICIPIO":d.CD_MUNICIPIO,
      "CD_MUNICIPIO_IBGE":d.CD_MUNICIPIO_IBGE,
      "latitude":d.latitude,"longitude":d.longitude,
      "votos_pt13":n13,"votos_oponente":n45,
      "numero_oponente":45,"total_validos":validos,
      "competitividade_2t":1-np.abs(n13-n45)/validos,
      "margem_assinada_pt13":(n13-n45)/validos
    }).sort_values(["SG_UF","CD_MUNICIPIO"])
    assert len(out)==5570 and validos.min()>0
    assert out.competitividade_2t.between(0,1).all()
    assert np.allclose(out.competitividade_2t,1-out.margem_assinada_pt13.abs())
    out.to_csv(a.saida,index=False,float_format="%.12f")
    notes.update({"status":"CONCILIADO_NACIONAL_BRASIL_EXTERIOR","municipios":len(out),
       "soma_votos_validos_municipais_brasil":int(out.total_validos.sum()),
       "soma_votos_validos_nacionais_com_exterior":int(sum(totais_nacionais.values())),
       "saida_sha256":hashlib.sha256(a.saida.read_bytes()).hexdigest(),
       "advertencia":"Brasil 5570 municipios (sem ZZ) e votacao no exterior (ZZ) conferidos separadamente; 2014 Dilma e Aecio, não equivale aos candidatos de 2018/2022."})
    a.manifesto.write_text(json.dumps(notes,ensure_ascii=False,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else str(x))+"\n")
    print(json.dumps(notes,ensure_ascii=False,indent=2,default=lambda x:int(x) if isinstance(x,np.integer) else str(x)))
if __name__=="__main__":main()
