# Geografia da competitividade eleitoral no Brasil: fatores socioeconômicos e contexto espacial nos segundos turnos presidenciais de 2018 e 2022

**Jacson Cruz do Nascimento**  
Mestre em Economia, pesquisador independente, Brasília, Brasil.  
ORCID: https://orcid.org/0009-0006-6535-9569  
**Manuscrito empírico, versão 3.0, 10 de outubro de 2026.** Documento de trabalho, ainda não submetido a periódico.

## Resumo

O artigo examina em que medida atributos socioeconômicos dos municípios e de suas vizinhanças explicam a competitividade territorial nas eleições presidenciais brasileiras de 2018 e 2022. A competitividade é definida como um menos a diferença absoluta entre as participações dos dois finalistas no segundo turno, assumindo valor unitário em uma disputa equilibrada. São utilizados resultados nominais do Tribunal Superior Eleitoral (TSE), correspondência territorial TSE-IBGE, malha municipal do IBGE e variáveis públicas de população, urbanização, composição por sexo e produto municipal. Os indicadores eleitorais abrangem 5.570 municípios em cada eleição; as estimações com controles utilizam amostra comum de 5.565, após exclusão documentada de cinco municípios sem dados censitários completos. Modelos lineares com efeitos fixos estaduais e covariáveis locais são confrontados com extensões que incorporam as médias socioeconômicas dos oito municípios geograficamente próximos, com sensibilidades para quatro e doze vizinhos. Em 2018, a inclusão do contexto elevou o coeficiente de determinação da competitividade de 0,4255 para 0,4303, com redução de 1,92% do erro de validação por UFs inteiras omitidas. Em 2022, o R² passou de 0,5211 para 0,5275, com redução de 4,99% do erro. Ao estudar separadamente a margem assinada, que distingue a candidatura nº 13 de seu oponente, os ganhos de validação foram maiores, 17,09% em 2018 e 18,53% em 2022. Na análise que atribui peso igual a cada município, a inclusão do contexto melhora a generalização geográfica, sobretudo para a margem assinada. Contudo, ao ponderar cada município pelos votos válidos, o ganho desaparece ou torna-se negativo em três das quatro comparações principais, e é apenas marginalmente positivo para competitividade em 2022. A contribuição estatística do contexto é, portanto, sensível à unidade de ponderação. Os resultados não demonstram influência social causal nem constituem previsão eleitoral.

**Palavras-chave:** competitividade eleitoral; eleições presidenciais; econometria espacial; diferenças socioeconômicas; municípios brasileiros; dados públicos.

## 1. Introdução

A semelhança dos resultados eleitorais entre localidades próximas é um fenômeno importante para a economia política e a geografia eleitoral. Ocorre, porém, uma dificuldade de identificação: municípios próximos podem apresentar comportamentos eleitorais semelhantes porque compartilham características econômicas, demográficas e históricas, sem que exista transmissão de preferências entre eleitores. Estudos com resultados agregados devem ainda evitar inferências indevidas sobre comportamento individual (King, 1997).

Neste trabalho a variável principal não é o voto de um candidato específico, nem o índice de concentração entre um número variável de candidaturas. A questão central é a competitividade entre os dois finalistas do segundo turno em cada município. Essa definição permite comparar eleições diferentes mantendo dois competidores por município, com uma mesma escala de 0 a 1. Para evitar perder a direção política do resultado, uma segunda variável identifica a vantagem da candidatura nº 13 perante o outro finalista, sem tratar os candidatos de 2018 e 2022 como a mesma pessoa.

A pergunta principal é: **em que medida as características socioeconômicas dos municípios e de seus vizinhos explicam as diferenças territoriais de competitividade nas eleições presidenciais brasileiras de 2018 e 2022?**

O estudo não transfere os parâmetros de um modelo de manada organizacional para eleitores brasileiros. A relação com o trabalho anterior de Nascimento (2026) é apenas conceitual e não fundamenta inferência causal sobre imitação, pressão social ou transmissão individual de votos.

## 2. Fundamentação e delimitação da contribuição

A autocorrelação espacial de Moran (1950) quantifica uma dimensão da associação geográfica, mas seu valor depende da unidade territorial e da estrutura de vizinhança. A mudança da escala espacial pode alterar padrões estatísticos, dificuldade associada ao problema da unidade de área modificável (Openshaw, 1984). A literatura sobre inferência ecológica (King, 1997) alerta que conclusões individuais não decorrem diretamente das regularidades observadas em municípios.

