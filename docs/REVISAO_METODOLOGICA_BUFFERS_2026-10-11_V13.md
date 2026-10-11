# Revisão metodológica v13 — validação por UF com buffers geográficos

**Autor:** Jacson Cruz do Nascimento. **Data:** 2026-10-11. **Base:** manuscrito v12 e resultados oficiais TSE/IBGE.

## A pergunta que a nova análise responde

O desenho anterior retinha UFs completas para validação, mas municípios de diferentes UFs podiam estar próximos entre treino e teste. Recalculamos a validação de cinco dobras por UFs inteiras com remoção de municípios de treinamento próximos aos municípios de teste: **0, 100 e 250 km**, segundo a distância entre centroides da malha IBGE de 2022. Os municípios testados são idênticos; as amostras de treino e os dois modelos são reestimados em cada dobra. As regressoras de vizinhança usam apenas covariáveis IBGE, não votos dos vizinhos. A versão 0 km reproduz o benchmark regional v02.

### Resultado: ganho de RMSE (%) frente a quatro controles locais + macrorregião

| Ano | Desfecho | Peso | 0 km | 100 km | 250 km |
|---|---|---|---:|---:|---:|
| 2018 | Competitividade | Igual | −1,10 | +0,50 | −1,46 |
| 2018 | Competitividade | População anterior | +0,45 | −0,42 | −1,07 |
| 2018 | Margem assinada | Igual | +4,67 | +3,95 | +9,49 |
| 2018 | Margem assinada | População anterior | +0,23 | +2,44 | +2,19 |
| 2022 | Competitividade | Igual | −0,54 | −1,15 | −1,76 |
| 2022 | Competitividade | População anterior | +0,55 | −0,85 | +1,03 |
| 2022 | Margem assinada | Igual | +4,47 | +5,40 | +8,47 |
| 2022 | Margem assinada | População anterior | −1,57 | +3,06 | +8,42 |

Com pesos uniformes, a competitividade **não** ganha estabilidade; a margem mantém incrementos positivos nos três recortes. Com pesos populacionais, os intervalos de UF continuam amplos e não respaldam um benefício geral. Uma faixa maior reduz o treino mínimo de 3.624 para 2.769 e 1.903 municípios por dobra, de forma que mudança de desempenho não identifica isoladamente 'vazamento espacial'. A matriz kNN8 e o uso das covariáveis de municípios testados no cálculo de WX são *transdutivos* para características IBGE, sem dados eleitorais de teste. Buffers não eliminam dependência entre UFs distantes e não constituem inferência causal.

## Reprodutibilidade

- [Código do novo teste](../scripts/27_validacao_buffer_espacial.py)
- [Workflow de teste automatizado](../.github/workflows/robustez_buffer_espacial_v13.yml)
- [Resultado das 36 especificações](../outputs/robustez_buffer_espacial_v13/validacao_uf_buffer_espacial.csv)
- [Somas de erros para 27 UFs por cenário](../outputs/robustez_buffer_espacial_v13/sse_por_uf_buffer_espacial.csv)
- [Composição das cinco dobras e faixas de exclusão](../outputs/robustez_buffer_espacial_v13/folds_buffer_espacial.csv)
- [Manifesto de métodos e limites](../outputs/robustez_buffer_espacial_v13/manifesto.json)
- [CI bem-sucedida](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/actions/runs/38170154738)

A reestimação não muda os resultados anteriormente verificados para C e M; é diagnóstico adicional. As versões antigas e a dissertação de Nascimento (2024), citada na fundamentação, permanecem preservadas. Mantém-se a ressalva documental sem causa explicada dos 76 votos no primeiro turno de 2018.

## Verificação externa das três publicações brasileiras

- [Masullo e Silva Junior (2024), USP](https://revistas.usp.br/rdg/pt_BR/article/view/207979): DOI 10.11606/eISSN.2236-2878.rdg.2024.207979; v.44, e207979.
- [Resende e Azevedo (2025), PUC Minas](https://periodicos.pucminas.br/geografia/article/view/36473): DOI 10.5752/P.2318-2962.2025v35n83p1195; v.35, n.83, páginas 1195–1223 confirmadas no [PDF da revista](https://periodicos.pucminas.br/geografia/article/download/36473/24678/145795).
- [Nicolau (2026), SciELO](https://www.scielo.br/j/ea/a/fPyVfr9W3dNRkv4xQZqXSSR/?format=html&ilang=pt_BR): DOI 10.1590/s0103-4014.2026.40117.005; v.40 n.117, e40117091.

As conferências são editoriais e computacionais do projeto, não auditoria científica independente. Nenhuma publicação/submissão foi efetuada e não se atribui nota ou aumento de pontuação sem avaliação externa.
