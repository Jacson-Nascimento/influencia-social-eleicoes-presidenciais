# Fechamento analítico preliminar — eleições presidenciais 2002–2022

**Autor:** Jacson Cruz do Nascimento. **Data:** 12/10/2026.  
**Status:** análises concluídas em repositório, redação do manuscrito ainda **não atualizada**. 1998 definitivamente excluído deste estudo. Versão v15 de 2014–2022 preservada.

## Metodologia bibliográfica e decisão censitária

A literatura de geografia eleitoral municipal documenta a utilidade de covariáveis territoriais e atenção à continuidade das unidades, sem estabelecer uma convenção única aplicável a todos os estudos:

- SOARES, G. A. D.; TERRON, S. L. *Dois Lulas: a geografia eleitoral da reeleição*. **Opinião Pública**, 14(2), 269–301, 2008. DOI: https://doi.org/10.1590/S0104-62762008000200001. Identifica trabalho comparável de geografia eleitoral municipal. Não se atribui a ele uma regra específica de substituição censitária sem confirmar a seção metodológica exata.
- EHRL, P. *Minimum comparable areas for the period 1872–2010: an aggregation of Brazilian municipalities*. **Estudos Econômicos**, 47(1), 215–229, 2017. DOI https://doi.org/10.1590/0101-416147182phe. Desenvolve **Áreas Mínimas Comparáveis (AMC)**, pertinentes às mudanças de limites entre os censos.
- IBGE, *Evolução da Divisão Territorial do Brasil, 1872–2010*, https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15771-evolucao-da-divisao-territorial-do-brasil.html; contém informação histórica de emancipações e alterações, mas **AMC não foi construída** no projeto.

**Critério preferido com censo estritamente antecedente:** Censo 2000 em 2002, 2006 e 2010; Censo 2010 em 2014, 2018 e 2022. Para 2010 a aplicação do próprio Censo 2010 é cenário retrospectivo de sensibilidade, não especificação antecedente. Para 2014 também foi estimada sensibilidade mantendo Censo 2000, para examinar quebra de vintage. Em anos posteriores, o Censo 2010 é mantido como referência demográfica comparável, reconhecendo defasagem crescente.

## Dados e resultados

- **Amostra comum de seis eleições:** 5.506 municípios × 6 pleitos = **33.036 observações**. Segundo turno de 2002, 2006, 2010, 2014, 2018 e 2022. Sem 1998.
- 2002 possui código TSE/MT 91065 sem vínculo à malha atual; não imputar. Em 2010, identificar votação em trânsito **VT** e exterior **ZZ** sem associá-las a municípios. As apurações territoriais são distintas dos totais nacionais, que incluem esses registros.
- **Modelo nuclear de seis pleitos:** log população anterior, urbanização e fração feminina do censo anterior, quatro dummies macrorregião, comparando contra acréscimo de médias IBGE dos oito vizinhos mais próximos (centroides de 2022). OLS C/M, logit fracionário C; pesos iguais/população. Fora da amostra por 5 folds de UFs e teste temporal expansivo. Bootstrap por UF (4.999).
- PIB fica **fora do modelo nuclear** porque PIB 2000 não foi obtido da série homogênea SIDRA 5938; não imputar. Na robustez de cinco eleições 2006–2022 com PIB 2004/2008/2012/2016/2020, amostra homogênea de 5.505 municípios.

### Resultados: validação geográfica, pesos iguais, OLS

| Ano | C (% ganho RMSE) censo estritamente antecedente | M (% ganho RMSE) censo estritamente antecedente |
|---|---:|---:|
| 2002 | +1,81 | +0,23 |
| 2006 | +0,59 | +1,20 |
| 2010 | −0,59 | +0,08 |
| 2014 | −0,92 | +1,54 |
| 2018 | −1,16 | +0,96 |
| 2022 | −0,54 | +0,09 |

Todos os intervalos exploratórios por UF de 95% das **12 comparações** incluem zero. Ganhos relativos são definidos **dentro do mesmo desfecho, ano e esquema de peso**, não comparando RMSE diretamente entre C e M.

### Teste de troca censitária em 2010, mesma amostra (5.506)

| Variável | Censo 2000 antecedente (% ganho) | Censo 2010 retrospectivo (% ganho) |
|---|---:|---:|
| C, pesos iguais, OLS | −0,59 | −0,31 |
| M, pesos iguais, OLS | +0,08 | +0,14 |

A troca isolada de vintage produz alteração, sem resultado robusto distinto nesses dois casos.

