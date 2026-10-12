# Consolidado para atualização do manuscrito — painel presidencial 2002–2022

**Data:** 12/10/2026. **Autor:** Jacson Cruz do Nascimento.

**Escopo:** resultados de 2002, 2006, 2010, 2014, 2018 e 2022. A eleição de 1998 foi excluída. A v15 (2014–2022) foi preservada.

## Base longitudinal principal

- 5.506 municípios em todos os seis pleitos = 33.036 observações município-eleição.
- Controle demográfico: último Censo **anterior** ao pleito, isto é, Censo 2000 para 2002/2006/2010 e Censo 2010 para 2014/2018/2022.
- População estimada do ano pré-eleitoral: 2001, 2005, 2009, 2013, 2017 e 2021.
- Modelo comum: log população, fração urbana censitária e fração feminina censitária, mais quatro macrorregiões, versus adição das médias dos três atributos de oito municípios vizinhos.
- Regra confirmada em Rafael Georges da Cruz, *Democracy and Social Policies for Inequality Reduction in Brazil: Representatives Policies' Congruence and Relevance – 1998–2018* (Universidade de Brasília, tese, 2019, p. 43; advertência sobre quebra censitária, p. 47): https://repositorio.unb.br/bitstream/10482/38312/1/2019_RafaelGeorgesdaCruz.pdf.

### Variação de RMSE com pesos iguais (%) — por UF omitida

| Eleição | C | M |
|---|---:|---:|
| 2002 | +1,81 | +0,23 |
| 2006 | +0,59 | +1,20 |
| 2010 | −0,59 | +0,08 |
| 2014 | −0,92 | +1,54 |
| 2018 | −1,16 | +0,96 |
| 2022 | −0,54 | +0,09 |

**Nenhum dos 12 IC 95% bootstrap de UF para essa especificação tem limite inferior maior que zero.** Os pontos estimados são sensíveis às covariáveis e à ponderação.

### Conciliação de cobertura

Os 5.506 municípios retêm, respectivamente, **99,775%, 99,761%, 99,746%, 99,732%, 99,716% e 99,707%** dos votos municipais do segundo turno, em 2002/2006/2010/2014/2018/2022.

- 2010: os 53.035 votos com código `VT` e os 81.025 votos de `ZZ` (exterior) não foram atribuídos a municípios.
- 2002: 869 votos de chave histórica sem correspondência direta ao cadastro atual; não foram imputados.
- A cobertura superior a 99,7% não corrige automaticamente a composição geográfica dos excluídos.
- Fonte: [auditoria de cobertura](../outputs/cobertura_amostra_2002_2022_v01/cobertura_votos_amostra_comum.csv).

## Robustez por renda proxy e Censo

Para isolar a inclusão da variável econômica foi utilizada amostra idêntica de **5.505 municípios**, cinco pleitos de 2006 a 2022, com e sem PIB. O PIB foi excluído da análise longitudinal de seis pleitos porque o PIB 2000 não consta da mesma tabela SIDRA 5938; a existência da **série histórica distinta do IBGE (1999–2002)** foi verificada e deverá ser pesquisada para a última checagem de comparabilidade: https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html.

| Pleito | M com 3 controles (ganho RMSE %, por UF) | M com 4 controles (ganho RMSE %, por UF) |
|---|---:|---:|
| 2006 | +1,19 | +3,16 |
| 2010 | +0,08 | +2,78 |
| 2014 | +1,54 | +2,89 |
| 2018 | +0,95 | +4,92 |
| 2022 | +0,09 | +4,55 |

Não apresentar diferenças como efeito causal do PIB. Na validação temporal com quatro controles, o acréscimo de vizinhança para a competitividade C apresentou **−7,93% em 2014** e **−3,93% em 2018**. O teste alternativo usando o Censo 2000 também no teste de 2014 produziu −7,86% para C, de modo que a ruptura censitária não explica isoladamente os resultados negativos de generalização.

Scripts / resultados:
- [Modelos principais seis pleitos](../scripts/36_modelos_seis_eleicoes_censo_anterior.py); [geográfica](../outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_geografica_2002_2022.csv); [temporal](../outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_temporal_2002_2022.csv).
- [Robustez censitária/econômica](../scripts/37_sensibilidade_censo_pib.py); [resultado 3 vs 4](../outputs/robustez_censo_pib_2006_2022_v01/geo_tres_quatro_controles.csv); [sensibilidade 2014](../outputs/robustez_censo_pib_2006_2022_v01/censo_vintage_2014.csv).
- [Auditoria de retenção eleitoral](../scripts/38_auditar_cobertura_municipal.py).

## O que falta para atualizar o artigo de forma defensável

1. **Conciliação histórica:** confrontar formalmente as totalizações por candidatura de 2002, 2006 e 2010 com publicações do TSE, além da já realizada conferência computacional dos arquivos.
2. **PIB de 2000:** consultar e checar a série histórica independente do IBGE 1999–2002; decidir se é comparável e, se não, documentar a justificativa de exclusão.
3. **Território:** caracterizar municípios sem controles completos e chaves sem correspondente, e documentar os efeitos do uso de centroides da malha de 2022.
4. **Escrita integrada:** atualizar título, Abstract único em inglês, pergunta, metodologia, tabelas, Discussão, Considerações Finais e bibliografia para seis pleitos. Indicar que tabelas antigas de v15 usam amostra e conjunto de controles distintos.
5. **Revisão antes da submissão:** conferir referências, declaração de IA, todas as figuras, disponibilidade de dados, paginação e exigências do periódico.

Nenhum modelo identifica causalidade ou contágio social. Não é apropriado aumentar a avaliação editorial automaticamente em função do número de pleitos.

**Arquivo adicional gerado localmente:** `Nota_Tecnica_Atualizacao_Artigo_2002_2022_v16.docx` (5 páginas) e PDF correspondente; a versão anterior do artigo não foi sobrescrita.