A contribuição pretendida é **comparativa e incremental**: confrontar características socioeconômicas locais e de municípios próximos como explicações da competitividade, testar se o acréscimo contextual melhora a generalização para UFs excluídas e distinguir esse desfecho da direção partidária do voto. A demonstração da existência de padrões regionais de votação não é, por si, reivindicada como descoberta nova.

## 3. Fontes e construção da base

### 3.1. Eleições e correspondência territorial

Os arquivos de resultados nominais por município-zona de 2018 e 2022 foram obtidos do TSE, agregados em nível municipal e cruzados com os códigos oficiais TSE-IBGE. Os 5.570 municípios brasileiros foram vinculados sem imputação territorial. Os votos no exterior (UF ZZ) foram preservados nas bases originais e excluídos apenas das estatísticas municipais brasileiras.

A auditoria documental detectou discrepância de +76 votos na soma do primeiro turno de 2018 do arquivo distribuído, relativamente à notícia de totalização histórica do TSE. Essa diferença permanece sem explicação conclusiva e foi preservada. Os totais nacionais dos segundos turnos e ambos os turnos de 2022 foram reconciliados quando se incluem os registros no exterior.

### 3.2. Competitividade e direção do voto no segundo turno

Em cada município \\(i\\) e eleição \\(e\\), sejam \\(V_{13,ie}\\) os votos da candidatura nº 13 e \\(V_{o,ie}\\) os votos da outra candidatura finalista. O total dos votos nominais válidos para os dois finalistas é \\(T_{ie}=V_{13,ie}+V_{o,ie}\\).

\\[
C_{ie}=1-\\left|\\frac{V_{13,ie}-V_{o,ie}}{T_{ie}}\\right|.
\\]

A competitividade \\(C_{ie}\\) vale 1 quando há empate e 0 quando uma candidatura recebe todos os votos válidos locais. Para estudar a **direção do voto**, define-se separadamente:

\\[
M_{ie}=\\frac{V_{13,ie}-V_{o,ie}}{T_{ie}}, \\quad C_{ie}=1-|M_{ie}|.
\\]

Em 2018, nº 13 identifica Fernando Haddad (PT) e nº 17 identifica Jair Bolsonaro (PSL). Em 2022, nº 13 identifica Luiz Inácio Lula da Silva (PT) e nº 22 identifica Jair Bolsonaro (PL). Portanto, \\(M\\) informa qual lado teve maior votação, mas não pode ser interpretada como preferência individual estável pela mesma pessoa no tempo.

O índice original HHI é mantido apenas para comparação histórica e não constitui variável dependente principal desta versão.

### 3.3. Primeiro turno como verificação complementar

A análise do primeiro turno distingue a competitividade **condicional às duas candidaturas mais votadas em cada município** da parcela total de votos válidos que essas candidaturas receberam. Também calcula o número efetivo de candidaturas, inverso do HHI, e a margem assinada entre os futuros finalistas como fração de todos os votos válidos do primeiro turno.

Essa decomposição evita comparar ingenuamente a competitividade de duas candidaturas dominantes quando, na realidade, outras candidaturas receberam parcela expressiva dos votos válidos.

### 3.4. Características municipais do IBGE

As variáveis socioeconômicas utilizadas são: estimativas de população de 2017 e 2021; PIB municipal de 2016 e 2020; proporção urbana e proporção feminina do Censo 2010. Para 2018, utiliza-se PIB de 2016 e população de 2017; para 2022, PIB de 2020 e população de 2021. A proxy de produto por habitante combina PIB e população de anos diferentes; não corresponde ao PIB per capita oficial do IBGE.

As versões foram consultadas em 2026 e podem incorporar revisões retrospectivas. Por isso a verificação fora da amostra é **geográfica**, não um teste de previsão estritamente disponível em 2018 ou 2022. Cinco municípios sem cobertura censitária completa foram excluídos dos modelos, conservando 5.565 unidades em amostra comum.

## 4. Estratégia de estimação

### 4.1. Modelos de competitividade

Para cada eleição estima-se separadamente um modelo local e uma extensão contextual:

