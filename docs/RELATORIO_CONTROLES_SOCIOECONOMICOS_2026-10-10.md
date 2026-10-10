# Controles socioeconômicos e autocorrelação espacial residual da concentração eleitoral municipal

**Relatório empírico, versão 1.0 | 10 de outubro de 2026**  
**Autor:** Jacson Cruz do Nascimento. ORCID: https://orcid.org/0009-0006-6535-9569

## Resumo

A pesquisa investiga se os padrões espaciais de concentração eleitoral identificados nos municípios brasileiros em 2018 e 2022 persistem após ajustes por população, urbanização, composição por sexo, atividade econômica e diferenças entre unidades da federação. Os dados são de fontes públicas, os tratamentos estão versionados e os resultados são reproduzidos em GitHub Actions. Utiliza-se o índice Herfindahl-Hirschman (HHI) calculado por município, eleição e turno. Quatro regressões OLS foram ajustadas para 5.565 municípios com controles completos. O incremento do coeficiente de determinação ao incluir controles em modelos com efeitos fixos por UF ficou entre 0,0231 e 0,0458. O Moran I dos resíduos permaneceu positivo, de 0,4246 a 0,4825 para oito vizinhos. O resultado sustenta a presença de associação territorial não explicada pelos quatro controles estudados, **sem identificar contágio interpessoal ou comportamento causal de manada**.

## Fontes e proveniência

- Tribunal Superior Eleitoral, resultados presidenciais agregados por município e candidatura em 2018 e 2022. Os totais de 2022 estão conciliados; permanece divergência de +76 votos no primeiro turno de 2018 entre o arquivo distribuído e a notícia histórica do TSE. Nenhuma alteração artificial foi feita.
- IBGE, Censo Demográfico 2010, SIDRA tabela 202, variável 93, situação do domicílio e sexo. Consulta: https://apisidra.ibge.gov.br/values/t/202/n6/all/v/93/p/2010/c1/0,1/c2/0,5?formato=json
- IBGE, Produto Interno Bruto dos Municípios, SIDRA tabela 5938, variável 37, períodos 2016 e 2020: https://apisidra.ibge.gov.br/values/t/5938/n6/all/v/37/p/2016,2020?formato=json
- IBGE, estimativas de população municipal, SIDRA tabela 6579, variável 9324, períodos 2017 e 2021: https://apisidra.ibge.gov.br/values/t/6579/n6/all/v/9324/p/2017,2021?formato=json
- TSE, correspondência oficial dos códigos municipais TSE-IBGE de outubro de 2026; IBGE, malha municipal digital de 2022. Links e hashes em [manifesto de dados espaciais](../outputs/municipal_v01/manifesto.json).

**Regra temporal:** para 2018 utilizam-se população de 2017 e PIB de 2016; para 2022, população de 2021 e PIB de 2020. Composição urbana e por sexo é do Censo 2010. Os indicadores têm período de referência anterior às eleições, mas as versões SIDRA acessadas em outubro de 2026 podem incluir revisões retrospectivas. Consequentemente, este exercício não constitui backtest com informações estritamente disponíveis em tempo real.

**Proporção de urbanização:** residentes em situação urbana / total de residentes de 2010.  
**Proporção feminina:** residentes mulheres / total de residentes de 2010.  
**Proxy de PIB por pessoa:** PIB municipal em mil reais, multiplicado por 1.000, dividido pela estimativa de população do ano seguinte. Essa composição com anos distintos **não é o PIB per capita oficial do IBGE**.

## Amostra e decisões de controle

Os 5.570 municípios brasileiros estão vinculados sem perdas nos dados eleitorais. Cinco municípios têm variáveis censitárias de 2010 ausentes, correspondentes aos códigos IBGE 5006275, 1504752, 4314548, 4220000 e 4212650. Foram excluídos, sem imputação, mantendo-se a mesma amostra balanceada de **5.565 municípios** em todos os quatro modelos. As unidades eleitorais do exterior (UF ZZ) não integram os modelos municipais.

