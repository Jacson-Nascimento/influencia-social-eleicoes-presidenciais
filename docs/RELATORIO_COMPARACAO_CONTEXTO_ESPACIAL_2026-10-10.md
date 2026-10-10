# Comparação de modelos convencionais e contexto socioespacial municipal

**Relatório empírico v1.0, 10/10/2026**  
**Jacson Cruz do Nascimento**, ORCID: https://orcid.org/0009-0006-6535-9569

## Resumo

A pesquisa analisa se informações socioeconômicas dos municípios próximos acrescentam capacidade explicativa à concentração eleitoral municipal medida pelo índice HHI, após considerar população, proxy de PIB por pessoa, urbanização, proporção feminina e diferenças entre UFs. São analisadas as eleições presidenciais de 2018 e 2022, primeiro e segundo turnos, com 5.565 municípios brasileiros que possuem informações completas. Os modelos locais são confrontados com extensões contextuais que utilizam médias das mesmas quatro características dos municípios próximos. No modelo com oito vizinhos, os acréscimos de R² variam de 0,00365 a 0,00788. A validação por UFs inteiras omitidas do treinamento aponta reduções relativas do RMSE de 0,95%, 2,04%, 7,70% e 5,11% para as quatro combinações ano-turno. Contudo, a redução da autocorrelação residual é muito pequena. Não há evidência de mecanismo causal de contágio; os resultados refletem associação territorial com covariáveis públicas.

## Fontes, amostra e horizonte informacional

O HHI por município foi produzido a partir de dados oficiais de votos nominais presidenciais do TSE. Os códigos eleitorais foram conciliados com o IBGE, sem pareamento aproximado. As variáveis municipais IBGE provêm do Censo 2010 (proporções urbana e feminina), PIB 2016/2020 e estimativas de população 2017/2021. A população e o PIB são defasados em relação a cada eleição, mas foram obtidos em versão disponível em outubro de 2026, sujeita a revisões retrospectivas. A proxy de PIB per capita combina PIB em um ano e população estimada no seguinte e não constitui indicador oficial de PIB per capita.

Dos 5.570 municípios do universo eleitoral brasileiro, cinco foram excluídos por ausência de algumas informações censitárias de 2010, sem imputação: códigos IBGE 5006275, 1504752, 4314548, 4220000 e 4212650. A mesma amostra de 5.565 unidades é usada nos quatro modelos de cada exercício. A base de 2018 mantém ressalva de +76 votos no primeiro turno frente à totalização histórica oficial, sem ajuste arbitrário. A malha municipal utilizada é a de 2022.

## Formulação estatística

Para cada ano e turno, os modelos são:

1. **Referência local:** HHI como função de intercepto, efeitos fixos por UF e quatro covariáveis próprias do município.
2. **Extensão de contexto territorial:** referência local acrescida das médias dessas mesmas quatro covariáveis para os k municípios mais próximos, com k=8 como especificação primária e k=4/12 como sensibilidades.

O conjunto de vizinhos é definido por distâncias aproximadas entre centroides da malha municipal IBGE 2022. Os atributos dos vizinhos **não incluem votos, HHI ou qualquer resultado eleitoral**. Portanto, o estudo não emprega a variável dependente de um município para antecipar a variável dependente de outro.

Para comparação dentro da amostra, cada especificação inclui os mesmos efeitos fixos por UF e a mesma amostra. Os modelos são ajustados por mínimos quadrados ordinários, sem qualquer alegação causal. São reportados R² e Moran I residual. A inclusão de regressores aumenta mecanicamente ou preserva R² in-sample; por isso, o teste mais relevante de generalização é a validação por estados inteiros omitidos.

## Resultado principal, oito vizinhos

| Ano | Turno | R² controles locais + UF | R² mais vizinhos + UF | Delta R² (p.p.) | Moran I residual local | Moran I residual contextual |
|---|---|---:|---:|---:|---:|---:|
| 2018 | 1º | 0,459631 | 0,463530 | +0,390 | 0,424564 | 0,422639 |
| 2018 | 2º | 0,459736 | 0,463383 | +0,365 | 0,482530 | 0,481865 |
| 2022 | 1º | 0,630383 | 0,638265 | +0,788 | 0,462113 | 0,460065 |
| 2022 | 2º | 0,550496 | 0,556975 | +0,648 | 0,471168 | 0,470919 |

Os resultados indicam melhora modesta de ajuste, com persistência praticamente inalterada da associação espacial dos resíduos. **A pequena redução de Moran I não elimina a necessidade de investigar outras características territoriais omitidas.**

## Verificação geográfica suplementar

