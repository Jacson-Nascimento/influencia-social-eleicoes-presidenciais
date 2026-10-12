#!/usr/bin/env python3
"""Estudo exploratório de seis eleições 2002–2022, amostra comum.

Censo 2000 em 2002/06, 2010 retrospectivo em 2010/14/18/22;
sensibilidade 2010 com Censo 2000. Nunca alterar versões originais.
Três controles (população pré-pleito, urbanização, fração feminina).
"""
import argparse,importlib.util,json
from pathlib import Path
import numpy as np,pandas as pd

HERE=Path(__file__).resolve().parent
def load(alias,filename):
 s=importlib.util.spec_from_file_location(alias,HERE/filename)
 x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
g=load("geo36","22_benchmark_geografico_competitividade.py")
h=load("temporal36","30_comparar_2014_2018_2022.py")
YEARS=[2002,2006,2010,2014,2018,2022]
FEATURES=["log_pop","urbanizacao","fracao_feminina"]
OUTCOMES={"competitividade":"competitividade_2t","direcao_pt13":"margem_assinada_pt13"}
FINAL={2002:[13,45],2006:[13,45],2010:[13,45],2014:[13,45],2018:[13,17],2022:[13,22]}
KEY=["SG_UF","CD_MUNICIPIO"]
def read(path,**kw):return pd.read_csv(path,**kw)
def historical(year,root):
 d=read(root/str(year)/f"votos_presidenciais_municipais_{year}.csv",dtype={"SG_UF":str})
 assert len(d)>0 and {1,2}==set(d.NR_TURNO.unique())
 d=d[(d.NR_TURNO==2)&(~d.SG_UF.isin(["ZZ","VT"]))].copy()
 assert set(d.NR_CANDIDATO)==set(FINAL[year]),(year,set(d.NR_CANDIDATO))
 if d.duplicated(KEY+["NR_CANDIDATO"]).any():raise ValueError("Duplicated historical key")
 tab=d.pivot(index=KEY,columns="NR_CANDIDATO",values="QT_VOTOS_NOMINAIS").reset_index()
 a,b=FINAL[year]
 if tab[[a,b]].isna().any().any():raise ValueError("Missing finalist votes")
 x,y=tab[a].astype("int64"),tab[b].astype("int64")
 total=x+y
 if (total<=0).any():raise ValueError("Nonpositive municipal votes")
 return pd.DataFrame({"ano":year,"SG_UF":tab.SG_UF,"CD_MUNICIPIO":tab.CD_MUNICIPIO,
    "competitividade_2t":1-(x-y).abs()/total,"margem_assinada_pt13":(x-y)/total})