\\[
C_{ie}=\\alpha_e+\\gamma_{UF(i),e}+\\boldsymbol{\\beta}_e'X_{ie}+u_{ie},
\\]

\\[
C_{ie}=\\alpha_e+\\gamma_{UF(i),e}+\\boldsymbol{\\beta}_e'X_{ie}
+\\boldsymbol{\\theta}_e'W_kX_{ie}+u_{ie}.
\\]

A matriz \\(W_k\\) contém os \\(k\\) municípios mais próximos por centroide geográfico, definidos a partir da malha municipal de 2022; a média dos atributos dos vizinhos é calculada para k=8, com k=4 e k=12 para análise de sensibilidade. \\(X\\) contém log da população, log da proxy de produto por pessoa, urbanização 2010 e proporção feminina 2010.

**Não há votos, margem, competitividade ou HHI dos vizinhos como regressoras.** A extensão é contextual e não estima contágio eleitoral.

### 4.2. Validação geográfica e sensibilidade direcional

A avaliação dentro da amostra compara o R² das regressões com efeitos fixos de UF. Como covariáveis extras não podem reduzir o R² usual de OLS na mesma amostra, também se avalia a generalização geográfica: cinco grupos de UFs inteiras são omitidos do treino, sem efeitos fixos de UF em qualquer modelo desse exercício, e compara-se o RMSE dos dois modelos.

A margem assinada \\(M\\) substitui \\(C\\) em uma análise de sensibilidade com as mesmas covariáveis, territórios e vizinhança. Assim é possível distinguir explicação da intensidade da competitividade de explicação do lado com vantagem em cada município.

O índice de Moran dos resíduos serve para verificar a permanência de autocorrelação espacial após os controles, não como demonstração causal. Permutações de resíduos de modelos estimados são tratadas como diagnóstico exploratório.

**Sensibilidade à importância eleitoral dos municípios.** Como a análise principal trata igualmente cada município, estima-se adicionalmente regressão ponderada por votos válidos nominais do segundo turno e RMSE de validação geográfica com os mesmos pesos. A ponderação distingue capacidade de explicar o município típico da capacidade de explicar os resultados de localidades proporcionalmente ao seu peso eleitoral. Os pesos foram observados ao fim do segundo turno, logo não representam informações disponíveis antes de uma eventual previsão ex ante.

## 5. Resultados

### 5.1. Distribuição municipal da competitividade

| Indicador municipal, não ponderado | 2018 | 2022 |
|---|---:|---:|
| Municípios analisados | 5.570 | 5.570 |
| Mediana da competitividade do 2º turno | 0,614843 | 0,698842 |
| Média municipal da competitividade do 2º turno | 0,610541 | 0,671042 |
| Fração dos municípios com vantagem da candidatura nº 13 | 50,45% | 56,07% |
| Cobertura mediana das duas candidaturas locais mais votadas no 1º turno | 81,77% | 94,09% |
| Mediana da competitividade condicional entre os dois líderes locais do 1º turno | 0,585973 | 0,696881 |
| Municípios em que os dois líderes locais do 1º turno não coincidem com os finalistas nacionais | 795 | 0 |

A mediana municipal da competitividade foi maior em 2022, mas a diferença entre municípios não deve ser confundida com diferença entre totais nacionais ponderados por número de votos. O registro da candidatura nº 13 permite verificar a direção local, mas refere-se a pessoas diferentes nos dois pleitos.

### 5.2. Competitividade do segundo turno, especificação principal de oito vizinhos

| Ano | R² local + UF | R² com contexto + UF | Acréscimo de R² | Redução de RMSE na validação por UFs |
|---|---:|---:|---:|---:|
| 2018 | 0,425523 | 0,430325 | +0,480 ponto percentual | 1,92% |
| 2022 | 0,521130 | 0,527468 | +0,634 ponto percentual | 4,99% |

Em 2018, duas das cinco partições territoriais apresentaram piora de erro com o contexto, apesar do ganho total agregado. Em 2022, houve melhora nas cinco partições. Os resultados sugerem contribuição estatística positiva, de magnitude limitada, das características socioeconômicas dos municípios vizinhos para a competitividade local.

