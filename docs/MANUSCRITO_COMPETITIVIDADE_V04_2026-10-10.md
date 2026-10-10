# Geografia da competitividade eleitoral no Brasil: fatores socioeconômicos e contexto espacial nos segundos turnos presidenciais de 2018 e 2022

**Jacson Cruz do Nascimento**  
Mestre em Economia, pesquisador independente, Brasília, Brasil.  
ORCID: https://orcid.org/0009-0006-6535-9569  
**Manuscrito empírico, versão 4.0, 10 de outubro de 2026.** Documento de trabalho, ainda não submetido a periódico.

## Resumo

O artigo examina em que medida atributos socioeconômicos dos municípios e de suas vizinhanças explicam a competitividade territorial nas eleições presidenciais brasileiras de 2018 e 2022. A competitividade é definida como um menos a diferença absoluta entre as participações dos dois finalistas no segundo turno, assumindo valor unitário em uma disputa equilibrada. São utilizados resultados nominais do Tribunal Superior Eleitoral (TSE), correspondência territorial TSE-IBGE, malha municipal do IBGE e variáveis públicas de população, urbanização, composição por sexo e produto municipal. Os indicadores eleitorais abrangem 5.570 municípios em cada eleição; as estimações com controles utilizam amostra comum de 5.565, após exclusão documentada de cinco municípios sem dados censitários completos. Modelos lineares com efeitos fixos estaduais e covariáveis locais são confrontados com extensões que incorporam as médias socioeconômicas dos oito municípios geograficamente próximos, com sensibilidades para quatro e doze vizinhos. Em 2018, a inclusão do contexto elevou o coeficiente de determinação da competitividade de 0,4255 para 0,4303, com redução de 1,92% do erro de validação por UFs inteiras omitidas. Em 2022, o R² passou de 0,5211 para 0,5275, com redução de 4,99% do erro. Ao estudar separadamente a margem assinada, que distingue a candidatura nº 13 de seu oponente, os ganhos de validação foram maiores, 17,09% em 2018 e 18,53% em 2022. Na análise que atribui peso igual a cada município, a inclusão do contexto melhora a generalização geográfica, sobretudo para a margem assinada. Contudo, ao ponderar cada município pelos votos válidos, o ganho desaparece ou torna-se negativo em três das quatro comparações principais, e é apenas marginalmente positivo para competitividade em 2022. A contribuição estatística do contexto é, portanto, sensível à unidade de ponderação. Os resultados não demonstram influência social causal nem constituem previsão eleitoral.

**Palavras-chave:** competitividade eleitoral; eleições presidenciais; econometria espacial; diferenças socioeconômicas; municípios brasileiros; dados públicos.

## 1. Introdução

A semelhança dos resultados eleitorais entre localidades próximas é um fenômeno importante para a economia política e a geografia eleitoral. Ocorre, porém, uma dificuldade de identificação: municípios próximos podem apresentar comportamentos eleitorais semelhantes porque compartilham características econômicas, demográficas e históricas, sem que exista transmissão de preferências entre eleitores. Estudos com resultados agregados devem ainda evitar inferências indevidas sobre comportamento individual (King, 1997).

Neste trabalho a variável principal não é o voto de um candidato específico, nem o índice de concentração entre um número variável de candidaturas. A questão central é a competitividade entre os dois finalistas do segundo turno em cada município. Essa definição permite comparar eleições diferentes mantendo dois competidores por município, com uma mesma escala de 0 a 1. Para evitar perder a direção política do resultado, uma segunda variável identifica a vantagem da candidatura nº 13 perante o outro finalista, sem tratar os candidatos de 2018 e 2022 como a mesma pessoa.

A pergunta principal é: **em que medida as características socioeconômicas dos municípios e de seus vizinhos explicam as diferenças territoriais de competitividade nas eleições presidenciais brasileiras de 2018 e 2022?**

O estudo não transfere os parâmetros de um modelo de manada organizacional para eleitores brasileiros. A relação com o trabalho anterior de Nascimento (2026) é apenas conceitual e não fundamenta inferência causal sobre imitação, pressão social ou transmissão individual de votos.

Na sensibilidade final, a ponderação pela população municipal de 2017/2021 reproduziu a instabilidade encontrada com pesos por votos: competitividade −3,26% em 2018 e +0,40% em 2022; margem assinada −0,89% e −1,87%, respectivamente. A exclusão de capitais e maiores municípios modificou o desempenho, sobretudo para a margem assinada, demonstrando que a contribuição do contexto depende do porte municipal, do desfecho e da ponderação. A auditoria final confirmou os dados dos dois segundos turnos e manteve ressalva documental de 76 votos no primeiro turno de 2018. A contribuição do estudo é, portanto, condicional e não causal.