A validação foi feita em cinco dobras que retêm UFs inteiras fora do treinamento. Como não é possível prever efeitos fixos para uma UF não observada no treino, ambas as especificações **retiram os efeitos fixos por UF neste exercício**, mas preservam os quatro controles locais. O modelo contextual acrescenta médias de controles IBGE dos municípios vizinhos. Os votos e HHIs observados dos municípios de teste não são consultados no ajuste dos parâmetros.

| Ano | Turno | RMSE com controles locais | RMSE com contexto (k=8) | Redução percentual | Dobras com piora |
|---|---|---:|---:|---:|---:|
| 2018 | 1º | 0,094139 | 0,093240 | 0,95% | 1/5 |
| 2018 | 2º | 0,087360 | 0,085581 | 2,04% | 2/5 |
| 2022 | 1º | 0,077782 | 0,071795 | 7,70% | 0/5 |
| 2022 | 2º | 0,072545 | 0,068838 | 5,11% | 0/5 |

O ganho é maior em 2022 que em 2018, mas há apenas dois períodos eleitorais distintos, e cada período é observado com seus dois turnos, que não são independentes. Os cinco folds não equivalem a cinco eleições independentes. Como as covariáveis de municípios de teste estão disponíveis para construir o contexto dos vizinhos, a avaliação é parcialmente transdutiva quanto às características socioeconômicas, sem transmissão de resultados eleitorais de teste. Os indicadores IBGE foram consultados em versão de 2026, de modo que não cabe qualificar esse teste como previsão ex ante em tempo real.

## Sensibilidade a quatro, oito e doze vizinhos

| Ano/turno | Delta R² com k=4 | Com k=8 | Com k=12 | Redução do RMSE CV k=4 | k=8 | k=12 |
|---|---:|---:|---:|---:|---:|---:|
| 2018, 1º | +0,264 p.p. | +0,390 p.p. | +0,531 p.p. | 0,88% | 0,95% | 1,06% |
| 2018, 2º | +0,259 p.p. | +0,365 p.p. | +0,490 p.p. | 1,60% | 2,04% | 2,23% |
| 2022, 1º | +0,597 p.p. | +0,788 p.p. | +0,953 p.p. | 6,08% | 7,70% | 8,69% |
| 2022, 2º | +0,480 p.p. | +0,648 p.p. | +0,793 p.p. | 4,18% | 5,11% | 5,67% |

A ampliação da vizinhança elevou o ganho de ajuste nesses exercícios. Isso pode refletir suavização espacial das características dos territórios, e não maior intensidade de qualquer mecanismo interpessoal de imitação.

## Interpretação científica

Os controles socioeconômicos locais reduziram parte da associação espacial, mas o padrão remanescente permaneceu elevado. Adicionar o contexto socioeconômico dos vizinhos melhorou o ajuste e, em média, a avaliação fora da UF, porém pouco modificou o Moran I dos resíduos. As hipóteses de estrutura territorial e efeitos sociais devem continuar distintas. Proximidade geográfica não identifica rede de interação, exposição midiática, pressão social ou decisões individuais.

A pesquisa ainda não adaptou nem calibrou os parâmetros de influência e silêncio do modelo de manada organizacional para o comportamento eleitoral. Este resultado avalia um **modelo contextual territorial**, não uma versão empiricamente validada da simulação original. A variável HHI mede concentração, não transferência de voto, e sua magnitude é sensível ao número de candidatos no turno.

## Contribuição e limites

A investigação avança metodologicamente ao estabelecer dados eleitorais auditados, correspondência territorial integral, controles públicos, testes espaciais e comparação com validação por UFs inteiras. Por outro lado, ainda não fornece identificação causal de influência social. Serão necessárias matrizes de contiguidade alternativas, variáveis sociais relevantes e validação temporal estrita sem vazamento das versões de dados.

Nenhuma análise estima vencedor, probabilidade de resultado ou preferência individual de eleitores de 2026. Os cálculos são retrospectivos e descritivos.

## Replicação

- Script: [14_comparacao_contexto_espacial.py](../scripts/14_comparacao_contexto_espacial.py).
- Especificações e fonte: [PROTOCOLO_CONTEXTO_ESPACIAL_2026-10-10.md](PROTOCOLO_CONTEXTO_ESPACIAL_2026-10-10.md).
- Tabela comparativa completa: [comparacao_contexto_espacial_k4_k8_k12.csv](../outputs/contexto_espacial_v01/comparacao_contexto_espacial_k4_k8_k12.csv).
- Validação detalhada por UF: [validacao_ufs_detalhada.json](../outputs/contexto_espacial_v01/validacao_ufs_detalhada.json).
- Manifesto metodológico: [metodologia.json](../outputs/contexto_espacial_v01/metodologia.json).
- GitHub Actions: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/actions/runs/38070717205.
