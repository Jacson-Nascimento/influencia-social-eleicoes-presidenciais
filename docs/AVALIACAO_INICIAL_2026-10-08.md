# Avaliação inicial dos totais nacionais de 2022

Autor: Jacson Cruz do Nascimento. Projeto independente de influência social e comportamento eleitoral.

## Fontes
- 1º turno: https://www.tse.jus.br/comunicacao/noticias/2022/Outubro/100-das-secoes-totalizadas-confira-como-ficou-o-quadro-eleitoral-apos-o-1o-turno
- 2º turno: https://www.tse.jus.br/comunicacao/noticias/2022/Outubro/100-das-secoes-totalizadas-confira-como-ficou-o-quadro-eleitoral-apos-o-2o-turno/

## Conciliação nacional
| Indicador | 1º turno | 2º turno | Variação |
|---|---:|---:|---:|
| Votos válidos | 118.229.719 | 118.552.353 | +322.634 |
| Candidatura 13 | 57.259.504 | 60.345.999 | +3.086.495 |
| Candidatura 22 | 51.072.345 | 58.206.354 | +7.134.009 |
| Outras candidaturas | 9.897.870 | Não se aplica | Não se aplica |

Identidade de controle: 3.086.495 + 7.134.009 = 9.897.870 + 322.634 = 10.220.504.

A identidade é contábil, não uma inferência de transferência individual de votos. Não demonstra comportamento de manada. Não é previsão para 2026.

## Auditoria
Os controles ficam em `data/controles/totalizacao_presidencial_2022_tse.csv`; a execução de referência está documentada em `outputs/relatorios/auditoria_agregados_2022_v01.json`. Nove testes unitários foram executados com sucesso no pacote local. Testes de software não substituem conferência de bases territoriais.

## Pendente
Coletar arquivos oficiais de votação por município e zona; verificar hashes e licenças, cobertura e totais municipais e nacionais; harmonizar malhas e executar comparação retrospectiva.