### Sensibilidade de 2014 com Censo 2000 fixo, amostra PIB 2006–2022 (5.505)

| Modelo M, validação por UF, pesos iguais | Censo 2000 | Censo 2010 |
|---|---:|---:|
| 3 controles | +0,55% | +1,54% |
| 4 controles com PIB | +2,48% | +2,89% |

Todos os ICs de 3 controles em 2014 incluem zero; os modelos de 4 controles com Censo 2010 têm limite inferior próximo de zero no bootstrap UF.

### Transferência temporal para 2022: 3 contra 4 controles, AMOSTRA FIXA de 5.505 municípios

Treinamento 2006+2010+2014+2018, teste 2022, desfecho M, pesos iguais, OLS:

| Controles | Ganho RMSE contextual | IC 95% por UF |
|---|---:|---|
| 3, sem PIB | +2,67% | [−0,64%; +5,35%] |
| 4, com PIB | −2,12% | [−5,68%; +0,74%] |

A mudança de sinal ao incluir PIB mostra **sensibilidade de especificação**, não evidência de melhora estável nem diferença estatisticamente comprovada entre as especificações. Ambos os intervalos incluem zero.

## Diretórios principais e estado de execução

- [Painel de seis eleições + manifesto TSE/IBGE](../outputs/painel_censos_2002_2022_v01/)
- [Estimativas principais com censo antecedente](../outputs/modelos_seis_eleicoes_censo_precedente_v01/)
- [Estimativas alternativas 2010 com censo do mesmo ano](../outputs/seis_eleicoes_censo_v01/)
- [Teste de Censo 2000 fixo](../outputs/sensibilidade_censo_fixo_2000_v01/)
- [Contraste 3 versus 4 controles e vintage de 2014](../outputs/robustez_censo_pib_2006_2022_v01/)
- [PIB 2006–2022 com amostra 5.505](../outputs/robustez_historica_full4_2006_2022_v01/)
- [Código novo](../scripts/36_seis_eleicoes_censo_2000_2010.py)
- [Código robustez PIB](../scripts/37_sensibilidade_censo_pib.py)

Os resultados foram executados e versionados via GitHub Actions. Isso não constitui revisão científica independente.

## O que falta para gerar manuscrito v16

1. **Conciliação externa final:** confrontar todas as totalizações nacionais/municipais de 2002, 2006 e 2010 contra fontes históricas TSE e documentação de VT/ZZ, incluindo exceção municipal MT 91065; registrar evidências e critérios em tabela do apêndice.
2. **Harmonização territorial:** obter e aplicar, se possível, crosswalk de AMCs (IBGE/Ipea) para 2000–2010. Enquanto não for executado, não chamar a amostra de 5.506 geocódigos de regiões perfeitamente comparáveis; documentar alterações de limites e estimar ao menos restrição territorial.
3. **Padronizar resultados oficiais para a redação:** principal = censo estritamente antecedente e 3 controles, 5.506 municípios; robustez = 2010 Censo 2010 retrospectivo, Censo 2000 fixo, PIB 2006–2022 com 5.505. Não misturar amostras nem submeter tabelas redundantes como principal.
4. **Reescrever texto editorial integralmente:** título e recorte 2002–2022; Abstract só inglês; pergunta/hipóteses e motivação; nova base e fórmula C/M; tabelas de 6 eleições com ICs; figura temporal; discussão da quebra censitária e impacto do PIB; atualizar conclusão sem afirmação de contágio/causalidade.
5. **Atualizar referências:** Soares/Terron, Ehrl e documentos IBGE/TSE verificáveis; manter a dissertação de Nascimento (2024) como antecedente delimitado; conferir os três artigos brasileiros recentes antes da submissão.
6. **Publicar replicação completa:** códigos, hashes, manifestos, proveniência de PIB/proxy, amostras excluídas, critérios de covariância; controle de dados sensíveis, declaração transparente de uso de IA e revisão humana.
7. **Revisão externa de novo artigo e normas da revista:** conferir manuscrito Word/PDF, tabelas e limitações; não atribuir nota acadêmica automaticamente; versões v14 e v15 intocadas.

**Conclusão analítica:** ampliação acrescenta amplitude temporal e sensibilidade metodológica importante, mas não mostra ganhos contextuais robustos e generalizáveis nos seis pleitos com três controles. A interpretação exata depende de especificação, peso, vintage censitária e unidade territorial. Não há identificação de influência interpessoal ou mecanismo causal.
