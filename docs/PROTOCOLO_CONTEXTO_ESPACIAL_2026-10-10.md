# Comparação de modelos convencionais e contexto municipal espacial

Protocolo metodológico da pesquisa de Jacson Cruz do Nascimento, iniciado em 10/10/2026.

## Pergunta e escopo

O objetivo é investigar se características socioeconômicas e demográficas dos municípios vizinhos acrescentam capacidade de explicar o HHI municipal além das características do próprio município. A hipótese espacial é formulada como diagnóstico de estrutura territorial, **não como teste de transmissão social ou de comportamento de manada**.

## Dados

Utilizam-se as mesmas 5.565 unidades com controles completos da regressão anterior e os mesmos indicadores do IBGE com defasagens documentadas. As informações eleitorais foram agregadas pelo TSE em 2018 e 2022. A correspondência de códigos TSE-IBGE é exata, com exclusão das cinco unidades sem informações do Censo 2010. A eleição de 2018 conserva ressalva de 76 votos no primeiro turno.

## Especificações comparadas

**A. Convencional:** intercepto, log população anterior, log proxy PIB per capita, urbanização 2010, fração feminina 2010, com efeitos fixos por UF no experimento in-sample.

**B. Contextual:** especificação A mais as médias dos quatro atributos socioeconômicos dos oito municípios geograficamente mais próximos, com k=4 e k=12 como diagnósticos de sensibilidade.

O critério de proximidade usa centroides da malha municipal do IBGE de 2022. Os atributos dos vizinhos são preexistentes aos votos observados no ano de referência. O **HHI e os votos dos vizinhos não entram como regressores**, evitando antecipação dos resultados eleitorais vizinhos.

## Validação

Para os mesmos períodos e territórios, são comparados o R² in-sample dos dois modelos, o Moran I dos resíduos e o RMSE de cinco partições de estados mantidos integralmente fora do treinamento. Neste último exercício são retirados os efeitos fixos por UF de ambos os modelos, para não prever efeitos estaduais de unidades ausentes da base de treino. A avaliação registra o desempenho de cada dobra e não apenas a média.

Informações IBGE de municípios mantidos fora do treinamento compõem médias dos atributos de vizinhança: o experimento é parcialmente transdutivo nas covariáveis, mas não utiliza os resultados de HHI dos territórios de teste. Essas informações foram recuperadas em 2026 e podem ter revisões históricas; a avaliação não constitui previsão eleitoral ex ante.

## Condição de interpretação

Um ganho de desempenho do modelo contextual mostrará apenas que o contexto geográfico medido pelos atributos públicos ajuda a explicar o HHI agregado. Não demonstrará difusão de preferências, imitação, pressão social, fluxo individual de votos ou previsão de vencedores. A avaliação causal da hipótese de manada permanece separada, dependente de identificação adicional e variáveis de interação social observáveis.

Scripts, entradas, valores calculados e versões anteriores devem permanecer públicos, independentes do repositório do artigo de manada organizacional.