def panel(a):
 maps=read(a.mapa,dtype={"CD_MUNICIPIO_IBGE":str})
 assert len(maps)==5570 and not maps.duplicated(KEY).any()
 early=read(a.controles2000,dtype={"CD_MUNICIPIO_IBGE":str})
 modern=read(a.controles2010,dtype={"CD_MUNICIPIO_IBGE":str})
 ib2014=read(a.controles2014,dtype={"CD_MUNICIPIO_IBGE":str})
 e2014=read(a.votos2014)
 later=read(a.votos2018_2022)
 assert len(e2014)==5570 and len(later)==11140
 etcols=["CD_MUNICIPIO_IBGE","urbanizacao_2000","fracao_feminina_2000","pop_2001","pop_2005","pop_2009"]
 moc=["CD_MUNICIPIO_IBGE","urbanizacao_2010","fracao_feminina_2010","pop_2017","pop_2021"]
 years=[]
 coverage=[]
 for year in YEARS:
  if year in (2002,2006,2010):v=historical(year,a.historicos)
  elif year==2014:v=e2014.copy()
  else:v=later[later.ano==year].copy()
  v=v.drop(columns=["CD_MUNICIPIO_IBGE","latitude","longitude"],errors="ignore")
  d=v.merge(maps,on=KEY,how="left",indicator=True,validate="one_to_one")
  n_nomatch=int(d._merge.ne("both").sum())
  d=d.drop(columns="_merge")
  d=d.merge(early[etcols],on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
  d=d.merge(modern[moc],on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
  if year==2014:
   d=d.merge(ib2014[["CD_MUNICIPIO_IBGE","pop_2013"]],on="CD_MUNICIPIO_IBGE",how="left",validate="many_to_one")
  census=2000 if year in [2002,2006] else 2010
  popcol={2002:"pop_2001",2006:"pop_2005",2010:"pop_2009",2014:"pop_2013",2018:"pop_2017",2022:"pop_2021"}[year]
  d["ano"]=year
  d["pop_antes"]=d[popcol]
  d["log_pop"]=np.log(d.pop_antes.where(d.pop_antes>0))
  d["urbanizacao"]=d[f"urbanizacao_{census}"]
  d["fracao_feminina"]=d[f"fracao_feminina_{census}"]
  d["censo_referencia"]=census
  use=["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude","pop_antes","censo_referencia"]+FEATURES+list(OUTCOMES.values())
  coverage.append({"ano":year,"n_votacao":len(v),"n_nomatch_mapa":n_nomatch,"censo":census,
      "pop_ano":int(popcol[-4:]),"n_controles_completos":int(d[FEATURES+["pop_antes"]].notna().all(axis=1).sum())})
  years.append(d[use])
 raw=pd.concat(years,ignore_index=True)
 essential=FEATURES+["latitude","longitude","pop_antes"]+list(OUTCOMES.values())
 valid=raw[essential].notna().all(axis=1) & raw.CD_MUNICIPIO_IBGE.notna()
 n=raw.loc[valid].groupby("CD_MUNICIPIO_IBGE").ano.nunique()
 keep=n[n.eq(6)].index
 out=raw[raw.CD_MUNICIPIO_IBGE.isin(keep)].copy()
 if len(keep)<5300 or len(out)!=len(keep)*6 or out.duplicated(["ano","CD_MUNICIPIO_IBGE"]).any():
  raise ValueError(f"Balanced sample invalid {len(keep)}")
 if not np.allclose(out.competitividade_2t,1-out.margem_assinada_pt13.abs()):
  raise ValueError("C/M consistency fail")
 return out,pd.DataFrame(coverage),early

def matrix(d):
 d=d.sort_values(KEY).reset_index(drop=True)
 x=d[FEATURES].to_numpy(float)
 mr=d.SG_UF.map(g.uf_region)
 if mr.isna().any():raise ValueError("Unknown UF")
 cats=pd.Categorical(mr,categories=["S","SE","CO","NE","N"])
 reg=pd.get_dummies(cats,drop_first=True,dtype=float).to_numpy()
 wx=x[g.sp.knn(d,8)].mean(axis=1)
 return d,np.column_stack([x,reg]),np.column_stack([x,reg,wx])

def own_cv(d,features,year,target,weight,logit):
 b,full=features
 y=d[OUTCOMES[target]].to_numpy(float)
 w=np.ones(len(d)) if weight=="uniforme" else d.pop_antes.to_numpy(float)
 summary,UF=g.cv_uf(d,b,full[:,b.shape[1]:],y,w,logit=logit)
 sse=[{"UF":r["UF"],"weight_sum":r["weight_sum"],"sse_local":r["sse_baseline"],"sse_contexto":r["sse_contexto"]} for r in UF]
 res=h.bootstrap(sse,seed=20022022+year+int(target=="direcao_pt13")*3+int(logit)*7+int(weight=="populacao_anterior")*13)
 if abs(res["ganho_rmse_pct"]-summary["reducao_rmse_pct"])>1e-7:raise ValueError("CV calculation mismatch")
 return res

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for k in ["historicos","mapa","controles2000","controles2010","controles2014","votos2014","votos2018_2022","out"]:
  p.add_argument("--"+k,type=Path,required=True)
 a=p.parse_args()
 if a.out.exists() and any(a.out.iterdir()):raise SystemExit("Never overwrite results")
 table,coverage,early=panel(a)
 frames={};features={}
 for year in YEARS:
  d,b,f=matrix(table[table.ano.eq(year)])
  if d.SG_UF.nunique()!=27:raise ValueError("Expected 27 states")
  frames[year]=d;features[year]=(b,f)
 geography=[];time=[];byuf=[];profiles=[]
 for year in YEARS:
  d=frames[year]
  profiles.append({"ano":year,"n":len(d),"censo":int(d.censo_referencia.iloc[0]),
    "media_C":float(d.competitividade_2t.mean()),"media_M":float(d.margem_assinada_pt13.mean())})
  for target in OUTCOMES:
   for weight in ("uniforme","populacao_anterior"):
    for logit in (False,True) if target=="competitividade" else (False,):
     item=own_cv(d,features[year],year,target,weight,logit)
     geography.append({"ano":year,"desfecho":target,"ponderacao":weight,
      "familia":"logit_fracionario" if logit else "linear","n_municipios":len(d),**item})
 scenarios=[([2002],2006),([2002,2006],2010),([2002,2006,2010],2014),
            ([2002,2006,2010,2014],2018),([2002,2006,2010,2014,2018],2022),
            ([2014,2018],2022)]
 for j,(train,targetyear) in enumerate(scenarios):
  for target in OUTCOMES:
   for weight in ("uniforme","populacao_anterior"):
    for logit in (False,True) if target=="competitividade" else (False,):
     seed=20102012+targetyear*7+j*23+int(logit)*11+int(target=="direcao_pt13")*3+int(weight=="populacao_anterior")*2
     res,recs=h.temporal(train,targetyear,frames,features,target,weight,logit,seed=seed)
     case="+".join(map(str,train))+"=>"+str(targetyear)
     fam="logit_fracionario" if logit else "linear"
     time.append({"caso":case,"treino_anos":",".join(map(str,train)),"teste_ano":targetyear,
      "desfecho":target,"ponderacao":weight,"familia":fam,
      "n_treino":len(train)*len(frames[targetyear]),"n_teste":len(frames[targetyear]),**res})
     byuf.extend([{"caso":case,"desfecho":target,"ponderacao":weight,"familia":fam,**r} for r in recs])
 # Compare 2010 census 2010 vs 2000 on the EXACT same 2010 municipalities.
 d10=frames[2010].copy()
 cols=["CD_MUNICIPIO_IBGE","urbanizacao_2000","fracao_feminina_2000"]
 d10=d10.merge(early[cols],on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
 if d10[cols[1:]].isna().any().any():raise ValueError("Missing 2000 census values for 2010 sensitivity")
 d10["urbanizacao"]=d10.urbanizacao_2000
 d10["fracao_feminina"]=d10.fracao_feminina_2000
 d10,b10,f10=matrix(d10)
 sens=[]
 for target in OUTCOMES:
  for weight in ("uniforme","populacao_anterior"):
   for logit in (False,True) if target=="competitividade" else (False,):
    res=own_cv(d10,(b10,f10),2010,target,weight,logit)
    fam="logit_fracionario" if logit else "linear"
    orig=next(r for r in geography if r["ano"]==2010 and r["desfecho"]==target and r["ponderacao"]==weight and r["familia"]==fam)
    sens.append({"ano":2010,"desfecho":target,"ponderacao":weight,"familia":fam,
      "ganho_censo_2010":orig["ganho_rmse_pct"],"ganho_censo_2000":res["ganho_rmse_pct"],
      "diferenca_pp":res["ganho_rmse_pct"]-orig["ganho_rmse_pct"],
      "ic95_censo2000_inf":res["ic95_uf_inf"],"ic95_censo2000_sup":res["ic95_uf_sup"]})
 if len(geography)!=36 or len(time)!=36 or len(sens)!=6:raise ValueError("Missing test combinations")
 a.out.mkdir(parents=True)
 for fn,obj in [("validacao_geografica.csv",geography),("validacao_temporal.csv",time),
                ("sensibilidade_censo_2010.csv",sens),("perfil_descritivo.csv",profiles),
                ("sse_por_uf_validacao_temporal.csv",byuf)]:
  pd.DataFrame(obj).to_csv(a.out/fn,index=False,float_format="%.10f")
 coverage.to_csv(a.out/"cobertura.csv",index=False)
 meta={"autor":"Jacson Cruz do Nascimento","status":"EXPLORATORIO_SEM_ALTERAR_V15",
       "anos":YEARS,"excluido":1998,"n_municipios":len(frames[2002]),"n_observacoes":len(table),
       "regra_censo":{"2002":2000,"2006":2000,"2010":2010,"2014":2010,"2018":2010,"2022":2010},
       "sensibilidade_2010":"Censo 2000 substitui Censo 2010 sem alterar outros regressores ou amostra",
       "modelo_nucleo":"log pop pré-pleito, proporção urbana, proporção feminina, 4 dummies macrorregião; + médias 8 vizinhos",
       "periodo_economico":"PIB NÃO usado para garantir mesmas covariáveis nos seis pleitos",
       "regras":["2010 Censo 2010 retrospectivo e não necessariamente disponível antes da votação",
                 "AMCs históricas não implementadas, geocódigos e centroides são aproximações",
                 "Anos e candidatos diferentes; M vantagem da candidatura PT13 por pleito",
                 "UF VT e exterior ZZ excluídos dos municípios, mantidos nos inventários",
                 "Dados públicos revisados depois do pleito não representam previsão em tempo real",
                 "Intervalos bootstrap 4999 UFs amostradas não eliminam dependência entre UFs vizinhas",
                 "Associação não equivale a efeito causal nem demonstra contágio eleitoral"]}
 (a.out/"manifesto.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
 print("MUNICIPIOS",len(frames[2002]),"OBSERVACOES",len(table))
 print(pd.DataFrame(geography)[["ano","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
 print("TEMPORAL")
 print(pd.DataFrame(time)[["caso","desfecho","ponderacao","familia","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
 print("CENSO")
 print(pd.DataFrame(sens).to_string(index=False))
if __name__=="__main__":main()
