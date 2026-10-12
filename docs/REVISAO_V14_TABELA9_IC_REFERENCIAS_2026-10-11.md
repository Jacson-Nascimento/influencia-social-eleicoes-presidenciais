# Revisão v14 — IC de 95% na Tabela 9 e verificação editorial externa

**Autor:** Jacson Cruz do Nascimento. **Data:** 11/10/2026.  
**Base original:** v13 — preservada integralmente.

## Alteração efetiva da Tabela 9

A Tabela 9 do artigo v13 reportava o ganho percentual de RMSE dos modelos contextuais sob buffers espaciais de **0, 100 e 250 km**, mas remetia o leitor ao material suplementar para consultar os intervalos de confiança. Na v14, a tabela apresenta na mesma célula:

- Linha 1: ganho ou perda percentual de RMSE;
- Linha 2: intervalo percentílico de 95%, entre colchetes, de **4.999 reamostragens pareadas das 27 UFs**.

Há oito combinações de ano (2018/2022), desfecho (competitividade C/margem assinada M) e ponderação (municípios iguais/população anterior), em três recortes espaciais: **24 ganhos e 24 intervalos**. Todos os resultados são os já calculados no trabalho v13; **nenhuma regressão ou base eleitoral foi reestimada especificamente para diagramar a v14**.

## Controle numérico independente do CSV de resultados

A partir do pacote `Resultados_Validacao_Buffer_Espacial_v13.zip`, os 27 registros por cenário em `sse_por_uf_buffer_espacial.csv` foram reagrupados e foi refeita a aritmética:

`RMSE = raiz( soma dos SSE / soma dos pesos )` e `ganho (%) = 100 * (1 - RMSE_contexto / RMSE_local)`.

Em seguida, usando as sementes definidas no código de análise, foram reproduzidas as 4.999 reamostragens de UFs com substituição e os percentis 2,5% e 97,5%. **As 24 linhas lineares reproduziram os resultados arquivados**, com diferenças abaixo de 1e-6.

### Valores de M, municípios com pesos iguais

| Eleição | Faixa | Ganho de RMSE | Intervalo exploratório 95% |
|---|---|---:|---:|
| 2018 | 0 km | +4,67% | [+1,40%; +7,13%] |
| 2018 | 100 km | +3,95% | [+0,94%; +7,00%] |
| 2018 | 250 km | +9,49% | [+3,04%; +13,17%] |
| 2022 | 0 km | +4,47% | [+0,93%; +6,80%] |
| 2022 | 100 km | +5,40% | [+1,70%; +7,98%] |
| 2022 | 250 km | +8,47% | [+3,40%; +11,44%] |

**Nota inferencial:** Esses IC são condicionados às partições fixas de UFs e pressupõem independência suficiente entre os grupos reamostrados. Não corrigem completamente a correlação entre UFs fronteiriças. A ampliação dos buffers reduz e altera a composição do treinamento. Os ganhos de M com ponderação populacional não apresentam intervalos consistentemente positivos, e os ganhos de C não são estáveis. Nenhum mecanismo causal é identificado.

## Fontes editoriais externas verificadas

- MASULLO, Yata Anderson Gonzaga; SILVA JUNIOR, Rubens Pereira e. *Geografia do voto: influências das singularidades territoriais nas eleições presidenciais do Brasil ao Maranhão*. **Revista do Departamento de Geografia**, vol. 44, e207979, 2024. DOI: https://doi.org/10.11606/eISSN.2236-2878.rdg.2024.207979. Ficha oficial da USP: https://revistas.usp.br/rdg/pt_BR/article/view/207979.
- RESENDE, Gustavo Sousa; AZEVEDO, Daniel Abreu de. *Conjuntura de fronteira e voto nas eleições presidenciais de 2022: uma análise do efeito contextual do espaço*. **Caderno de Geografia**, 35(83), **1195–1223**, 2025. DOI: https://doi.org/10.5752/P.2318-2962.2025v35n83p1195. Registro da PUC Minas: https://periodicos.pucminas.br/geografia/article/view/36473. PDF integral: https://periodicos.pucminas.br/geografia/article/download/36473/24678/145795. A primeira página impressa é 1195 e a última, **1223**, comprovadas no PDF de 29 páginas.
- NICOLAU, Jairo. *Ascensão urbana e recuo metropolitano: a geografia eleitoral de Jair Bolsonaro em 2018 e 2022*. **Estudos Avançados**, 40(117), 2026. DOI: https://doi.org/10.1590/s0103-4014.2026.40117.005. Texto e ficha na SciELO: https://www.scielo.br/j/ea/a/fPyVfr9W3dNRkv4xQZqXSSR/?format=html&ilang=pt_BR.

A conferência foi feita em documentos publicados por editoras, não em resumos de ferramentas ou em notas internas do projeto. Não constitui auditoria científica externa nem assegura ausência de plágio.

## Avaliação de uma terceira eleição

A adição das eleições presidenciais de **2014** é tecnicamente viável como novo exercício: o TSE disponibiliza resultados por município/zona e segundo turno. Fonte oficial: https://www.tse.jus.br/comunicacao/noticias/2014/Outubro/estatisticas-de-resultados-do-segundo-turno-ja-estao-disponiveis. A série mais longa exigiria reconstruir a base IBGE em versões temporais apropriadas, auditar a correspondência municipal e interpretar o finalista do PT nº 13 em 2014 como candidatura diferente daquelas de 2018/2022. **Nenhum resultado de 2014 foi calculado ou adicionado na v14.**

## Entregas e preservação

- Manuscrito v14: DOCX, DOC e PDF com **24 páginas A4**, mantendo as **12 tabelas** e a dissertação de Nascimento (2024).
- Tabela 9 diagramada para apresentar 24 ganhos e os correspondentes ICs de 95% no próprio artigo; legenda explicita OLS/WLS, sem confusão com logit fracionário.
- A conclusão separa C e M e ressalva a sensibilidade à ponderação populacional.
- Não alterados: arquivos e estimativas TSE/IBGE, modelos anteriores, autoria, versão v13, arquivos precedentes e o repositório de manada organizacional.
- Publicação/submissão não efetuada.
