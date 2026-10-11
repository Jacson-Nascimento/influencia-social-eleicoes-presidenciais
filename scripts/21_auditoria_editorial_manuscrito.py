#!/usr/bin/env python3
"""Auditoria editorial automatizada do manuscrito de competitividade v05.

Valida dados, requisitos conhecidos da revista e nota da ressalva 2018.
Não substitui leitura editorial humana, verificação antiplágio ou escolha final do periódico.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import pandas as pd

def parsear(arquivo):
    texto=Path(arquivo).read_text(encoding="utf-8")
    titulo=texto.splitlines()[0].removeprefix("# ").strip()
    resumo=texto.split("## Resumo",1)[1].split("## Introdução",1)[0].strip()
    linhas=texto.splitlines()
    metadados={}
    for idioma in ("Português","English","Español","Français"):
        rows=[x.split("**",2)[-1].strip(": ").strip() for x in linhas if x.startswith("**"+idioma+":**")]
        if len(rows)!=1:raise ValueError("Falta título no idioma "+idioma)
        metadados[idioma]=rows[0]
    chaves={}
    for prefix in ("Palavras-chave","Keywords","Palabras clave","Mots-clés"):
        vals=[x for x in linhas if x.startswith("**"+prefix+":**")]
        if len(vals)!=1:raise ValueError("Palavras-chave "+prefix+" não são únicas")
        chaves[prefix]=[x.strip(" .") for x in vals[0].split("**",2)[-1].strip().split(";") if x.strip()]
    return texto,titulo,resumo,metadados,chaves

def auditar(manu,modelos,pesos,robustez,ci,concil):
    txt,title,abstract,trans,keys=parsear(manu)
    errs=[]
    count=len(txt.split())
    if not 7000<=count<=14000:errs.append(f"Extensão {count} fora da faixa 7000–14000.")
    if len(title.split())>20:errs.append("Título em português tem mais de 20 palavras.")
    if len(abstract)>900:errs.append("Resumo supera 900 caracteres.")
    for k,v in keys.items():
        if len(v)!=5:errs.append("Palavras-chave não são cinco em "+k)
    if re.search(r"^#{2,3}\s+\d+\.",txt,flags=re.MULTILINE):
        errs.append("Seções numeradas identificadas.")
    if "Não foi possível identificar documentalmente a causa exata da divergência." not in txt:
        errs.append("Ressalva documental de 2018 não está escrita sem causa.")
    for v in ("107.050.749","107.050.673","76 a mais","20 votos","46 da candidatura","10 das demais"):
        if v not in txt:errs.append("Falta informação na observação 2018: "+v)
    if txt.count("**Tabela ")!=6:errs.append("Não há exatamente 6 títulos de tabelas.")
    if txt.count("*Fonte: elaboração própria")!=6:errs.append("Fontes de tabelas ausentes.")
    for nome in ("CAMERON,","CONLEY,","Nicolau","Alkmim","Resende","Braga"):
        if nome.lower() not in txt.lower():errs.append("Referência ausente: "+nome)
    tab=pd.read_csv(modelos);pes=pd.read_csv(pesos);rob=pd.read_csv(robustez);boot=pd.read_csv(ci);aud=pd.read_csv(concil)
    for ano in (2018,2022):
        for desfecho in ("competitividade","direcao_pt13"):
            base=tab[(tab.ano==ano)&(tab.desfecho==desfecho)&(tab.k==8)]
            p=pes[(pes.ano==ano)&(pes.desfecho==desfecho)&(pes.k==8)]
            r=rob[(rob.ano==ano)&(rob.desfecho==desfecho)&(rob.amostra=="todos")&(rob.peso=="populacao_anterior")]
            b=boot[(boot.ano==ano)&(boot.desfecho==desfecho)&(boot.peso=="populacao_anterior")]
            if not all(len(x)==1 for x in (base,p,r,b)):
                errs.append(f"Cobertura especificação {(ano,desfecho)} faltante");continue
            if abs(float(r.iloc[0].ganho_rmse_cv_pct)-float(b.iloc[0].ganho_rmse_observado_pct))>1e-6:
                errs.append(f"Bootstrap e robustez inconsistentes para {(ano,desfecho)}")
            pct=f"{float(r.iloc[0].ganho_rmse_cv_pct):+.2f}".replace(".",",")
            if pct not in txt:
                errs.append(f"Resultado {pct} de {(ano,desfecho)} ausente do manuscrito")
    diff=aud[(aud.ano==2018)&(aud.turno==1)&(aud.tipo=="total_validos")]
    if len(diff)!=1 or int(diff.iloc[0].diferenca)!=76:errs.append("Divergência auditada 2018 não é 76.")
    for ano,turno in ((2018,2),(2022,1),(2022,2)):
        x=aud[(aud.ano==ano)&(aud.turno==turno)]
        if (x.diferenca!=0).any():errs.append(f"Divergência inesperada {ano}/{turno}")
    return {"status":"APROVADA NA AUDITORIA AUTOMÁTICA" if not errs else "REPROVADA",
            "texto_palavras_separadas_espacos":count,"titulo_palavras":len(title.split()),
            "resumo_caracteres":len(abstract),"numero_tabelas":txt.count("**Tabela "),
            "cinco_palavras_chave_em_quatro_idiomas":all(len(x)==5 for x in keys.values()),
            "titulos":trans,"notas":{"76_votos":"RESSALVA EXPLÍCITA SEM CAUSA IDENTIFICADA"},
            "periodo":"2018 e 2022","arquivo_manuscrito_sha256":hashlib.sha256(txt.encode("utf-8")).hexdigest(),
            "falhas":errs,
            "nao_auditado":["Antiplágio","integridade de trabalhos de terceiros além das referências verificadas",
                            "formatacao final .doc e figuras","políticas editoriais no ato da submissão",
                            "checagem humana de cada linha de narrativa"]}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ("manuscrito","modelos","pesos","robustez","bootstrap","conciliacao","saida"):
        p.add_argument("--"+n,required=True,type=Path)
    a=p.parse_args()
    if a.saida.exists():raise SystemExit("Saída existente preservada.")
    report=auditar(a.manuscrito,a.modelos,a.pesos,a.robustez,a.bootstrap,a.conciliacao)
    a.saida.parent.mkdir(parents=True,exist_ok=True)
    a.saida.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if report["falhas"]:raise SystemExit("Auditoria não aprovada: corrigir falhas, sem publicar como versão pronta.")
if __name__=="__main__":main()
