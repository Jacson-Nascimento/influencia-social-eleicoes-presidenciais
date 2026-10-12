#!/usr/bin/env python3
"""Painel de seis eleições presidenciais 2002–2022 sem dados de 1998.

Censos anteriores: 2000 para 2002/2006/2010, 2010 para 2014/2018/2022.
Modelo principal de comparabilidade: log da população anterior ao pleito,
urbanização e fração feminina do último Censo anterior (três covariáveis).
Modelo de sensibilidade 2006–2022: incorpora proxy PIB/pop anterior, quatro.
Municípios são identificados pela chave TSE (UF, município) sem imputação.
Saídas NÃO sobrescrevem v14 ou v15, nem transformam resultados passados.
"""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

YR=(2002,2006,2010,2014,2018,2022)
KEY=["SG_UF","CD_MUNICIPIO"]
R_COLS=["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude",
        "votos_pt13","votos_oponente","total_validos",
        "competitividade_2t","margem_assinada_pt13",
        "pop_antes","log_pop","urbanizacao_censo","fracao_feminina_censo","log_pibpc_proxy"]
FINALISTAS={2002:[13,45],2006:[13,45],2010:[13,45]}

def read(p,**kw):
    d=pd.read_csv(p,**kw)
    if d.empty:raise ValueError("CSV sem dados: "+str(p))
    return d

