# Sensibilidade da competitividade à ponderação por votos válidos municipais

**Jacson Cruz do Nascimento**  
ORCID: https://orcid.org/0009-0006-6535-9569  
Data: 10/10/2026. Relatório complementar ao artigo sobre competitividade eleitoral.

## Pergunta

O ganho explicativo do contexto socioeconômico dos municípios vizinhos persiste quando municípios com maior votação válida recebem maior peso na estimação e na validação geográfica?

## Fontes e desenho

Votos nominais de segundo turno do TSE (2018 e 2022), correspondência de códigos TSE-IBGE, covariáveis IBGE de anos de referência antecedentes, malha municipal IBGE 2022. A mesma amostra de 5.565 municípios foi utilizada nos modelos ponderados e não ponderados. O indicador principal é `C_i=1-|v13-vop|/(v13+vop)`; a análise direcional usa `M_i=(v13-vop)/(v13+vop)`.

O **peso de cada município** é seu total de votos nominais válidos do segundo turno, extraído da fonte oficial. Na amostra estimada, a soma dos pesos é de 104.622.798 em 2018 e 118.217.929 em 2022. São totais da amostra nacional com cinco municípios excluídos por covariáveis incompletas, e também excluem o exterior; portanto, **não se devem confundir com a totalização nacional oficial**.

Os modelos são regressões ponderadas por mínimos quadrados (WLS), com intercepto, efeitos fixos por UF e quatro covariáveis locais (log população estimada, log proxy de PIB por pessoa, urbanização 2010 e participação feminina 2010). A extensão contextual acrescenta médias dos atributos dos k municípios próximos por centroide, com k=8 como especificação principal e k=4/12 como sensibilidades.

A validação mantém grupos inteiros de UFs fora da estimação e não utiliza efeitos fixos estaduais nos dois modelos comparados. A métrica de validação é RMSE ponderado pelo total de votos válidos municipais. O uso desses pesos medidos após a eleição é apropriado apenas como análise retrospectiva de representatividade; **não é previsão ex ante**.

## Comparação principal, oito municípios vizinhos

| Desfecho | Ano | Delta R² in-sample ponderado (p.p.) | RMSE ponderado local | RMSE ponderado com contexto | Melhora relativa de RMSE | Dobras com piora |
|---|---|---:|---:|---:|---:|---:|
| Competitividade | 2018 | +1,943 | 0,189104 | 0,195304 | -3,28% | 5/5 |
| Competitividade | 2022 | +1,450 | 0,160356 | 0,159815 | +0,34% | 3/5 |
| Margem assinada | 2018 | +1,687 | 0,268516 | 0,269945 | -0,53% | 2/5 |
| Margem assinada | 2022 | +3,123 | 0,245474 | 0,249942 | -1,82% | 2/5 |

Valor negativo na melhoria significa **aumento do erro de validação**.

Nas especificações sem ponderação municipal, os ganhos foram, respectivamente: competitividade +1,92% (2018) e +4,99% (2022); margem assinada +17,09% (2018) e +18,53% (2022). As duas análises usam a mesma amostra, mas funções de perda e coeficientes ajustados diferentes. Elas respondem a prioridades de agregação distintas.

## Sensibilidade da ponderação à vizinhança

| Desfecho/ano | Melhora RMSE k=4 | k=8 | k=12 |
|---|---:|---:|---:|
| Competitividade 2018 | -1,89% | -3,28% | -4,61% |
| Competitividade 2022 | +0,98% | +0,34% | +0,16% |
| Margem assinada 2018 | -5,90% | -0,53% | +5,14% |
| Margem assinada 2022 | -5,67% | -1,82% | +4,41% |

O sinal da melhoria depende da especificação: a competitividade ponderada piora em 2018 com k=4,8,12; em 2022 melhora apenas marginalmente; a margem assinada melhora em k=12, mas piora em k=4 e k=8 nos dois anos. Assim, **a contribuição dos atributos de vizinhança não é estável entre escalas territoriais, escolhas de k e definição de pesos**.

## Consequências para a conclusão do artigo

1. O modelo contextual acrescenta regressores e, na mesma amostra, melhora mecanicamente ou preserva R² dentro da amostra. Isso não autoriza alegar superioridade de generalização.
2. Em municípios tratados como unidades de igual importância, houve ganho agregado do RMSE ao introduzir atributos dos vizinhos.
3. Quando a função de perda prioriza localidades com mais votos válidos, esse ganho praticamente desaparece ou se converte em piora.
4. O resultado impede afirmar que o contexto espacial socioeconômico melhora genericamente a capacidade de explicar a competitividade ou a direção da votação.
5. O contraste é, ele próprio, um achado metodológico: avaliações territoriais e avaliações ponderadas pela dimensão eleitoral podem produzir conclusões opostas.
6. O experimento é não causal. A análise não testa transmissão interpessoal e não utiliza votos vizinhos como variáveis explicativas.

## Restrições

Os pesos são o número de votos válidos observados no segundo turno, e sua utilização não implica disponibilidade antes da eleição. A validação geográfica com cinco folds não equivale à validação temporal de uma eleição independente. PIB/população é proxy de anos diferentes, as versões do IBGE foram baixadas em 2026 e podem ter revisões; cinco municípios são excluídos por falta de informações censitárias. O HHI original do estudo anterior não é a variável dependente desta versão. Os votos no exterior não entram na amostra municipal, e o primeiro turno de 2018 permanece com ressalva documental de 76 votos no arquivo do TSE.

## Replicação

- [Script de sensibilidade WLS](../scripts/17_sensibilidade_ponderacao_eleitoral.py).
- [Workflow GitHub Actions](../.github/workflows/sensibilidade_competitividade_pesos_v01.yml).
- [Saída auditada de modelos WLS](../outputs/competitividade_ponderada_v01/modelos_ponderados_competitividade_e_direcao.csv).
- [Validação geográfica detalhada](../outputs/competitividade_ponderada_v01/validacao_ponderada_ufs.json).
- [Manifesto](../outputs/competitividade_ponderada_v01/manifesto.json).
- [Modelos não ponderados](../outputs/competitividade_modelos_v01/modelos_competitividade_e_direcao_k4_k8_k12.csv).
