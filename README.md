# Dinâmica de influência social e comportamento eleitoral no Brasil

**Autor:** Jacson Cruz do Nascimento  
**ORCID:** https://orcid.org/0009-0006-6535-9569  
**ISNI:** 0000 0005 3052 9869  
**Início:** 8 de outubro de 2026  
**Situação:** artigo de competitividade eleitoral, versão v04 com testes executados de ponderação populacional anterior às eleições, influência de capitais e grandes municípios, confronto bibliográfico e auditoria eleitoral final; trabalho editorial e inferência espacial mais exigente ainda pendentes.

## Objetivo
Investigar padrões de concentração, interação territorial e mudanças agregadas de preferências entre turnos presidenciais, avaliando se medidas espaciais acrescentam capacidade explicativa em relação a modelos simples.

Não há identificação do voto individual. Semelhança territorial não comprova influência social ou contágio. Mudanças agregadas não identificam transferências individuais.

## Projeto independente
Este estudo possui repositório, protocolo, dados, código, testes e eventual DOI próprios. O trabalho anterior de dinâmica de manada organizacional (DOI: https://doi.org/10.5281/zenodo.21985858) é apenas referência conceitual. Os parâmetros dos 60 agentes e seus percentuais simulados não são resultados eleitorais.

Repositório do trabalho anterior: https://github.com/Jacson-Nascimento/dinamica-manada-organizacional

## Fontes públicas
- Resultados 2018: https://dadosabertos.tse.jus.br/dataset/resultados-2018
- Resultados 2022: https://dadosabertos.tse.jus.br/dataset/resultados-2022
- Resultados 2026: https://dadosabertos.tse.jus.br/dataset/resultados-2026
- Boletins de urna 2026: https://dadosabertos.tse.jus.br/dataset/resultados-2026-boletim-de-urna

O licenciamento de cada recurso precisa ser conferido antes de redistribuir bases brutas. Coletas terão manifesto com fonte, ID do recurso, data, bytes e SHA-256.

## Estrutura e replicação
- `docs/`: protocolo, fontes, interpretação e manuscrito.
- `scripts/`: coleta e transformação dos recursos oficiais e auditoria.
- `data/brutos/`: cópias imutáveis de arquivos oficiais, após obtenção.
- `data/controles/`: totais históricos observados e suas fontes.
- `data/tratados/`: derivados abertos.
- `tests/`: testes com dados fictícios.
- `outputs/`: resultados verificados e figuras.

Instalar Python 3.11+ e executar:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/04_conferir_agregados_historicos.py --arquivo data/controles/totalizacao_presidencial_2022_tse.csv --saida outputs/relatorios/auditoria_agregados_2022_v02.json
python scripts/01_coletar_tse.py --dataset resultados-2022 --list
```

A saída v02 serve para preservar o arquivo v01 existente; não sobrepor versões anteriores. Consulte `docs/REPLICACAO.md`.

## Estado da investigação
A base municipal presidencial de 2022 foi coletada do ZIP oficial do TSE, consolidada e conciliada exatamente nos dois turnos. A base de 2018 foi igualmente coletada e disponibilizada **com ressalva**: há diferença de +76 votos no 1º turno entre o arquivo oficial baixado e a totalização histórica de referência; o 2º turno de 2018 conciliou integralmente. Não houve alterações artificiais para ajustar os dados. Ambos os anos cobrem 5.570 municípios brasileiros por turno; locais no exterior (ZZ) são documentados em separado. Nenhuma inferência causal de manada foi validada.

- **Base auditada 2022:** [CSV aberto](data/tratados/votos_presidente_municipio_2022.csv)
- **Base 2018 sob ressalva:** [CSV aberto](data/tratados/votos_presidente_municipio_2018_RESSALVA.csv)
- **Comparativo territorial v02:** [resumo nacional](outputs/comparativo_v02/resumo_nacional_2018_2022.csv) e [resumo por UF](outputs/comparativo_v02/resumo_uf_2018_2022.csv)
- **Relatório técnico:** [avaliação territorial de 2018 e 2022](docs/AVALIACAO_TERRITORIAL_2018_2022_2026-10-10.md)
- **Auditoria 2018:** [JSON com divergências](outputs/relatorios/auditoria_2018_ressalva.json)
- **Auditoria 2022:** [JSON conciliado](outputs/relatorios/auditoria_municipal_2022.json)

As versões anteriores foram preservadas para auditoria. Os ZIPs originais são obtidos pelos links oficiais do TSE, com SHA-256 documentado em `outputs/relatorios/`. Nenhum resultado do modelo organizacional original foi reclassificado como resultado eleitoral.

## Análise espacial exploratória (UF)

Foram avaliadas as 27 UFs com HHI da composição de votos por candidatura, malha IBGE, Moran I global, 9.999 permutações e pesos por k vizinhos (3 a 6). No cenário de referência k=4, a autocorrelação de 2022 no primeiro turno foi I=0,402263, p bruto=0,0009 e p ajustado Holm=0,0036. Os demais testes de referência não apresentaram p ajustado abaixo de 0,05. **Associação espacial não é evidência causal de influência social.**

- [Relatório espacial e sensibilidade](docs/AVALIACAO_ESPACIAL_E_SENSIBILIDADE_2026-10-10.md)
- [Resultados Moran e geometria](outputs/espacial_v01/moran_hhi_ufs_2018_2022.json)
- [Sensibilidade k=3..6](outputs/espacial_v02/sensibilidade_knn_moran.csv)
- [Ajuste Holm](outputs/espacial_v02/holm_quatro_testes.json)

O próximo estágio exige ligação TSE-IBGE validada para malhas municipais históricas e avaliação de modelos espaciais fora da amostra. O estudo **não** apresenta previsão de vencedores ou probabilidades para 2026.

## Avaliação municipal espacial e temporal (10/10/2026)

A partir de votos presidenciais públicos do TSE, da correspondência oficial TSE-IBGE e da malha municipal do IBGE de 2022, foram relacionados 5.570 municípios em 2018 e 2022 sem perdas territoriais. O índice de Moran I do HHI municipal foi positivo nos dois anos e turnos, inclusive após centralização por UF. Para oito vizinhos, os valores brutos variaram de 0,6761 a 0,7898 e os centrados por UF, de 0,4353 a 0,4878. Todos os testes primários tiveram valor-p ajustado Holm de 0,0020. A correlação municipal do HHI entre 2018 e 2022 foi de 0,8083 no primeiro turno e 0,9252 no segundo.

Esses valores **não demonstram manada, transferência individual de votos, causalidade ou previsões eleitorais**. Persistência temporal elevada é um alerta para fatores territoriais não observados. O HHI entre turnos está sujeito ao efeito mecânico da diminuição de candidaturas. A divergência documental de 76 votos no primeiro turno de 2018 permanece preservada e assinalada.

- [Relatório empírico municipal](docs/RELATORIO_MUNICIPAL_ESPACIAL_2026-10-10.md)
- [Protocolo municipal e limites](docs/PROTOCOLO_ESPACIAL_MUNICIPAL_2026-10-10.md)
- [Índices de Moran e sensibilidades](outputs/municipal_v01/moran_municipal_sensibilidade.csv)
- [Correspondência municipal e centroides](outputs/municipal_v01/chaves_tse_ibge_5570_centroides.csv)
- [Estabilidade temporal e mudanças entre turnos](outputs/municipal_v02/persistencia_temporal_e_delta_hhi.json)
- [Manifesto dos dados e hashes](outputs/municipal_v01/manifesto.json)
- [Execução GitHub Actions aprovada](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/actions/runs/38068129663)

O artigo original de dinâmica de manada é metodologicamente distinto e não foi modificado.

## Controles socioeconômicos e comparação de contexto espacial (10/10/2026)

As tabelas oficiais IBGE 202 (Censo 2010), 5938 (PIB 2016 e 2020) e 6579 (população 2017 e 2021) foram baixadas, registradas com SHA-256 e disponibilizadas na versão v02 corrigida. Dos 5.570 municípios eleitorais, 5.565 apresentam todas as covariáveis exigidas. Nenhum valor ausente foi preenchido artificialmente; a primeira extração incompleta v01 foi preservada para auditoria.

Nas regressões descritivas com efeitos fixos de UF, incluir controles locais aumentou R² em 2,31 a 4,58 pontos percentuais. Moran I dos resíduos permaneceu elevado, entre 0,4246 e 0,4825 para oito vizinhos, após ajuste de UF e controles.

Extensões com médias de características IBGE de oito municípios próximos geraram acréscimo in-sample de 0,36 a 0,79 ponto percentual de R² e, na validação com UFs mantidas fora do treinamento, reduções de RMSE entre 0,95% e 7,70% conforme eleição e turno. O contexto usa apenas covariáveis, nunca HHI ou votos dos vizinhos. **Ganhos estatísticos de contexto territorial não comprovam comportamento de manada ou influência social causal.**

- [Relatório de controles socioeconômicos](docs/RELATORIO_CONTROLES_SOCIOECONOMICOS_2026-10-10.md)
- [Relatório de contexto territorial](docs/RELATORIO_COMPARACAO_CONTEXTO_ESPACIAL_2026-10-10.md)
- [Dados IBGE derivados v02](data/ibge_tratados/controles_pre_eleitorais_v02.csv)
- [Manifesto de fontes IBGE v02](outputs/controles_ibge_v02/manifesto.json)
- [Tabela de regressões](outputs/socioeconomico_v01/modelos_e_moran_residual.csv)
- [Comparação convencional vs contexto k=4,8,12](outputs/contexto_espacial_v01/comparacao_contexto_espacial_k4_k8_k12.csv)
- [Script de replicação dos modelos](scripts/13_modelos_controles_socioeconomicos.py)
- [Script de comparação espacial](scripts/14_comparacao_contexto_espacial.py)

**Próximo requisito científico:** testes adicionais de especificação, controles independentes de vulnerabilidade e escolaridade, análise de sensibilidade das matrizes e desenhos de identificação plausíveis antes de discutir causalidade; toda extrapolação temporal deve assegurar vintages informacionais disponíveis à época. O repositório deste artigo permanece independente do estudo organizacional publicado no Zenodo.

## Foco atual: competitividade presidencial no segundo turno (10/10/2026)

**Pergunta:** Em que medida as características socioeconômicas dos municípios e de seus vizinhos explicam as diferenças territoriais de competitividade nas eleições presidenciais brasileiras de 2018 e 2022?

A variável principal deixou de ser o HHI. Agora é a competitividade entre as duas candidaturas finalistas de segundo turno, **C = 1 - |v13 - voponente| / (v13 + voponente)**, em escala de 0 a 1. A margem assinada **M = (v13 - voponente) / (v13 + voponente)** preserva a direção da votação. O primeiro turno recebe análise complementar com os dois líderes locais, sua cobertura dos votos válidos e o número efetivo de candidaturas.

**Resultados principais:** 5.570 municípios nos indicadores e 5.565 nos modelos com IBGE. Medianas da competitividade em 2018 e 2022: 0,6148 e 0,6988. Na validação por UFs inteiras, o contexto de oito vizinhos reduziu o RMSE **sem ponderação** em 1,92% (2018) e 4,99% (2022) para competitividade; para a margem assinada, 17,09% e 18,53%. Contudo, **ponderado pelo total de votos válidos**, o ganho da competitividade virou **piora de 3,28%** em 2018 e melhora de apenas **0,34%** em 2022. Para a margem assinada, houve piora ponderada de 0,53% em 2018 e de 1,82% em 2022. Portanto **não há evidência estável de superioridade geral** do modelo contextual.

Essa discrepância entre ponderações é um resultado importante que deve permanecer explícito. Os modelos são associativos, não demonstram influência social causal, não projetam vencedores e não podem ser extrapolados diretamente para a eleição de 2026.

- [Manuscrito atual, v03](docs/MANUSCRITO_COMPETITIVIDADE_V03_2026-10-10.md).
- [Protocolo da competitividade](docs/PROTOCOLO_COMPETITIVIDADE_ELEITORAL_V01.md).
- [Indicadores segundo turno, versão v02](outputs/competitividade_v02/competitividade_e_margem_assinada_segundo_turno.csv).
- [Indicadores complementares primeiro turno, v02](outputs/competitividade_v02/indicadores_complementares_primeiro_turno.csv).
- [Modelos para competitividade e direção](outputs/competitividade_modelos_v01/modelos_competitividade_e_direcao_k4_k8_k12.csv).
- [Sensibilidade ponderada por votos](outputs/competitividade_ponderada_v01/modelos_ponderados_competitividade_e_direcao.csv).
- [Relatório dos modelos ponderados](docs/RELATORIO_SENSIBILIDADE_PONDERADA_2026-10-10.md).

**Preservação:** versões anteriores de HHI, manuscrito v01/v02, dados e scripts originais permanecem disponíveis. O repositório do artigo de dinâmica de manada organizacional não foi alterado.

## Quatro verificações finais para o manuscrito v04 (10/10/2026)

Concluídas as verificações de robustez solicitadas para a versão submetível, mantendo intactos os insumos e as versões antigas:

1. **Peso demográfico ex ante por ano de referência:** população IBGE 2017 para 2018 e 2021 para 2022 (versões acessadas em 2026). Na validação geográfica, contexto k=8 diminuiu o RMSE da competitividade em **−3,26%** (piora) em 2018 e **+0,40%** em 2022. Para margem assinada, **−0,89%** e **−1,87%**.
2. **Capitais e cidades grandes:** identificação dos 27 códigos de capitais via API de localidades IBGE; exclusões de capitais, dos 56 (1%) e dos 279 (5%) municípios mais populosos. A margem assinada ponderada por população passa de −0,89%/−1,87% na amostra completa para +14,95%/+15,62% sem os maiores 5%. Esta sensibilidade é descritiva, não causal.
3. **Literatura:** cinco antecedentes editoriais comparados. A novidade só pode ser afirmada de forma **incremental e condicionada**, não como primeira análise espacial eleitoral brasileira ou descoberta de efeitos de influência social.
4. **Auditoria documental:** 2018, primeiro turno **sob ressalva de +76 votos** frente à matéria histórica do TSE, decompostos em 20/46/10. Segundo turno de 2018 e ambos os turnos de 2022 **integralmente conciliados**. O desfecho principal usa somente segundos turnos, sem dados do primeiro turno de 2018.

- [Manuscrito acadêmico atualizado, v04](docs/MANUSCRITO_COMPETITIVIDADE_V04_2026-10-10.md).
- [Relatório de fechamento das quatro verificações](docs/FECHAMENTO_QUATRO_VERIFICACOES_2026-10-10.md).
- [Matriz de literatura](docs/REVISAO_LITERATURA_COMPETITIVIDADE_2026-10-10.md).
- [Dados de robustez demográfica e capitais](outputs/robustez_demografica_v01/robustez_pesos_populacao_e_grandes_cidades.csv).
- [Manifesto da robustez](outputs/robustez_demografica_v01/manifesto.json).
- [Auditoria documental independente](outputs/auditoria_documental_final_v01/manifesto_auditoria_2018_2022.json).

**Condição editorial restante:** revisar integralmente os antecedentes científicos e o texto final, analisar inferência apropriada à dependência espacial, normalizar tabelas/equações e completar submissão conforme critérios do periódico escolhido. Os achados não identificam causalidade nem validam previsões eleitorais fora do tempo.

## Revisão editorial e metodológica v05 — 10/10/2026

O **[manuscrito revisado v05](docs/MANUSCRITO_COMPETITIVIDADE_V05_REVISAO_EDITORIAL.md)** substitui a v04 como versão de trabalho mais recente, mas mantém todas as versões anteriores preservadas. O estudo permanece descritivo, não causal e independente da simulação organizacional. Foi confirmada a incerteza dos ganhos de desempenho por **bootstrap de 27 UFs** (4.999 repetições) e foram calculados testes conjuntos com **erros agrupados por UF** e covariância espacial **Conley HAC, raios 100/250 km**.

O ganho de contexto na **competitividade** com peso uniforme foi de 1,92% em 2018 (IC 95%: +0,11% a +4,42%) e 4,99% em 2022 (IC: +2,57% a +8,10%). Com **população anterior** como peso, os ganhos foram −3,26% em 2018 (IC: −4,54% a −1,63%) e +0,40% em 2022 (IC: −1,87% a +2,83%). A diferença de direção do resultado também foi auditada na análise de margem assinada. Não há ganho populacional estável de generalização.

A nota documental sobre **+76 votos no primeiro turno de 2018** foi incorporada expressamente ao manuscrito sem explicação causal inventada: +20 candidatura 17, +46 candidatura 13, +10 outras. O estudo principal utiliza segundos turnos totalmente conciliados.

**Periódico de referência provisório:** *Opinião Pública* (CESOP/Unicamp). Os requisitos editoriais foram verificados na página oficial de submissão: mínimo 7.000 e máximo 14.000 palavras, resumo até 900 caracteres, título e cinco palavras-chave em quatro idiomas, citações e referências ABNT, títulos de seção sem numeração, arquivo .doc. A auditoria automatizada do manuscrito v05 concluiu: **7.967 palavras, 611 caracteres no resumo, título com 15 palavras, seis tabelas com fontes e nenhuma falha nas verificações programadas**. Ainda é necessário preparar o arquivo .doc com tabelas formatadas, completar dados de cadastro de autoria e realizar revisão visual final; não foi efetuada submissão.

- [Manuscrito v05](docs/MANUSCRITO_COMPETITIVIDADE_V05_REVISAO_EDITORIAL.md)
- [Leitura crítica dos cinco antecedentes](docs/REVISAO_INTEGRAL_ANTECEDENTES_2026-10-10.md)
- [Parecer metodológico espacial](docs/PARECER_METODOLOGICO_FINAL_2026-10-10.md)
- [Checklist editorial da Opinião Pública](docs/AUDITORIA_EDITORIAL_REVISTA_OPINIAO_PUBLICA_2026-10-10.md)
- [Relatório automático de auditoria v05](outputs/auditoria_editorial_v05/resultado_auditoria.json)
- [Intervalos por UF](outputs/inferencia_espacial_final_v01/incerteza_rmse_bootstrap_uf.csv)
- [Testes Wald UF e Conley HAC](outputs/inferencia_espacial_final_v01/wald_contexto_cluster_e_conley.json)

