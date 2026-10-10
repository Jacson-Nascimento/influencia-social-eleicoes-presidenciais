#!/usr/bin/env python3
"""Regressões de competitividade no 2º turno e sensibilidade de direção do voto.

Estimativas associativas, sem previsão eleitoral e sem inferência individual.
Preserva versões HHI e usa fontes eleitorais/IBGE públicas já auditadas.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent

def load(name,filename):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

m=load("municipal_comp","10_espacial_municipal.py")
s=load("ols_comp","13_modelos_controles_socioeconomicos.py")
c=load("context_comp","14_comparacao_contexto_espacial.py")

OUTCOMES = {"competitividade":"competitividade_2t",
            "direcao_pt13":"margem_assinada_pt13"}


def preparar(mapa,hhi,ibge,compet):
    base,excluidos,sem_chave=s.preparar(mapa,hhi,ibge)
    base=base[base.NR_TURNO.eq(2)].copy()
    v=pd.read_csv(compet,dtype={"SG_UF":str})
    keys=["ano","SG_UF","CD_MUNICIPIO"]
    if v.duplicated(keys).any() or len(v)!=11140:
        raise ValueError("Indicadores segundo turno duplicados ou incompletos.")
    if set(v.ano.unique())!={2018,2022}:
        raise ValueError("Faltam eleições.")
    base=base.merge(v[keys+list(OUTCOMES.values())+["total_validos","votos_pt13","votos_oponente"]],
                    on=keys,how="left",validate="one_to_one")
    if len(base)!=11130 or base[list(OUTCOMES.values())].isna().any().any():
        raise ValueError("Junção de competitividade/controles perdeu linhas.")
    if not np.allclose(base.competitividade_2t,1-np.abs(base.margem_assinada_pt13)):
        raise ValueError("Identidade de competitividade incorreta.")
    if len(excluidos)!=5 or sem_chave:
        raise ValueError("Amostra alterada em relação à auditoria IBGE v02.")
    return base,excluidos


def regress(x,y,ufs):
    uf=pd.get_dummies(ufs,drop_first=True,dtype=float).to_numpy()
    fixed=np.c_[np.ones(len(y)),uf]
    mx=x.mean(axis=0);sd=x.std(axis=0)
    if (sd<=0).any():raise ValueError("Atributos sem variação")
    X=np.c_[fixed,(x-mx)/sd]
    return s.fit(X,y)


def comparar(base,reps=999):
    linhas=[];folds=[]
    for ano in (2018,2022):
        frame=s.especificacao_modelo(base.loc[base.ano.eq(ano)].copy(),ano)
        frame=frame.sort_values(["SG_UF","CD_MUNICIPIO"]).reset_index(drop=True)
        if len(frame)!=5565: raise ValueError("Cobertura da amostra diferente de 5.565.")
        nn={k:m.knn(frame,k) for k in (4,8,12)}
        xx=frame[s.COVARS].to_numpy(dtype=float)
        ufs=frame.SG_UF.to_numpy()
        for key,col in OUTCOMES.items():
            y=frame[col].to_numpy(dtype=float)
            for k in (4,8,12):
                lag=xx[nn[k]].mean(axis=1)
                model0=regress(xx,y,frame.SG_UF)
                model1=regress(np.column_stack([xx,lag]),y,frame.SG_UF)
                # cv com a MESMA observação e divisão, SEM efeito UF (UF inteira no teste).
                work=frame.copy()
                work["hhi"]=y
                v=c.crossval_uf(work,xx,lag)
                linha={"ano":ano,"desfecho":key,"k":k,"n":len(y),
                    "r2_local_uf":float(model0["r2"]),
                    "r2_local_contexto_uf":float(model1["r2"]),
                    "delta_r2":float(model1["r2"]-model0["r2"]),
                    "moran_residuo_local":float(m.moran(model0["resid"],nn[k])),
                    "moran_residuo_contexto":float(m.moran(model1["resid"],nn[k])),
                    "rmse_cv_local":v["rmse_controles_locais"],
                    "rmse_cv_contexto":v["rmse_controles_mais_contexto"],
                    "reducao_rmse_cv_pct":v["mudanca_relativa_rmse_pct"],
                    "dobras_com_piora":v["dobras_com_piora"]}
                if k==8:
                    pm=m.permutar(model1["resid"],nn[k],ufs,reps,20261010+ano*5+int(key=="direcao_pt13"),True)
                    linha.update({"moran_residuo_contexto_p_perm":pm["p_bicaudal"],
                                  "moran_residuo_contexto_media_nula":pm["media_nula"]})
                linhas.append(linha)
                folds.append({"ano":ano,"desfecho":key,"k":k,"cv":v})
    df=pd.DataFrame(linhas)
    df["p_holm_k8_por_desfecho"]=np.nan
    for key in OUTCOMES:
        sel=(df.desfecho==key)&(df.k==8)
        df.loc[sel,"p_holm_k8_por_desfecho"]=m.holm(df.loc[sel,"moran_residuo_contexto_p_perm"].to_numpy())
    return df,folds


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("mapa","hhi","ibge","competitividade","pasta"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--permutacoes",type=int,default=999)
    a=p.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):
        raise SystemExit("Resultados existentes preservados.")
    merged,excluded=preparar(a.mapa,a.hhi,a.ibge,a.competitividade)
    table,folds=comparar(merged,a.permutacoes)
    a.pasta.mkdir(parents=True,exist_ok=True)
    table.to_csv(a.pasta/"modelos_competitividade_e_direcao_k4_k8_k12.csv",index=False,float_format="%.10f")
    (a.pasta/"validacao_uf_detalhada.json").write_text(json.dumps(folds,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    manifest={"autor":"Jacson Cruz do Nascimento","anos":[2018,2022],
       "municipios_por_eleicao":5565,"excluidos_ibge":excluded,
       "desfecho_principal":"competitividade = 1 - |v13 - voponente|/(v13 + voponente) no segundo turno",
       "sensibilidade_direcional":"margem assinada candidatura 13 versus outra finalista, por eleição",
       "modelos":"UF fixo + quatro características municipais versus UF fixo + características locais e médias IBGE de k municípios vizinhos",
       "validacao":"cinco folds de UFs inteiras omitidas, modelos SEM efeito fixo de UF, com as mesmas amostras e atributos",
       "matriz":"vizinhos centroides IBGE 2022 k=8 principal, k=4/12 sensibilidades",
       "permutacoes_residuais":a.permutacoes,
       "controle_multiplicidade":"Holm para dois testes ano 2018/2022 em k8, separadamente por desfecho",
       "restricoes":["2018 teve 76 votos de divergência no primeiro turno histórico do TSE, não ajustados.",
         "Os coeficientes não estabelecem causalidade, contágio social ou mudança individual de voto.",
         "Os atributos IBGE foram baixados em 2026 e podem ter revisões históricas; CV geográfica não é validação temporal ex ante.",
         "O contexto não usa votos, margens ou competitividade dos municípios vizinhos como covariáveis.",
         "R² maior com regressoras extras in-sample é propriedade mecânica de OLS.",
         "A margem assinada difere da competitividade porque identifica lado com vantagem."] }
    (a.pasta/"manifesto.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(table.to_string(index=False))
if __name__=="__main__":
    main()