## 2. Fundamentação e delimitação da contribuição

A autocorrelação espacial de Moran (1950) quantifica uma dimensão da associação geográfica, mas seu valor depende da unidade territorial e da estrutura de vizinhança. A mudança da escala espacial pode alterar padrões estatísticos, dificuldade associada ao problema da unidade de área modificável (Openshaw, 1984). A literatura sobre inferência ecológica (King, 1997) alerta que conclusões individuais não decorrem diretamente das regularidades observadas em municípios.

A literatura brasileira oferece antecedentes diretos. Braga e Zolnerkevic (2020) analisam padrões eleitorais temporais e espaciais desde 1989; Alkmim e Terron (2022) examinam polarização eleitoral e geográfica municipal até 2018; Masullo e Silva Junior (2024) estudam a configuração territorial dos pleitos de 2018 e 2022; Resende e Azevedo (2025) tratam do contexto espacial em municípios da fronteira em 2022; Nicolau (2026) demonstra a importância do porte municipal, das metrópoles e das margens eleitorais nas duas eleições. Assim, a contribuição não consiste em descobrir agrupamentos espaciais, modelos contextuais ou a relevância das grandes cidades, fenômenos previamente documentados. Busca-se quantificar a estabilidade do valor incremental de características de vizinhança sob medidas de competitividade e direção e sob diferentes funções de ponderação, de forma aberta e replicável. A comparação foi documentada em [matriz de literatura](REVISAO_LITERATURA_COMPETITIVIDADE_2026-10-10.md).

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

### 5.6. Pesos populacionais anteriores às eleições e efeito do porte municipal

Para verificar se a instabilidade associada à ponderação decorre da utilização dos votos válidos observados, a validação foi refeita com **estimativas populacionais de 2017 (eleição de 2018) e de 2021 (eleição de 2022)**. São referências anteriores aos pleitos, mas recuperadas em versões do IBGE consultadas em 2026, que podem ter sido revisadas. Não se trata, portanto, de backtest estritamente histórico.

| Desfecho, k=8 | 2018, peso uniforme | 2018, população anterior | 2022, peso uniforme | 2022, população anterior |
|---|---:|---:|---:|---:|
| Competitividade | +1,92% | **−3,26%** | +4,99% | **+0,40%** |
| Margem assinada | +17,09% | **−0,89%** | +18,53% | **−1,87%** |

O sinal do incremento de generalização depende fortemente da ponderação. Os ganhos com municípios tratados como unidades equivalentes não se reproduzem quando se utiliza a população anterior como peso. Isso reforça o achado da sensibilidade por votos válidos, sem depender de utilizar o comparecimento observado como peso.

A influência de localidades grandes foi avaliada em quatro amostras: 5.565 municípios completos; 5.538 municípios excluindo 27 capitais; 5.509 municípios excluindo os 56 mais populosos; e 5.286 municípios excluindo os 279 mais populosos. Em cada amostra a matriz de oito vizinhos foi reconstruída, e as UFs inteiras foram mantidas como unidades de validação. A exclusão de Brasília elimina o DF na amostra sem capitais ou sem grandes municípios; os experimentos restritos têm 26 UFs.

| Amostra, população anterior, k=8 | Competitividade 2018 | Competitividade 2022 | Margem assinada 2018 | Margem assinada 2022 |
|---|---:|---:|---:|---:|
| Todos os municípios | −3,26% | +0,40% | −0,89% | −1,87% |
| Sem capitais | −2,18% | −1,05% | +6,25% | +4,73% |
| Sem 1% mais populosos | −1,93% | −1,34% | +11,52% | +10,43% |
| Sem 5% mais populosos | +0,17% | +0,94% | +14,95% | +15,62% |

Na competitividade, a exclusão de grandes cidades atenua a piora ponderada de 2018, mas não demonstra um ganho relevante e estável. Na margem assinada, o modelo contextual passa a apresentar maior ganho com o afastamento dos grandes centros. Isso indica **heterogeneidade por porte municipal**; não demonstra que os grandes municípios causem a redução do desempenho, visto que a mudança de amostra também modifica a vizinhança e a composição dos conjuntos de validação.

No universo completo, as 27 capitais correspondem a aproximadamente 49,5 milhões de habitantes na estimativa de 2017 e a 50,9 milhões na de 2021. Os 279 municípios mais populosos representam mais da metade da população estimada de cada amostra. Assim, uma avaliação que atribui peso igual aos municípios e outra ponderada pela população priorizam partes substancialmente diferentes do território eleitoral.