Os índices de Moran I dos resíduos foram 0,460704 no modelo local e 0,458557 no contextual em 2018; e 0,458046 contra 0,457380 em 2022. A inclusão do contexto pouco reduziu a autocorrelação residual, exigindo cautela com interpretações sobre mecanismos subjacentes.

### 5.3. Sensibilidade com margem assinada do voto

| Ano | R² local + UF | R² com contexto + UF | Acréscimo de R² | Redução de RMSE na validação por UFs |
|---|---:|---:|---:|---:|
| 2018 | 0,808386 | 0,821872 | +1,349 ponto percentual | 17,09% |
| 2022 | 0,772391 | 0,789344 | +1,695 ponto percentual | 18,53% |

O contexto dos vizinhos apresenta melhora de generalização geográfica muito maior para a **direção relativa de votos** que para a competitividade. Isso não implica que vizinhos causem a preferência por determinada candidatura: pode refletir características comuns da estrutura regional.

O Moran residual da margem assinada permaneceu elevado após o contexto: 0,530191 em 2018 e 0,503836 em 2022 na referência de oito vizinhos. Em 2018, o valor residual é até ligeiramente superior ao do modelo apenas local. Portanto, a adição de covariáveis espaciais não eliminou a estrutura de dependência.

### 5.4. Sensibilidade da vizinhança

Os acréscimos de R² para o modelo de competitividade foram positivos com k=4, k=8 e k=12. A redução de erro geográfico variou de 1,50% a 2,09% em 2018 e de 4,05% a 5,55% em 2022. Para a margem assinada, a faixa foi de 13,87% a 18,75% em 2018 e de 14,60% a 20,35% em 2022.

Essa sensibilidade reforça que escolher um único tamanho de vizinhança após observar os resultados poderia exagerar conclusões. Por isso k=8 permanece a especificação previamente registrada, com k=4/12 como verificações complementares.

### 5.5. Sensibilidade à ponderação pela votação municipal

O resultado principal muda de interpretação quando os municípios recebem pesos proporcionais à quantidade de votos nominais válidos do segundo turno.

| Desfecho | 2018: redução de RMSE sem pesos | 2018: com pesos | 2022: sem pesos | 2022: com pesos |
|---|---:|---:|---:|---:|
| Competitividade | +1,92% | **-3,28%** | +4,99% | **+0,34%** |
| Margem assinada | +17,09% | **-0,53%** | +18,53% | **-1,82%** |

Um sinal negativo significa piora do erro ao incluir as características dos vizinhos. O teste usa a mesma amostra de 5.565 municípios, mas modifica a função de perda e os coeficientes estimados ao privilegiar localidades com mais votos.

Para competitividade, a especificação ponderada de 2018 piorou em **cinco de cinco dobras** da validação por UF. Em 2022 houve pequena melhora agregada, mas **três de cinco dobras** pioraram. Os ganhos anteriormente observados no experimento sem ponderação **não são robustos** a essa definição de importância dos municípios.

A sensibilidade com k=4 e k=12 confirma a instabilidade: competitividade ponderada de 2018 piorou com todas as vizinhanças examinadas; a de 2022 melhorou apenas marginalmente. Para a margem assinada, apenas k=12 apresentou melhora agregada ponderada nos dois anos, enquanto k=4 e k=8 apresentaram piora.

**Conclusão metodológica:** não é adequado afirmar superioridade geral do modelo contextual. Sua utilidade depende do objetivo estatístico, do critério de ponderação e do conjunto territorial de avaliação. O resultado é uma condição de fronteira para a contribuição do artigo, não uma falha a omitir.

## 6. Discussão

O resultado central distingue dois fenômenos. A competitividade mede a distância de um empate, sem informar qual candidatura venceu a maioria dos votos locais. A margem assinada informa a direção do apoio e pode variar de maneira fortemente estruturada no espaço. Na amostra analisada, características socioeconômicas locais e de vizinhança explicaram melhor a direção territorial do voto que o grau de equilíbrio da disputa.

A contribuição do artigo não é descobrir que municípios próximos votam de forma semelhante, fenômeno já estudado pela geografia eleitoral. Consiste em separar desfechos que podem ser confundidos, quantificar o ganho contextual frente aos controles locais e mostrar que esse ganho se altera substancialmente quando os resultados são ponderados pela dimensão eleitoral dos municípios.