Preservaram-se as versões v01 da coleta preliminar do IBGE, cuja consulta do Censo 2010 retornava categorias incorretas e valores ausentes. A coleta corrigida v02 foi auditada e publicada separadamente. Os arquivos brutos de cada fonte, metadados de origem e hashes de integridade estão versionados em [data/ibge_brutos/sidra_v02](../data/ibge_brutos/sidra_v02) e [manifesto de controles IBGE](../outputs/controles_ibge_v02/manifesto.json).

## Estratégia de estimação

Para cada combinação eleição-turno, ajustaram-se:

- **Modelo A:** HHI municipal explicado apenas por intercepto e efeitos fixos de UF.
- **Modelo B:** Modelo A acrescido de logaritmo da população estimada, logaritmo da proxy de PIB por pessoa, urbanização 2010 e participação feminina 2010. As quatro variáveis foram padronizadas dentro de cada estimação.

As comparações de ajuste são feitas **na mesma amostra e com a mesma variável dependente**. Reportam-se R², R² ajustado e raiz quadrada do erro quadrático médio no próprio conjunto de estimação (RMSE in-sample).

Para investigar a dependência espacial remanescente, calculou-se Moran I dos resíduos com k=8 municípios mais próximos por centroide da malha IBGE 2022, e k=4/12 como sensibilidades de geometria. Foram feitas 999 permutações dos resíduos **dentro das UFs**, depois de retirar suas médias estaduais, e ajuste de Holm sobre quatro testes de referência no modelo B. Trata-se de diagnóstico de associação espacial dos resíduos; permutar resíduos de regressão estimada não satisfaz automaticamente as hipóteses de um teste inferencial causal exato.

## Ajuste dos modelos

| Eleição | Turno | R² UF | R² UF + controles | Ganho (p.p.) | RMSE UF | RMSE UF + controles |
|---|---|---:|---:|---:|---:|---:|
| 2018 | Primeiro | 0,430305 | 0,459631 | 2,933 | 0,072763 | 0,070866 |
| 2018 | Segundo | 0,436588 | 0,459736 | 2,315 | 0,069427 | 0,067986 |
| 2022 | Primeiro | 0,584551 | 0,630383 | 4,583 | 0,058566 | 0,055242 |
| 2022 | Segundo | 0,513191 | 0,550496 | 3,731 | 0,057360 | 0,055119 |

A inclusão de covariáveis melhorou o ajuste nas quatro regressões. O aumento de R² é relativamente limitado frente à variação previamente explicada pelos efeitos fixos estaduais. R² não é evidência de causalidade nem, isoladamente, de validade preditiva.

## Associação espacial dos resíduos

| Eleição | Turno | Moran I residual Modelo A | Moran I residual Modelo B | p bruto B | p ajustado Holm B |
|---|---|---:|---:|---:|---:|
| 2018 | Primeiro | 0,434408 | 0,424564 | 0,001 | 0,004 |
| 2018 | Segundo | 0,486948 | 0,482530 | 0,001 | 0,004 |
| 2022 | Primeiro | 0,484598 | 0,462113 | 0,001 | 0,004 |
| 2022 | Segundo | 0,486891 | 0,471168 | 0,001 | 0,004 |

A referência com k=8 indica que a associação residual espacial permanece elevada após inclusão de população, proxy de atividade econômica, urbanização, proporção feminina e UF. Os resultados dos resíduos controlados também foram positivos com k=4 e k=12. As estatísticas são condicionais à especificação e não afastam confundimento por fatores socioeconômicos, culturais ou institucionais não medidos, não linearidades e dependência estrutural.

## Validação geográfica suplementar

Separadamente das regressões com efeitos fixos, verificou-se o erro de um modelo sem covariáveis (média de treinamento) contra um modelo linear com quatro covariáveis. Foram utilizados cinco folds compostos por **UFs inteiras deixadas de fora**, sem efeitos fixos estaduais, pois sua previsão seria indefinida quando uma UF não aparece no treinamento.

