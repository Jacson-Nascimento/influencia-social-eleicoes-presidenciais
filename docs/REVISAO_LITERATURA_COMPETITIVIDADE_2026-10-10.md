# Revisão comparativa da literatura e delimitação de contribuição

**Artigo:** Geografia da competitividade eleitoral no Brasil: fatores socioeconômicos e contexto espacial nos segundos turnos de 2018 e 2022.  
**Autor:** Jacson Cruz do Nascimento. **Atualização:** 10/10/2026.

## Escopo e critério de verificação

Foram conferidos título, autores, ano, resumo, fonte editorial e, quando disponível, DOI na página pública da editora. Os comentários de conteúdo abaixo são limitados ao resumo e às descrições publicadas, salvo quando expressamente assinalado. Não se alega revisão sistemática exaustiva nem leitura integral de todos os artigos.

A pesquisa corrente diferencia duas variáveis agregadas no segundo turno: competitividade `C = 1 - |v13-voponente|/(v13+voponente)` e margem assinada `M=(v13-voponente)/(v13+voponente)`. Confronta modelos socioeconômicos locais e contextuais, com validação por UFs fora do treino, tanto com pesos municipais uniformes quanto com pesos por população anterior e votos válidos observados. O foco não é demonstrar causalidade de influência interpessoal.

## Matriz de comparação (obras confirmadas)

| Referência | Questão e recorte documentados | Relação com este artigo | Limite para reivindicação de novidade |
|---|---|---|---|
| **Braga e Zolnerkevic (2020)** | Classificam eleições presidenciais de 1989 a 2018 em padrões espaciais e temporais, com análise fatorial da votação dos primeiros colocados em microrregiões. | Antecedente sobre persistência e mudanças territoriais do voto. | Não reivindicar pioneirismo em comparar persistência espaço-temporal das eleições brasileiras. |
| **Alkmim e Terron (2022)** | Estudam polarização geográfica em oito eleições presidenciais, de 1989 a 2018, com estatísticas espaciais em 5.570 municípios. | Referência central de polarização e agrupamentos municipais. | Moran e georreferenciamento de votos, isoladamente, não são contribuição original. |
| **Masullo e Silva Junior (2024)** | Examinam a geografia do voto de 2018 e 2022, comparando escalas nacional, regional e local no Maranhão. | Precedente com o mesmo intervalo eleitoral, e alerta para efeitos de escala. | Não alegar ineditismo de estudo geográfico de 2018 e 2022. |
| **Resende e Azevedo (2025)** | Analisam efeito contextual do espaço em municípios da zona de fronteira na eleição de 2022, com modelagem de regressão e recorte territorial específico. | Evidencia que contexto territorial e covariáveis já são objetos de investigação. | Não alegar primeiro uso de modelos com efeitos contextuais eleitorais no Brasil. |
| **Nicolau (2026)** | Estuda o peso relativo de metrópoles, porte dos municípios e margens eleitorais de 2018 e 2022, destacando a assimetria entre cidades. | Antecedente especialmente importante para testar exclusão de capitais e ponderações por população/votos. | Qualquer conclusão sobre grandes municípios deve ser confrontada com esse resultado documentado. |

## Fontes verificadas, com ligações editoriais

- BRAGA, Maria do Socorro; ZOLNERKEVIC, Aleksei. **Padrões de votação no tempo e no espaço: classificando as eleições presidenciais brasileiras**. *Opinião Pública*, Campinas, 26(1), p. 1–33, 2020. Página oficial: https://periodicos.sbu.unicamp.br/ojs/index.php/op/article/view/8659514.
- ALKMIM, Antonio Carlos; TERRON, Sonia Luiza. **O Brasil é realmente um país polarizado? Análise das eleições presidenciais de 1989 a 2018**. *Estudos Avançados*, 36(106), 2022. DOI: https://doi.org/10.1590/s0103-4014.2022.36106.002.
- MASULLO, Yata Anderson Gonzaga; SILVA JUNIOR, Rubens Pereira e. **Geografia do voto: influências das singularidades territoriais nas eleições presidenciais do Brasil ao Maranhão**. *Revista do Departamento de Geografia*, 2024. DOI: https://doi.org/10.11606/eISSN.2236-2878.rdg.2024.207979.
- RESENDE, Gustavo Sousa; AZEVEDO, Daniel Abreu de. **Conjuntura de fronteira e voto nas eleições presidenciais de 2022: uma análise do efeito contextual do espaço**. *Caderno de Geografia*, 35(83), p. 1195, 2025. DOI: https://doi.org/10.5752/P.2318-2962.2025v35n83p1195.
- NICOLAU, Jairo. **Ascensão urbana e recuo metropolitano: a geografia eleitoral de Jair Bolsonaro em 2018 e 2022**. *Estudos Avançados*, 40(117), 2026. DOI: https://doi.org/10.1590/s0103-4014.2026.40117.005.

## Contribuição incremental defensável

O estudo atual poderá acrescentar quatro elementos comparativos, a depender dos testes finais: (i) medida simétrica da competitividade separada da direção assinada do voto; (ii) contraste formal entre controles locais e médias socioeconômicas da vizinhança, sob a mesma unidade municipal e variável dependente; (iii) avaliação de generalização para UFs inteiras omitidas; (iv) contraste explícito entre pesos uniformes, população de período anterior e votos válidos observados, combinado com exclusões de capitais e grandes cidades.

**Não é legítimo interpretar maior R² in-sample como prova de poder preditivo superior.** Com regressoras adicionais, o R² ordinário nunca cai na mesma amostra; importam resultados fora da amostra e a estabilidade da ponderação.

O mecanismo de influência social não é identificado por semelhança espacial nem pela inclusão de características dos vizinhos. O artigo não reivindicará causalidade, difusão comportamental ou previsão de eleição futura.

## Pendências para julgamento editorial

1. Registrar os resultados das análises com pesos populacionais 2017/2021, exclusão de capitais e maiores 1% e 5%, confrontando sinal e magnitude do RMSE.
2. Avaliar a existência de colinearidade espacial e capacidade adicional frente à correlação histórica da competitividade, sem reutilizar resultados de anos de teste como covariáveis de treino.
3. Atualizar resumo, título e conclusões conforme a análise de robustez, inclusive casos de piora; evitar alegar contribuição universal.
4. Na revisão editorial final, conferir páginas e demais dados bibliográficos e realizar leitura integral dos principais trabalhos para comparação metodológica aprofundada, não apenas de resumos.