É necessário evitar uma conclusão exagerada: os R² e RMSE são medidas descritivas/preditivas para **indicadores agregados de eleições passadas**. Não estabelecem exogeneidade das covariáveis, influência interpessoal, transferência individual de votos ou capacidade de antecipar resultado de eleição futura. A dependência residual pode ter origens socioeconômicas, institucionais e históricas não incluídas na especificação.

## 7. Conclusões provisórias e pendências

A inclusão de características socioeconômicas de municípios próximos eleva o R² dentro da amostra e produz melhorias modestas de generalização geográfica da competitividade quando cada município tem peso igual. Contudo, esse benefício não se mantém de forma consistente quando o ajuste e a avaliação são ponderados pelos votos válidos municipais. A margem assinada apresenta ganhos ainda maiores na análise não ponderada, mas a melhora também desaparece na especificação ponderada de oito vizinhos. Assim, as conclusões apontam contribuição **condicionada à métrica de avaliação**, não superioridade geral de modelos socioespaciais. A autocorrelação residual permanece expressiva em todas as alternativas.

Para submissão será necessário: (a) revisar a literatura eleitoral brasileira pertinente e fundamentar a contribuição incremental; (b) aprofundar a influência de municípios grandes, fronteiras entre UFs e sensibilidade às malhas, pois a avaliação por votos válidos já demonstrou resultados instáveis; (c) confrontar diferentes medidas de competitividade e analisar possíveis não linearidades; (d) resolver ou documentar definitivamente a ressalva dos 76 votos do primeiro turno de 2018; (e) avaliar inferência sob dependência espacial; (f) revisar referências, metadados e declarações editoriais. A possibilidade de extrapolação temporal exige reconstruir vintages de dados disponíveis antes de cada pleito.

## Disponibilidade dos dados e replicação

Os resultados eleitorais derivam de bases públicas do TSE e as covariáveis, de fontes públicas do IBGE. O repositório independente mantém scripts, controles, bases derivadas, registros de integridade e execuções automatizadas:

- [Indicadores de competitividade, segundo turno v02](../outputs/competitividade_v02/competitividade_e_margem_assinada_segundo_turno.csv)
- [Complementos de primeiro turno v02](../outputs/competitividade_v02/indicadores_complementares_primeiro_turno.csv)
- [Resultados de regressão e sensibilidade direcional](../outputs/competitividade_modelos_v01/modelos_competitividade_e_direcao_k4_k8_k12.csv)
- [Validação por UFs](../outputs/competitividade_modelos_v01/validacao_uf_detalhada.json)
- [Sensibilidade por votos válidos](../outputs/competitividade_ponderada_v01/modelos_ponderados_competitividade_e_direcao.csv)
- [Relatório da ponderação](RELATORIO_SENSIBILIDADE_PONDERADA_2026-10-10.md)
- [Protocolo e definições](PROTOCOLO_COMPETITIVIDADE_ELEITORAL_V01.md)
- [Script de indicadores](../scripts/15_indicadores_competitividade.py)
- [Script dos modelos](../scripts/16_modelos_competitividade.py)
- [Repositório](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais)

A versão anterior do artigo sobre HHI foi preservada como documento de trabalho distinto; nenhum código ou resultado do artigo de dinâmica de manada organizacional foi alterado.

## Referências metodológicas iniciais

KING, Gary. *A Solution to the Ecological Inference Problem: Reconstructing Individual Behavior from Aggregate Data*. Princeton: Princeton University Press, 1997.

MORAN, P. A. P. Notes on Continuous Stochastic Phenomena. *Biometrika*, v. 37, n. 1–2, p. 17–23, 1950. DOI: https://doi.org/10.1093/biomet/37.1-2.17.

OPENSHAW, Stan. *Ecological Fallacies and the Analysis of Areal Census Data*. Environment and Planning A, 1984. DOI: https://doi.org/10.1068/a160017.

NASCIMENTO, Jacson Cruz do. *Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional*. Zenodo, 2026. https://doi.org/10.5281/zenodo.21985858.

TRIBUNAL SUPERIOR ELEITORAL (TSE). *Portal de Dados Abertos*. Resultados presidenciais de 2018 e 2022. https://dadosabertos.tse.jus.br.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). *SIDRA*. Tabelas 202, 5938 e 6579. https://sidra.ibge.gov.br.