| Eleição | Turno | RMSE média geral | RMSE quatro controles | Redução relativa do RMSE |
|---|---|---:|---:|---:|
| 2018 | Primeiro | 0,102750 | 0,094139 | 8,38% |
| 2018 | Segundo | 0,097107 | 0,087360 | 10,04% |
| 2022 | Primeiro | 0,098423 | 0,077782 | 20,97% |
| 2022 | Segundo | 0,087683 | 0,072545 | 17,26% |

A melhora agregada não foi uniforme entre folds. Em 2018, primeiro turno, duas das cinco divisões apresentaram erro maior com controles; no segundo turno, uma. Em 2022, primeiro turno, nenhuma; no segundo turno, duas. Os grupos de UFs foram definidos por partição determinística da lista ordenada de siglas, e não são amostras independentes dos municípios de uma eleição futura.

**Advertência comparativa:** o teste geográfico confronta média global com controles sem efeitos fixos, enquanto o R² anterior confronta UF fixo com UF fixo acrescido de controles; tratam-se de experimentos distintos. Não interpretar os resultados como validação de previsão de candidaturas, votos ou vencedores de 2026. A variável estimada é a concentração de votos de eleições já encerradas.

## Alcance das conclusões

Há evidência descritiva, neste desenho, de que associação espacial de concentração eleitoral persiste após a inclusão dos quatro controles especificados. Não foi demonstrado mecanismo causal de influência social, comportamento de manada, efeito de vizinhos sobre indivíduos, transferência individual de votos ou capacidade de antecipar o resultado de uma eleição. A persistência geográfica pode refletir processos históricos e sociais não mensurados. A centralização por UF e as variáveis incluídas não bastam para controlar todos os fatores de confusão. O grande N municipal não substitui o número limitado de eleições presidenciais históricas independentes.

A extrapolação do modelo original de manada organizacional exigiria parametrização própria, dados sobre redes de interação e desenho de identificação adequado. O projeto presente permanece separado metodologicamente, com artefatos e fontes públicos próprios.

## Limitações e continuidade

O HHI aumenta mecanicamente quando o número de candidaturas diminui entre turnos; comparar magnitudes absolutas de turnos ou eleições diferentes exige cautela. As matrizes de vizinhança por centroide dependem da geometria, da definição de k e de seus parâmetros. A amostra de 2018 mantém ressalva documental de 76 votos. O PIB dividido pela população estimada de ano diferente é proxy aproximada, sujeita a viés de denominador; os dados censitários de 2010 podem não representar composição contemporânea. As fontes foram consultadas em 2026 e podem ter sido revisadas.

Próxima etapa para avaliação científica: adicionar outras variáveis justificadas empiricamente, testar especificações não lineares e matrizes de contiguidade territorial, avaliar agrupamentos de erros e dependência geográfica, e selecionar um modelo de referência pré-especificado para avaliação fora da amostra temporal quando for viável. Modelos espaciais não devem ser comparados de modo a permitir vazamento de votos observados no teste.

## Artefatos

- [Controle IBGE, dados derivados](../data/ibge_tratados/controles_pre_eleitorais_v02.csv)
- [Manifesto IBGE e hashes](../outputs/controles_ibge_v02/manifesto.json)
- [Script de coleta SIDRA](../scripts/12_coletar_controles_ibge.py)
- [Script de regressões e autocorrelação](../scripts/13_modelos_controles_socioeconomicos.py)
- [Resultados e Moran residual](../outputs/socioeconomico_v01/modelos_e_moran_residual.csv)
- [Validação geográfica com folds de UF](../outputs/socioeconomico_v01/cv_ufs.json)
- [Coeficientes padronizados descritivos](../outputs/socioeconomico_v01/coeficientes_padronizados_descritivos.csv)
- [Manifesto das especificações e exclusões](../outputs/socioeconomico_v01/manifesto_controles_e_modelos.json)
- [Execução aprovada no GitHub Actions](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/actions/runs/38070344384)
