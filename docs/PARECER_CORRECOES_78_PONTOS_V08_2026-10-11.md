# Correções da avaliação externa de 78/100 — manuscrito v08

**Artigo:** Geografia da competitividade eleitoral no Brasil: contexto socioeconômico e eleições presidenciais de 2018 e 2022.  
**Autor:** Jacson Cruz do Nascimento. **Data:** 11 de outubro de 2026.  
**Escopo:** revisão editorial e reamostragem de intervalos; sem alterar votos, covariáveis, modelos ou resultados pontuais.

## 1. Por que apareciam 1.999 e 4.999 reamostragens?

Os experimentos eram diferentes: a análise anterior de validação e inferência espacial em `outputs/inferencia_espacial_final_v01` usou **4.999** reamostragens de unidades da federação; a primeira execução do benchmark geográfico em `outputs/benchmark_geografico_v02` usou **1.999**. Portanto, a divergência no texto era explicável pela versão de origem dos intervalos, mas prejudicava a clareza editorial.

Para uniformizar o manuscrito, foi executada **nova reamostragem com 4.999 repetições** sobre as somas de erros quadráticos, por UF, já validadas e publicadas em v02. O número de municípios, os cinco folds, os controles, a tabela de SSE e as estimativas de RMSE permaneceram idênticos. O código está em [scripts/25_bootstrap_regional_4999.py](../scripts/25_bootstrap_regional_4999.py); a nova saída é [benchmark_geografico_v03](../outputs/benchmark_geografico_v03).

| Desfecho e peso | 2018: ganho e IC 95%, benchmark com macrorregião | 2022: ganho e IC 95%, benchmark com macrorregião |
|---|---|---|
| C, municípios iguais | −1,10%; [−3,27%; +0,69%] | −0,54%; [−1,83%; +0,75%] |
| C, população anterior | +0,45%; [−1,40%; +1,78%] | +0,55%; [−1,21%; +2,22%] |
| M, municípios iguais | +4,67%; [+1,30%; +7,17%] | +4,47%; [+1,08%; +6,82%] |
| M, população anterior | +0,23%; [−4,65%; +3,83%] | −1,57%; [−6,65%; +3,87%] |

Os intervalos são percentis de UFs reamostradas de forma pareada. UFs vizinhas podem ter dependência, e esses resultados não são inferência causal.

## 2. Abstract atualizado

O resumo agora informa os resultados relevantes dos **dois desfechos**, sem confundi-los: C piora sob pesos iguais com macrorregião; M melhora 4,67%/4,47% sob pesos iguais, mas a vantagem não persiste sob ponderação populacional, com pontos +0,23% e −1,57% e ICs que atravessam zero.

## 3. Discussão e considerações finais reestruturadas

A redação diferencia três contextos de comparação: (a) benchmark socioeconômico local simples, no qual se observaram ganhos em C e M; (b) benchmark com macrorregião, que elimina o ganho em C e preserva apenas ganho moderado em M para municípios uniformes; (c) ponderação demográfica, que torna M inconclusiva e C próxima de zero. Nenhum RMSE ou R² é comparado diretamente entre C e M, pois os desfechos têm distribuições distintas.

Também foram removidas referências à fase editorial anterior, a expressão sobre revisão editorial dentro da Discussão e menções inadequadas a cálculos 'auditados' como se houvesse auditoria externa.

## 4. Fontes bibliográficas independentes verificadas

- MASULLO, Yata Anderson Gonzaga; SILVA JUNIOR, Rubens Pereira e. *Geografia do voto: influências das singularidades territoriais nas eleições presidenciais do Brasil ao Maranhão*. Revista do Departamento de Geografia, 44, e207979 (2024). DOI: https://doi.org/10.11606/eISSN.2236-2878.rdg.2024.207979. Página da editora: https://revistas.usp.br/rdg/pt_BR/article/view/207979
- RESENDE, Gustavo Sousa; AZEVEDO, Daniel Abreu de. *Conjuntura de fronteira e voto nas eleições presidenciais de 2022: uma análise do efeito contextual do espaço*. Caderno de Geografia, 35(83), 1195 (2025). DOI: https://doi.org/10.5752/P.2318-2962.2025v35n83p1195. Página da editora: https://periodicos.pucminas.br/geografia/article/view/36473
- NICOLAU, Jairo. *Ascensão urbana e recuo metropolitano: a geografia eleitoral de Jair Bolsonaro em 2018 e 2022*. Estudos Avançados, 40(117), e40117091 (2026). DOI: https://doi.org/10.1590/s0103-4014.2026.40117.005. Página da editora: https://www.scielo.br/j/ea/a/fPyVfr9W3dNRkv4xQZqXSSR/?format=html&ilang=pt_BR

Os títulos, DOIs, autoria e escopo publicado foram verificados independentemente em editoras. Essa verificação não substitui uma pesquisa bibliográfica sistemática ou avaliação de similaridade textual.

## 5. Integridade e apresentação

- 11 tabelas, figuras e apêndice mantidos, com nova Tabela 7 consistente;
- Nota de +76 votos no primeiro turno de 2018 mantida sem atribuir explicação não demonstrada;
- Endereço de arquivo markdown relativo retirado do texto principal;
- Disclosure do uso de ferramentas de inteligência artificial mantida;
- Dados, scripts e manuscritos anteriores preservados;
- Preparados DOCX, PDF e .doc na versão v08, com revisão visual da paginação.

**Status:** correções efetuadas; submissão não realizada. A avaliação por pares e os requisitos específicos do periódico continuam procedimentos independentes.
