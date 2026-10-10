# Concentração eleitoral, dependência espacial e contexto socioeconômico: evidências municipais das eleições presidenciais brasileiras de 2018 e 2022

**Jacson Cruz do Nascimento**  
Pesquisador independente, Brasília, Distrito Federal, Brasil.  
ORCID: https://orcid.org/0009-0006-6535-9569  
**Versão empírica 1.0:** 10 de outubro de 2026. Documento de trabalho, ainda não submetido à publicação.

## Resumo

Este artigo investiga a persistência espacial da concentração de votos nas eleições presidenciais brasileiras de 2018 e 2022 e examina em que medida características socioeconômicas e demográficas municipais explicam a dependência observada. A pesquisa integra votos nominais presidenciais disponibilizados pelo Tribunal Superior Eleitoral (TSE), geocódigos oficiais de correspondência TSE-IBGE, a malha municipal do Instituto Brasileiro de Geografia e Estatística (IBGE) e indicadores públicos de população, urbanização, composição por sexo e atividade econômica. O universo eleitoral abrange 5.570 municípios e os modelos com covariáveis completas incluem 5.565. Empregam-se o índice de concentração Herfindahl-Hirschman (HHI), autocorrelação global de Moran, regressões com efeitos fixos por UF e validação com estados mantidos fora do treinamento. A introdução dos controles municipais elevou o R² dos modelos em 2,31 a 4,58 pontos percentuais, mas a autocorrelação dos resíduos permaneceu elevada. A incorporação das características socioeconômicas de oito municípios próximos acrescentou entre 0,36 e 0,79 ponto percentual ao R², com melhoria agregada do RMSE na validação geográfica de 0,95% a 7,70%. Os resultados são consistentes com a presença de padrões territoriais persistentes não inteiramente explicados pelas variáveis observadas. Não constituem identificação causal de influência interpessoal, transferência individual de votos ou comportamento de manada.

**Palavras-chave:** comportamento eleitoral; econometria espacial; dependência territorial; concentração de votos; eleições presidenciais; dados abertos.

## 1. Introdução

A análise de resultados eleitorais agregados frequentemente identifica áreas contíguas com distribuições semelhantes de votos. Essa regularidade, contudo, não é suficiente para demonstrar a existência de imitação de preferências entre eleitores. População, urbanização, estrutura econômica, características demográficas e trajetória sociopolítica dos territórios podem estar associadas simultaneamente à composição do voto e à proximidade geográfica. Além disso, inferências sobre escolhas individuais a partir de unidades territoriais agregadas incorrem no problema de inferência ecológica discutido por King (1997).

O objetivo deste estudo é investigar a distribuição municipal de um indicador de concentração do voto presidencial, sua estabilidade entre eleições e a extensão em que variáveis públicas do IBGE reduzem a autocorrelação espacial observada. Uma questão complementar consiste em verificar se as características dos municípios próximos trazem informação explicativa adicional àquela fornecida pelas características do próprio município.

O estudo se relaciona conceitualmente com o artigo de Nascimento (2026) sobre dinâmica de manada em estruturas organizacionais, mas constitui uma pesquisa independente. O modelo organizacional parte de hipóteses de sinais informacionais, hierarquia e custos de discordância que não podem ser transpostas automaticamente para eleições democráticas. Preferências eleitorais não são acertos ou erros informacionais e, portanto, os parâmetros e estatísticas da simulação original não são utilizados como medidas empíricas do eleitorado.

## 2. Referencial e restrições de inferência

A autocorrelação espacial global pode ser quantificada pelo índice I de Moran (Moran, 1950), cuja interpretação depende da variável analisada e da matriz de vizinhança. A literatura metodológica de análise espacial, incluindo Anselin (1995), distingue padrões globais e heterogeneidade local. A configuração da unidade de agregação pode alterar substancialmente os resultados, conforme o problema da unidade areal modificável discutido por Openshaw (1984). Em estudos eleitorais, é necessário preservar a distinção entre associação geográfica e comportamento individual, nos termos de King (1997).

