#!/usr/bin/env python3
"""Preparar painel eleitoral presidencial 2002–2022, excluindo 1998.

Metodologia baseada em estudos de geografia eleitoral com IBGE e AMCs:
- Censo anterior (2000 para 2002/06/10; 2010 para 2014/18/22);
- segunda especificação mantém o Censo 2000 fixo nos seis pleitos;
- municípios sem chave TSE/IBGE não são imputados, amostra comum;
- NÃO denominar amostra comum como AMC sem crosswalk genealogicamente verificado.
Fontes:
Ehrl 2017 DOI 10.1590/0101-416147182phe
Sousa, Portéglio & Ribeiro DOI 10.5380/recp.v10i1.70422
TSE: resultados 2002/2006/2010, 2014/2018/2022.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np,pandas as pd

YEARS=[2002,2006,2010,2014,2018,2022]
K=["SG_UF","CD_MUNICIPIO"]
def digest(path):
 h=hashlib.sha256()
 with Path(path).open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()

def parse_votes(path,year,mapping):
 t=pd.read_csv(path,dtype={"SG_UF":str})
 t=t[t.NR_TURNO.eq(2)].copy()
 # Mesmo candidato PT #13 (Lula/Dilma) contra oponentes #45 em 2002/06/10.
 if set(t.NR_CANDIDATO.unique())!={13,45}:raise ValueError("Finalistas inesperados em "+str(year))
 full=t.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum()
 if set(full.index)!={13,45}:raise ValueError("Candidaturas ausentes")
 special=t[t.SG_UF.isin(["ZZ","VT"])].groupby(["SG_UF","NR_CANDIDATO"]).QT_VOTOS_NOMINAIS.sum()
 mun=t[~t.SG_UF.isin(["ZZ","VT"])].copy()
 pivot=mun.pivot_table(index=K,columns="NR_CANDIDATO",values="QT_VOTOS_NOMINAIS",aggfunc="sum")
 if pivot.isna().any().any():raise ValueError("Faltam candidaturas no município")
 pivot=pivot.reset_index()
 n0=len(pivot)
 pivot=pivot.merge(mapping,on=K,how="left",validate="one_to_one",indicator=True)
 mismatch=pivot.loc[pivot._merge.ne("both"),K].to_dict("records")
 good=pivot[pivot._merge.eq("both")].copy()
 if good.CD_MUNICIPIO_IBGE.duplicated().any():raise ValueError("Código IBGE duplicado")
 good["ano"]=year
 good["votos_pt13"]=good[13].astype("int64")
 good["votos_oponente"]=good[45].astype("int64")
 good["total_validos"]=good.votos_pt13+good.votos_oponente
 good["competitividade_2t"]=1-(good.votos_pt13-good.votos_oponente).abs()/good.total_validos
 good["margem_assinada_pt13"]=(good.votos_pt13-good.votos_oponente)/good.total_validos
 out=good[["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE",
       "latitude","longitude","votos_pt13","votos_oponente","total_validos",
       "competitividade_2t","margem_assinada_pt13"]]
 report={"ano":year,"n_municipios_no_arquivo":n0,"n_chaves_mapa":len(out),
   "sem_correspondencia":mismatch[:30],
   "votos_nacionais_candidato":{str(int(k)):int(v) for k,v in full.items()},
   "votos_especiais":{f"{k[0]}_{int(k[1])}":int(v) for k,v in special.items()},
   "votos_municipais":int(pivot[[13,45]].sum().sum()),
   "n_municipios_excluidos_por_chave":len(mismatch),
   "documentacao":"Exclui ZZ exterior e VT voto em trânsito do nível municipal; totais nacionais preservados nos relatórios."}
 assert len(out)>5500 and out.total_validos.gt(0).all()
 return out,report

def main():
 p=argparse.ArgumentParser()
 for arg in ("tse2002","tse2006","tse2010","votos2014","votos2018_2022",
             "ibge_historico","ibge_2014","ibge_recente","mapa","out"):p.add_argument("--"+arg,required=True,type=Path)
 a=p.parse_args()
 if a.out.exists() and any(a.out.iterdir()):raise SystemExit("Saída ocupada: versões antigas preservadas.")
 mp=pd.read_csv(a.mapa,dtype={"SG_UF":str,"CD_MUNICIPIO_IBGE":str})
 mp["CD_MUNICIPIO"]=mp.CD_MUNICIPIO.astype(int)
 assert len(mp)==5570 and not mp.duplicated(K).any()
 hist=pd.read_csv(a.ibge_historico,dtype={"CD_MUNICIPIO_IBGE":str})
 cc14=pd.read_csv(a.ibge_2014,dtype={"CD_MUNICIPIO_IBGE":str})
 recent=pd.read_csv(a.ibge_recente,dtype={"CD_MUNICIPIO_IBGE":str})
 assert not hist.CD_MUNICIPIO_IBGE.duplicated().any()
 oldyear={2002:a.tse2002,2006:a.tse2006,2010:a.tse2010}
 data=[];reports=[]
 for yr,path in oldyear.items():
  d,r=parse_votes(path,yr,mp)
  data.append(d);reports.append(r)
 votes14=pd.read_csv(a.votos2014,dtype={"CD_MUNICIPIO_IBGE":str})
 assert len(votes14)==5570 and set(votes14.ano)=={2014}
 data.append(votes14[["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE",
    "latitude","longitude","votos_pt13","votos_oponente","total_validos",
    "competitividade_2t","margem_assinada_pt13"]])
 later=pd.read_csv(a.votos2018_2022)
 later=later.merge(mp,on=K,validate="many_to_one",how="left")
 assert set(later.ano)=={2018,2022} and len(later)==11140
 data.append(later[["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE",
    "latitude","longitude","votos_pt13","votos_oponente","total_validos",
    "competitividade_2t","margem_assinada_pt13"]])
 panel=pd.concat(data,ignore_index=True)
 assert not panel.duplicated(["ano","CD_MUNICIPIO_IBGE"]).any()
 assert set(panel.ano)==set(YEARS)
 features_hist=["CD_MUNICIPIO_IBGE","urbanizacao_2000","fracao_feminina_2000",
     "pop_2001","pop_2005","pop_2009","log_pibpc_proxy_2006","log_pibpc_proxy_2010"]
 cols_recent=["CD_MUNICIPIO_IBGE","urbanizacao_2010","fracao_feminina_2010",
     "pop_2017","pop_2021","pibpc_proxy_2016_2017_reais","pibpc_proxy_2020_2021_reais"]
 assert set(features_hist).issubset(hist) and set(cols_recent).issubset(recent)
 assert {"CD_MUNICIPIO_IBGE","pop_2013","pibpc_proxy_2012_2013_reais"}.issubset(cc14)
 d=panel.merge(hist[features_hist],on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
 d=d.merge(recent[cols_recent],on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
 d=d.merge(cc14[["CD_MUNICIPIO_IBGE","pop_2013","pibpc_proxy_2012_2013_reais"]],
           on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
 d["censo_antecedente"]=np.where(d.ano.le(2010),2000,2010)
 d["urbanizacao_censo_vigente"]=np.where(d.ano.le(2010),d.urbanizacao_2000,d.urbanizacao_2010)
 d["fracao_feminina_censo_vigente"]=np.where(d.ano.le(2010),d.fracao_feminina_2000,d.fracao_feminina_2010)
 d["urbanizacao_censo_fixo2000"]=d.urbanizacao_2000
 d["fracao_feminina_censo_fixo2000"]=d.fracao_feminina_2000
 pops={2002:"pop_2001",2006:"pop_2005",2010:"pop_2009",2014:"pop_2013",2018:"pop_2017",2022:"pop_2021"}
 gdps={2006:"log_pibpc_proxy_2006",2010:"log_pibpc_proxy_2010"}
 for yr in YEARS:
  cond=d.ano.eq(yr)
  d.loc[cond,"pop_previa"]=d.loc[cond,pops[yr]]
  if yr in gdps:
   d.loc[cond,"log_pibpc_proxy"]=d.loc[cond,gdps[yr]]
  if yr==2014:d.loc[cond,"log_pibpc_proxy"]=np.log(d.loc[cond,"pibpc_proxy_2012_2013_reais"].where(lambda s:s>0))
  if yr==2018:d.loc[cond,"log_pibpc_proxy"]=np.log(d.loc[cond,"pibpc_proxy_2016_2017_reais"].where(lambda s:s>0))
  if yr==2022:d.loc[cond,"log_pibpc_proxy"]=np.log(d.loc[cond,"pibpc_proxy_2020_2021_reais"].where(lambda s:s>0))
 d["log_pop_previa"]=np.log(d.pop_previa.where(d.pop_previa.gt(0)))
 main_cols=["log_pop_previa","urbanizacao_censo_vigente","fracao_feminina_censo_vigente",
    "urbanizacao_censo_fixo2000","fracao_feminina_censo_fixo2000",
    "latitude","longitude","competitividade_2t","margem_assinada_pt13"]
 complete=d[main_cols].notna().all(axis=1)
 available=d.loc[complete].groupby("CD_MUNICIPIO_IBGE").ano.nunique()
 common=sorted(available[available==6].index)
 balance=d[d.CD_MUNICIPIO_IBGE.isin(common)].copy()
 if len(common)<5350 or len(balance)!=6*len(common):
  raise ValueError(f"Amostra histórica comum insuficiente: {len(common)}")
 if len(balance.loc[balance.ano.eq(2014)])!=len(common):raise ValueError("2014 não balanceado")
 if not np.allclose(balance.competitividade_2t,1-balance.margem_assinada_pt13.abs()):
  raise ValueError("Indicadores C/M incompatíveis")
 if balance.log_pop_previa.isna().any():raise ValueError("População ausente")
 a.out.mkdir(parents=True,exist_ok=True)
 final_cols=["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude",
   "votos_pt13","votos_oponente","total_validos","competitividade_2t","margem_assinada_pt13",
   "censo_antecedente","log_pop_previa","pop_previa","log_pibpc_proxy",
   "urbanizacao_censo_vigente","fracao_feminina_censo_vigente",
   "urbanizacao_censo_fixo2000","fracao_feminina_censo_fixo2000"]
 balance[final_cols].sort_values(["ano","SG_UF","CD_MUNICIPIO_IBGE"]).to_csv(a.out/"painel_seis_eleicoes_2002_2022.csv",index=False,float_format="%.12f")
 coverage=d.groupby("ano").agg(
   municipios_originais=("CD_MUNICIPIO_IBGE","size"),
   municipios_com_3_controles=("log_pop_previa",lambda x:int(x.notna().sum())),
   municipios_PIB_observado=("log_pibpc_proxy",lambda x:int(x.notna().sum())))
 coverage["municipios_balanceados"]=len(common)
 coverage.to_csv(a.out/"cobertura_por_eleicao.csv")
 manifest={"escopo":"Estudo 2002–2022 (sem 1998), seis segundos turnos",
   "amostra_comum":len(common),"n_observacoes":len(balance),
   "nao_usar_1998":True,"modelo_principal":"Três regressoras locais: log população no ano anterior, urbanização e fração feminina do censo antecedente",
   "vintages":{"2002,2006,2010":"Censo 2000","2014,2018,2022":"Censo 2010"},
   "sensibilidade":"Fixar Censo 2000 em todos os seis pleitos para avaliar ruptura das variáveis demográficas",
   "pib":"Não incluir PIB no modelo principal porque SIDRA 5938 não devolveu 2000; PIB apenas na sensibilidade 2006–2022",
   "geografia":"Unidades com códigos estáveis e cobertura em todos os pleitos; NÃO equivalem a áreas mínimas comparáveis completas (AMC).",
   "atencao":"Uma amostra municipal comum não neutraliza desmembramentos de áreas; agregar em AMCs somente com crosswalk oficial verificado.",
   "modelagem":"Eleições diferentes e candidaturas PT #13 distintas. Modelos descritivos, sem inferência causal.",
   "tse_conciliacao_pendente":"2002 2006 2010 inventariados, extrair VT/ZZ e comparar com registros oficiais antes de considerá-los plenamente auditados",
   "desvio_2002":"Código TSE 91065/MT sem mapa 2018, excluído do painel e documentado.",
   "fontes":{"Ehrl2017":"https://doi.org/10.1590/0101-416147182phe",
     "Sousa2019":"https://doi.org/10.5380/recp.v10i1.70422",
     "IpeaGEO":"https://portalantigo.ipea.gov.br/ipeageo/arquivos/Tutorial_IpeaGEO_VF.pdf"},
   "insumos_sha256":{key:digest(getattr(a,key)) for key in (
     "tse2002","tse2006","tse2010","votos2014","votos2018_2022",
     "ibge_historico","ibge_2014","ibge_recente","mapa")},
   "origens":[*reports]}
 (a.out/"manifesto.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
 print(json.dumps({"amostra":len(common),"observacoes":len(balance),
   "cobertura":coverage.reset_index().to_dict("records"),
   "eleicoes_n":balance.groupby("ano").size().to_dict()},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
