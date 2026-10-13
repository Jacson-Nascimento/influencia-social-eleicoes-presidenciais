# Resposta técnica ao parecer - versão v16.1 (13/10/2026)

Autor: Jacson Cruz do Nascimento. Escopo: seis segundos turnos presidenciais brasileiros (2002-2022). Manuscrito de trabalho, NÃO SUBMETIDO. 1998 EXCLUÍDA.

## Revisão da literatura

Verificados metadados em fontes editoriais/academicas:
- Soares e Terron (2008): Opinião Pública 14(2), pp. 269-301, DOI 10.1590/S0104-62762008000200001. Ano bibliográfico 2008, mesmo quando sistemas mostram disponibilização eletrônica em 2009 ou datas posteriores de atualização.
- Ehrl (2017): Estudos Econômicos 47(1), pp. 215-229, DOI 10.1590/0101-416147182phe. AMCs do intervalo censitário 1872-2010, sem garantia de série homogênea até 2022.
- Braga e Zolnerkevic (2020): Opinião Pública 26(1), pp. 1-33, DOI 10.1590/1807-019120202611, primeiro turno agregado por microrregiões; não substitui validação de segundo turno.
- Alkmim e Terron (2022): Estudos Avançados 36(106), pp. 7-32, DOI 10.1590/s0103-4014.2022.36106.002; geografia de eleições 1989-2018.
- Masullo e Silva Junior (2024): Revista do Departamento de Geografia v.44, e207979, DOI 10.11606/eISSN.2236-2878.rdg.2024.207979.
- Nicolau (2026): Estudos Avançados 40(117), artigo e40117091, DOI 10.1590/s0103-4014.2026.40117.005.
- Resende e Azevedo (2025): Caderno de Geografia 35(83), artigo 1195, DOI 10.5752/P.2318-2962.2025v35n83p1195. Sem alegação de resultado/regressão espacial não confirmada.
- Papke e Wooldridge (1996), Journal of Applied Econometrics 11(6), pp.619-632: logit fracionário.
- King (1997), Princeton University Press: limitação da inferência ecológica.
- Cameron e Miller (2015), Journal of Human Resources 50(2), pp.317-372: cluster-robust.
- Conley (1999), Journal of Econometrics 92(1), pp.1-45: dependência transversal espacial.
- Openshaw (1984), Environment and Planning A 16(1), pp.17-31: falácia ecológica e problemas das unidades areais.

## Divergência entre v12 e v16 - documentação obrigatória

Na versão anterior v12 (2018-2022), sob pesos uniformes e macrorregião: ganho da margem assinada M 2018 +4,67% (IC [+1,30;+7,17]); 2022 +4,47% (IC [+1,08;+6,82]); amostra de 5.565 municípios e quatro controles socioeconômicos.

Na v16 (2002-2022), sob pesos uniformes e macrorregião: ganho M 2018 +0,9564888196% (IC [-2,2449259392;+3,8174175939]); 2022 +0,0873957207% (IC [-2,0512667240;+2,8835537048]); amostra de 5.506 municípios e três controles socioeconômicos.

A divergência NÃO identifica isoladamente o papel do PIB. Precisa de experimento controlado, com mesmo universo, partições e critérios geográficos, para separar os efeitos da amostra, dados, PIB, vintage, população e atributos de vizinhança. Não há prova de que v12 tenha sido formalmente divulgada; caso tenha circulado, acompanhar futuras versões com nota de comparabilidade.

Fonte v12 preservada no Drive: https://docs.google.com/document/d/10ADj3AsJlu8aUFMEAt4sAperGsU0VmAq/edit
Fontes v16: outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_geografica_2002_2022.csv e validacao_temporal_2002_2022.csv.

## Inferência espacial - restrição de versão

Versões de 2018-2022 contêm CR1 por UF, Conley e buffers de exclusão espacial, mas foram calculadas para n=5.565 e quatro controles. Não transportar números-p ou testes para v16, que usa n=5.506 e três controles. Reestimar os diagnósticos espaciais no painel correto ANTES da versão submetível.

## Metadados primários e integridade

Os scripts de montagem atuais consomem variáveis urbanização_2000 e fracao_feminina_2000 de arquivos previamente preparados. A tabela SIDRA ou fonte IBGE exata da coleta do Censo 2000 ainda não foi identificada nessa inspeção; recuperar linhagem de coleta original. Manter ressalva de divergência de 76 votos no primeiro turno de 2018 sem causa atribuída. Não imputar dados nem excluir originais.

## Transparência de uso de IA

A v16.1 inclui declaração do uso de ChatGPT/OpenAI nas etapas de organização, preparação e revisão editorial, estruturação de texto, apoio computacional e formatação de tabelas/gráficos, com identificação das seções e limites de responsabilidade. Política consultada: https://periodicos.sbu.unicamp.br/ojs/index.php/index/diretrizes . O autor deverá validar a completude do histórico efetivo e adequar a declaração às regras da revista escolhida.

## Estado e conclusão

Gerado manuscrito editorial revisado v16.1 em Word/PDF, preservando v16 e versões anteriores. Esta revisão NÃO é auditoria independente dos scripts, nem reexecução de inferência espacial, de testes causais, ou de reconciliação primária de todos os dados TSE. Não submeter antes de encerradas pendências quantitativas e do periódico escolhido.