A hipótese empírica examinada é limitada: municípios próximos exibem indicadores de concentração semelhantes mesmo depois de controlar pelas quatro características socioeconômicas e demográficas disponíveis e pelas diferenças médias estaduais. A hipótese não exige, e o desenho não permite, inferir circulação de informação, coerção, influência de lideranças ou migração individual de votos entre candidaturas.

## 3. Dados e construção da amostra

### 3.1. Resultados eleitorais e geografia

Os votos nominais presidenciais são provenientes dos conjuntos de resultados do TSE de 2018 e 2022, por município e zona eleitoral, agregados por candidatura. Foram empregados os dois turnos de cada eleição. A correspondência entre o código eleitoral e o geocódigo de sete dígitos do IBGE foi estabelecida por meio da tabela oficial do TSE, sem aproximação por nomes. A geometria municipal provém da malha digital do IBGE de 2022.

Os registros de votação no exterior (UF ZZ) permanecem nas bases eleitorais originais, mas não integram as matrizes espaciais dos 5.570 municípios brasileiros.

A auditoria documental identificou divergência de 76 votos nominais válidos no primeiro turno de 2018 entre a distribuição do arquivo atual do TSE e a notícia histórica de totalização. A causa exata não foi estabelecida. Os dados originais foram preservados e o primeiro turno de 2018 permanece sob essa ressalva. O segundo turno de 2018 e ambos os turnos de 2022 foram conciliados.

### 3.2. Variável dependente

A concentração municipal dos votos presidenciais é descrita pelo índice HHI, calculado para cada município \\(i\\), eleição \\(e\\) e turno \\(t\\):

\\[
HHI_{iet} = \\sum_{c \\in C_{et}} \\left(\\frac{V_{icet}}{\\sum_{j \\in C_{et}}V_{ijet}}\\right)^2.
\\]

O índice assume valores mais elevados quando os votos válidos se concentram em menos candidaturas. Como o número de concorrentes diminui no segundo turno, parte da variação do HHI entre turnos é mecânica. Por isso, as regressões são estimadas separadamente por eleição e turno; diferenças de nível não são interpretadas diretamente como intensificação de influência social.

### 3.3. Covariáveis observáveis

Foram extraídos exclusivamente dados públicos do IBGE:

- População estimada em 2017 e 2021, para os exercícios associados a 2018 e 2022.
- PIB municipal a preços correntes de 2016 e 2020, expresso em mil reais.
- Parcela urbana da população e parcela feminina da população no Censo Demográfico 2010.

A proxy de PIB por pessoa resulta do PIB municipal, convertido de milhares de reais, dividido pela população estimada no ano subsequente. Trata-se de uma aproximação com referências temporais diferentes, não do indicador oficial de PIB per capita.

Os indicadores possuem anos de referência anteriores às eleições respectivas, mas foram obtidos em versões das bases públicas consultadas em 2026, que podem incluir revisões. Essa condição impede tratar a presente base como conjunto informacional estritamente disponível antes dos pleitos.

Cinco municípios não possuem todas as variáveis censitárias de 2010 na tabela analisada. Foram excluídos sem imputação, mantendo-se 5.565 municípios em uma amostra comum aos quatro modelos.

## 4. Estratégia empírica

### 4.1. Dependência espacial exploratória

A matriz espacial de referência utiliza os oito centroides municipais mais próximos, calculados com a geometria IBGE 2022. Examinam-se também quatro e doze vizinhos. O índice de Moran é estimado com 1.999 permutações para a caracterização original e 999 permutações na avaliação dos resíduos controlados. Os testes residuais incluem permutações restritas às UFs após centralização estadual e correção de Holm entre as quatro comparações principais.

Os valores-p de resíduos ajustados constituem diagnósticos exploratórios. O procedimento de permutar resíduos de regressão, sem uma estrutura de identificação específica, não fornece um teste formal de causalidade.

### 4.2. Modelos socioeconômicos

A primeira comparação emprega:

\\[
HHI_{iet}=\\alpha_{et}+\\gamma_{UF(i),et}+\\varepsilon_{iet},
\\]

e

\\[
HHI_{iet}=\\alpha_{et}+\\gamma_{UF(i),et}
+\\boldsymbol{\\beta}_{et}^{\\prime}X_{ie}
+\\varepsilon_{iet},
\\]

