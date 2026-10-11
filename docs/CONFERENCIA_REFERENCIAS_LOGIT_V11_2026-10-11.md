# Conferência das referências e do logit fracionário — v11 (11/10/2026)

**Artigo:** Geografia da competitividade eleitoral no Brasil: contexto socioeconômico e eleições presidenciais de 2018 e 2022. **Autor:** Jacson Cruz do Nascimento.

## 1. Referências verificadas em fontes externas ao projeto

Foram abertos os registros editoriais originais, confirmando a autoria, os títulos, a publicação e os DOIs:

1. MASULLO, Yata Anderson Gonzaga; SILVA JUNIOR, Rubens Pereira e. **Geografia do voto: influências das singularidades territoriais nas eleições presidenciais do Brasil ao Maranhão**. *Revista do Departamento de Geografia*, v. 44, e207979, 2024. DOI: https://doi.org/10.11606/eISSN.2236-2878.rdg.2024.207979. **Fonte editorial:** https://revistas.usp.br/rdg/pt_BR/article/view/207979. O PDF do artigo conta 14 páginas, iniciadas na página 1 e terminadas na 14.
2. RESENDE, Gustavo Sousa; AZEVEDO, Daniel Abreu de. **Conjuntura de fronteira e voto nas eleições presidenciais de 2022: uma análise do efeito contextual do espaço**. *Caderno de Geografia*, v. 35, n. 83, **p. 1195–1223**, 2025. DOI: https://doi.org/10.5752/P.2318-2962.2025v35n83p1195. **Fonte editorial:** https://periodicos.pucminas.br/geografia/article/view/36473. **Texto integral:** https://periodicos.pucminas.br/geografia/article/download/36473/24678/145795. A faixa 1195–1223 foi confirmada diretamente nos números impressos no PDF de 29 páginas; a página inicial aparece na primeira folha e a final na última. A forma automática "Como Citar" do periódico exibe apenas a página inicial, portanto a paginação integral foi conferida no PDF.
3. NICOLAU, Jairo. **Ascensão urbana e recuo metropolitano: a geografia eleitoral de Jair Bolsonaro em 2018 e 2022**. *Estudos Avançados*, v. 40, n. 117, e40117091, 2026. DOI: https://doi.org/10.1590/s0103-4014.2026.40117.005. **Fonte editorial:** https://www.scielo.br/j/ea/a/fPyVfr9W3dNRkv4xQZqXSSR/abstract/?lang=en. A SciELO confirma artigo, data eletrônica, autor e identificador.

Os três registros **existem nas páginas das editoras**. Isso é verificação bibliográfica externa, não revisão por pares do presente manuscrito nem auditoria científica independente.

## 2. OLS e logit fracionário de 2018: coincidência apenas no arredondamento

**Especificação:** desfecho C; quatro controles municipais do IBGE; cinco macrorregiões (quatro dummies); contextual k=8; pesos iguais entre os 5.565 municípios; cinco partições com UFs inteiras omitidas.

Os registros em `outputs/benchmark_geografico_v02/comparacao_benchmarks_regionais.csv` têm:

| Modelo | RMSE local | RMSE local + vizinhos | Ganho relativo exato |
|---|---:|---:|---:|
| OLS | 0,200183997 | 0,202394349 | **−1,104160277%** |
| Logit fracionário | 0,200035563 | 0,202241844 | **−1,102944424%** |

Em ambos os casos, a apresentação com **duas casas decimais é −1,10%**, embora os valores sejam distintos em 0,001216 ponto percentual.

**Conferência independente da aritmética:** os 27 registros estaduais de `outputs/benchmark_geografico_v02/sse_por_uf_e_modelo.csv` foram somados por modelo; o RMSE foi recalculado como a raiz da razão entre SSE e soma dos pesos. O percentual de diferença entre RMSE local e contextual concordou com o CSV original até a precisão do armazenamento.

**Conferência da implementação:** `scripts/22_benchmark_geografico_competitividade.py`, funções `predict` e `cv_uf`, contém dois estimadores diferentes: mínimos quadrados ponderados no caso linear; quase-verossimilhança Bernoulli com ligação logística inversa `expit` e otimização L-BFGS-B para o desfecho fracionário. Médias/desvios para padronização são calculados somente nos dados de treino, assim como os coeficientes. A perda de validação é calculada nos municípios dos estados omitidos. Não há indício nessa rotina de que os dois estimadores compartilhem os mesmos coeficientes por engano.

A concordância do resultado em duas casas decimais **não demonstra igualdade dos estimadores**, nem estabelece que o modelo esteja correto em todos os seus pressupostos. O logit fracionário é uma análise de sensibilidade, não instrumento de causalidade.

## 3. Alterações editoriais restritas da versão v11

- Resultados exatos de 2018 (−1,104160% OLS e −1,102944% logit fracionário) incluídos nos resultados, explicando o arredondamento.
- Declaração de IA explicita que as verificações automáticas e a conciliação do projeto **não constituem auditoria externa ou certificação científica independente**.
- Considerações finais restauram a negativa inequívoca: **não se identifica causalidade nem se demonstra contágio social entre eleitores**.
- Mantidos os resultados econômicos, metodológicos, estatísticos, seis tabelas principais, cinco suplementares, nove imagens, declarações e a nota documental dos 76 votos do primeiro turno de 2018.
- Documento v10 preservado. v11 criada como arquivos DOCX, PDF e DOC separados, com PDF de 22 páginas e revisão visual.

**Estado para submissão:** pronto para conferência final do próprio autor e compatibilização com um periódico escolhido; avaliação por pares, detector de similaridade e documentação de responsabilidade autoral continuam etapas separadas.
