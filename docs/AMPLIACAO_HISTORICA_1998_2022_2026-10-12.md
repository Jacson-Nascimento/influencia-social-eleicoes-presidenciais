# Ampliação histórica da geografia eleitoral brasileira (1998–2022)

**Autor:** Jacson Cruz do Nascimento  
**Data:** 12 de outubro de 2026  
**Situação:** relatório exploratório, não submetido. Manuscritos v14 e v15 não alterados.

## Escopo empírico efetivamente concluído

Foram executados dois estudos complementares:

1. **Seis eleições com segundo turno, 2002–2022:** 5.506 municípios comuns, 33.036 observações município-eleição. Controles: log da população pré-eleitoral, urbanização e proporção feminina do censo anterior, e quatro dummies de macrorregião. PIB excluído do benchmark comum porque a série SIDRA 5938 consultada não disponibiliza PIB de 2000. Indicadores C=1−|M| e M=(v13−voponente)/(v13+voponente), número 13 do PT contra o adversário do segundo turno em cada ano.
2. **Cinco eleições, 2006–2022:** 5.505 municípios comuns, 27.525 observações; os mesmos controles com adição da proxy PIB municipal nominal do ano anterior ao ano da população. É uma **análise de robustez com outra amostra e mais uma covariável**, não uma substituição direta dos resultados de seis eleições.

Em ambos os exercícios, cinco folds omitem UFs inteiras e validam se as médias das covariáveis IBGE nos oito municípios mais próximos (kNN8, centroides IBGE 2022) reduzem RMSE frente ao modelo local e macrorregional. Bootstrap pareado de 27 UFs com 4.999 reamostragens; intervalos exploratórios, não inferência causal.

## Validação geográfica: seis pleitos, pesos iguais, OLS

Ganho de RMSE contextual relativo ao local, entre colchetes IC exploratório de 95%:

| Ano | Competitividade C | Margem M |
|---|---:|---:|
| 2002 | +1,81% [−0,21%; +4,17%] | +0,23% [−1,12%; +1,96%] |
| 2006 | +0,59% [−1,72%; +2,44%] | +1,20% [−2,82%; +3,33%] |
| 2010 | −0,59% [−2,52%; +1,32%] | +0,08% [−2,44%; +2,37%] |
| 2014 | −0,92% [−2,05%; +0,52%] | +1,54% [−2,60%; +4,97%] |
| 2018 | −1,16% [−3,31%; +0,70%] | +0,96% [−2,34%; +3,86%] |
| 2022 | −0,54% [−2,09%; +1,10%] | +0,09% [−2,01%; +2,92%] |

Os doze ICs abrangem zero, não mostrando melhoria contextual uniforme para C ou M nesse benchmark de três controles.

## Validação temporal expansiva, seis pleitos, pesos iguais, OLS

| Treino (somente eleições anteriores) → teste | C, ganho RMSE | M, ganho RMSE |
|---|---:|---:|
| 2002 → 2006 | +0,52% [−0,77%; +1,71%] | +0,32% [−0,36%; +0,99%] |
| 2002+2006 → 2010 | +1,05% [−0,31%; +2,13%] | +1,32% [−0,20%; +2,41%] |
| 2002+2006+2010 → 2014 | −1,11% [−2,89%; +0,56%] | +1,12% [−1,19%; +2,42%] |
| 2002+2006+2010+2014 → 2018 | −0,33% [−1,33%; +0,77%] | +1,18% [−1,13%; +2,65%] |
| 2002+2006+2010+2014+2018 → 2022 | −0,34% [−1,60%; +0,71%] | +2,00% [−0,75%; +4,20%] |

Os ICs abrangem zero. A transferência do contexto socioeconômico dos vizinhos entre eleições não demonstrou melhora estável em toda a janela.

## Robustez com PIB, cinco pleitos

No modelo com quatro controles (2006–2022), os resultados temporais são sensíveis ao contexto de treinamento. Exemplos com pesos iguais, OLS, C:
- 2006 → 2010: +3,47%, IC [+0,54%; +6,24%];
- 2006+2010 → 2014: −7,93%, IC [−10,90%; −4,57%];
- 2006+2010+2014 → 2018: −3,93%, IC [−5,12%; −2,55%];
- 2006+2010+2014+2018 → 2022: −0,13%, IC [−1,19%; +0,77%].

