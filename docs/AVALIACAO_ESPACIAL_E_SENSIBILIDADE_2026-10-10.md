# Autocorrelação espacial da concentração eleitoral nas UFs: 2018 e 2022

**Autor:** Jacson Cruz do Nascimento. **Resultado exploratório, não causal.**

## Dados e definição

Votos presidenciais nominais por município/zona divulgados pelo Tribunal Superior Eleitoral, agregados por UF e candidatura, excluídas as unidades eleitorais no exterior (`ZZ`). Indicador HHI = soma do quadrado das participações de candidaturas no total de votos presidenciais nominais válidos dentro de cada UF.

Geometria: malha das 27 UFs fornecida pelo IBGE, com identificadores validados pelo cadastro oficial de UFs. Proximidade: os quatro centroides de UFs mais próximos por distância de Haversine; pesos dirigidos, uniformes entre os vizinhos e normalizados por linha. São 27 observações por teste, 9.999 permutações com semente 20261010.

- Geometrias IBGE: https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?intrarregiao=UF&formato=application/vnd.geo%2Bjson&qualidade=minima
- Cadastro UFs IBGE: https://servicodados.ibge.gov.br/api/v1/localidades/estados
- Hash da geometria: `07c671aa87aa1ab296c446de6294df9827112782537b996c0a160284907e7c0f`
- Hash do cadastro: `7ca1368dea3af83cba1af84ae8a7e88f1173c97586831d086cc8b3c1ba9c6596`

## Índice global de Moran, k=4

| Ano | Turno | Moran I | p permutacional (bicaudal) | p ajustado Holm (quatro testes) |
|---|---|---:|---:|---:|
| 2018 | 1º | 0,057622 | 0,4108 | 0,8216 |
| 2018 | 2º | -0,007043 | 0,7831 | 0,8216 |
| 2022 | 1º | 0,402263 | 0,0009 | 0,0036 |
| 2022 | 2º | 0,186514 | 0,0487 | 0,1461 |

Somente o primeiro turno de 2022 conserva valor-p inferior a 0,05 após o ajuste de Holm para as quatro hipóteses fixadas com k=4.

## Sensibilidade a escolhas espaciais

| Ano e turno | k=3 (I; p) | k=4 (I; p) | k=5 (I; p) | k=6 (I; p) |
|---|---|---|---|---|
| 2018, 1º | 0,07776; 0,3941 | 0,05762; 0,4108 | 0,04800; 0,3828 | 0,00218; 0,6496 |
| 2018, 2º | -0,07792; 0,7783 | -0,00704; 0,7831 | -0,09635; 0,5718 | -0,08517; 0,6092 |
| 2022, 1º | 0,35295; 0,0050 | 0,40226; 0,0009 | 0,30531; 0,0035 | 0,33329; 0,0012 |
| 2022, 2º | 0,09890; 0,3078 | 0,18651; 0,0487 | 0,09138; 0,1865 | 0,11350; 0,0796 |

No primeiro turno de 2022, a autocorrelação positiva permanece observável para todas as quatro escolhas de vizinhos, com valores-p brutos inferiores a 0,01. No segundo turno de 2022 o resultado não é estável às escolhas de k nem ao ajuste Holm.

Os valores-p de sensibilidade para k=3,5,6 não receberam correção conjunta para o processo exploratório de escolha da matriz; devem ser tratados como diagnóstico de estabilidade e não como testes confirmatórios adicionais.

## Limitações e alcance

**Moran I mede associação espacial, não contágio nem influência social causal.** UFs vizinhas podem se parecer devido a covariáveis econômicas, demográficas e institucionais. O HHI é também influenciado pelo número de candidaturas. O uso de centroides da malha vigente na data da coleta, em eleições anteriores, exige cautela. A amostra estadual de 27 unidades e a exploração de várias especificações tornam necessária interpretação conservadora.

2018 permanece sob ressalva de +76 votos no primeiro turno do ZIP atual em relação à totalização histórica publicada. Esses votos não foram ajustados. O segundo turno de 2018 e ambos os turnos de 2022 foram conciliados.

O resultado espacial fornece uma hipótese para investigação municipal futura. Não sustenta inferência sobre como eleitores individuais decidiram nem previsão do segundo turno de 2026.

## Pacote de replicação

- Modelo-base: [scripts/08_autocorrelacao_uf.py](../scripts/08_autocorrelacao_uf.py)
- Teste de sensibilidade: [scripts/09_sensibilidade_moran_uf.py](../scripts/09_sensibilidade_moran_uf.py)
- Resultados-base: [outputs/espacial_v01/moran_hhi_ufs_2018_2022.json](../outputs/espacial_v01/moran_hhi_ufs_2018_2022.json)
- Sensibilidade: [outputs/espacial_v02/sensibilidade_knn_moran.csv](../outputs/espacial_v02/sensibilidade_knn_moran.csv)
- Ajuste Holm: [outputs/espacial_v02/holm_quatro_testes.json](../outputs/espacial_v02/holm_quatro_testes.json)
- Execução reprodutível em GitHub Actions: [sensibilidade_moran_uf.yml](../.github/workflows/sensibilidade_moran_uf.yml)

Os CSVs de votos derivados e os manifests de hashes estão no repositório. Para reproduzir exatamente a etapa espacial é preciso preservar os insumos geográficos cujos SHA-256 estão documentados. Os arquivos geográficos foram também arquivados em pacote de suporte no Drive do projeto.