em que \\(X_{ie}\\) contém logaritmo da população, logaritmo da proxy de PIB por pessoa, fração urbana e fração feminina. Os modelos são descritivos e não presumem exogeneidade causal das covariáveis.

### 4.3. Extensão de contexto territorial

A especificação contextual acrescenta médias das mesmas características nos municípios vizinhos:

\\[
HHI_{iet}=\\alpha_{et}+\\gamma_{UF(i),et}
+\\boldsymbol{\\beta}_{et}^{\\prime}X_{ie}
+\\boldsymbol{\\theta}_{et}^{\\prime}W_k X_{ie}
+\\varepsilon_{iet}.
\\]

A matriz \\(W_k\\) emprega k=8 como especificação de referência, com k=4 e k=12 em sensibilidade. Não se utiliza \\(W_k HHI\\) nem se incorporam votos dos vizinhos ao conjunto de regressores. Logo, a especificação não estima transmissão de comportamento eleitoral.

### 4.4. Verificação geográfica

Comparações de modelos são realizadas na mesma amostra e sob igual variável dependente. Além do R² em amostra, foram executadas cinco partições com UFs inteiras mantidas fora do treinamento. Para evitar o uso de efeitos fixos não observados, a validação emprega modelos sem efeitos estaduais: a versão convencional contém quatro covariáveis municipais e a contextual acrescenta suas médias de vizinhança. Comparam-se os erros RMSE.

O cálculo dos atributos de vizinhança pode empregar características IBGE de municípios de teste, mas nunca seus valores observados de votos ou HHI. O exercício é parcialmente transdutivo quanto às covariáveis e não constitui previsão eleitoral ex ante.

## 5. Resultados

### 5.1. Controles municipais

| Ano | Turno | R² UF | R² UF + controles | Incremento |
|---|---|---:|---:|---:|
| 2018 | Primeiro | 0,4303 | 0,4596 | +2,93 p.p. |
| 2018 | Segundo | 0,4366 | 0,4597 | +2,31 p.p. |
| 2022 | Primeiro | 0,5846 | 0,6304 | +4,58 p.p. |
| 2022 | Segundo | 0,5132 | 0,5505 | +3,73 p.p. |

O aumento do ajuste indica que os controles capturam parcela adicional da heterogeneidade municipal de concentração. O Moran I dos resíduos, entretanto, permaneceu entre 0,4246 e 0,4825 na referência com oito vizinhos após sua inclusão, indicando estrutura espacial residual importante.

### 5.2. Ganho incremental do contexto socioeconômico dos vizinhos

| Ano | Turno | Ganho R² com contexto, k=8 | Melhora do RMSE em UFs de teste | Moran residual após contexto |
|---|---|---:|---:|---:|
| 2018 | Primeiro | +0,390 p.p. | 0,95% | 0,4226 |
| 2018 | Segundo | +0,365 p.p. | 2,04% | 0,4819 |
| 2022 | Primeiro | +0,788 p.p. | 7,70% | 0,4601 |
| 2022 | Segundo | +0,648 p.p. | 5,11% | 0,4709 |

Os ganhos adicionais foram modestos dentro da amostra. Na verificação geográfica, o agregado do RMSE melhorou nos quatro casos, mas houve dobras isoladas com piora em 2018. Os resultados positivos de 2022 em todas as cinco dobras não garantem desempenho semelhante fora dessas duas eleições históricas.

### 5.3. Sensibilidade e persistência

O incremento de R² contextual foi positivo para k=4, 8 e 12 em todas as combinações de eleição-turno. A associação espacial dos resíduos, contudo, permaneceu elevada, mesmo com os atributos dos municípios próximos. Como exercício separado, a correlação municipal do HHI entre 2018 e 2022 foi 0,8083 no primeiro turno e 0,9252 no segundo, sugerindo relativa persistência da distribuição territorial da concentração. Esse resultado também pode estar associado a fatores estruturais omitidos.

## 6. Discussão

Três resultados se destacam: a concentração eleitoral apresenta associação espacial na escala municipal; essa associação não desaparece após a inclusão das covariáveis examinadas; e o acréscimo de contexto socioeconômico da vizinhança produz um ganho modesto de explicação e de generalização geográfica.