### 5.7. Auditoria documental dos votos de 2018 e 2022

A auditoria final independente ratificou a soma de 107.050.749 votos válidos no arquivo nominal distribuído do primeiro turno de 2018, contra 107.050.673 na matéria oficial histórica do TSE. A diferença de **76 votos**, correspondente a aproximadamente **0,000071%** do total histórico, é decomposta em +20 votos para a candidatura 17, +46 para a candidatura 13 e +10 para outras candidaturas. Sua causa específica não foi localizada, e nenhuma contagem foi modificada.

**O segundo turno de 2018 e os dois turnos de 2022 conciliaram integralmente**, tanto em total geral quanto nos grupos de candidatura auditados. Como a variável principal do artigo utiliza exclusivamente dados de segundo turno, a divergência está localizada na análise complementar do primeiro turno de 2018. Ela permanece registrada como ressalva documental, sem apresentação enganosa de conciliação perfeita em 2018.

## 6. Discussão

O resultado central distingue dois fenômenos. A competitividade mede a distância de um empate, sem informar qual candidatura venceu a maioria dos votos locais. A margem assinada informa a direção do apoio e pode variar de maneira fortemente estruturada no espaço. Na amostra analisada, características socioeconômicas locais e de vizinhança explicaram melhor a direção territorial do voto que o grau de equilíbrio da disputa.

A contribuição do artigo não é descobrir que municípios próximos votam de forma semelhante, fenômeno já estudado pela geografia eleitoral. Consiste em separar desfechos que podem ser confundidos, quantificar o ganho contextual frente aos controles locais e mostrar que esse ganho se altera substancialmente quando os resultados são ponderados pela dimensão eleitoral dos municípios.

O confronto com Nicolau (2026) reforça a necessidade de não generalizar resultados municipais uniformemente para o eleitorado agregado. A relação entre o desempenho da extensão de contexto e o porte demográfico não é constante: para a variável de competitividade, a ponderação populacional e a ponderação por votos válidos enfraquecem ou revertem os ganhos; para a direção agregada, os ganhos reaparecem quando grandes municípios são retirados. Esses padrões refletem diferentes objetivos estatísticos e possivelmente heterogeneidade territorial não capturada pelos quatro controles. A retirada de capitais e dos maiores municípios também reconfigura as distâncias e o conjunto de unidades avaliadas, de modo que não é um experimento causal.

É necessário evitar uma conclusão exagerada: os R² e RMSE são medidas descritivas/preditivas para **indicadores agregados de eleições passadas**. Não estabelecem exogeneidade das covariáveis, influência interpessoal, transferência individual de votos ou capacidade de antecipar resultado de eleição futura. A dependência residual pode ter origens socioeconômicas, institucionais e históricas não incluídas na especificação.

## 7. Conclusões provisórias e pendências

A inclusão de características socioeconômicas de municípios próximos eleva o R² dentro da amostra e produz melhorias modestas de generalização geográfica da competitividade quando cada município tem peso igual. Contudo, esse benefício não se mantém de forma consistente quando o ajuste e a avaliação são ponderados pelos votos válidos municipais. A margem assinada apresenta ganhos ainda maiores na análise não ponderada, mas a melhora também desaparece na especificação ponderada de oito vizinhos. Assim, as conclusões apontam contribuição **condicionada à métrica de avaliação**, não superioridade geral de modelos socioespaciais. A autocorrelação residual permanece expressiva em todas as alternativas.

A documentação central já incorpora a revisão comparativa da literatura, ponderação populacional anterior, exclusão de capitais e grandes municípios e auditoria documental dos votos. Antes de submeter, continuam necessários: (a) verificação bibliográfica integral dos principais antecedentes e normalização das referências; (b) avaliação inferencial adequada à dependência espacial e análise de especificações de vizinhança/contiguidade; (c) justificativa editorial transparente do caráter retrospectivo das versões do IBGE e da divergência não resolvida no primeiro turno de 2018; (d) inspeção final das bases abertas, licenças, tabelas, equações e metadados; e (e) eventual validação temporal estrita, caso se pretenda reivindicar previsão fora do tempo. Não reivindicar causalidade ou superioridade preditiva geral. A possibilidade de extrapolação temporal exige reconstruir vintages de dados disponíveis antes de cada pleito.

## Disponibilidade dos dados e replicação

Os resultados eleitorais derivam de bases públicas do TSE e as covariáveis, de fontes públicas do IBGE. O repositório independente mantém scripts, controles, bases derivadas, registros de integridade e execuções automatizadas:

