#!/usr/bin/env python3
"""Painel exploratório de seis eleições presidenciais com segundo turno 2002-2022.

Comparação espacial e validação temporal em amostra ESTÁVEL, com 3 controles
disponíveis antes dos pleitos: log(população anterior), urbanização e fração
feminina do censo anterior. Sem PIB: série 2000 não localizada no SIDRA5938.
Não usar resultados deste modelo reduzido como substituição da especificação
anterior de quatro covariáveis do artigo v14/v15.
"""
import argparse,json,hashlib,importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("geo_historic",HERE/"22_benchmark_geografico_competitividade.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
YEARS=[2002,2006,2010,2014,2018,2022]
REGIONS=g.uf_region
OUT={"C":"competitividade_2t","M":"margem_assinada_pt13"}
EXPECTED={2002:{13:52793364,45:33370739},2006:{13:58295042,45:37543178},2010:{13:55752529,45:43711388}}
FEATURES=["log_pop","urban","feminina"]

def main():
 p=argparse.ArgumentParser()
 for x in ("mapa","historicos","ibgeantigo","votos2014","ibge2014","votos2018_22","ibge2018_22","out"):
  p.add_argument("--"+x,type=Path,required=True)
 a=p.parse_args()
 if a.out.exists() and any(a.out.iterdir()):raise SystemExit("Não sobrescrever resultados anteriores.")
 mapa=pd.read_csv(a.mapa,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
 ibge0=pd.read_csv(a.ibgeantigo,dtype={"CD_MUNICIPIO_IBGE":str})
 ibge14=pd.read_csv(a.ibge2014,dtype={"CD_MUNICIPIO_IBGE":str})
 ibge2=pd.read_csv(a.ibge2018_22,dtype={"CD_MUNICIPIO_IBGE":str})
 r14=pd.read_csv(a.votos2014,dtype={"CD_MUNICIPIO_IBGE":str})
 r18=pd.read_csv(a.votos2018_22,dtype={"SG_UF":str})
 frames=[];records={}
 for year in (2002,2006,2010):
  source=a.historicos/str(year)/f"votos_presidenciais_municipais_{year}.csv"
  t=pd.read_csv(source,dtype={"SG_UF":str})
  t=t[t.NR_TURNO.eq(2)]
  by=t.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum()
  if {13:int(by.get(13,0)),45:int(by.get(45,0))}!=EXPECTED[year]:
   raise ValueError(f"Contagens 2o turno inesperadas {year}: {by.to_dict()}")
  local=t[t.SG_UF.isin(REGIONS)].copy()
  # Extraterritoriais ZZ e VT não recebem coordenadas municipais.
  other=t[~t.SG_UF.isin(REGIONS)]
  ids=set(local.NR_CANDIDATO.unique())
  if ids!={13,45}:raise ValueError("Candidatos inesperados")
  v=local.pivot(index=["SG_UF","CD_MUNICIPIO"],columns="NR_CANDIDATO",values="QT_VOTOS_NOMINAIS")
  if v.isna().any().any():raise ValueError("Voto candidato ausente no município.")
  v=v.reset_index()
  d=v.merge(mapa[["SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude"]],
      how="left",on=["SG_UF","CD_MUNICIPIO"],indicator=True,validate="one_to_one")
  records[year]={"chaves_nao_correspondentes":int(d._merge.ne("both").sum()),
    "extraterritoriais_codigos":sorted(other.SG_UF.unique().tolist()),
    "votos_extraterritoriais":int(other.QT_VOTOS_NOMINAIS.sum()),
    "municipios_arquivo":len(v),"municipios_atuais_com_chave":int(d._merge.eq("both").sum())}
  d=d[d._merge.eq("both")].drop(columns="_merge")
  d=d.merge(ibge0,on="CD_MUNICIPIO_IBGE",validate="many_to_one",how="left")
  d["ano"]=year
  d["votos_pt13"]=d[13];d["votos_oponente"]=d[45]
  d["total_validos"]=d.votos_pt13+d.votos_oponente
  d["margem_assinada_pt13"]=(d.votos_pt13-d.votos_oponente)/d.total_validos
  d["competitividade_2t"]=1-d.margem_assinada_pt13.abs()
  yearprev={2002:2001,2006:2005,2010:2009}[year]
  d["pop_antes"]=d[f"pop_{yearprev}"]
  d["log_pop"]=d[f"log_pop_{year}"]
  d["urban"]=d.urbanizacao_2000;d["feminina"]=d.fracao_feminina_2000
  frames.append(d[["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude","pop_antes"]+FEATURES+list(OUT.values())])
 # 2014
 r14=r14.merge(ibge14[["CD_MUNICIPIO_IBGE","pop_2013","log_pop","urbanizacao_2010","fracao_feminina_2010"]],
        how="left",on="CD_MUNICIPIO_IBGE",validate="one_to_one",suffixes=("","_ibge"))
 r14["pop_antes"]=r14.pop_2013
 r14["urban"]=r14.urbanizacao_2010;r14["feminina"]=r14.fracao_feminina_2010
 frames.append(r14[["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude","pop_antes"]+FEATURES+list(OUT.values())])
 # 2018/2022
 r18=r18.merge(mapa[["SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude"]],
       how="left",on=["SG_UF","CD_MUNICIPIO"],validate="many_to_one")
 r18=r18.merge(ibge2[["CD_MUNICIPIO_IBGE","pop_2017","pop_2021","urbanizacao_2010","fracao_feminina_2010"]],
                 on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
 for year in (2018,2022):
  d=r18[r18.ano.eq(year)].copy()
  d["pop_antes"]=d["pop_2017" if year==2018 else "pop_2021"]
  d["log_pop"]=np.log(d.pop_antes.where(d.pop_antes.gt(0)))
  d["urban"]=d.urbanizacao_2010
  d["feminina"]=d.fracao_feminina_2010
  frames.append(d[["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude","pop_antes"]+FEATURES+list(OUT.values())])
 all_=pd.concat(frames,ignore_index=True)
 required=["pop_antes","latitude","longitude"]+FEATURES+list(OUT.values())
 complete=all_[required].notna().all(axis=1)&all_.pop_antes.gt(0)
 all_=all_[complete]
 kept=all_.groupby("CD_MUNICIPIO_IBGE").ano.nunique()
 common=sorted(kept[kept.eq(6)].index)
 panel=all_[all_.CD_MUNICIPIO_IBGE.isin(common)].copy()
 if len(common)<5300 or len(panel)!=len(common)*6:
  raise ValueError(f"Amostra comum insuficiente: {len(common)}")
 for yr in YEARS:
  d=panel[panel.ano.eq(yr)]
  if len(d)!=len(common) or not d.competitividade_2t.between(0,1).all():raise ValueError("Cobertura/intervalo")
  if not np.allclose(d.competitividade_2t,1-d.margem_assinada_pt13.abs()):raise ValueError("C identidade")
 features={};df={}
 for year in YEARS:
  d=panel[panel.ano.eq(year)].sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
  if len(d)!=len(common) or d.SG_UF.nunique()!=27:raise ValueError("UF/ano inconsistentes")
  X=d[FEATURES].to_numpy(float)
  cats=pd.Categorical(d.SG_UF.map(REGIONS),categories=["S","SE","CO","NE","N"])
  macro=pd.get_dummies(cats,drop_first=True,dtype=float).to_numpy()
  local=np.column_stack([X,macro])
  near=g.sp.knn(d,8)
  wX=X[near].mean(axis=1)
  df[year]=d;features[year]=(local,wX)
 geographic=[];temporal=[];peruf=[]
 for year in YEARS:
  d=df[year];X,WX=features[year]
  for desfecho,col in OUT.items():
   yy=d[col].to_numpy(float)
   for weights in ("uniforme","populacao_anterior"):
    ww=np.ones(len(d)) if weights=="uniforme" else d.pop_antes.to_numpy(float)
    for fractional in (False,True) if desfecho=="C" else (False,):
     res,uf=g.cv_uf(d,X,WX,yy,ww,logit=fractional)
     check=_bootstrap([{"UF":u["UF"],"weight_sum":u["weight_sum"],"sse_local":u["sse_baseline"],"sse_contextual":u["sse_contexto"]} for u in uf],
       seed=20261012+year*11+(desfecho=="M")*4+(weights=="populacao_anterior")*2+int(fractional))
     if abs(res["reducao_rmse_pct"]-check["ganho_rmse_pct"])>1e-6:raise ValueError("UF-RMSE não reproduzido")
     geographic.append({"ano":year,"desfecho":desfecho,"ponderacao":weights,
       "familia":"logit_fracionario" if fractional else "linear",**check})
 temporal_windows=[(YEARS[:i],YEARS[i]) for i in range(1,len(YEARS))]
 for ytrain,ytest in temporal_windows:
  d=pd.concat([df[y] for y in ytrain],ignore_index=True)
  test=df[ytest]
  xl=np.vstack([features[y][0] for y in ytrain])
  xc=np.vstack([np.column_stack(features[y]) for y in ytrain])
  xt0=features[ytest][0]
  xt1=np.column_stack(features[ytest])
  for desfecho,col in OUT.items():
   trainy=d[col].to_numpy(float);truth=test[col].to_numpy(float)
   for weighting in ("uniforme","populacao_anterior"):
    wtr=np.ones(len(d)) if weighting=="uniforme" else d.pop_antes.to_numpy(float)
    wte=np.ones(len(test)) if weighting=="uniforme" else test.pop_antes.to_numpy(float)
    for fractional in (False,True) if desfecho=="C" else (False,):
     p0=g.predict(xl,xt0,trainy,wtr,logit=fractional)
     p1=g.predict(xc,xt1,trainy,wtr,logit=fractional)
     rows=[]
     for uf in sorted(set(test.SG_UF)):
      pos=test.SG_UF.eq(uf).to_numpy()
      rows.append({"UF":uf,"weight_sum":float(wte[pos].sum()),
        "sse_local":float(np.sum(wte[pos]*(truth[pos]-p0[pos])**2)),
        "sse_contextual":float(np.sum(wte[pos]*(truth[pos]-p1[pos])**2))})
     ci=_bootstrap(rows,seed=20261012+ytest*13+(desfecho=="M")*4+(weighting=="populacao_anterior")*2+int(fractional))
     scenario="+".join(map(str,ytrain))+"=>"+str(ytest)
     temporal.append({"treino_anos":"+".join(map(str,ytrain)),"teste_ano":ytest,
        "cenario":scenario,"desfecho":desfecho,"ponderacao":weighting,
        "familia":"logit_fracionario" if fractional else "linear",
        "n_treino":len(d),"n_teste":len(test),**ci})
     peruf.extend([{**{"cenario":scenario,"desfecho":desfecho,"ponderacao":weighting,
                     "familia":"logit_fracionario" if fractional else "linear"},**row} for row in rows])
 a.out.mkdir(parents=True,exist_ok=True)
 gd=pd.DataFrame(geographic);tm=pd.DataFrame(temporal)
 if len(gd)!=6*6 or len(tm)!=5*6 or len(peruf)!=5*6*27:
  raise ValueError("Dimensão das tabelas inválida")
 gd.to_csv(a.out/"validacao_geografica_2002_2022.csv",index=False,float_format="%.10f")
 tm.to_csv(a.out/"validacao_temporal_expansiva_2002_2022.csv",index=False,float_format="%.10f")
 pd.DataFrame(peruf).to_csv(a.out/"sse_por_uf_validacao_temporal.csv",index=False,float_format="%.10f")
 info={"status":"ESTUDO_EXPLORATORIO_NAO_SUBMETIDO","anos":YEARS,
   "municipios_comuns":len(common),"observacoes_municipio_ano":len(panel),
   "variaveis_comuns":["log da população no ano anterior","urbanização e proporção de mulheres no censo anterior"],
   "ausencia_PIB_2000":"modelo reduzido de tres covariáveis, NÃO equivalente ao original de quatro covariáveis",
   "censos":{"2002_2006_2010":2000,"2014_2018_2022":2010},
   "finalistas_segundo_turno":{"2002":"Lula/PT13 e Serra/PSDB45","2006":"Lula/PT13 e Alckmin/PSDB45",
    "2010":"Dilma/PT13 e Serra/PSDB45","2014":"Dilma/PT13 e Aécio/PSDB45",
    "2018":"Haddad/PT13 e Bolsonaro/PSL17","2022":"Lula/PT13 e Bolsonaro/PL22"},
   "geografia":"kNN8 centroides IBGE2022 e macrorregiões; observações com fronteiras e códigos validáveis somente na amostra comum",
   "2002_2006_2010_chaves_registros":records,
   "intervalos":"4.999 bootstrap pareado de UFs; limitados pela dependencia espacial",
   "limites":["Não há 1998 neste painel: eleição apenas de 1º turno e dados incompletos.",
              "Os seis pleitos têm candidatos/oponentes diferentes; M representa sempre número 13 versus o outro finalista.",
              "Modelos são avaliados retrospectivamente; controle IBGE revisado não corresponde a disponibilidade em tempo real.",
              "Municípios com códigos estáveis não garantem perímetro espacial perfeitamente idêntico.",
              "Treinos temporais empilham os mesmos municípios em eleições diferentes.",
              "Não demonstrar causalidade nem contágio social.",
              "Comparar ganhos relativos só dentro do mesmo desfecho/ponderação/horizonte."],
   "implementacao":"scripts/36_modelos_historicos_reduzidos.py"}
 (a.out/"manifesto.json").write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(info,ensure_ascii=False,indent=2))
 print("VALIDACAO ESPACIAL\n"+gd.query("ponderacao=='uniforme' and familia=='linear'")[["ano","desfecho","ganho_rmse_pct","ci_inf","ci_sup"]].to_string(index=False))
 print("VALIDACAO TEMPORAL\n"+tm.query("ponderacao=='uniforme' and familia=='linear'")[["cenario","desfecho","ganho_rmse_pct","ci_inf","ci_sup"]].to_string(index=False))

def _bootstrap(rows,seed):
 z=np.array([[r["weight_sum"],r["sse_local"],r["sse_contextual"]] for r in rows],float)
 if len(z)!=27 or np.any(z[:,0]<=0):raise ValueError("SSE por UF incompleto")
 rng=np.random.default_rng(seed)
 d=rng.integers(0,27,size=(4999,27))
 sums=z[d].sum(axis=1)
 bs=100*(1-np.sqrt(sums[:,2]/sums[:,1]))
 b=np.sqrt(z[:,1].sum()/z[:,0].sum());c=np.sqrt(z[:,2].sum()/z[:,0].sum())
 return {"rmse_local":float(b),"rmse_contextual":float(c),
   "ganho_rmse_pct":float(100*(1-c/b)),"ci_inf":float(np.quantile(bs,.025)),
   "ci_sup":float(np.quantile(bs,.975)),
   "n_ufs_piora":int(np.count_nonzero(z[:,2]>z[:,1]))}
if __name__=="__main__": main()