Esses achados não permitem atribuir o padrão à dinâmica de manada. Um mecanismo de influência pressupõe informações sobre contatos, exposição, aprendizado social ou alguma variação exógena no ambiente de interação. O estudo utiliza apenas resultados territoriais agregados e características públicas municipais. Assim, as inferências dizem respeito à organização espacial da concentração de votos, não à decisão individual ou ao efeito de um eleitor sobre outro.

A diferença entre os testes estaduais e municipais anteriores também recomenda cautela: resultados de dependência geográfica são sensíveis à escala de agregação e à estrutura da matriz espacial. A contribuição atual do artigo é descritiva e metodológica, apoiada na transparência e replicabilidade dos cálculos.

## 7. Considerações finais

Nas eleições presidenciais brasileiras de 2018 e 2022, os controles socioeconômicos municipais selecionados aumentaram o ajuste da concentração do voto, sem eliminar a associação espacial residual. Incluir os atributos médios dos municípios próximos acrescentou ganhos estatísticos moderados, mas tampouco explicou integralmente a estrutura territorial remanescente.

As evidências não validam nem refutam diretamente o mecanismo de manada do modelo computacional organizacional. Para esse objetivo, serão necessárias medidas de exposição e interação social, estratégias de identificação adequadas e validação temporal com informação estritamente disponível no corte analisado. O artigo não fornece previsão de vencedor ou probabilidade de resultado para as eleições de 2026.

## Declaração de dados e replicação

As bases utilizadas são públicas e estão identificadas por fonte, período, código e integridade documental no repositório [influencia-social-eleicoes-presidenciais](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais). Bases municipais derivadas, scripts, protocolos, manifestações de integridade e resultados estão abertos, preservando versões anteriores. As fontes originais do TSE e IBGE mantêm suas respectivas condições de atribuição. A exceção de 76 votos na conciliação histórica do primeiro turno de 2018 está documentada, sem correção arbitrária.

Os principais artefatos são [modelos com controles](../outputs/socioeconomico_v01/modelos_e_moran_residual.csv), [comparação espacial](../outputs/contexto_espacial_v01/comparacao_contexto_espacial_k4_k8_k12.csv), [dados IBGE](../data/ibge_tratados/controles_pre_eleitorais_v02.csv) e [manifesto da comparação](../outputs/contexto_espacial_v01/metodologia.json).

## Referências verificadas

ANSELIN, Luc. Local Indicators of Spatial Association—LISA. *Geographical Analysis*, v. 27, n. 2, p. 93–115, 1995. DOI: https://doi.org/10.1111/j.1538-4632.1995.tb00338.x.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Censo Demográfico 2010, SIDRA, tabela 202; Produto Interno Bruto dos Municípios, tabela 5938; Estimativas da População, tabela 6579. Portal SIDRA, consultas em outubro de 2026. https://sidra.ibge.gov.br.

KING, Gary. *A Solution to the Ecological Inference Problem: Reconstructing Individual Behavior from Aggregate Data*. Princeton: Princeton University Press, 1997. https://gking.harvard.edu/publication/a-solution-to-the-ecological-inference-problem-reconstructing-individual-behavior-from-aggregate-data/.

MORAN, Patrick A. P. Notes on Continuous Stochastic Phenomena. *Biometrika*, v. 37, n. 1-2, p. 17–23, 1950. DOI: https://doi.org/10.1093/biomet/37.1-2.17.

NASCIMENTO, Jacson Cruz do. *Dinâmica de Manada Organizacional: um arcabouço teórico-computacional para hierarquia, influência social, silêncio e independência informacional*. Zenodo, versão 1.3, 2026. DOI: https://doi.org/10.5281/zenodo.21985858.

OPENSHAW, Stan. Ecological Fallacies and the Analysis of Areal Census Data. *Environment and Planning A*, v. 16, n. 1, 1984. DOI: https://doi.org/10.1068/a160017.

TRIBUNAL SUPERIOR ELEITORAL (TSE). Portal de Dados Abertos. Resultados eleitorais por município e zona, 2018 e 2022. https://dadosabertos.tse.jus.br/dataset/.
