#!/usr/bin/env python3
"""Cobertura de votos na amostra municipal balanceada 2002–2022.

Calcular fração de votos válidos do segundo turno preservada no painel
de 5506 municípios, sem adicionar votos de exterior ou locais especiais.
Auditar separadamente registros TSE com UF ZZ (exterior) ou VT.
Comparar cobertura de votos, estados, universo territorial e perdas.
"""
import argparse,hashlib,json
from pathlib import Path
import pandas as pd
YEARS=(2002,2006,2010,2014,2018,2022)
FIN={2002:{13,45},2006:{13,45},2010:{13,45},2014:{13,45},2018:{13,17},2022:{13,22}}
def main():
    pa=argparse.ArgumentParser()
    for k in ("panel","votos_2002","votos_2006","votos_2010","votos_2014","votos_2018_2022","out"):
        pa.add_argument("--"+k,type=Path,required=True)
    args=pa.parse_args()
    if args.out.exists() and any(args.out.iterdir()):raise SystemExit("Preservar arquivos")
    panel=pd.read_csv(args.panel,dtype={"CD_MUNICIPIO_IBGE":str})
    selected=set(panel.CD_MUNICIPIO_IBGE)
    if len(selected)!=5506:raise ValueError("Amostra mudou")
    city=pd.read_csv(args.votos_2014,dtype={"CD_MUNICIPIO_IBGE":str})
    last=pd.read_csv(args.votos_2018_2022)
    # Need modern TSE to IBGE keys for early elections. Historic second round
    # lacks IBGE code, read mapping present on GitHub.
    mmap=pd.read_csv("outputs/municipal_v01/chaves_tse_ibge_5570_centroides.csv",
        dtype={"CD_MUNICIPIO_IBGE":str})
    allrows=[]
    for year in YEARS:
        if year in (2002,2006,2010):
            votes=pd.read_csv(getattr(args,f"votos_{year}"),dtype={"SG_UF":str})
            sec=votes[votes.NR_TURNO.eq(2)&votes.NR_CANDIDATO.isin(FIN[year])].copy()
            sec["tipo_abrangencia"]=sec.SG_UF.map(lambda s:"exterior" if s=="ZZ" else "especial_VT" if s=="VT" else "municipal")
            territory=sec[sec.tipo_abrangencia.eq("municipal")].copy()
            territory=territory.merge(mmap[["SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE"]],
                how="left",on=["SG_UF","CD_MUNICIPIO"],validate="many_to_one",indicator=True)
            territory["na_amostra"]=territory.CD_MUNICIPIO_IBGE.isin(selected)
            total=int(sec.QT_VOTOS_NOMINAIS.sum())
            n_total_city=int(territory.QT_VOTOS_NOMINAIS.sum())
            n_in=int(territory.loc[territory.na_amostra,"QT_VOTOS_NOMINAIS"].sum())
            n_foreign=int(sec.loc[sec.tipo_abrangencia.eq("exterior"),"QT_VOTOS_NOMINAIS"].sum())
            n_special=int(sec.loc[sec.tipo_abrangencia.eq("especial_VT"),"QT_VOTOS_NOMINAIS"].sum())
            unlinked=int(territory.loc[territory._merge.ne("both"),"QT_VOTOS_NOMINAIS"].sum())
            cities=territory[["SG_UF","CD_MUNICIPIO"]].drop_duplicates().shape[0]
        else:
            sec=(city if year==2014 else last[last.ano.eq(year)]).copy()
            total=int(sec.total_validos.sum())
            n_total_city=total
            n_in=int(sec.loc[sec.CD_MUNICIPIO_IBGE.isin(selected),"total_validos"].sum()) if year==2014 else None
            if year!=2014:
                terr=sec.merge(mmap[["SG_UF","CD_MUNICIPIO","CD_MUNICIPIO_IBGE"]],on=["SG_UF","CD_MUNICIPIO"],validate="one_to_one")
                n_in=int(terr.loc[terr.CD_MUNICIPIO_IBGE.isin(selected),"total_validos"].sum())
            n_foreign=n_special=unlinked=0
            cities=len(sec)
        if n_in<=0 or n_in>n_total_city or total<n_total_city:
            raise ValueError("Totais absurdos "+str(year))
        allrows.append({"ano":year,"municipios_com_votos":cities,
            "votos_segundo_turno_fonte_incluindo_especial":total,
            "votos_municipais_somados":n_total_city,
            "votos_conservados_na_amostra_5506":n_in,
            "pct_votos_municipais_retidos":100*n_in/n_total_city,
            "votos_municipais_excluidos":n_total_city-n_in,
            "votos_no_exterior_na_fonte":n_foreign,
            "votos_em_codigo_VT_na_fonte":n_special,
            "votos_sem_cadastro_moderno":unlinked,
            "n_municipios_amostra":5506})
    out=pd.DataFrame(allrows)
    assert len(out)==6 and out.pct_votos_municipais_retidos.between(80,100).all()
    args.out.mkdir(parents=True)
    out.to_csv(args.out/"cobertura_votos_amostra_comum.csv",index=False,float_format="%.7f")
    doc={"nota":"2014/2018/2022 já se encontram sem exterior, enquanto 2002/2006/2010 contêm ZZ e, em 2010, VT. Não comparar o campo de totais brutos entre períodos sem separar recortes.",
      "anos":list(YEARS),"n_comum":5506,
      "n_cidades_atual":5570,
      "cautelas":["Áreas municipais e código TSE podem mudar; cadastro de 2022 é proxy para correspondência histórica.",
                  "Percentual de votos retidos não substitui checagem de concentração territorial das exclusões.",
                  "Não imputar votos de VT/exterior em municípios."],
      "sha256_saida":hashlib.sha256((args.out/"cobertura_votos_amostra_comum.csv").read_bytes()).hexdigest()}
    (args.out/"manifesto.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
    print(out.to_string(index=False))
if __name__=="__main__":main()
