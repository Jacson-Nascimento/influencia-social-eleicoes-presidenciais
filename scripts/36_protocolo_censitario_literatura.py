#!/usr/bin/env python3
"""Protocolo censitário replicando Silva, Santos e Silva (2022), Opiniao Publica.

Censo 2000 -> 2002, 2006.
Censo 2010 -> 2010, 2014, 2018, 2022 (extensão 2022 explicitada).
Sensibilidade 2010 -> Censo 2000 para leitura estritamente anterior ao pleito.
1998 EXCLUÍDO. Nenhum voto/regressão é reestimado nesta etapa.
O artigo de referência é municipal do Rio e usa IDS, NÃO as nossas variáveis;
é o critério de alinhamento censitário que está sendo replicado.

PIB/período: 2002 não possui PIB2000 no SIDRA 5938; não imputar.
Coorte comum 2002–2022 deve ser definida posteriormente conciliando códigos
eleitorais por ano e excluindo registros especiais ZZ/VT, sem imputação implícita.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
YEARS=[2002,2006,2010,2014,2018,2022]
CENSUS={2002:2000,2006:2000,2010:2010,2014:2010,2018:2010,2022:2010}
POP={2002:2001,2006:2005,2010:2009,2014:2013,2018:2017,2022:2021}
PIB={2002:None,2006:2004,2010:2008,2014:2012,2018:2016,2022:2020}
DOC={"principal":"Silva, Santos e Silva. Do Leme a Santa Cruz: a territorialização eleitoral de Jair Bolsonaro no município do Rio de Janeiro. Opinião Pública 28(1), 2022. DOI 10.1590/1807-0191202228192",
 "municipal":"Soares; Terron. Dois Lulas: a geografia eleitoral da reeleição. Opinião Pública 14(2), 2008. DOI 10.1590/S0104-62762008000200001",
 "porte":"Nicolau (2026), Estudos Avançados 40(117), usa Censo 2022 para faixas de porte na análise retrospectiva, não para os 4 controles socioeconômicos utilizados aqui."}
def read(path):
    d=pd.read_csv(path,dtype={"CD_MUNICIPIO_IBGE":str})
    if d.CD_MUNICIPIO_IBGE.duplicated().any():
        raise ValueError("Geocódigo IBGE duplicado: "+str(path))
    return d
def main():
    pa=argparse.ArgumentParser()
    for name in ("mapa","historicos","controles2014","controles2018_2022","saida","manifesto"):
        pa.add_argument("--"+name,required=True,type=Path)
    a=pa.parse_args()
    if a.saida.exists() or a.manifesto.exists():
        raise SystemExit("Saída anterior existe: não sobrescrever")
    mp=read(a.mapa)
    hist=read(a.historicos)
    c14=read(a.controles2014)
    c18=read(a.controles2018_2022)
    if len(mp)!=5570 or len(c14)!=5570:
        raise ValueError("Cadastro IBGE/controles 2014 não tem 5570 municípios")
    if not set(["urbanizacao_2000","fracao_feminina_2000","pop_2001","pop_2005","pop_2009","pib_mil_2004","pib_mil_2008"]).issubset(hist):
        raise ValueError("Arquivo censitário antigo sem colunas necessárias.")
    cols14=["CD_MUNICIPIO_IBGE","pop_2013","pib_2012","urbanizacao_2010","fracao_feminina_2010"]
    if not set(cols14).issubset(c14):raise ValueError("2014 faltam variáveis")
    cols18=["CD_MUNICIPIO_IBGE","pop_2017","pop_2021","pib_mil_reais_2016","pib_mil_reais_2020","urbanizacao_2010","fracao_feminina_2010"]
    if not set(cols18).issubset(c18):raise ValueError("2018/2022 faltam variáveis")
    d=mp[["CD_MUNICIPIO_IBGE","SG_UF","CD_MUNICIPIO","latitude","longitude"]].merge(
        hist,on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one").merge(
        c14[["CD_MUNICIPIO_IBGE","pop_2013","pib_2012"]],on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one").merge(
        c18[cols18],on="CD_MUNICIPIO_IBGE",how="left",validate="one_to_one")
    rows=[]
    for yr in YEARS:
        c=CENSUS[yr]
        part=d[["CD_MUNICIPIO_IBGE","SG_UF","CD_MUNICIPIO","latitude","longitude"]].copy()
        part["ano"]=yr
        part["censo_demografico"]=c
        part["ano_populacao"]=POP[yr]
        part["ano_pib"]=PIB[yr] if PIB[yr] else np.nan
        part["populacao_antes"]=d[f"pop_{POP[yr]}"]
        part["urbanizacao_censo"]=d[f"urbanizacao_{c}"]
        part["fracao_feminina_censo"]=d[f"fracao_feminina_{c}"]
        part["log_pop"]=np.log(part.populacao_antes.where(part.populacao_antes>0))
        part["log_pibpc_proxy"]=np.nan
        if yr==2006:
            p=d.pib_mil_2004
        elif yr==2010:
            p=d.pib_mil_2008
        elif yr==2014:
            p=d.pib_2012
        elif yr==2018:
            p=d.pib_mil_reais_2016
        elif yr==2022:
            p=d.pib_mil_reais_2020
        else:
            p=None
        if p is not None:
            ratio=1000*p/part.populacao_antes
            part["log_pibpc_proxy"]=np.log(ratio.where(ratio>0))
        part["n_controles_igual_3"]=part[["log_pop","urbanizacao_censo","fracao_feminina_censo"]].notna().sum(axis=1)
        part["completo_modelo_3"]=part.n_controles_igual_3.eq(3)
        part["completo_modelo_4"]=part.completo_modelo_3 & part.log_pibpc_proxy.notna()
        if not part.urbanizacao_censo.dropna().between(0,1).all():
            raise ValueError("Urbanizacao fora intervalo para "+str(yr))
        rows.append(part)
    out=pd.concat(rows,ignore_index=True)
    if len(out)!=5570*6 or set(out.ano)!=set(YEARS):
        raise ValueError("Ano ou cobertura incorreto")
    sens=out[out.ano==2010].copy()
    sens["censo_demografico"]=2000
    sens["urbanizacao_censo"]=d.urbanizacao_2000.to_numpy()
    sens["fracao_feminina_censo"]=d.fracao_feminina_2000.to_numpy()
    sens["n_controles_igual_3"]=sens[["log_pop","urbanizacao_censo","fracao_feminina_censo"]].notna().sum(axis=1)
    sens["completo_modelo_3"]=sens.n_controles_igual_3.eq(3)
    sens["completo_modelo_4"]=sens.completo_modelo_3 & sens.log_pibpc_proxy.notna()
    complete=out.groupby("CD_MUNICIPIO_IBGE").completo_modelo_3.all()
    s=pd.concat([out.assign(especificacao="literatura_retrospectiva"),
                 sens.assign(especificacao="sensibilidade_2010_censo2000")],ignore_index=True)
    a.saida.parent.mkdir(parents=True,exist_ok=True)
    s.to_csv(a.saida,index=False,float_format="%.12f")
    check=[]
    for year in YEARS:
        z=out[out.ano.eq(year)]
        check.append({"eleicao":year,"censo_primario":CENSUS[year],"populacao":POP[year],
            "pib":PIB[year],"linhas_cadastro_5570":len(z),
            "completos_tres_controles":int(z.completo_modelo_3.sum()),
            "completos_quatro_controles":int(z.completo_modelo_4.sum())})
    meta={"nome":"Protocolo longitudinal municipal IBGE/TSE 2002–2022",
        "anos_eleitorais":YEARS,"exclusoes":["1998 descartado por decisão do autor"],
        "fontes_pesquisa":DOC,
        "regra_replicada":"2000 Censo para 2002/2006; 2010 Censo para 2010/2014/2018. Estendido 2010 Censo para 2022 a fim de manter urbanização/fração feminina comparáveis às outras eleições do bloco.",
        "nota_2010":"Censo 2010 e pleito 2010 no mesmo ano = contextualização retrospectiva. Não declarar ex-ante. Modelo 2010 com Censo 2000 registrado como sensibilidade.",
        "modelo_comum":"3 controles: log população do ano anterior, urbanização e fração feminina censitárias. PIB municipal de 2000 ausente do SIDRA5938 impede modelo 4 controles para 2002.",
        "modelo_quatro":"4 controles: acrescentar log PIB2012/pop2013 etc. de 2006 a 2022, por períodos, como análise restrita.",
        "sem_imputacao":"Municípios sem censo não recebem valores de origem nem médias inventadas; excluir da amostra principal até crosswalk de distritos oficialmente validada.",
        "nao_calculado":"Nenhum voto ou regressão foi reestimado nesta rotina. Indicadores completos ainda dependem de conciliação eleitoral 2002 2006 2010 com exclusão ZZ e VT.",
        "regra_total":check,
        "municipios_com_modelo_3_completo_todos_6_anos_na_grade_IBGE":int(complete.sum()),
        "contraste_sensibilidade_2010":{"principal_completos_3":int(out.loc[out.ano.eq(2010),"completo_modelo_3"].sum()),
                                      "2000_completos_3":int(sens.completo_modelo_3.sum())},
        "saida_sha256":__import__("hashlib").sha256(a.saida.read_bytes()).hexdigest()}
    a.manifesto.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(meta,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
