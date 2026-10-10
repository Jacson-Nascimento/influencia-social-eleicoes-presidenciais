#!/usr/bin/env python3
"""Auditoria independente da votação presidencial TSE 2018/2022.

Confirma divergência histórica do 1º turno de 2018 sem corrigir microdados.
O desfecho principal do artigo é baseado em segundos turnos conciliados.
"""
import argparse,hashlib,json
from pathlib import Path
import pandas as pd

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as fp:
        for b in iter(lambda:fp.read(1048576),b""):h.update(b)
    return h.hexdigest()

def auditar(votos,referencia):
    rec=[]
    for ano,path in votos:
        v=pd.read_csv(path,dtype={"SG_UF":str})
        if len(v)==0 or not v.ANO_ELEICAO.eq(ano).all():
            raise ValueError("Dados eleitorais ausentes ou do ano incorreto.")
        k=["ANO_ELEICAO","NR_TURNO","SG_UF","CD_MUNICIPIO","NR_CANDIDATO"]
        if v.duplicated(k).any() or v.QT_VOTOS_NOMINAIS.lt(0).any():
            raise ValueError("Duplicação de chave ou votos negativos.")
        for turno in (1,2):
            d=v[v.NR_TURNO.eq(turno)]
            r=referencia[(referencia.ANO_ELEICAO==ano)&(referencia.NR_TURNO==turno)]
            if len(r)!=1 or len(d)==0:
                raise ValueError("Controle histórico ou turno ausente.")
            r=r.iloc[0]
            cand=d.groupby("NR_CANDIDATO").QT_VOTOS_NOMINAIS.sum().to_dict()
            total=int(d.QT_VOTOS_NOMINAIS.sum())
            chosen=[int(r["CANDIDATO_1"]),int(r["CANDIDATO_2"])]
            for code in chosen:
                esperado=int(r["VOTOS_CANDIDATO_1"] if code==chosen[0] else r["VOTOS_CANDIDATO_2"])
                observado=int(cand.get(code,0))
                rec.append({"ano":ano,"turno":turno,"tipo":"candidatura","codigo":code,
                  "observado":observado,"referencia":esperado,"diferenca":observado-esperado})
            outros=total-sum(int(cand.get(k,0)) for k in chosen)
            rec.append({"ano":ano,"turno":turno,"tipo":"outras_candidaturas","codigo":-1,
                        "observado":outros,"referencia":int(r.VOTOS_OUTROS),
                        "diferenca":outros-int(r.VOTOS_OUTROS)})
            rec.append({"ano":ano,"turno":turno,"tipo":"total_validos","codigo":-1,
                        "observado":total,"referencia":int(r.TOTAL_VALIDOS),
                        "diferenca":total-int(r.TOTAL_VALIDOS)})
            municipios=d.loc[d.SG_UF.ne("ZZ"),["SG_UF","CD_MUNICIPIO"]].drop_duplicates().shape[0]
            if municipios!=5570:raise ValueError("Cobertura municipal brasileira incompleta.")
    out=pd.DataFrame(rec)
    def diff(year,turno,tipo,code=-1):
        x=out[(out.ano==year)&(out.turno==turno)&(out.tipo==tipo)&(out.codigo==code)]
        if len(x)!=1:raise ValueError("Auditoria ambígua.")
        return int(x.iloc[0].diferenca)
    if diff(2018,1,"total_validos")!=76 or diff(2018,1,"candidatura",17)!=20 or diff(2018,1,"candidatura",13)!=46 or diff(2018,1,"outras_candidaturas")!=10:
        raise ValueError("A divergência documental de 2018 mudou: investigar antes de aceitar.")
    for ano,turno in ((2018,2),(2022,1),(2022,2)):
        if (out[(out.ano==ano)&(out.turno==turno)].diferenca!=0).any():
            raise ValueError("Divergência inesperada no controle de "+str((ano,turno)))
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for nm in ("arquivo2018","arquivo2022","controles","pasta"):
        p.add_argument("--"+nm,type=Path,required=True)
    a=p.parse_args()
    if a.pasta.exists() and any(a.pasta.iterdir()):
        raise SystemExit("Versão anterior preservada.")
    ctr=pd.read_csv(a.controles)
    detail=auditar([(2018,a.arquivo2018),(2022,a.arquivo2022)],ctr)
    a.pasta.mkdir(parents=True,exist_ok=True)
    detail.to_csv(a.pasta/"reconciliacao_candidatos_e_totais.csv",index=False)
    meta={
      "status_2018_1t":"SOB RESSALVA DOCUMENTAL, NÃO CONCILIADO",
      "diferenca_total_2018_1t":76,
      "decomposicao_diferenca_2018_1t":{"candidato_17":20,"candidato_13":46,"outros":10},
      "controle_2018_1t":"https://www.tse.jus.br/comunicacao/noticias/2018/Outubro/concluida-totalizacao-de-votos-do-1o-turno-das-eleicoes-2018",
      "status_2018_2t":"CONCILIADO INTEGRALMENTE",
      "status_2022_1t":"CONCILIADO INTEGRALMENTE",
      "status_2022_2t":"CONCILIADO INTEGRALMENTE",
      "impacto_objeto_central":"O desfecho do estudo é definido com dados de segundo turno, cujos totais conferem com TSE. O 1º turno de 2018 é análise complementar sob ressalva e não integra o modelo principal.",
      "percentual_de_divergencia_1t":100*76/107050673,
      "critica":"Não identificada causa da diferença entre arquivo distribuído e matéria histórica, sem hipótese atribuída e sem alterar voto.",
      "sha256_insumos":{"votos2018":sha(a.arquivo2018),"votos2022":sha(a.arquivo2022),
                        "controles_historicos":sha(a.controles)},
      "regras":["Sem duplicações na chave município-candidatura-turno.",
                "Sem votos negativos.",
                "Cobertura completa de 5.570 municípios brasileiros em cada turno.",
                "Candidato 13 e 17/22 e 'outros' conciliados conforme arquivo de referência.",
                "Não usar ausência de divergência no segundo turno para alegar consistência perfeita no primeiro turno."]
    }
    (a.pasta/"manifesto_auditoria_2018_2022.json").write_text(json.dumps(meta,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(detail.to_string(index=False))
    print(json.dumps(meta,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
