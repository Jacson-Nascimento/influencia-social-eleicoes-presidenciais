#!/usr/bin/env python3
"""Sensibilidade Censo 2000 congelado em todos os seis pleitos 2002-2022.

O protocolo principal usa último Censo anterior (2000 até 2010;
2010 desde 2014). Este teste mantém composição demográfica do Censo
2000 fixa, sem mexer na população/PIB anuais, para avaliar se a quebra
de mensuração censitária explica parte da instabilidade dos modelos.

Este congelamento é apenas diagnóstico: a composição de 2000 não é
uma descrição atual de 2022. Nenhuma série posterior à eleição entra
nos regressores de um teste temporal.
"""
import argparse,importlib.util,json
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location("est37",(HERE/"37_modelos_seis_eleicoes.py"))
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for nm in ("panel3","ibge2000","base_geo","base_temporal","out"):
  ap.add_argument("--"+nm,type=Path,required=True)
 a=ap.parse_args()
 if a.out.exists() and any(a.out.iterdir()): raise SystemExit("Preservar outputs anteriores")
 d=pd.read_csv(a.panel3,dtype={"CD_MUNICIPIO_IBGE":str})
 controls=pd.read_csv(a.ibge2000,dtype={"CD_MUNICIPIO_IBGE":str})
 assert len(d)==33036 and d.CD_MUNICIPIO_IBGE.nunique()==5506
 keep=controls[["CD_MUNICIPIO_IBGE","urbanizacao_2000","fracao_feminina_2000"]]
 p=d.merge(keep,on="CD_MUNICIPIO_IBGE",validate="many_to_one")
 if p[["urbanizacao_2000","fracao_feminina_2000"]].isna().any().any():
  raise ValueError("Ausência de demografia histórica")
 p["urbanizacao_censo"]=p.urbanizacao_2000
 p["fracao_feminina_censo"]=p.fracao_feminina_2000
 p=p.drop(columns=["urbanizacao_2000","fracao_feminina_2000"])
 assert len(p)==33036 and p.ano.nunique()==6
 a.out.mkdir(parents=True)
 p.to_csv(a.out/"painel_6_eleicoes_censo2000_congelado.csv",index=False,float_format="%.12f")
 geo,time,ufs,n=m.calculate(a.out,"seis_eleicoes_censo2000_fixo",a.out/"painel_6_eleicoes_censo2000_congelado.csv",m.YEARS3,3)
 original_geo=pd.read_csv(a.base_geo)
 original_geo=original_geo[original_geo.amostra.eq("seis_eleicoes")]
 original_tem=pd.read_csv(a.base_temporal)
 original_tem=original_tem[original_tem.amostra.eq("seis_eleicoes")]
 geo=geo.merge(original_geo[["ano","desfecho","ponderacao","familia","ganho_rmse_pct"]],
   on=["ano","desfecho","ponderacao","familia"],suffixes=("","_censo_por_periodo"),validate="one_to_one")
 time=time.merge(original_tem[["tipo_treino","anos_treino","ano_teste","desfecho","ponderacao","familia","ganho_rmse_pct"]],
   on=["tipo_treino","anos_treino","ano_teste","desfecho","ponderacao","familia"],
   suffixes=("","_censo_por_periodo"),validate="one_to_one")
 for tab in (geo,time):
  tab["delta_ganho_congelar_censo_pp"]=tab.ganho_rmse_pct-tab.ganho_rmse_pct_censo_por_periodo
 old=geo[geo.ano.le(2010)]
 if old.delta_ganho_congelar_censo_pp.abs().max()>1e-8:
  raise ValueError("Os modelos 2002/2006/2010 não deveriam mudar!")
 assert len(geo)==36 and len(time)==60 and len(ufs)==1620
 geo.to_csv(a.out/"comparacao_geografica_censo_fixo_vs_anterior.csv",index=False,float_format="%.10f")
 time.to_csv(a.out/"comparacao_temporal_censo_fixo_vs_anterior.csv",index=False,float_format="%.10f")
 info={"metodo":"Contrafactual descritivo com composição demográfica de 2000 fixa para todos os pleitos",
     "amostra_municipios":5506,"anos":[2002,2006,2010,2014,2018,2022],
     "controles":"log_pop_variavel_no_tempo, urbanizacao_Censo2000 fixa, fracao_feminina_Censo2000 fixa",
     "censo_2010_deslocado_para_apos_2022":"não, somente cenário de congelamento 2000",
     "inferencias":["Comparação de sensibilidade de mensuração censitária, não previsão real nem causalidade.",
       "Uso da composição de 2000 em eleições posteriores é defasagem deliberada e potencialmente imprecisa.",
       "Diferenças de ganho percentual não são testes pareados formais da significância da troca de Censo."],
     "principal":"outputs/modelos_seis_eleicoes_2002_2022_v01",
     "teste_auditoria":"Modelos 2002/2006/2010 preservam resultados exatamente (mesmo Censo2000)"}
 (a.out/"manifesto.json").write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n")
 print(time[(time.tipo_treino=="acumulado")&(time.familia=="linear")&(time.ponderacao=="uniforme")][
   ["caso","desfecho","ganho_rmse_pct","ganho_rmse_pct_censo_por_periodo","delta_ganho_congelar_censo_pp"]].to_string(index=False))
if __name__=="__main__":main()
