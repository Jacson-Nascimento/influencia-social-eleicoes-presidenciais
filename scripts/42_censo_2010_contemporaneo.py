#!/usr/bin/env python3
"""Teste de sensibilidade 2010 com Censo 2010 contemporâneo ao pleito.

Amostra idêntica (5506) e mesmos folds; não substituir o desenho principal
com Censo 2000 anterior ao pleito. Censo 2010 não era disponível ex ante.
"""
import argparse,json,importlib.util
from pathlib import Path
import numpy as np,pandas as pd
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("geo2010",HERE/"22_benchmark_geografico_competitividade.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def main():
 p=argparse.ArgumentParser()
 for arg in ("painel","censo2010","referencia","out"):p.add_argument("--"+arg,type=Path,required=True)
 a=p.parse_args()
 if a.out.exists() and any(a.out.iterdir()):raise SystemExit("Preservar resultados")
 t=pd.read_csv(a.painel,dtype={"CD_MUNICIPIO_IBGE":str})
 t=t[t.ano.eq(2010)].copy().sort_values(["SG_UF","CD_MUNICIPIO_IBGE"]).reset_index(drop=True)
 assert len(t)==5506 and t.SG_UF.nunique()==27
 c=pd.read_csv(a.censo2010,dtype={"CD_MUNICIPIO_IBGE":str})
 t=t.merge(c[["CD_MUNICIPIO_IBGE","urbanizacao_2010","fracao_feminina_2010"]],
           on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
 assert t[["urbanizacao_2010","fracao_feminina_2010"]].notna().all().all()
 geo=pd.get_dummies(pd.Categorical(t.SG_UF.map(g.uf_region),
             categories=["S","SE","CO","NE","N"]),drop_first=True,dtype=float).to_numpy()
 output=[]
 for mode in ("censo2000_anterior","censo2010_contemporaneo"):
  f=["log_pop_previa"]+(
    ["urbanizacao_censo_vigente","fracao_feminina_censo_vigente"] if mode=="censo2000_anterior"
    else ["urbanizacao_2010","fracao_feminina_2010"])
  x=t[f].to_numpy(float)
  b=np.column_stack([x,geo])
  neighbors=g.sp.knn(t,8)
  wx=x[neighbors].mean(axis=1)
  for desfecho,col in (("competitividade","competitividade_2t"),("direcao_pt13","margem_assinada_pt13")):
   y=t[col].to_numpy(float)
   for weight in ("uniforme","populacao_anterior"):
    w=np.ones(len(t)) if weight=="uniforme" else t.pop_previa.to_numpy(float)
    for fam in (["linear","logit_fracionario"] if desfecho=="competitividade" else ["linear"]):
     ret,ufs=g.cv_uf(t,b,wx,y,w,logit=fam=="logit_fracionario")
     arr=np.asarray([[r["sse_baseline"],r["sse_contexto"]] for r in ufs],float)
     rng=np.random.default_rng(2010*17+len(mode)+len(desfecho)+len(weight)+len(fam))
     sim=arr[rng.integers(0,27,size=(4999,27))].sum(axis=1)
     gains=100*(1-np.sqrt(sim[:,1]/sim[:,0]))
     output.append({"modelo_censo":mode,"ano":2010,"desfecho":desfecho,
       "ponderacao":weight,"familia":fam,"n_municipios":len(t),
       "ganho_rmse_pct":ret["reducao_rmse_pct"],
       "ic95_inf":float(np.quantile(gains,.025)),
       "ic95_sup":float(np.quantile(gains,.975))})
 result=pd.DataFrame(output)
 assert len(result)==12
 ref=pd.read_csv(a.referencia)
 prior=result[result.modelo_censo.eq("censo2000_anterior")]
 z=prior.merge(ref[(ref.ano==2010)],on=["ano","desfecho","ponderacao","familia"],suffixes=("_t","_ref"))
 assert len(z)==6
 assert (z.ganho_rmse_pct_t-z.ganho_rmse_pct_ref).abs().lt(1e-6).all(),z.to_string()
 a.out.mkdir(parents=True)
 result.to_csv(a.out/"sensibilidade_censo_2010_mesmo_ano.csv",index=False,float_format="%.10f")
 pivot=result.pivot_table(index=["ano","desfecho","ponderacao","familia"],columns="modelo_censo",values="ganho_rmse_pct").reset_index()
 pivot["delta_pontos_percentuais"]=pivot.censo2010_contemporaneo-pivot.censo2000_anterior
 pivot.to_csv(a.out/"contraste_2010_censos.csv",index=False,float_format="%.10f")
 meta={"ano":2010,"amostra":5506,
   "principal":"Censo 2000, estritamente anterior à eleição",
   "sensibilidade":"Censo 2010, simultâneo ao ano do pleito e potencialmente publicado depois",
   "nao_previsao_ex_ante":True,
   "notas":["Apenas 2010 alterado, 2014-2022 já adotam Censo 2010.","Diferença nos ganhos não é parâmetro causal.",
            "Valores 2010 com Censo 2010 devem ser reportados apenas como robustez retrospectiva."]}
 (a.out/"manifesto.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
 print(pivot.to_string(index=False))
if __name__=="__main__":main()
