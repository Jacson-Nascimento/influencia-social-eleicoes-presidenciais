# Correções científicas e editoriais v06 — 11/10/2026

**Jacson Cruz do Nascimento.** Versões anteriores preservadas, sem submissão a periódico.

## Benchmark regional

O artigo foi reestimado em 5.565 municípios de 2018 e 2022, com validação por grupos de UFs omitidas. O benchmark novo inclui macrorregiões e, em sensibilidades, latitude/longitude e termos quadráticos, além dos quatro controles IBGE. Com pesos iguais e oito vizinhos, a redução do erro RMSE da competitividade muda de +1,92% para **−1,10% (2018)** e de +4,99% para **−0,54% (2022)** ao acrescentar macrorregião no modelo convencional. Para a margem assinada, os ganhos caem de +17,09% para +4,67% e de +18,53% para +4,47%, respectivamente. Intervalos exploratórios de 95% para competitividade com macrorregião: −3,25% a +0,79% (2018) e −1,82% a +0,80% (2022), contendo zero.

## Logit fracionário e modelos espaciais

Em substituição à suposição de que OLS é a única família aceitável para competitividade em [0,1], a sensibilidade logit fracionária foi executada e produziu reduções de RMSE de **−1,10% e −0,56%** no benchmark com macrorregião e pesos iguais. Foram executados SEM-GMM e SAR-IV/2SLS; o último apresentou coeficientes espaciais próximos ou superiores a 1 e primeiro estágio parcial modesto, portanto seus parâmetros não devem receber interpretação estrutural estável nem causal.

## Bootstrap geográfico corrigido

A versão inicial dos benchmarks regionais apresentou erro na fórmula dos **intervalos bootstrap**: denominador da soma dos pesos em lugar da soma dos erros quadráticos do modelo de referência. O **ganho pontual do RMSE não foi afetado**. O erro foi corrigido e publicado em [benchmark geográfico v02](../outputs/benchmark_geografico_v02/comparacao_benchmarks_regionais.csv); os intervalos da v01 não devem ser utilizados. A v01 foi preservada por transparência.

## Correções de integridade e apresentação

Foram removidos LaTeX bruto, caminhos Markdown relativos e instruções internas. A Figura 2 foi substituída por comparação legível de benchmarks; foram acrescentadas duas tabelas com resultados novos, eliminada a alegação de “auditoria independente” e incluída declaração transparente de apoio da IA generativa à redação, scripts e editoração. Os DOIs dos artigos de Masullo e Silva Junior (2024), Resende e Azevedo (2025) e Nicolau (2026) foram confirmados em periódicos. Inclusas referências de Papke e Wooldridge (1996) e Anselin (1988). O limite de duas eleições e a impossibilidade de inferência causal permanecem expressos.

A ressalva documental de **76 votos no primeiro turno de 2018** continua no manuscrito, com decomposição de 20, 46 e 10 votos, sem causa identificada. O desfecho central do artigo utiliza o segundo turno de 2018, cujos totais foram conciliados.

## Conclusão

A melhora de previsão obtida com atributos dos municípios vizinhos no benchmark local simples não persiste para competitividade após controlar a macrorregião. Esta é uma correção substantiva da conclusão do artigo. Não se afirma influência social entre eleitores.

Repositório: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais

Scripts: [benchmarks regionais](../scripts/22_benchmark_geografico_competitividade.py) e [modelos espaciais](../scripts/24_modelos_espaciais_formais_v02.py). Arquivos Word, PDF e planilha suplementar foram arquivados no Google Drive do projeto.
