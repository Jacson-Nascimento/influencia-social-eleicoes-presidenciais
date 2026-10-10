#!/usr/bin/env python3
"""Robustez: ponderação populacional anterior e influência de capitais/grandes municípios.

Indicadores de segundo turno calculados em bases públicas do TSE.
Populações IBGE: 2017 para 2018, 2021 para 2022 (versões obtidas em 2026).
Não há identificação causal, previsão temporal ou transferência individual de voto.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
import math
import unicodedata
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
def load(mod,p):
    s=importlib.util.spec_from_file_location(mod,HERE/p)
    x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x

base=load("base_comp","16_modelos_competitividade.py")
space=load("espacial_comp","10_espacial_municipal.py")
weight=load("ponderacao_comp","17_sensibilidade_ponderacao_eleitoral.py")
soc=load("socio_comp","13_modelos_controles_socioeconomicos.py")

CAPITAIS={
"AC":"Rio Branco","AL":"Maceió","AP":"Macapá","AM":"Manaus",
"BA":"Salvador","CE":"Fortaleza","DF":"Brasília","ES":"Vitória",
"GO":"Goiânia","MA":"São Luís","MT":"Cuiabá","MS":"Campo Grande",
"MG":"Belo Horizonte","PA":"Belém","PB":"João Pessoa","PR":"Curitiba",
"PE":"Recife","PI":"Teresina","RJ":"Rio de Janeiro","RN":"Natal",
"RS":"Porto Alegre","RO":"Porto Velho","RR":"Boa Vista","SC":"Florianópolis",
"SP":"São Paulo","SE":"Aracaju","TO":"Palmas"}


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD",str(s).upper())
                   if unicodedata.category(c)!="Mn").strip()


def capitais_do_ibge(blob):
    all_municipios=json.loads(blob)
    if not isinstance(all_municipios,list) or len(all_municipios)<5500:
        raise ValueError("Catálogo municipal IBGE incompleto.")
    capital_names={k:norm(v) for k,v in CAPITAIS.items()}
    municipios=[]
    match=[]
    for d in all_municipios:
        uf=d.get("microrregiao",{}).get("mesorregiao",{}).get("UF",{}).get("sigla")
        if uf is None:
            uf=d.get("regiao-imediata",{}).get("regiao-intermediaria",{}).get("UF",{}).get("sigla")
        if not uf: raise ValueError("UF não resolvida na resposta IBGE.")
        name=d["nome"]
        code=str(d["id"])
        municipios.append(code)
        if capital_names.get(uf)==norm(name):
            match.append({"SG_UF":uf,"CD_MUNICIPIO_IBGE":code,"nome_ibge":name})
    if len(set(municipios))!=len(municipios):
        raise ValueError("Códigos duplicados na API de localidades IBGE.")
    caps=pd.DataFrame(match)
    if len(caps)!=27 or set(caps.SG_UF)!=set(CAPITAIS) or caps.CD_MUNICIPIO_IBGE.duplicated().any():
        raise ValueError("Inconsistência na identificação oficial das 27 capitais: "+caps.to_json(orient="records"))
    if not caps.CD_MUNICIPIO_IBGE.str.fullmatch(r"\d{7}").all():
        raise ValueError("Código IBGE de capital inválido.")
    return caps.sort_values("SG_UF").reset_index(drop=True)


def amostras(d,ano,cod_capitais):
    pop="pop_2017" if ano==2018 else "pop_2021"
    if not d[pop].gt(0).all():raise ValueError("População observada ausente ou inválida.")
    ordered=d.sort_values(pop,ascending=False)
    n=len(d)
    top1=set(ordered.head(math.ceil(n*.01)).CD_MUNICIPIO_IBGE.astype(str))
    top5=set(ordered.head(math.ceil(n*.05)).CD_MUNICIPIO_IBGE.astype(str))
    cases={
       "todos":d.copy(),
       "sem_capitais":d.loc[~d.CD_MUNICIPIO_IBGE.astype(str).isin(cod_capitais)].copy(),
       "sem_1pct_maiores":d.loc[~d.CD_MUNICIPIO_IBGE.astype(str).isin(top1)].copy(),
       "sem_5pct_maiores":d.loc[~d.CD_MUNICIPIO_IBGE.astype(str).isin(top5)].copy()}
    for label,x in cases.items():
        if len(x)<5000 or x.CD_MUNICIPIO_IBGE.duplicated().any():
            raise ValueError("Amostra inválida após exclusões: "+label)
        if x.SG_UF.nunique()<26:
            raise ValueError("Amostra excluiu inesperadamente mais de uma UF: "+label)
    return cases,{"top1_excluidos":len(top1),"top5_excluidos":len(top5),
                  "n_capitais_amostra":len(d)-len(cases["sem_capitais"])}


def design(d,xx,lag):
    uf=pd.get_dummies(d.SG_UF,drop_first=True,dtype=float).to_numpy()
    fix=np.c_[np.ones(len(d)),uf]
    z=np.column_stack([xx,lag])
    z0=(xx-xx.mean(axis=0))/xx.std(axis=0)
    z1=(z-z.mean(axis=0))/z.std(axis=0)
    return np.c_[fix,z0],np.c_[fix,z1]


def validacao_uf(d,xx,lag,y,weights):
    siglas=np.sort(d.SG_UF.unique())
    groups=d.SG_UF.to_numpy()
    full=np.column_stack([xx,lag])
    entries=[]
    for k in range(5):
        test=np.isin(groups,siglas[k::5])
        train=~test
        if test.sum()<10 or train.sum()<100:raise ValueError("Fold inválido.")
        x0=weight.padronizar(xx,train)
        x1=weight.padronizar(full,train)
        b0=weight.wls(np.c_[np.ones(train.sum()),x0[train]],y[train],weights[train])["beta"]
        b1=weight.wls(np.c_[np.ones(train.sum()),x1[train]],y[train],weights[train])["beta"]
        p0=np.c_[np.ones(test.sum()),x0[test]]@b0
        p1=np.c_[np.ones(test.sum()),x1[test]]@b1
        entries.append({"fold":k+1,"ufs_teste":siglas[k::5].tolist(),
                        "n_municipios":int(test.sum()),
                        "peso_total":float(weights[test].sum()),
                        "sse_local":float(np.sum(weights[test]*(y[test]-p0)**2)),
                        "sse_contexto":float(np.sum(weights[test]*(y[test]-p1)**2))})
    total=sum(q["peso_total"] for q in entries)
    rmse0=math.sqrt(sum(q["sse_local"] for q in entries)/total)
    rmse1=math.sqrt(sum(q["sse_contexto"] for q in entries)/total)
    return {"rmse_local":rmse0,"rmse_contexto":rmse1,
            "ganho_rmse_pct":100*(rmse0-rmse1)/rmse0,
            "dobras_com_piora":sum(q["sse_contexto"]>q["sse_local"] for q in entries),
            "dobras":entries}


def rodar(base_frame,caps):
    records=[];detail=[];samples=[]
    capset=set(caps.CD_MUNICIPIO_IBGE.astype(str))
    for ano in (2018,2022):
        year=soc.especificacao_modelo(base_frame[base_frame.ano==ano],ano)
        year=year.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
        cases,ncount=amostras(year,ano,capset)
        for label,d in cases.items():
            d=d.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
            size=len(d)
            pop=d["pop_2017" if ano==2018 else "pop_2021"].to_numpy(dtype=float)
            if not np.isfinite(pop).all():raise ValueError("Peso populacional não finito.")
            neighbors=space.knn(d,8)
            x=d[soc.COVARS].to_numpy(dtype=float)
            lag=x[neighbors].mean(axis=1)
            X0,X1=design(d,x,lag)
            samples.append({"ano":ano,"amostra":label,"n":size,"ufs":int(d.SG_UF.nunique()),
                            "pop_total":int(pop.sum()),"top1_excluidos":ncount["top1_excluidos"],
                            "top5_excluidos":ncount["top5_excluidos"],
                            "n_capitais_amostra_cheia":ncount["n_capitais_amostra"]})
            for outcome,col in base.OUTCOMES.items():
                y=d[col].to_numpy(dtype=float)
                for scheme in ("igual","populacao_anterior"):
                    w=np.ones(size) if scheme=="igual" else pop
                    mod0=weight.wls(X0,y,w)
                    mod1=weight.wls(X1,y,w)
                    cv=validacao_uf(d,x,lag,y,w)
                    row={"ano":ano,"desfecho":outcome,"amostra":label,"peso":scheme,
                         "k":8,"n":size,"ufs":int(d.SG_UF.nunique()),
                         "populacao_soma_estimada":int(pop.sum()),
                         "r2_local":mod0["r2_ponderado"],
                         "r2_contexto":mod1["r2_ponderado"],
                         "incremento_r2":mod1["r2_ponderado"]-mod0["r2_ponderado"],
                         "rmse_cv_local":cv["rmse_local"],"rmse_cv_contexto":cv["rmse_contexto"],
                         "ganho_rmse_cv_pct":cv["ganho_rmse_pct"],
                         "dobras_com_piora":cv["dobras_com_piora"]}
                    records.append(row)
                    detail.append({**{z:row[z] for z in ("ano","desfecho","amostra","peso")},"cv":cv})
    return pd.DataFrame(records),pd.DataFrame(samples),detail


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for n in ("mapa","hhi","ibge","competitividade","municipios_ibge_json","pasta"):
        ap.add_argument("--"+n.replace("_","-"),type=Path,required=True)
    a=ap.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):
        raise SystemExit("Diretório de saída existe; versão anterior preservada.")
    blob=a.municipios_ibge_json.read_bytes()
    capitals=capitais_do_ibge(blob)
    panel,excluded=base.preparar(a.mapa,a.hhi,a.ibge,a.competitividade)
    model,samples,folds=rodar(panel,capitals)
    a.pasta.mkdir(parents=True,exist_ok=True)
    model.to_csv(a.pasta/"robustez_pesos_populacao_e_grandes_cidades.csv",index=False,float_format="%.10f")
    samples.to_csv(a.pasta/"amostras_e_exclusoes.csv",index=False)
    capitals.to_csv(a.pasta/"capitais_identificadas_ibge.csv",index=False)
    (a.pasta/"validacao_uf_detalhada.json").write_text(json.dumps(folds,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest={"consulta_municipios":"https://servicodados.ibge.gov.br/api/v1/localidades/municipios",
              "sha256_catalogo_ibge":hashlib.sha256(blob).hexdigest(),
              "n_capitais_verificadas":len(capitals),"n_especificacoes":len(model),
              "anos":[2018,2022],"pesos":{"2018":"IBGE estimativa de população de 2017, consultada em 2026",
                                           "2022":"IBGE estimativa de população de 2021, consultada em 2026"},
              "cenarios":["todos","sem_capitais","sem_1pct_maiores","sem_5pct_maiores"],
              "efeito_exclusao":"Vizinhança espacial k=8 recalculada após cada restrição da amostra.",
              "limites":["Comparação retrospectiva por UF, sem previsibilidade eleitoral ex ante.",
                         "Fonte IBGE foi acessada em 2026 e pode conter revisões.",
                         "Ponderação populacional não se confunde com total de votos válidos.",
                         "Efeitos fixos de UF incluídos apenas nos ajustes in-sample, não na CV de UFs excluídas.",
                         "As exclusões alteram amostra e vizinhança; interpretar como teste de sensibilidade, não estimativas causais.",
                         "DF deixa de integrar a amostra ao excluir a capital única.",
                         "Cinco municípios sem Censo 2010 completo já excluídos em todas as análises."]}
    (a.pasta/"manifesto.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(model.to_string(index=False))
    print(json.dumps(manifest,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