def historically(year,dir_,histctrl,map_,notes):
    raw=read(dir_/str(year)/f"votos_presidenciais_municipais_{year}.csv",dtype={"SG_UF":str})
    v=raw[raw.NR_TURNO.eq(2)].copy()
    assert set(v.NR_CANDIDATO.unique())==set(FINALISTAS[year])
    nat=v.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum().to_dict()
    sub=v[~v.SG_UF.isin(["ZZ","VT"])]
    split=v[v.SG_UF.isin(["ZZ","VT"])].groupby(["SG_UF","NR_CANDIDATO"]).QT_VOTOS_NOMINAIS.sum()
    x=sub.pivot_table(index=KEY,columns="NR_CANDIDATO",values="QT_VOTOS_NOMINAIS",aggfunc="sum")
    if x.isna().any().any() or (x<=0).any().any():
        raise ValueError("Turno histórico incompleto ou votos não positivos")
    x=x.reset_index().merge(map_,on=KEY,how="left",validate="one_to_one",indicator=True)
    unmatched=x[x._merge.ne("both")][KEY].to_dict("records")
    npre=len(x)
    x=x[x._merge.eq("both")].drop(columns="_merge")
    x["ano"]=year
    x["votos_pt13"]=x[13].astype("int64")
    x["votos_oponente"]=x[45].astype("int64")
    x["total_validos"]=x.votos_pt13+x.votos_oponente
    x["margem_assinada_pt13"]=(x.votos_pt13-x.votos_oponente)/x.total_validos
    x["competitividade_2t"]=1-x.margem_assinada_pt13.abs()
    part=histctrl[["CD_MUNICIPIO_IBGE","urbanizacao_2000","fracao_feminina_2000",f"pop_{year-1}",f"log_pop_{year}"]+
              ([f"log_pibpc_proxy_{year}"] if year>=2006 else [])]
    x=x.merge(part,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
    x["pop_antes"]=x[f"pop_{year-1}"]
    x["log_pop"]=x[f"log_pop_{year}"]
    x["urbanizacao_censo"]=x.urbanizacao_2000
    x["fracao_feminina_censo"]=x.fracao_feminina_2000
    x["log_pibpc_proxy"]=x[f"log_pibpc_proxy_{year}"] if year>=2006 else np.nan
    notes[year]={
       "n_municipios_tse_sem_ZZ_VT":npre,
       "n_chaves_no_mapa_atual":len(x),
       "chaves_historicas_sem_correspondencia":unmatched,
       "votos_nacionais_nominais_com_ZZ_VT":{str(k):int(z) for k,z in nat.items()},
       "votos_separados_ZZ_VT":{str(k):int(z) for k,z in split.items()},
       "n_controles_3_completos":int(x[["log_pop","urbanizacao_censo","fracao_feminina_censo"]].notna().all(axis=1).sum()),
       "n_controles_4_completos":int(x[["log_pop","urbanizacao_censo","fracao_feminina_censo","log_pibpc_proxy"]].notna().all(axis=1).sum())}
    return x[R_COLS]

def from_recent(year,v14,c14,v18,ctrl,map_):
    if year==2014:
        x=v14.merge(c14,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
        x["pop_antes"]=x.pop_2013
        x["log_pop"]=x.log_pop
        x["log_pibpc_proxy"]=x.log_pibpc_proxy
        x["urbanizacao_censo"]=x.urbanizacao_2010
        x["fracao_feminina_censo"]=x.fracao_feminina_2010
        return x[R_COLS]
    x=v18[v18.ano.eq(year)].merge(map_,on=KEY,how="left",validate="many_to_one")
    x=x.merge(ctrl,on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
    if year==2018:pop,pib="pop_2017","pibpc_proxy_2016_2017_reais"
    else:pop,pib="pop_2021","pibpc_proxy_2020_2021_reais"
    x["pop_antes"]=x[pop]
    x["log_pop"]=np.log(x[pop].where(x[pop]>0))
    x["log_pibpc_proxy"]=np.log(x[pib].where(x[pib]>0))
    x["urbanizacao_censo"]=x.urbanizacao_2010
    x["fracao_feminina_censo"]=x.fracao_feminina_2010
    return x[R_COLS]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for nm in ("historico","controles_historicos","votos2014","controles2014","votos2018_2022",
               "controles2018_2022","mapa","saida"):
        p.add_argument("--"+nm,type=Path,required=True)
    a=p.parse_args()
    if a.saida.exists() and any(a.saida.iterdir()):
        raise SystemExit("Diretório com dados anteriores; preservar.")
    map_=read(a.mapa,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
    histctrl=read(a.controles_historicos,dtype={"CD_MUNICIPIO_IBGE":str})
    v14=read(a.votos2014,dtype={"CD_MUNICIPIO_IBGE":str})
    c14=read(a.controles2014,dtype={"CD_MUNICIPIO_IBGE":str})
    v18=read(a.votos2018_2022,dtype={"SG_UF":str})
    ctrl=read(a.controles2018_2022,dtype={"CD_MUNICIPIO_IBGE":str})
    if map_.duplicated(KEY).any() or map_.CD_MUNICIPIO_IBGE.duplicated().any():raise ValueError("Mapa chave não única")
    if len(map_)!=5570 or len(histctrl)!=5570 or len(v14)!=5570:
        raise ValueError("Inputs não possuem cobertura esperada")
    notes={}
    t=[historically(y,a.historico,histctrl,map_,notes) for y in (2002,2006,2010)]
    t+=[from_recent(y,v14,c14,v18,ctrl,map_) for y in (2014,2018,2022)]
    panel=pd.concat(t,ignore_index=True)
    if panel.duplicated(["ano"]+KEY).any():raise ValueError("Duplicidade TSE ano e município")
    if panel.duplicated(["ano","CD_MUNICIPIO_IBGE"]).any():raise ValueError("IBGE com código duplicado")
    if not panel.competitividade_2t.dropna().between(0,1).all():
        raise ValueError("Competitividade fora dos limites.")
    if not np.allclose(panel.competitividade_2t,1-panel.margem_assinada_pt13.abs()):
        raise ValueError("C e M sem identidade.")
    core=["log_pop","urbanizacao_censo","fracao_feminina_censo","pop_antes",
          "competitividade_2t","margem_assinada_pt13","latitude","longitude"]
    panel["complete_3"]=panel[core].notna().all(axis=1)
    panel["complete_4"]=panel["complete_3"] & panel.log_pibpc_proxy.notna()
    c3=panel.loc[panel.complete_3].groupby("CD_MUNICIPIO_IBGE").ano.nunique()
    c3=set(c3[c3.eq(6)].index)
    c4=panel.loc[panel.complete_4 & panel.ano.ge(2006)].groupby("CD_MUNICIPIO_IBGE").ano.nunique()
    c4=set(c4[c4.eq(5)].index)
    p3=panel[panel.CD_MUNICIPIO_IBGE.isin(c3)]
    p4=panel[panel.CD_MUNICIPIO_IBGE.isin(c4)&panel.ano.ge(2006)]
    if not 5400<=len(c3)<=5570 or not 5400<=len(c4)<=5570:
        raise ValueError(f"Baixa cobertura do painel: {len(c3)} e {len(c4)}")
    if len(p3)!=6*len(c3) or len(p4)!=5*len(c4):
        raise ValueError("Amostra balanceada inválida.")
    a.saida.mkdir(parents=True)
    panel.to_csv(a.saida/"painel_nao_balanceado_2002_2022.csv",index=False,float_format="%.12f")
    p3.to_csv(a.saida/"painel_balanceado_6_eleicoes_3_controles.csv",index=False,float_format="%.12f")
    p4.to_csv(a.saida/"painel_balanceado_5_eleicoes_4_controles.csv",index=False,float_format="%.12f")
    diag=[{"ano":y,"n_tse_municipios_mapeados":len(panel[panel.ano.eq(y)]),
      "complete_3":int(panel.loc[panel.ano.eq(y),"complete_3"].sum()),
      "complete_4":int(panel.loc[panel.ano.eq(y),"complete_4"].sum()),
      "censo_demografico":2000 if y<=2010 else 2010,
      "populacao_ano":y-1,"pib_ano":y-2 if y>=2006 else None} for y in YR]
    pd.DataFrame(diag).to_csv(a.saida/"cobertura_por_eleicao.csv",index=False)
    manifest={"anos":list(YR),"ano_excluido_explicitamente":1998,
        "autor":"Jacson Cruz do Nascimento","status":"PAINEL_EXPLORATORIO_SEM_ESTIMACAO",
        "censo_2000":[2002,2006,2010],"censo_2010":[2014,2018,2022],
        "amostra_3_controles":len(c3),"observacoes_6_eleicoes":len(p3),
        "amostra_4_controles":len(c4),"observacoes_5_eleicoes":len(p4),
        "chaves_e_totais_historicos":{str(k):v for k,v in notes.items()},
        "cobertura":diag,
        "restricoes":["Censo demográfico anterior ao pleito, não posterior.",
         "2010 utiliza Censo 2000 como série inteiramente anterior, não os dados da coleta do ano da eleição.",
         "PIB para 2002 não obtido da série SIDRA5938, não imputado.",
         "2002 contém chave histórica TSE não conciliada ao mapa atual; município fica excluído com contagem documentada.",
         "2010 inclui chaves especiais VT; não são tratadas como municípios brasileiros.",
         "Pontos espaciais são centroides IBGE2022 e geometria histórica pode divergir.",
         "Não representa previsão ex ante em tempo real, pois séries IBGE podem ter sido revisadas.",
         "1998 foi expressamente excluída por decisão do autor.",
         "Sem inferência individual, causal ou de contágio social."],
        "sha256_arquivos":{}}
    for file in a.saida.glob("*.csv"):
        manifest["sha256_arquivos"][file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
    (a.saida/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in manifest.items() if k!="chaves_e_totais_historicos" and k!="sha256_arquivos"},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
