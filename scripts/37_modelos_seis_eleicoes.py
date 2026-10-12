#!/usr/bin/env python3
"""Validação geográfica e temporal presidencial 2002–2022 (sem 1998).

Especificação A: seis pleitos, 3 controles locais + 4 macro; compara +WX3.
Especificação B: cinco pleitos (2006–2022), 4 controles + 4 macro; +WX4.
Mesma amostra de municípios em cada especificação; validação UF 5 folds
e testes temporais cronológicos com treino estritamente anterior.
Não pressupor interpretação causal ou previsão verdadeira em tempo real.
"""
import argparse,importlib.util,json,hashlib
from pathlib import Path
import numpy as np,pandas as pd
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("geov37",HERE/"22_benchmark_geografico_competitividade.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
YEARS3=(2002,2006,2010,2014,2018,2022)
YEARS4=(2006,2010,2014,2018,2022)
OUT={"competitividade":"competitividade_2t","direcao_pt13":"margem_assinada_pt13"}
MACRO=["S","SE","CO","NE","N"]

def get_panel(path,years,k):
 p=pd.read_csv(path,dtype={"CD_MUNICIPIO_IBGE":str,"SG_UF":str})
 if set(p.ano)!=set(years) or p.CD_MUNICIPIO_IBGE.nunique()*len(years)!=len(p):
  raise ValueError("Painel não balanceado no protocolo")
 feats=["log_pop","urbanizacao_censo","fracao_feminina_censo"]
 if k==4:feats.append("log_pibpc_proxy")
 assert p[feats+list(OUT.values())+["pop_antes"]].notna().all().all()
 data={};x={}
 for yr in years:
  d=p[p.ano.eq(yr)].sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
  assert len(d)==p.CD_MUNICIPIO_IBGE.nunique() and d.SG_UF.nunique()==27
  raw=d[feats].to_numpy(dtype=float)
  cats=pd.Categorical(d.SG_UF.map(g.uf_region),categories=MACRO)
  macro=pd.get_dummies(cats,drop_first=True,dtype=float).to_numpy()
  assert macro.shape==(len(d),4)
  n=g.sp.knn(d,8)
  neigh=raw[n].mean(axis=1)
  b=np.column_stack([raw,macro])
  x[yr]=(b,np.column_stack([b,neigh]),neigh)
  data[yr]=d
 return data,x,feats

def boot(ufs,seed):
 z=np.array([[r["weight_sum"],r["sse_local"],r["sse_contexto"]] for r in ufs],dtype=float)
 if len(z)!=27 or not (z[:,0]>0).all():raise ValueError("Há UF sem observações")
 rm0=np.sqrt(z[:,1].sum()/z[:,0].sum())
 rm1=np.sqrt(z[:,2].sum()/z[:,0].sum())
 rng=np.random.default_rng(seed)
 random=rng.integers(0,27,size=(4999,27))
 total=z[random].sum(axis=1)
 gain=100*(1-np.sqrt(total[:,2]/total[:,1]))
 return {"rmse_local":float(rm0),"rmse_contexto":float(rm1),
         "ganho_rmse_pct":float(100*(1-rm1/rm0)),
         "ic95_uf_inf":float(np.quantile(gain,.025)),
         "ic95_uf_sup":float(np.quantile(gain,.975)),
         "ufs_piora":int((z[:,2]>z[:,1]).sum())}

def temporal(d,x,training,target,outcome,weight,frac,seed):
 train=pd.concat([d[y] for y in training],ignore_index=True)
 test=d[target]
 baset=np.concatenate([x[y][0] for y in training],axis=0)
 ctxt=np.concatenate([x[y][1] for y in training],axis=0)
 basez,ctxz,_=x[target]
 ytr=train[OUT[outcome]].to_numpy(float);yte=test[OUT[outcome]].to_numpy(float)
 wtr=np.ones(len(train)) if weight=="uniforme" else train.pop_antes.to_numpy(float)
 wte=np.ones(len(test)) if weight=="uniforme" else test.pop_antes.to_numpy(float)
 p0=g.predict(baset,basez,ytr,wtr,logit=frac)
 p1=g.predict(ctxt,ctxz,ytr,wtr,logit=frac)
 u=test.SG_UF.to_numpy()
 per=[]
 for uf in sorted(set(u)):
  match=u==uf
  per.append({"UF":uf,"weight_sum":float(wte[match].sum()),
   "sse_local":float(np.sum(wte[match]*(yte[match]-p0[match])**2)),
   "sse_contexto":float(np.sum(wte[match]*(yte[match]-p1[match])**2))})
 return boot(per,seed),per

def calculate(root,key,path,years,k):
 d,x,features=get_panel(path,years,k)
 cross=[];times=[];ufs=[]
 for yr in years:
  a=d[yr];bx,cx,wx=x[yr]
  for outcome,col in OUT.items():
   y=a[col].to_numpy(float)
   for weight in ("uniforme","populacao_anterior"):
    w=np.ones(len(a)) if weight=="uniforme" else a.pop_antes.to_numpy(float)
    for frac in ((False,True) if outcome=="competitividade" else (False,)):
     fam="logit_fracionario" if frac else "linear"
     initial,part=g.cv_uf(a,bx,wx,y,w,logit=frac)
     records=[{"UF":r["UF"],"weight_sum":r["weight_sum"],
       "sse_local":r["sse_baseline"],"sse_contexto":r["sse_contexto"]} for r in part]
     metrics=boot(records,seed=20261012+yr*7+k*71+int(frac)*31+int(outcome=="direcao_pt13")*9+int(weight!="uniforme")*17)
     if abs(metrics["ganho_rmse_pct"]-initial["reducao_rmse_pct"])>1e-7:
      raise ValueError("Erro recomposição UF")
     cross.append({"amostra":key,"controles":k,"ano":yr,"desfecho":outcome,
      "ponderacao":weight,"familia":fam,"n":len(a),**metrics})
 # EXPANDING: usa todas as eleições anteriores para cada teste.
 # PREVIOUS: apenas o pleito imediatamente anterior.
 for j in range(1,len(years)):
  target=years[j]
  for tipo,training in (("anterior",[years[j-1]]),
                         ("acumulado",list(years[:j]))):
   for outcome in OUT:
    for weight in ("uniforme","populacao_anterior"):
     for frac in ((False,True) if outcome=="competitividade" else (False,)):
      fam="logit_fracionario" if frac else "linear"
      metrics,per=temporal(d,x,training,target,outcome,weight,frac,
         seed=20261012+target*9+k*41+j*13+int(frac)*47+int(outcome=="direcao_pt13")*23+int(weight!="uniforme")*31+(tipo=="acumulado")*51)
      case="+".join(map(str,training))+"=>"+str(target)
      times.append({"amostra":key,"controles":k,"tipo_treino":tipo,
       "anos_treino":"+".join(map(str,training)),"ano_teste":target,
       "caso":case,"desfecho":outcome,"ponderacao":weight,"familia":fam,
       "n_treino":len(training)*len(d[target]),"n_teste":len(d[target]),**metrics})
      ufs.extend([{"amostra":key,"controles":k,"tipo_treino":tipo,
                  "caso":case,"desfecho":outcome,"ponderacao":weight,"familia":fam,**r} for r in per])
 return pd.DataFrame(cross),pd.DataFrame(times),pd.DataFrame(ufs),len(d[years[0]])

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--panel3",required=True,type=Path)
 parser.add_argument("--panel4",required=True,type=Path)
 parser.add_argument("--out",required=True,type=Path)
 a=parser.parse_args()
 if a.out.exists() and any(a.out.iterdir()):
  raise SystemExit("Pasta anterior preservada")
 o3=calculate(a.out,"seis_eleicoes",a.panel3,YEARS3,3)
 o4=calculate(a.out,"cinco_eleicoes",a.panel4,YEARS4,4)
 geo=pd.concat([o3[0],o4[0]],ignore_index=True)
 temporal=pd.concat([o3[1],o4[1]],ignore_index=True)
 peruf=pd.concat([o3[2],o4[2]],ignore_index=True)
 # seis eleicoes 6*2*3=36; cinco eleicoes 5*2*3=30.
 if len(geo)!=66 or len(temporal)!=(5+4)*2*2*3 or len(peruf)!=len(temporal)*27:
  raise ValueError(f"Quantidade de resultados inesperada {len(geo)} {len(temporal)} {len(peruf)}")
 if (geo.ano==1998).any() or (temporal.ano_teste==1998).any():
  raise ValueError("1998 foi excluído")
 a.out.mkdir(parents=True)
 geo.to_csv(a.out/"validacao_geografica_6_e_5_eleicoes.csv",index=False,float_format="%.10f")
 temporal.to_csv(a.out/"validacao_temporal_2002_2022.csv",index=False,float_format="%.10f")
 peruf.to_csv(a.out/"erros_por_uf_validacao_temporal.csv",index=False,float_format="%.10f")
 m={"status":"ESTIMATIVAS_EXPLORATORIAS_SEM_SUBMISSAO",
    "anos_seis":list(YEARS3),"anos_cinco":list(YEARS4),
    "n_municipios_amostra_seis":o3[3],"n_municipios_amostra_cinco":o4[3],
    "n_cv_geo":len(geo),"n_cv_temporal":len(temporal),
    "regressores_3":["log_pop","urbanizacao_censo","fracao_feminina_censo"],
    "regressores_4":["log_pop","urbanizacao_censo","fracao_feminina_censo","log_pibpc_proxy"],
    "estimadores":["OLS/WLS","logit fracionario apenas C"],
    "tempo":"Treino: eleições anteriores ao teste, sem compartilhamento dos votos do futuro.",
    "censo":"Censo2000 para 2002/2006/2010, Censo2010 para 2014/2018/2022",
    "pontos_de_cuidado":[
      "Testes três e quatro controles têm amostras distintas; comparar mudanças somente em especificações e universos coincidentes.",
      "Dados IBGE foram recuperados em 2026, podem ter revisão temporal e não são previsões com dados disponíveis à época.",
      "Códigos TSE antigos mapeados à malha 2022 não tratam perfeitamente mudanças territoriais.",
      "2010 contém registros especiais VT; incluídos em total TSE histórico, excluídos do município.",
      "M define vantagem PT13 com candidatos distintos por ano.",
      "Bootstrap 4999 UFs, IC exploratório com correlação residual entre UFs fronteiriças.",
      "C e M diferem em escala e distribuição; não comparar RMSE bruto entre eles.",
      "Nenhuma identificação causal de contágio social ou preferência individual."],
    "codigo":"scripts/37_modelos_seis_eleicoes.py","fontes_painel":"outputs/painel_harmonizado_2002_2022_v01"}
 (a.out/"manifesto.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n")
 print("VALIDACAO GEOGRAFICA LINEAR PESOS IGUAIS")
 print(geo[(geo.familia=="linear")&(geo.ponderacao=="uniforme")][["amostra","ano","desfecho","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
 print("VALIDACAO TEMPORAL ACUMULADO LINEAR PESOS IGUAIS")
 print(temporal[(temporal.familia=="linear")&(temporal.ponderacao=="uniforme")&(temporal.tipo_treino=="acumulado")][["amostra","caso","desfecho","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
if __name__=="__main__":main()
