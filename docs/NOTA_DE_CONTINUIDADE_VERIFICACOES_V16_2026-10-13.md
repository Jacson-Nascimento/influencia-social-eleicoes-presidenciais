# Nota de continuidade e verificação documental - v16 (13/10/2026)

**Autor:** Jacson Cruz do Nascimento. **Escopo:** segundo turno presidencial de 2002, 2006, 2010, 2014, 2018 e 2022. 1998 EXCLUÍDA.
**Status:** atualização da revisão metodológica, sem alteração das saídas econométricas existentes. Manuscritos v14/v15 preservados.

## 1. Fonte quantitativa verificada diretamente no GitHub
- `outputs/painel_censos_2002_2022_v01/manifesto.json` (Git blob SHA `3db0421716ccf67b72685ab7de309b7a50e921b4`): 5.506 municípios e 33.036 município-eleições; 3 controles e Censo 2000 em 2002/2006/2010, 2010 em 2014/2018/2022.
- `outputs/modelos_seis_eleicoes_censo_precedente_v01/manifesto.json` (SHA `d94152a9d862673697beb4cbfa8e6782abb75b5d`): 36 cenários geográficos, 30 temporais e 4.999 reamostragens UF.
- `outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_geografica_2002_2022.csv` (SHA `455dd781f057ff68fe8eab02a9de4d18202145be`) e `validacao_temporal_2002_2022.csv` (SHA `1cc344d17817882480d2735e9a61c9133b9462d8`): confirmados os resultados de C e M, especificação OLS, pesos uniformes.
- `outputs/cobertura_amostra_2002_2022_v01/cobertura_votos_amostra_comum.csv` (SHA `49644a9b7449de154e1130ba72533b3c395306ce`): retenção de 99,7071% a 99,7749% dos votos municipais na amostra comum.
- Há uma exceção de sensibilidade a destacar: em 2002+2006 => 2010, desfecho M, OLS ponderado por população, ganho +1,9005824660%, IC exploratório [0,1572638403; 3,0204147218]. Não tratar essa comparação isolada como evidência confirmatória; ajuste multipletestes/dependência espacial não executado.

## 2. Conciliação aritmética interna (não é validação primária independente)
| Ano | Votos nacionais candidatos somados | ZZ | VT | Votos municipais (= nacional - ZZ - VT) | Votos municipais na amostra |
|---|---:|---:|---:|---:|---:|
| 2002 | 86.164.103 | 34.514 | 0 | 86.129.589 | 85.935.731 |
| 2006 | 95.838.220 | 38.860 | 0 | 95.799.360 | 95.569.967 |
| 2010 | 99.463.917 | 81.025 | 53.035 | 99.329.857 | 99.077.924 |

Os três balanços internos fecham exatamente. Em 2002, a chave TSE MT/91065, com 869 votos, continua não atribuída à malha municipal recente; conferir seu desdobramento específico na etapa territorial.

**Pendente P1:** conferir separadamente totalizações históricas por candidatura e rubricas especiais em documentos/datasets primários independentes do TSE; os links https://www.tse.jus.br/eleicoes/resultados-eleicoes/eleicoes-2002 , /eleicoes-2006 e /eleicoes-2010 são entradas oficiais, mas as páginas não trouxeram, nesta verificação, quadros numéricos completos para confronto direto.

## 3. PIB 2000 - decisão técnica provisória
O IBGE mantém publicação *Produto interno bruto dos municípios: 1999-2002* e a série atual de PIB dos municípios foi retropolada até 2002 na referência 2010. Fonte oficial: https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html .

A EXISTÊNCIA histórica de PIB de 2000 não estabelece comparabilidade automática com a série corrente referência 2010, nem a integridade da mesma cobertura e geocodificação. **Manter o PIB fora do modelo nuclear de seis pleitos** até análise documental e quantitativa da compatibilidade. Não imputar.

## 4. Território e AMCs
IBGE, *Evolução da Divisão Territorial do Brasil, 1872-2010*, indica disponibilidade de tabelas genealógicas e desmembramentos: https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15771-evolucao-da-divisao-territorial-do-brasil.html .
Ehrl, P. (2017), DOI https://doi.org/10.1590/0101-416147182phe, documenta rotina AMC para subperíodos 1872-2010. A rotina NÃO cobre automaticamente o ano 2022. Não declarar harmonização territorial integral antes de um crosswalk efetivamente aplicado.

## 5. Decisões
1. Nenhum modelo foi reexecutado; saídas versionadas preservadas.
2. Não houve reconciliação forçada, reatribuição de votos, nem imputação de PIB.
3. A conclusão da análise principal permanece: os ganhos em RMSE fora da amostra não são estáveis nos seis pleitos. Esta nota registra exceções condicionais e limitações.
4. Manuscrito v16 é rascunho acadêmico enquanto P1/P2, inspeção de scripts, revisão integral de literatura e política editorial do periódico não forem concluídos.
5. Ressalva de 76 votos no PRIMEIRO TURNO de 2018 deve constar em nota documental, sem atribuir causa e sem contaminar as medidas do SEGUNDO TURNO.
