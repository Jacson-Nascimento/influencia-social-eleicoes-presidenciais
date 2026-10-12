#!/usr/bin/env python3
"""Painel histórico retrospectivo 2002–2022: comparação dos seis segundos turnos.

Exclui 1998: sem segundo turno e com arquivo de resultados incompleto segundo TSE.
2002,2006,2010: TSE nominal oficial; 2014/18/22: saídas anteriores versionadas.
Três covariáveis disponíveis pré-pleito em TODOS seis anos: log população,
urbanização Censo 2000 (até 2010), fração feminina Censo 2000; para
2014/18/22 os dois indicadores são Censo 2010. PIB omitido da análise
principal dos seis anos porque série uniforme anterior a 2002 não foi
recuperada. Não misturar com benchmark original de 4 covariáveis.

O contexto k=8 é média de covariáveis IBGE entre centroides IBGE2022.
UF holdout 5 dobras e treino progressivo por eleição anterior.
Resultados associativos e retrospectivos sem inferência causal ou
previsão eleitoral em tempo real.
"""
import argparse,importlib.util,json
from pathlib import Path
import numpy as np,pandas as pd

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("historico_benchmark",HERE/"22_benchmark_geografico_competitividade.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

YEARS=[2002,2006,2010,2014,2018,2022]
FINALISTS={2002:(13,45),2006:(13,45),2010:(13,45),2014:(13,45),2018:(13,17),2022:(13,22)}
COUNTS={2002:{13:52793364,45:33370739},2006:{13:58295042,45:37543178},2010:{13:55752529,45:43711388}}
FEATS=["log_pop","urbanizacao","fracao_feminina"]
KEY=["SG_UF","CD_MUNICIPIO"]
YCOL={"C":"competitividade_2t","M":"margem_assinada_pt13"}

def main():
    ap=argparse.ArgumentParser()
    for name in ("mapa","historico","ibge_historico","votos2014","ibge2014","votos2018_2022","ibge2018_2022","saida"):
        ap.add_argument("--"+name,required=True,type=Path)
    a=ap.parse_args()
    if a.saida.exists() and any(a.saida.iterdir()):raise SystemExit("Não alterar saídas existentes.")
    mapa=pd.read_csv(a.mapa,dtype={"SG_UF":str,"CD_MUNICIPIO":str,"CD_MUNICIPIO_IBGE":str})
    mapa.CD_MUNICIPIO=mapa.CD_MUNICIPIO.astype(int)
    assert len(mapa)==5570 and not mapa.duplicated(KEY).any()
    histibge=pd.read_csv(a.ibge_historico,dtype={"CD_MUNICIPIO_IBGE":str})
    ibge2014=pd.read_csv(a.ibge2014,dtype={"CD_MUNICIPIO_IBGE":str})
    ibge_new=pd.read_csv(a.ibge2018_2022,dtype={"CD_MUNICIPIO_IBGE":str})
    votes2014=pd.read_csv(a.votos2014,dtype={"SG_UF":str,"CD_MUNICIPIO_IBGE":str})
    votes2014.CD_MUNICIPIO=votes2014.CD_MUNICIPIO.astype(int)
    votes_new=pd.read_csv(a.votos2018_2022,dtype={"SG_UF":str})
    votes_new.CD_MUNICIPIO=votes_new.CD_MUNICIPIO.astype(int)
    data=[];integ=[]
    for year in YEARS:
        if year in (2002,2006,2010):
            f=a.historico/str(year)/f"votos_presidenciais_municipais_{year}.csv"
            v=pd.read_csv(f,dtype={"SG_UF":str})
            t2=v[v.NR_TURNO.eq(2)].copy()
            counts={int(k):int(val) for k,val in t2.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum().items()}
            if counts!=COUNTS[year]:raise ValueError(f"2010/2006/2002 votos fora dos totais conhecidos {year}: {counts}")
            specials=t2.loc[~t2.SG_UF.isin(mapa.SG_UF.unique()),:]
            domestic=t2.loc[t2.SG_UF.isin(mapa.SG_UF.unique())].copy()
            domestic.CD_MUNICIPIO=domestic.CD_MUNICIPIO.astype(int)
            codes=set(domestic.NR_CANDIDATO.unique())
            if codes!={13,45}:raise ValueError("Finalistas incoerentes")
            p=domestic.pivot(index=KEY,columns="NR_CANDIDATO",values="QT_VOTOS_NOMINAIS")
            if p[[13,45]].isna().any().any():raise ValueError("Candidato ausente")
            p=p.reset_index()
            m=p.merge(mapa,on=KEY,how="left",validate="one_to_one",indicator=True)
            notmapped=m[m._merge!="both"]
            m=m[m._merge=="both"].drop(columns=["_merge"]).copy()
            if year==2002:
                pop="pop_2001"
            elif year==2006:pop="pop_2005"
            else:pop="pop_2009"
            m=m.merge(histibge[["CD_MUNICIPIO_IBGE",pop,"urbanizacao_2000","fracao_feminina_2000"]],on="CD_MUNICIPIO_IBGE",validate="one_to_one",how="left")
            m["pop_antes"]=m[pop]
            m["urbanizacao"]=m.urbanizacao_2000
            m["fracao_feminina"]=m.fracao_feminina_2000
            m["votos_pt13"]=m[13]
            m["votos_oponente"]=m[45]
            integ.append({"ano":year,"soma_nacional":int(t2.QT_VOTOS_NOMINAIS.sum()),"total_nacional_de_referencia":sum(COUNTS[year].values()),
                 "votos_nao_municipais_ZZ_VT":int(specials.QT_VOTOS_NOMINAIS.sum()),
                 "municipios_territoriais":len(p),"municipios_associados_mapa2022":len(m),
                 "municipios_nao_associados":int(len(notmapped)),
                 "chaves_nao_associadas":notmapped[KEY].to_dict("records")[:35]})
        elif year==2014:
            m=votes2014.merge(ibge2014[["CD_MUNICIPIO_IBGE","pop_2013","urbanizacao_2010","fracao_feminina_2010"]],on="CD_MUNICIPIO_IBGE",validate="one_to_one",how="left")
            m["pop_antes"]=m.pop_2013
            m["urbanizacao"]=m.urbanizacao_2010;m["fracao_feminina"]=m.fracao_feminina_2010
            integ.append({"ano":year,"municipios_territoriais":len(m),"municipios_associados_mapa2022":len(m),
                 "municipios_nao_associados":0})
        else:
            m=votes_new[votes_new.ano.eq(year)].merge(mapa,on=KEY,validate="one_to_one",how="left")
            m=m.merge(ibge_new,on="CD_MUNICIPIO_IBGE",validate="one_to_one",how="left")
            pop="pop_2017" if year==2018 else "pop_2021"
            m["pop_antes"]=m[pop]
            m["urbanizacao"]=m.urbanizacao_2010
            m["fracao_feminina"]=m.fracao_feminina_2010
            integ.append({"ano":year,"municipios_territoriais":len(m),"municipios_associados_mapa2022":len(m),
                 "municipios_nao_associados":0})
        m["log_pop"]=np.log(m.pop_antes.where(m.pop_antes>0))
        m["total_validos"]=m.votos_pt13+m.votos_oponente
        m["competitividade_2t"]=1-(m.votos_pt13-m.votos_oponente).abs()/m.total_validos
        m["margem_assinada_pt13"]=(m.votos_pt13-m.votos_oponente)/m.total_validos
        if m.total_validos.le(0).any():raise ValueError("Município sem votos")
        if not m.competitividade_2t.between(0,1).all():raise ValueError("C fora dos limites")
        if not np.allclose(m.competitividade_2t,1-abs(m.margem_assinada_pt13)):
            raise ValueError("C != 1-|M|")
        m["ano"]=year
        columns=["ano","SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE","latitude","longitude","pop_antes"]+FEATS+list(YCOL.values())
        data.append(m[columns])
    panel=pd.concat(data,ignore_index=True)
    if panel.duplicated(["ano","CD_MUNICIPIO_IBGE"]).any():raise ValueError("Geocódigos duplicados")
    valid=panel[["pop_antes","latitude","longitude"]+FEATS+list(YCOL.values())].notna().all(axis=1)
    common=panel.loc[valid].groupby("CD_MUNICIPIO_IBGE").ano.nunique()
    ids=sorted(common[common==6].index)
    if len(ids)<5400:raise ValueError("Amostra municipal comum pequena: "+str(len(ids)))
    d=panel.loc[panel.CD_MUNICIPIO_IBGE.isin(ids)].copy()
    if len(d)!=len(ids)*6:raise ValueError("Painel não balanceado")
    frames={};features={}
    for year in YEARS:
        x=d[d.ano.eq(year)].copy().sort_values(KEY).reset_index(drop=True)
        if len(x)!=len(ids) or x.SG_UF.nunique()!=27:raise ValueError("Amostra por pleito")
        r=x.SG_UF.map(g.uf_region)
        cats=pd.Categorical(r,categories=["S","SE","CO","NE","N"])
        region=pd.get_dummies(cats,drop_first=True,dtype=float).to_numpy()
        local=x[FEATS].to_numpy(dtype=float)
        k=g.sp.knn(x,8)
        context=local[k].mean(axis=1)
        base=np.column_stack([local,region])
        frames[year]=x;features[year]=(base,np.column_stack([base,context]),context)

    def boot(recs,seed):
        vals=np.array([[z["weight_sum"],z["sse_baseline"],z["sse_contexto"]] for z in recs],dtype=float)
        if len(vals)!=27:raise ValueError("27 UFs obrigatórias")
        a=np.sqrt(vals[:,1].sum()/vals[:,0].sum());b=np.sqrt(vals[:,2].sum()/vals[:,0].sum())
        rng=np.random.default_rng(seed)
        sample=rng.integers(0,27,size=(4999,27))
        sums=vals[sample].sum(axis=1)
        gains=100*(1-np.sqrt(sums[:,2]/sums[:,1]))
        return {"rmse_local":float(a),"rmse_contextual":float(b),"ganho_rmse_pct":float(100*(1-b/a)),
                "ic95_uf_inf":float(np.quantile(gains,.025)),"ic95_uf_sup":float(np.quantile(gains,.975)),
                "ufs_piora":int(np.sum(vals[:,2]>vals[:,1]))}

    geo=[];temporal=[];sse_temporal=[];profiles=[]
    for year in YEARS:
        x=frames[year];base,full,context=features[year]
        profiles.append({"ano":year,"n_municipios":len(x),
          "media_competitividade_municipios":float(x.competitividade_2t.mean()),
          "media_margem_assinada_municipios":float(x.margem_assinada_pt13.mean()),
          "fracao_municipios_vantagem_pt13":float((x.margem_assinada_pt13>0).mean())})
        for outcome,col in YCOL.items():
            y=x[col].to_numpy(float)
            for weight in ("uniforme","populacao_anterior"):
                w=np.ones(len(x)) if weight=="uniforme" else x.pop_antes.to_numpy(float)
                for family in (["linear","logit_fracionario"] if outcome=="C" else ["linear"]):
                    logit=(family=="logit_fracionario")
                    fitted,uf_rows=g.cv_uf(x,base,context,y,w,logit=logit)
                    rows=[{"weight_sum":z["weight_sum"],"sse_baseline":z["sse_baseline"],"sse_contexto":z["sse_contexto"]} for z in uf_rows]
                    res=boot(rows,20261012+year*29+(outcome=="M")*7+(weight=="populacao_anterior")*5+int(logit))
                    if abs(res["ganho_rmse_pct"]-fitted["reducao_rmse_pct"])>1e-7:raise ValueError("CV UF inconsistente")
                    geo.append({"ano":year,"desfecho":outcome,"ponderacao":weight,"familia":family,"n":len(x),**res})
    # Somente treino com eleições ANTERIORES ao teste, sem usar votos futuros.
    scenarios=[]
    for j in range(1,len(YEARS)):
        scenarios.append(([YEARS[j-1]],YEARS[j],"anterior"))
        scenarios.append((YEARS[:j],YEARS[j],"expansivo"))
    seen=set()
    for tryears,testyear,strategy in scenarios:
        key=(tuple(tryears),testyear)
        if key in seen:continue
        seen.add(key)
        train=pd.concat([frames[year] for year in tryears],ignore_index=True)
        xtrain=np.concatenate([features[y][0] for y in tryears])
        ftrain=np.concatenate([features[y][1] for y in tryears])
        test=frames[testyear];bt,ft,_=features[testyear]
        for outcome,col in YCOL.items():
            for weight in ("uniforme","populacao_anterior"):
                wt=np.ones(len(train)) if weight=="uniforme" else train.pop_antes.to_numpy(float)
                wte=np.ones(len(test)) if weight=="uniforme" else test.pop_antes.to_numpy(float)
                for family in (["linear","logit_fracionario"] if outcome=="C" else ["linear"]):
                    logit=family=="logit_fracionario"
                    pred0=g.predict(xtrain,bt,train[col].to_numpy(float),wt,logit=logit)
                    pred1=g.predict(ftrain,ft,train[col].to_numpy(float),wt,logit=logit)
                    yte=test[col].to_numpy(float)
                    records=[]
                    for uf in sorted(test.SG_UF.unique()):
                        mask=test.SG_UF.eq(uf).to_numpy()
                        records.append({"UF":uf,"weight_sum":float(wte[mask].sum()),
                          "sse_baseline":float(np.sum(wte[mask]*(yte[mask]-pred0[mask])**2)),
                          "sse_contexto":float(np.sum(wte[mask]*(yte[mask]-pred1[mask])**2))})
                    case="+".join(map(str,tryears))+"=>"+str(testyear)
                    res=boot(records,20261012+testyear*37+len(tryears)*8+(outcome=="M")*4+(weight=="populacao_anterior")*2+int(logit))
                    temporal.append({"caso":case,"treino_anos":"+".join(map(str,tryears)),"teste_ano":testyear,
                       "estrategia":strategy,"desfecho":outcome,"ponderacao":weight,
                       "familia":family,"n_treino":len(train),"n_teste":len(test),**res})
                    sse_temporal.extend([{**{"caso":case,"desfecho":outcome,"ponderacao":weight,"familia":family},**z} for z in records])
    out=a.saida
    out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(geo).to_csv(out/"validacao_uf_seis_eleicoes.csv",index=False,float_format="%.10f")
    pd.DataFrame(temporal).to_csv(out/"validacao_temporal_seis_eleicoes.csv",index=False,float_format="%.10f")
    pd.DataFrame(sse_temporal).to_csv(out/"sse_por_uf_temporal.csv",index=False,float_format="%.10f")
    pd.DataFrame(profiles).to_csv(out/"perfil_seis_eleicoes.csv",index=False,float_format="%.10f")
    manifest={"status":"EXPLORATORIO_NAO_SUBMETIDO","autor":"Jacson Cruz do Nascimento",
      "anos":YEARS,"municipios_amostra_comum":len(ids),"observacoes":len(d),
      "controles_comuns":["log população prévia","urbanização Censo2000 antes 2014, Censo2010 depois","fração feminina Censo2000 antes 2014, Censo2010 depois"],
      "pib":"EXCLUIDO DO BENCHMARK COMUM DE SEIS ELEICOES porque indisponivel 2000 SIDRA 5938",
      "ano_censo_2002_2010":2000,"ano_censo_2014_2022":2010,
      "vizinhos":"oito centroides municipais IBGE2022, mudancas territoriais anteriores requerem cautela",
      "1998":"EXCLUIDO: sem segundo turno e fonte TSE incompleta",
      "validacao":"5 folds UF inteiras omitidas e treino temporal em anos anteriores, bootstrap 4999 UFs",
      "historicos_TSE_nacional":integ,
      "alertas":["Diferenças de amostra e regressoras impedem comparar numericamente novos RMSE com v14/v15 sem refazer modelos na amostra nova.",
                "Macroregioes constantes; covariaveis demograficas Censo2000/Censo2010 mudam de vintage a partir 2014.",
                "O efeito de transferir parametros entre pleitos não é causal, e a leitura dos votos do PT não indica voto individual em partido.",
                "IBGE baixado em 2026 com eventuais revisoes a posteriori; não é previsao em tempo real.",
                "1998 excluido, sem segundo turno e TSE reconhece incompletude.",
                "Centroides de 2022 nao sao geometria historica.",
                "UFs vizinhas podem ser dependentes; ICs percentis exploratorios."]}
    (out/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print("\n--- AMOSTRA ---",len(ids),len(d),int(pd.DataFrame(geo).shape[0]),int(pd.DataFrame(temporal).shape[0]))
    print("\n--- UF PESOS IGUAIS OLS ---")
    print(pd.DataFrame(geo).query("ponderacao=='uniforme' and familia=='linear'")[["ano","desfecho","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
    print("\n--- TEMPORAL PESOS IGUAIS OLS ---")
    print(pd.DataFrame(temporal).query("ponderacao=='uniforme' and familia=='linear'")[["caso","desfecho","ganho_rmse_pct","ic95_uf_inf","ic95_uf_sup"]].to_string(index=False))
if __name__=="__main__":main()
