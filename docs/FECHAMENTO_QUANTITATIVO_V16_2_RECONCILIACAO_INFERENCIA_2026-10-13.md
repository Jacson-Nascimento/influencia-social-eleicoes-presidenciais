# Fechamento quantitativo v16.2 - reconciliação e inferência espacial

**Data:** 13/10/2026. **Autor:** Jacson Cruz do Nascimento.
**Escopo:** seis segundos turnos presidenciais (2002/2006/2010/2014/2018/2022). A eleição de 1998 segue **excluída**. V12, v15, v16, v16.1 e saídas anteriores preservadas. Não submetido.

## 1. Reconciliação controlada da margem assinada M

Fonte efetivamente consultada: `outputs/robustez_censo_pib_2006_2022_v01/geo_tres_quatro_controles.csv`. Dentro da **mesma amostra de 5.505 municípios**, mesma avaliação geográfica por UF, OLS e pesos iguais:

| Ano | 3 controles sem PIB, ganho RMSE e IC 95% | 4 controles com proxy PIB, ganho RMSE e IC 95% | V12 em amostra de 5.565 (não comparável diretamente) |
|--|--|--|--|
| 2018 | +0,950109% [−2,215326%; +3,815521%] | +4,924696% [+1,470237%; +7,559967%] | +4,67% |
| 2022 | +0,088284% [−2,002598%; +2,901005%] | +4,548062% [+0,853378%; +7,067326%] | +4,47% |

Diferença de ganho em mesma amostra: +3,974587 p.p. (2018) e +4,459778 p.p. (2022) ao incluir PIB. O ganho da versão **principal** v16, 5.506 municípios e três controles, foi +0,956489% (2018) e +0,087396% (2022). O uso de uma quarta covariável constitui uma sensibilidade de especificação, **não efeito causal de PIB**. A reconciliação **não está integralmente concluída**, pois as v12/v16 diferem também em 59 municípios, vintage, população, atributos de vizinhança e outros detalhes.

## 2. Reestimação própria CR1 e Conley para v16 (CONCLUÍDA)

Workflow: `.github/workflows/reconciliacao_inferencia_espacial_v16_v01.yml`.
Script: `scripts/43_reconciliacao_inferencia_espacial_v16.py`.
Execução GitHub Actions **sucesso**, run: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/actions/runs/38394453752.
Saídas: `outputs/reconciliacao_inferencia_espacial_v16_v01/`, contendo CSVs, 4.999 bootstrap e manifesto com **9 SHA-256 de entrada idênticos à trilha do painel**.

Amostra 5.506 municípios, 27 UFs, seis pleitos, dois desfechos C e M, pesos iguais e populacionais. Regressão linear por eleição: três atributos municipais + quatro dummies regionais + três médias dos oito vizinhos (kNN8). Coeficientes contextuais testados conjuntamente com CR1/UF (F[3,26]) e Conley Bartlett nos cortes de 100/250 km (qui2[3], assintótico). São **24 linhas de teste**.

| Ano | Desfecho | Pesos | p CR1/UF | p Conley 250 km |
|--|--|--|--:|--:|
| 2018 | C | uniformes | 0,176578 | 0,151579 |
| 2018 | M | uniformes | 0,000606 | <0,000001 |
| 2022 | C | uniformes | 0,179884 | 0,039150 |
| 2022 | M | uniformes | 0,000055 | <0,000001 |

**Esses testes são de associação de coeficientes DENTRO da amostra. Não são testes de melhora de RMSE fora da amostra.** A relevância estatística é sensível a ponderação, raio e multiplicidade. CR1 não resolve correlação entre UFs, Conley não elimina endogeneidade; efeitos temporais conjuntos não foram corrigidos.

## 3. Exclusão espacial no treinamento (CONCLUÍDA)

24 comparações de validação para 2018/2022, C/M, pesos uniformes/populacionais e buffers de 0/100/250 km. **Buffer de 0 km conferido automaticamente contra o CSV anterior** `validacao_geografica_2002_2022.csv` com tolerância 2e-6 pontos percentuais.

| Ano | M, pesos uniformes, buffer | Ganho RMSE | IC 95% exploratório |
|--|--|--:|--|
| 2018 | 0 km | +0,956489% | [−2,244926%; +3,817418%] |
| 2018 | 100 km | +2,312978% | [−0,699021%; +5,368156%] |
| 2018 | 250 km | **−3,700891%** | [−5,388083%; −0,698537%] |
| 2022 | 0 km | +0,087396% | [−2,051267%; +2,883554%] |
| 2022 | 100 km | +0,676182% | [−1,690010%; +3,926616%] |
| 2022 | 250 km | **−3,840103%** | [−5,632577%; −1,358711%] |

Com 250 km, os mínimos de treino por fold caem de 3.565 para 1.858, enquanto todas as UFs de teste permanecem fora do treino. Os resultados com buffer mudam **a composição e o tamanho do treinamento**, não isolam efeito causal da proximidade. Os intervalos UF de 95% continuam condicionais à escolha dos folds e assumem limitações de dependência espacial.

## 4. Síntese e limites

A existência de coeficientes contextuais de M estatisticamente detectáveis em modelos no próprio pleito coexiste com a ausência de melhora preditiva sustentada fora da amostra. Os buffers de 250 km reforçam a fragilidade dos ganhos recentes na especificação uniforme de três controles.

Permanecem antes da submissão: (i) conciliação histórica independente dos votos nacionais/ZZ/VT/TSE e ressalva 2018 primeiro turno 76 votos sem causa identificada; (ii) genealogia municipal e AMCs; (iii) auditoria externa integral do código e dos resultados; (iv) dependência longitudinal e ajuste de múltiplas comparações; (v) ponte completa v12->v16 isolando mudança de amostra, PIB, população e demais covariáveis. Nenhuma alteração de versão antiga e nenhum ajuste arbitrário de votos ou PIB.
