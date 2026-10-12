# Continuidade do artigo: extensão histórica de 1998 a 2022 — nota v16

**Data:** 12/10/2026. **Autor:** Jacson Cruz do Nascimento.  
**Status:** novas bases e modelos reproduzíveis; **não substituir a v15 nem submeter** até revisão de pares e harmonização histórica.

## 1. Recorte e fonte TSE
Foram coletados os arquivos `votacao_candidato_munzona_{ano}.zip` para **1998, 2002, 2006, 2010** do TSE, com metadados, hashes SHA256 e resumos versionados em [outputs/inventario_tse_historico_v01](../outputs/inventario_tse_historico_v01). As séries de 2014, 2018 e 2022 já estavam no repositório.

- **1998**: pleito presidencial sem segundo turno, não equivalente às medidas de C/M do segundo turno. A fonte nominal por município/zona contém 5.513 códigos municipais e **votos nominais zerados** nessa extração. Foi testada a alternativa oficial `votacao_secao_1998_BR.zip`, cujo TXT sem cabeçalho contém 481.078 registros agregáveis, porém só **27 códigos municipais**. O próprio [portal do TSE](https://dadosabertos.tse.jus.br/dataset/resultados-1998) adverte que os dados de 1998 estão incompletos. **Não imputar**, não generalizar essas 27 cidades e não incluir 1998 na regressão nacional. Documentos em [outputs/alternativa_tse_1998_secao_v02](../outputs/alternativa_tse_1998_secao_v02) e [outputs/reconstrucao_1998_secao_v01](../outputs/reconstrucao_1998_secao_v01).
- **2002**: arquivo nacional de segundo turno completo na extração; 5.565 códigos territoriais brasileiros, um não mapeado diretamente à malha atual (`MT/91065`), exterior `ZZ` separado.
- **2006**: arquivo nacional de segundo turno com 5.565 códigos municipais brasileiros, todos correspondentes na malha atual; `ZZ` exterior separado.
- **2010**: 5.567 códigos municipais brasileiros ligados à malha atual, além de registros especiais `VT` e `ZZ` não atribuídos artificialmente aos municípios.

O objeto principal **2002–2022** contém as seis eleições presidenciais com segundo turno nesse recorte. A margem assinada refere-se sempre ao candidato de número **13 do PT** em relação ao outro finalista (identidades dos candidatos variam por ano), e `C = 1 - |M|`.

## 2. Controles IBGE e amostras

[IBGE SIDRA tabela 202](https://sidra.ibge.gov.br/pesquisa/censo-demografico/demografico-2000/universo/) fornece urbanização e proporção de mulheres de 2000 para 2002/06/10; a partir de 2014 usa-se Censo 2010. As [estimativas de população](https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-population.html) anteriores aos pleitos servem aos seis anos. Em 2006/2010/2014/2018/2022 foi acrescentada a proxy PIB corrente de dois anos antes dividido pela população de um ano antes, **não equivalente ao PIB per capita oficial**. Em 2002 a série SIDRA5938 consultada não retorna o PIB2000; não imputamos esse campo, nem tratamos como equivalente a eventual série metodológica histórica de 1999–2002.

| Especificação | Pleitos | Municípios comuns | Observações município-ano | Controles |
|---|---|---:|---:|---|
| Reduzida, comparável | 2002, 2006, 2010, 2014, 2018, 2022 | **5.506** | **33.036** | log população pré-pleito, taxa urbana e fração feminina do censo anterior |
| Sensibilidade com PIB | 2006, 2010, 2014, 2018, 2022 | **5.505** | **27.525** | três controles anteriores + log da proxy PIB |

Métodos: OLS/WLS, logit fracionário para C, macrorregiões, médias de oito vizinhos por centroides IBGE2022, validação em cinco grupos de UFs e testes temporais com treino apenas de eleições anteriores. IC exploratório: bootstrap pareado de UFs, 4.999 reamostragens.

## 3. Resultados geográficos (pesos iguais, modelo linear)

**Ganho RMSE (%) [IC 95%]** na adição de contexto de vizinhança ao benchmark local com macrorregião:

| Ano | C reduzido | M reduzido | C com PIB | M com PIB |
|---|---|---|---|---|
| 2002 | +1,81 [−0,25; +4,12] | +0,23 [−1,14; +1,90] | — | — |
| 2006 | +0,59 [−1,59; +2,46] | +1,20 [−2,67; +3,33] | +1,46 [−1,91; +4,03] | +3,16 [−0,89; +5,53] |
| 2010 | −0,59 [−2,51; +1,32] | +0,08 [−2,41; +2,45] | +0,99 [−2,20; +3,34] | +2,78 [−0,57; +5,13] |
| 2014 | −0,92 [−2,05; +0,56] | +1,54 [−2,61; +4,94] | +0,13 [−1,38; +1,77] | +2,89 [+0,13; +4,35] |
| 2018 | −1,16 [−3,29; +0,71] | +0,96 [−2,27; +3,93] | −1,25 [−3,26; +0,55] | +4,92 [+1,38; +7,62] |
| 2022 | −0,54 [−2,08; +1,00] | +0,09 [−2,08; +2,92] | −0,46 [−1,80; +0,86] | +4,55 [+0,89; +7,12] |

A evidência muda conforme o conjunto de controles, além da amostra: o exercício reduzido não traz ICs positivos exclusivamente, ao passo que o exercício com PIB traz ganho de M geográfico em 2014/2018/2022 para pesos iguais.

## 4. Validação temporal (pesos iguais, modelo linear)

### Reduzido: treino acumulado desde 2002

| Treino → teste | C | M |
|---|---:|---:|
| 2002 → 2006 | +0,52% | +0,32% |
| 2002+2006 → 2010 | +1,05% | +1,32% |
| 2002+2006+2010 → 2014 | −1,11% | +1,12% |
| 2002+2006+2010+2014 → 2018 | −0,33% | +1,18% |
| 2002+2006+2010+2014+2018 → 2022 | −0,34% | +2,00% |

Os ICs por UF dessas dez estimativas cruzam zero. Nenhum ganho temporal contextual estável aparece nessa especificação.

### Com PIB: treino acumulado desde 2006

| Treino → teste | C (IC 95%) | M (IC 95%) |
|---|---|---|
| 2006 → 2010 | +3,47% [+0,54; +6,24] | +0,08% [−6,57; +6,91] |
| 2006+2010 → 2014 | −7,93% [−10,90; −4,57] | −0,58% [−9,58; +6,98] |
| 2006+2010+2014 → 2018 | −3,93% [−5,12; −2,55] | +2,58% [−4,74; +7,58] |
| 2006+2010+2014+2018 → 2022 | −0,13% [−1,19; +0,77] | −2,12% [−5,65; +0,69] |

A divergência de sinal de C entre os testes temporais e os ganhos geográficos de M evidenciam **heterogeneidade** e desaconselham interpretações de ganhos universais.

## 5. Reprodutibilidade

- [scripts/31_inventario_tse_historico.py](../scripts/31_inventario_tse_historico.py) e [dados históricos](../outputs/inventario_tse_historico_v01);
- [scripts/34_coletar_ibge_2002_2010.py](../scripts/34_coletar_ibge_2002_2010.py) e [controles com hashes](../outputs/controles_ibge_historicos_v01);
- [scripts/36_modelos_historicos_reduzidos.py](../scripts/36_modelos_historicos_reduzidos.py) e [resultados de seis pleitos](../outputs/analises_sistema_eleitoral_2002_2022_v01);
- [scripts/37_modelos_historicos_full4_2006_2022.py](../scripts/37_modelos_historicos_full4_2006_2022.py) e [sensibilidade com PIB](../outputs/robustez_historica_full4_2006_2022_v01);
- [scripts/35_reconstruir_tse_secao_1998.py](../scripts/35_reconstruir_tse_secao_1998.py) e [relatório parcial de 1998](../outputs/reconstrucao_1998_secao_v01).

**Limites:** possível dependência entre UFs mesmo após bootstrap; geografia de centroides 2022; dados de censos e PIB revisados retrospectivamente; mesmo município medido em diferentes eleições; alterações de candidaturas e contextos eleitorais. Os modelos não identificam contágio social nem causalidade.

**Preservação:** manuscrito v15 e toda documentação anterior intactos; esta nota não equivale a uma nova versão submetida. A dissertação de mestrado de Nascimento (2024) continua citada no manuscrito de referência. Uma v16 do artigo só deve ser redigida após revisão do desenho com séries históricas heterogêneas e da consistência espacial municipal.
