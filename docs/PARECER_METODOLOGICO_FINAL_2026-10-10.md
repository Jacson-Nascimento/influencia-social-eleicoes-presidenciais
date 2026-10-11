# Parecer metodológico final — inferência espacial e validação geográfica

**Autor:** Jacson Cruz do Nascimento · **Documento técnico:** 10/10/2026.  
**Base reprodutível:** [inferencia_espacial_final_v01](../outputs/inferencia_espacial_final_v01/).

## Objeto

Avaliação do ganho incremental de médias das quatro variáveis socioeconômicas de municípios vizinhos (k=8), em regressões da competitividade presidencial e, separadamente, da margem assinada, nos segundos turnos de 2018 e 2022. Amostra de 5.565 municípios com covariáveis IBGE completas, TSE/IBGE, efeitos fixos de UF nos ajustes em amostra, validação por cinco divisões que deixam UFs inteiras fora de treinamento.

## Incerteza do ganho de validação: bootstrap por 27 unidades da federação

| Desfecho | Eleição | Peso municipal | Ganho de RMSE | IC 95% por reamostragem de UFs |
|---|---|---|---:|---|
| Competitividade | 2018 | Igual | +1,92% | +0,11% a +4,42% |
| Competitividade | 2018 | População 2017 | **−3,26%** | **−4,54% a −1,63%** |
| Competitividade | 2022 | Igual | +4,99% | +2,57% a +8,10% |
| Competitividade | 2022 | População 2021 | +0,40% | −1,87% a +2,83% |
| Margem assinada | 2018 | Igual | +17,09% | +12,42% a +21,91% |
| Margem assinada | 2018 | População 2017 | −0,89% | −9,71% a +9,17% |
| Margem assinada | 2022 | Igual | +18,53% | +13,91% a +23,12% |
| Margem assinada | 2022 | População 2021 | −1,87% | −12,26% a +9,98% |

Intervalos percentílicos de 4.999 reamostragens da contribuição das 27 UFs inteiras. A reamostragem não considera correlação residual transfronteiriça entre UFs próximas; os folds compartilham conjuntos de treinamento. Os intervalos devem ser tratados como diagnóstico de sensibilidade territorial, não garantia nominal exata de cobertura probabilística.

## Inferência conjunta de coeficientes contextuais: cluster e HAC espacial

| Eleição | Desfecho | Peso | Wald por UF, p (27 grupos) | Conley 100 km, p | Conley 250 km, p |
|---|---|---|---:|---:|---:|
| 2018 | Competitividade | Igual | 0,3892 | 0,0054 | 0,0958 |
| 2018 | Competitividade | População | 0,1459 | 0,0352 | 0,0393 |
| 2022 | Competitividade | Igual | 0,2413 | 0,0002 | 0,0206 |
| 2022 | Competitividade | População | 0,0005 | menor que 0,0001 | 0,0003 |
| 2018 | Margem assinada | Igual | menor que 0,0001 | menor que 0,0001 | menor que 0,0001 |
| 2018 | Margem assinada | População | 0,0006 | menor que 0,0001 | menor que 0,0001 |
| 2022 | Margem assinada | Igual | menor que 0,0001 | menor que 0,0001 | menor que 0,0001 |
| 2022 | Margem assinada | População | 0,0007 | menor que 0,0001 | menor que 0,0001 |

O Wald da amostra ajustada pergunta se as quatro covariáveis de contexto têm coeficientes conjuntamente nulos sob determinada hipótese de covariância. O RMSE de validação pergunta se acrescentá-las melhora o desempenho em UFs não usadas no treino. **São perguntas distintas** e podem produzir respostas aparentemente discordantes. É possível observar coeficientes associados à votação e ainda não obter melhoria de generalização populacional.

O cálculo Conley usa kernel Bartlett sobre distâncias de centroides com raios 100/250 km; o ajuste por UF usa matriz CR1, teste conjunto F de quatro coeficientes com 26 graus de liberdade denominador. Os pressupostos assintóticos e a quantidade de clusters (27) exigem cautela. A metodologia de Cameron e Miller (2015) e Conley (1999) fundamenta essa abordagem; os valores-p não eliminam confundimento ou endogeneidade.

## Implicações para o manuscrito

- Evitar expressões como “efeito positivo de vizinhança” ou “poder preditivo superior comprovado” sem ressalvas. Preferir: “informação contextual incrementa o ajuste dentro da amostra, mas o ganho de validação depende do desfecho, dos pesos e da composição dos municípios”.
- Não escolher um único teste de significância com base no menor valor-p. Reportar a fragilidade dos critérios e a diferença entre análise por estados e dependência espacial por distância.
- Manter o HHI apenas como complemento, pois competitividade simétrica e direção de preferência não são equivalentes.
- Documentar as cinco exclusões sem imputação.
- Documentar a ressalva factual dos 76 votos **apenas para o primeiro turno de 2018**, sem causa determinada. Os desfechos centrais são derivados de segundos turnos integralmente conciliados.
- Não alegar identificação de manada, influência social causal ou previsão do pleito de 2026.

## Referências metodológicas

CAMERON, A. C.; MILLER, D. L. A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, 50(2), 317–372, 2015. https://doi.org/10.3368/jhr.50.2.317.

CONLEY, T. G. GMM estimation with cross sectional dependence. *Journal of Econometrics*, 92(1), 1–45, 1999. https://doi.org/10.1016/S0304-4076(98)00084-0.

## Artefatos

- [Script reproduzível](../scripts/20_inferencia_espacial_validacao.py)
- [Intervalos de reamostragem UF](../outputs/inferencia_espacial_final_v01/incerteza_rmse_bootstrap_uf.csv)
- [Contribuições de SSE e pesos por UF](../outputs/inferencia_espacial_final_v01/erros_validacao_por_uf.csv)
- [Wald com CR1 e Conley](../outputs/inferencia_espacial_final_v01/wald_contexto_cluster_e_conley.json)
- [Manifesto e restrições](../outputs/inferencia_espacial_final_v01/manifesto.json)
