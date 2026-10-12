#!/usr/bin/env python3
"""Sensibilidade documentada: manter Censo 2000 fixo nos seis pleitos.

O benchmark principal já usa Censo 2000 até 2010 e Censo 2010 a partir 2014.
Aqui troca SOMENTE urbanização e fração feminina por Censo 2000 para todos,
com a mesma amostra de 5506 municípios, mesmos pesos e mesmos folds.
Sem dados pós-pleito nas covariáveis da especificação principal.
"""
import argparse,importlib.util,json
from pathlib import Path
import numpy as np,pandas as pd
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("geo_sens",HERE/"22_benchmark_geografico_competitividade.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
YEARS=[2002,2006,2010,2014,2018,2022]
TARGETS={"C":"competitividade_2t","M":"margem_assinada_pt13"}
def build(d,year):
 t=d[d.ano.eq(year)].sort_values(["SG_UF","CD_MUNICIPIO_IBGE"]).reset_index(drop=True)
 assert len(t)==5506 and t.SG_UF.nunique()==27
 x=t[["log_pop_previa","urbanizacao_censo_fixo2000","fracao_feminina_censo_fixo2000"]].to_numpy(float)
 cats=pd.Categorical(t.SG_UF.map(g.uf_region),categories=["S","SE","CO","NE","N"])
 reg=pd.get_dummies(cats,drop_first=True,dtype=float).to_numpy()
 assert reg.shape==(5506,4)
 b=np.column_stack([x,reg])
 near=g.sp.knn(t,8)
 wx=x[near].mean(axis=1)
 return t,b,wx
def metrics(records,seed):
 a=np.asarray([[r["weight_sum"],r["sse_baseline"],r["sse_contexto"]] for r in records],float)
 assert len(a)==27
 baseline=np.sqrt(a[:,1].sum()/a[:,0].sum())
 context=np.sqrt(a[:,2].sum()/a[:,0].sum())
 rng=np.random.default_rng(seed)
 sums=a[rng.integers(0,27,size=(4999,27))].sum(axis=1)
 vals=100*(1-np.sqrt(sums[:,2]/sums[:,1]))
 return {"rmse_baseline":float(baseline),"rmse_contexto":float(context),
         "ganho_rmse_pct":float(100*(1-context/baseline)),
         "ic95_inf":float(np.quantile(vals,.025)),
         "ic95_sup":float(np.quantile(vals,.975))}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--painel",required=True,type=Path)
 ap.add_argument("--orig_geo",required=True,type=Path)
 ap.add_argument("--orig_temp",required=True,type=Path)
 ap.add_argument("--out",required=True,type=Path)
 args=ap.parse_args()
 if args.out.exists() and any(args.out.iterdir()): raise SystemExit("Nunca substituir resultados anteriores")
 d=pd.read_csv(args.painel,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
 assert sorted(d.ano.unique().tolist())==YEARS
 assert len(d)==33036
 data={year:build(d,year) for year in YEARS}
 geo=[];times=[]
 for year in YEARS:
  t,b,wx=data[year]
  for target,col in TARGETS.items():
   y=t[col].to_numpy(float)
   for weight in ("uniforme","populacao_anterior"):
    w=np.ones(len(t)) if weight=="uniforme" else t.pop_previa.to_numpy(float)
    for kind in (["linear","logit_fracionario"] if target=="C" else ["linear"]):
     out,rows=g.cv_uf(t,b,wx,y,w,logit=kind=="logit_fracionario")
     stat=metrics(rows,seed=20261012+year*17+(target=="M")*5+(weight=="populacao_anterior")*3+(kind=="logit_fracionario"))
     if abs(stat["ganho_rmse_pct"]-out["reducao_rmse_pct"])>1e-7:
      raise ValueError("CV de UF não reconcilia")
     geo.append({"ano":year,"desfecho":target,"ponderacao":weight,"familia":kind,**stat})
 for i,year in enumerate(YEARS[1:]):
  years=YEARS[:i+1]
  train=pd.concat([data[y][0] for y in years],ignore_index=True)
  bt=np.vstack([data[y][1] for y in years])
  ft=np.vstack([np.column_stack([data[y][1],data[y][2]]) for y in years])
  te,b,wx=data[year];fc=np.column_stack([b,wx])
  for target,col in TARGETS.items():
   yt=te[col].to_numpy(float)
   for weight in ("uniforme","populacao_anterior"):
    wt=np.ones(len(train)) if weight=="uniforme" else train.pop_previa.to_numpy(float)
    wte=np.ones(len(te)) if weight=="uniforme" else te.pop_previa.to_numpy(float)
    for kind in (["linear","logit_fracionario"] if target=="C" else ["linear"]):
     logit=kind=="logit_fracionario"
     pb=g.predict(bt,b,train[col].to_numpy(float),wt,logit=logit)
     pc=g.predict(ft,fc,train[col].to_numpy(float),wt,logit=logit)
     rec=[]
     for uf in sorted(te.SG_UF.unique()):
      idx=te.SG_UF.eq(uf).to_numpy()
      rec.append({"weight_sum":float(wte[idx].sum()),
                 "sse_baseline":float(np.sum(wte[idx]*(yt[idx]-pb[idx])**2)),
                 "sse_contexto":float(np.sum(wte[idx]*(yt[idx]-pc[idx])**2))})
     stat=metrics(rec,seed=20500212+year*41+(target=="M")*5+(weight=="populacao_anterior")*3+logit)
     times.append({"treino_anos":"+".join(map(str,years)),"teste_ano":year,"desfecho":target,"ponderacao":weight,"familia":kind,**stat})
 res_geo=pd.DataFrame(geo);res_temp=pd.DataFrame(times)
 assert len(res_geo)==36 and len(res_temp)==30
 prev_geo=pd.read_csv(args.orig_geo);prev_time=pd.read_csv(args.orig_temp)
 prev_geo["desfecho"]=prev_geo.desfecho.replace({"competitividade":"C","direcao_pt13":"M"})
 prev_time["desfecho"]=prev_time.desfecho.replace({"competitividade":"C","direcao_pt13":"M"})
 keys=["ano","desfecho","ponderacao","familia"]
 cmp=res_geo.merge(prev_geo[keys+["ganho_rmse_pct"]],on=keys,suffixes=("_censo2000_fixo","_censo_antecedente"),validate="one_to_one")
 cmp["delta_pontos_percentuais"]=cmp.ganho_rmse_pct_censo2000_fixo-cmp.ganho_rmse_pct_censo_antecedente
 keys_t=["teste_ano","desfecho","ponderacao","familia"]
 cmp_t=res_temp.merge(prev_time[keys_t+["ganho_rmse_pct"]],on=keys_t,suffixes=("_censo2000_fixo","_censo_antecedente"),validate="one_to_one")
 cmp_t["delta_pontos_percentuais"]=cmp_t.ganho_rmse_pct_censo2000_fixo-cmp_t.ganho_rmse_pct_censo_antecedente
 if len(cmp)!=36 or len(cmp_t)!=30:raise ValueError("Resultados não comparáveis")
 args.out.mkdir(parents=True)
 res_geo.to_csv(args.out/"censo_fixo2000_validacao_geografica.csv",index=False,float_format="%.10f")
 res_temp.to_csv(args.out/"censo_fixo2000_validacao_temporal.csv",index=False,float_format="%.10f")
 cmp.to_csv(args.out/"contraste_censo_geografico.csv",index=False,float_format="%.10f")
 cmp_t.to_csv(args.out/"contraste_censo_temporal.csv",index=False,float_format="%.10f")
 meta={"tipo":"sensibilidade sem recomputação das séries nominais de voto",
   "anos":YEARS,"amostra":5506,"n_observacoes":33036,
   "censo_principal":"2000 2002/2006/2010; 2010 2014/2018/2022",
   "censo_alternativo":"2000 fixo em TODOS os pleitos",
   "criterio":"mesma amostra, mesmos folds e controles (3), mesmas macrorregiões, k=8",
   "cautela":"Censo 2000 fixo evita quebra de vintage mas perde atualização demográfica ao longo do tempo; não escolher resultado mais favorável.",
   "inferencias":"bootstrap de 4.999 reamostragens por UF, UFs fronteiriças dependentes; não causal.",
   "referencia":"https://doi.org/10.1590/0101-416147182phe"}
 (args.out/"manifesto.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
 print("GEOGRAFIA\n"+cmp[["ano","desfecho","ponderacao","familia","ganho_rmse_pct_censo_antecedente","ganho_rmse_pct_censo2000_fixo","delta_pontos_percentuais"]].to_string(index=False))
 print("TEMPORAL\n"+cmp_t[["teste_ano","desfecho","ponderacao","familia","ganho_rmse_pct_censo_antecedente","ganho_rmse_pct_censo2000_fixo","delta_pontos_percentuais"]].to_string(index=False))
if __name__=="__main__": main()
