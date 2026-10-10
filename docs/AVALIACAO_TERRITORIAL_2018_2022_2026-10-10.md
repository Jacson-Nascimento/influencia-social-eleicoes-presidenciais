# Avaliação territorial inicial: eleições presidenciais de 2018 e 2022

**Autor:** Jacson Cruz do Nascimento. **Data:** 10/10/2026.  
**Situação:** 2022 integralmente conciliado; 2018 com divergência documental no primeiro turno, sem normalização artificial dos votos.

## Origem e integridade dos dados

Fonte original: Tribunal Superior Eleitoral, *Votação nominal por município e zona*, abrangência presidencial nacional (`*_BR.csv`), 1º e 2º turnos, incluindo UF `ZZ` para votação no exterior.

- 2018: https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2018.zip
- 2022: https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2022.zip
- SHA-256 do ZIP original de 2018: `f880848ef4ba340b15cb91ff0754aa370d34ca7b7e605d6607c0f2a75009adc8` (395.389.280 bytes)
- SHA-256 do ZIP original de 2022: `f7d1ea8ec71ff37d9b3af8ebbc06387b1e86f4c187d4a2ea81ce1f16f67d96bc` (596.166.602 bytes)

Ambos os ZIPs passaram pela verificação de integridade no GitHub Actions. O processamento selecionou o CSV nacional `BR`, sem somar novamente os arquivos `BRASIL` e estaduais eventualmente existentes no mesmo pacote. O arquivo bruto original não foi modificado.

## Cobertura territorial

| Ano | Municípios brasileiros, por turno | Localidades eleitorais no exterior (ZZ), por turno | UFs brasileiras |
|---|---:|---:|---:|
| 2018 | 5.570 | 138 | 27 |
| 2022 | 5.570 | 181 | 27 |

A categoria `ZZ` representa unidades eleitorais no exterior, não municípios brasileiros. A cobertura municipal interna está completa nos dois turnos de cada ano, segundo as chaves territoriais observadas.

## Concentração descritiva

| Indicador | 2018, 1º turno | 2018, 2º turno | 2022, 1º turno | 2022, 2º turno |
|---|---:|---:|---:|---:|
| Mediana municipal do índice Herfindahl-Hirschman (HHI), Brasil | 0,396680 | 0,574173 | 0,479511 | 0,545348 |
| Média municipal de HHI ponderada por votos válidos, Brasil | 0,389602 | 0,582893 | 0,469195 | 0,549375 |
| Mediana municipal da participação dos dois finalistas no voto válido, Brasil | 81,1051% | 100% | 94,0871% | 100% |
| Parcela nacional dos dois finalistas nos votos válidos | 75,3092% | 100% | 91,6283% | 100% |

O HHI foi calculado sobre candidaturas com votos positivos em cada município e turno, como soma dos quadrados das respectivas parcelas dos votos nominais válidos. A elevação do HHI no segundo turno decorre em parte, mecanicamente, da redução do universo a dois concorrentes. Portanto, **não mede comportamento de manada** nem comprova influência ou causalidade.

## Mudança de votos válidos entre turnos, nível municipal

| Indicador | 2018 | 2022 |
|---|---:|---:|
| Municípios brasileiros presentes nos dois turnos | 5.570 | 5.570 |
| Municípios em que votos válidos diminuíram | 73,4650% | 40,5386% |
| Municípios em que votos válidos aumentaram | 26,4093% | 59,1741% |
| Mediana da variação percentual municipal de votos válidos | -2,5537% | +0,5129% |
| Mediana da variação absoluta municipal de votos válidos | -112 | +30 |

Os percentuais de municípios são **não ponderados**. A mudança no total de votos válidos não equivale à mudança no comparecimento ou à transferência individual de preferência: também pode refletir alterações entre brancos, nulos e votos válidos.

## Conciliação com a totalização histórica do TSE

| Ano e turno | Total válido extraído do ZIP | Referência histórica do TSE | Resíduo |
|---|---:|---:|---:|
| 2018, 1º | 107.050.749 | 107.050.673 | +76 |
| 2018, 2º | 104.838.753 | 104.838.753 | 0 |
| 2022, 1º | 118.229.719 | 118.229.719 | 0 |
| 2022, 2º | 118.552.353 | 118.552.353 | 0 |

O desvio de 76 votos em 2018 concentra-se em +20 votos na candidatura 17, +46 na candidatura 13 e +10 nas demais candidaturas, em comparação com o total publicado na notícia histórica. A origem exata não foi identificada. É plausível que reflita atualizações do conjunto de dados posteriores à notícia, mas isso **não foi demonstrado**. O arquivo original, os resultados de auditoria e os valores extraídos foram preservados sem ajustes para forçar fechamento.

**Critério de aceitação:** 2022 aprovado; 2018 permanece com ressalva. Os indicadores de 2018 são exploratórios e devem ser citados com esta advertência.

## Referências de conciliação
- TSE, primeiro turno 2018: https://www.tse.jus.br/comunicacao/noticias/2018/Outubro/concluida-totalizacao-de-votos-do-1o-turno-das-eleicoes-2018
- TSE, segundo turno 2018: https://www.tse.jus.br/comunicacao/noticias/2018/Outubro/eleicoes-2018-justica-eleitoral-conclui-totalizacao-dos-votos-do-segundo-turno
- TSE, primeiro turno 2022: https://www.tse.jus.br/comunicacao/noticias/2022/Outubro/100-das-secoes-totalizadas-confira-como-ficou-o-quadro-eleitoral-apos-o-1o-turno
- TSE, segundo turno 2022: https://www.tse.jus.br/comunicacao/noticias/2022/Outubro/100-das-secoes-totalizadas-confira-como-ficou-o-quadro-eleitoral-apos-o-2o-turno/

## Limitações e próximos testes
1. O número de candidaturas altera mecanicamente HHI, concentração e entropia. Comparações diretas entre turnos não identificam manada.
2. Sem informação individual e identificação causal, não é possível estimar transferência de votos nem influências interpessoais apenas com dados agregados.
3. Para autocorrelação espacial, o próximo passo é harmonizar os códigos TSE com malhas e vizinhança do IBGE; não há índice de Moran calculado neste relatório.
4. Modelos espaciais devem ser comparados com alternativas não espaciais e validados fora da amostra, com sensibilidade à unidade territorial e à dependência.
5. A fonte pública de 2018 precisa ser conciliada com uma referência temporalmente compatível antes de tratá-la como integralmente validada.