Isso demonstra a necessidade de reportar separadamente especificação reduzida e completa. A mudança dos resultados **não identifica qualquer mecanismo causal**.

## 1998: por que não entrou no painel

- Em **1998, não houve segundo turno presidencial**. Portanto, um desfecho de competitividade do segundo turno não existe naquele ano.
- O [TSE adverte que os dados de resultados de 1998 estão incompletos](https://dadosabertos.tse.jus.br/dataset/resultados-1998).
- No arquivo nominal `votacao_candidato_munzona_1998.zip`, as contagens consolidadas vieram zeradas e não são utilizadas na inferência.
- Um arquivo presidencial alternativo `votacao_secao_1998_BR.zip` oferece informação apenas para **27 códigos territoriais distintos**, insuficiente para painel municipal nacional.
- Os arquivos estaduais `votacao_secao_1998_AC.zip`, `..._RS.zip` e `..._SP.zip` usam o **esquema oficial com 23 colunas**, diferente do TXT BR. Após ler as colunas `DS_CARGO`, `NR_VOTAVEL`, `QT_VOTOS` corretamente, o cargo **PRESIDENTE não aparece** nesses três arquivos: só governador, senador e deputados. Assim, **esses recursos estaduais não complementam a votação presidencial do BR**.
- Documentação e possível alternativa: [página oficial do TSE com base histórica Access para 1998](https://www.tse.jus.br/eleicoes/eleicoes-anteriores/eleicoes-1998/candidaturas-votacao-e-resultados/resultados-das-eleicoes-de-1998). A cobertura dessa outra fonte ainda não foi auditada; não incluímos 1998 na série estatística.

## Conciliação municipal e questões abertas

- Os registros de 2002 têm uma chave sem correspondência com o mapa atual: (`MT`, `91065`); não foi feita correspondência especulativa.
- O arquivo de 2010 inclui os códigos especiais `VT` e `ZZ`, excluídos das regressões municipais e conciliados à parte no total nacional. Os totais nominais do segundo turno coincidiram com a referência numérica usada nos testes, mas os registros especiais e o recorte municipal devem permanecer expressamente diferenciados.
- Os anos eleitorais 2002–2010 utilizam composição demográfica do Censo 2000; 2014–2022, do Censo 2010. A troca do censo em 2014 interfere na avaliação temporal e exige ressalva.
- A base IBGE foi recuperada em 2026; valores históricos podem ter sido revisados. A validação temporal é retrospectiva, **não previsão em tempo real**.
- Os centroides são da malha de 2022, que não recupera limites antigos integralmente. Municípios com código constante podem ter mudado perímetro.
- Os mesmos municípios reaparecem no treino e no teste em anos diferentes; períodos eleitorais nacionais são apenas seis e não independentes como 33 mil linhas.
- Não há evidência de causalidade ou contágio social entre eleitores; nenhuma conclusão desta pesquisa qualifica uma candidatura.

## Replicação

**Seis eleições:**
- [Script](../scripts/36_modelos_seis_eleicoes_historicos.py)
- [Workflow](../.github/workflows/modelos_2002_2022_historicos_v01.yml)
- [Manifesto e CSVs](../outputs/modelos_seis_eleicoes_v01/)
- [Execução concluída](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/actions/runs/38245381489)

**Cinco eleições, com PIB:**
- [Script](../scripts/37_modelos_historicos_full4_2006_2022.py)
- [Resultados e manifesto](../outputs/robustez_historica_full4_2006_2022_v01/)

**Séries originais:**
- [TSE inventários de 1998/2002/2006/2010](../outputs/inventario_tse_historico_v01/)
- [IBGE histórico e manifesto](../outputs/controles_ibge_historicos_v01/)
- [Verificação 1998 por UF](../outputs/verificacao_presidente_1998_ufs_v01/)
- [Resumo das amostras do TSE de 1998](../outputs/leiaute_tse_1998_ufs_v01/)

Nenhum manuscrito anterior foi sobrescrito, nenhuma submissão foi efetuada e não se reivindica verificação científica externa independente.
