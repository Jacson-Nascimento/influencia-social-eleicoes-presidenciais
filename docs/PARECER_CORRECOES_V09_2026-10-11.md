# Revisão crítica v09 — inferência macrorregional, referências e redação

**Autor:** Jacson Cruz do Nascimento. **Data:** 11 de outubro de 2026.  
**Evidência:** manuscrito v08, reestimação independente no mesmo repositório e páginas editoriais originais. Versões anteriores preservadas.

## Inferência: atualização obrigatória da Tabela A2

A versão anterior da Tabela A2 reportava teste conjunto de médias socioeconômicas de vizinhos de modelos **com efeitos fixos de UF, sem macrorregião separada**. Não pode ser citada como inferência do benchmark de cinco macrorregiões usado na Tabela 7.

A reestimação v09 usa intercepto, quatro covariáveis socioeconômicas municipais, quatro indicadores macrorregionais e quatro médias socioeconômicas de vizinhança (k=8), amostra de 5.565 municípios por eleição, **sem efeitos fixos de UF adicionais**, pois estes tornariam as dummies de região colineares. A UF serve de unidade de agrupamento para erros robustos CR1; Conley (100/250 km) permite associação residual através de fronteiras estaduais. Os resultados do segundo turno são:

| Ano | Desfecho | Peso | p Wald CR1 por UF | p Conley 250 km |
|---|---|---|---:|---:|
| 2018 | C | Igual | 0,248599 | 0,187228 |
| 2018 | C | População | 0,531972 | 0,379910 |
| 2018 | M | Igual | 1,38411 × 10⁻⁷ | 9,68939 × 10⁻¹⁶ |
| 2018 | M | População | 0,005515 | 0,002375 |
| 2022 | C | Igual | 0,316862 | 0,081860 |
| 2022 | C | População | 0,194260 | 0,055032 |
| 2022 | M | Igual | 2,79777 × 10⁻⁸ | 7,51243 × 10⁻¹⁸ |
| 2022 | M | População | 0,001440 | 0,000167 |

Os coeficientes contextuais de **M** estão conjuntamente associados à votação segundo essas matrizes de covariância. Isso **não contradiz** a falta de ganho estável no erro de validação de M com pesos populacionais. O Wald é inferência de coeficientes em amostra; o RMSE mede generalização geográfica em UFs omitidas. Reamostragem de 27 UFs não elimina correlação entre estados vizinhos.

- [Código reproduzível](../scripts/26_inferencia_regional_wald_conley.py)
- [Resultados Wald/Conley](../outputs/inferencia_regional_v09/wald_conley_com_macrorregiao.csv)
- [Manifesto de especificação](../outputs/inferencia_regional_v09/manifesto.json)

## Discussão e limites

O artigo v09 qualifica os intervalos por UFs positivos de M como evidência **sugestiva**: para peso municipal igual e macrorregião, o ganho RMSE é +4,67% (IC 95% +1,30% a +7,17%) em 2018, e +4,47% (+1,08% a +6,82%) em 2022, mas o método não trata integralmente dependência entre UFs vizinhas. Sob população anterior os ganhos são +0,23% e −1,57%, com intervalos que cruzam zero.

A **Tabela 8** é retomada na Discussão e na conclusão: SEM-GMM apresenta elevada dependência residual, inclusive Moran bruto acima de 0,5; SAR-IV apresentou estimativas de rho próximas ou superiores a 1 e primeiro estágio parcial de aproximadamente 0,07 a 0,11. Não se interpretam como parâmetros estruturais estáveis nem como identificação de influência interpessoal. O artigo permanece limitado a duas eleições, centroides e validação geográfica de cinco folds.

## Conciliação documental

A seção que antes se intitulava *Auditoria documental* foi renomeada **Conciliação documental dos votos de 2018 e 2022**. Conservam-se os 76 votos de diferença no primeiro turno de 2018 entre o arquivo de votação e o registro histórico oficial do TSE, sem atribuição de causa ou ajuste artificial das contagens. O desfecho principal permanece calculado com segundos turnos conciliados.

## Referências brasileiras recentes verificadas no catálogo editorial

- MASULLO, Yata Anderson Gonzaga; SILVA JUNIOR, Rubens Pereira e. *Geografia do voto: influências das singularidades territoriais nas eleições presidenciais do Brasil ao Maranhão*. **Revista do Departamento de Geografia**, v. 44, e207979, publicado em 14 ago. 2024. DOI: https://doi.org/10.11606/eISSN.2236-2878.rdg.2024.207979. Editora: https://revistas.usp.br/rdg/pt_BR/article/view/207979.
- RESENDE, Gustavo Sousa; AZEVEDO, Daniel Abreu de. *Conjuntura de fronteira e voto nas eleições presidenciais de 2022: uma análise do efeito contextual do espaço*. **Caderno de Geografia**, 35(83), 1195, publicado em 1º out. 2025. DOI: https://doi.org/10.5752/P.2318-2962.2025v35n83p1195. Editora: https://periodicos.pucminas.br/geografia/article/view/36473.
- NICOLAU, Jairo. *Ascensão urbana e recuo metropolitano: a geografia eleitoral de Jair Bolsonaro em 2018 e 2022*. **Estudos Avançados**, 40(117), e40117091, publicado em 7 ago. 2026. DOI: https://doi.org/10.1590/s0103-4014.2026.40117.005. Texto integral e metadados: https://www.scielo.br/j/ea/a/fPyVfr9W3dNRkv4xQZqXSSR/?format=html&ilang=pt_BR.

Confirmação editorial de autoria, título, DOI, ano e pertinência de conteúdo; não se apresenta como detector formal de plágio nem revisão sistemática.

## Entrega

Novo arquivo Word/PDF em 23 páginas, com onze tabelas preservadas, Tabela A2 atualizada, seção de Conciliação documental renomeada, discussão dos diagnósticos espaciais e manutenção do **Abstract apenas em inglês** e declaração de IA. Versão v08 e demais originais preservados; submissão não efetuada.