- [Indicadores de competitividade, segundo turno v02](../outputs/competitividade_v02/competitividade_e_margem_assinada_segundo_turno.csv)
- [Complementos de primeiro turno v02](../outputs/competitividade_v02/indicadores_complementares_primeiro_turno.csv)
- [Resultados de regressão e sensibilidade direcional](../outputs/competitividade_modelos_v01/modelos_competitividade_e_direcao_k4_k8_k12.csv)
- [Validação por UFs](../outputs/competitividade_modelos_v01/validacao_uf_detalhada.json)
- [Sensibilidade por votos válidos](../outputs/competitividade_ponderada_v01/modelos_ponderados_competitividade_e_direcao.csv)
- [Relatório da ponderação](RELATORIO_SENSIBILIDADE_PONDERADA_2026-10-10.md)
- [Pesos populacionais, capitais e grandes cidades](../outputs/robustez_demografica_v01/robustez_pesos_populacao_e_grandes_cidades.csv)
- [Manifesto da robustez demográfica](../outputs/robustez_demografica_v01/manifesto.json)
- [Conciliação de candidaturas e totais eleitorais](../outputs/auditoria_documental_final_v01/reconciliacao_candidatos_e_totais.csv)
- [Status de auditoria documental](../outputs/auditoria_documental_final_v01/manifesto_auditoria_2018_2022.json)
- [Matriz de literatura](REVISAO_LITERATURA_COMPETITIVIDADE_2026-10-10.md)
- [Protocolo e definições](PROTOCOLO_COMPETITIVIDADE_ELEITORAL_V01.md)
- [Script de indicadores](../scripts/15_indicadores_competitividade.py)
- [Script dos modelos](../scripts/16_modelos_competitividade.py)
- [Repositório](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais)

A versão anterior do artigo sobre HHI foi preservada como documento de trabalho distinto; nenhum código ou resultado do artigo de dinâmica de manada organizacional foi alterado.

## Referências e fontes acadêmicas verificadas

BRAGA, Maria do Socorro; ZOLNERKEVIC, Aleksei. Padrões de votação no tempo e no espaço: classificando as eleições presidenciais brasileiras. *Opinião Pública*, 26(1), p. 1–33, 2020. https://periodicos.sbu.unicamp.br/ojs/index.php/op/article/view/8659514.

ALKMIM, Antonio Carlos; TERRON, Sonia Luiza. O Brasil é realmente um país polarizado? Análise das eleições presidenciais de 1989 a 2018. *Estudos Avançados*, 36(106), 2022. DOI: https://doi.org/10.1590/s0103-4014.2022.36106.002.

MASULLO, Yata Anderson Gonzaga; SILVA JUNIOR, Rubens Pereira e. Geografia do voto: influências das singularidades territoriais nas eleições presidenciais do Brasil ao Maranhão. *Revista do Departamento de Geografia*, 2024. DOI: https://doi.org/10.11606/eISSN.2236-2878.rdg.2024.207979.

RESENDE, Gustavo Sousa; AZEVEDO, Daniel Abreu de. Conjuntura de fronteira e voto nas eleições presidenciais de 2022: uma análise do efeito contextual do espaço. *Caderno de Geografia*, 35(83), p. 1195, 2025. DOI: https://doi.org/10.5752/P.2318-2962.2025v35n83p1195.

NICOLAU, Jairo. Ascensão urbana e recuo metropolitano: a geografia eleitoral de Jair Bolsonaro em 2018 e 2022. *Estudos Avançados*, 40(117), 2026. DOI: https://doi.org/10.1590/s0103-4014.2026.40117.005.

KING, Gary. *A Solution to the Ecological Inference Problem: Reconstructing Individual Behavior from Aggregate Data*. Princeton: Princeton University Press, 1997.

MORAN, P. A. P. Notes on Continuous Stochastic Phenomena. *Biometrika*, v. 37, n. 1–2, p. 17–23, 1950. DOI: https://doi.org/10.1093/biomet/37.1-2.17.

OPENSHAW, Stan. *Ecological Fallacies and the Analysis of Areal Census Data*. Environment and Planning A, 1984. DOI: https://doi.org/10.1068/a160017.

NASCIMENTO, Jacson Cruz do. *Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional*. Zenodo, 2026. https://doi.org/10.5281/zenodo.21985858.

TRIBUNAL SUPERIOR ELEITORAL (TSE). *Portal de Dados Abertos*. Resultados presidenciais de 2018 e 2022. https://dadosabertos.tse.jus.br.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). *SIDRA*. Tabelas 202, 5938 e 6579. https://sidra.ibge.gov.br.
