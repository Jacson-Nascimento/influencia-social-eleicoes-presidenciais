# Protocolo censitário adotado — eleições presidenciais municipais 2002–2022

**Autor:** Jacson Cruz do Nascimento. **Data:** 12 de outubro de 2026.  
**Decisão explícita:** excluir 1998 de todas as novas estimações e da série comparativa; manter os arquivos de tentativas anteriores somente para rastreabilidade, **sem utilizá-los ou apagá-los**. A versão v15 (2014/2018/2022) permanece inalterada.

## 1. Evidência direta da literatura para a transição 2000 → 2010

**SILVA, Mayra Goulart; SANTOS, Paula Frias dos; SILVA, Luan Sudário da.** *Do Leme a Santa Cruz: a territorialização eleitoral de Jair Bolsonaro no município do Rio de Janeiro*. **Opinião Pública**, v. 28, n. 1, 2022. DOI https://doi.org/10.1590/1807-0191202228192. Texto integral: https://www.scielo.br/j/op/a/BQtw4D8Hy7NcVZfGKvrrynJ/?lang=pt.

Na seção *Metodologia*, os autores declaram explicitamente que aplicam o **IDS derivado do Censo 2000 às eleições de 2002 e 2006**, e o **IDS derivado do Censo 2010 às eleições de 2010, 2014 e 2018**. A organização temporal aqui é uma **replicação da periodização censitária**, não do IDS: nossa unidade empírica é todo o município brasileiro, com variáveis de urbanização e proporção feminina, e não regiões administrativas do Rio de Janeiro.

**SOARES, Gláucio Ary Dillon; TERRON, Sonia Luiza.** *Dois Lulas: a geografia eleitoral da reeleição (explorando conceitos, métodos e técnicas de análise geoespacial)*. **Opinião Pública**, v. 14, n. 2, p. 269–301, 2008. DOI https://doi.org/10.1590/S0104-62762008000200001. Texto completo: https://www.scielo.br/j/op/a/DtVyrpxMJGNMV4MfqmrjzgH/?format=html.

Estudo da geografia eleitoral de 2002 e 2006 em escala municipal nacional. A nota metodológica relata a imputação de indicadores de 57 municípios criados após 2000 a partir de municípios de origem. **Não replicamos automaticamente tal imputação**, pois requer correspondências oficiais e justificativa para o desenho de validação espacial. Preferimos manter a amostra observada e documentar exclusões.

**NICOLAU, Jairo.** *Ascensão urbana e recuo metropolitano: a geografia eleitoral de Jair Bolsonaro em 2018 e 2022*. **Estudos Avançados**, v. 40, n. 117, 2026. DOI https://doi.org/10.1590/s0103-4014.2026.40117.005. Texto: https://www.scielo.br/j/ea/a/fPyVfr9W3dNRkv4xQZqXSSR/?format=html&lang=pt.

O artigo utiliza faixas de tamanho municipal calculadas pelo **Censo de 2022** na segmentação retrospectiva. Esse precedente justifica análises históricas com um censo escolhido para classificação do porte, mas **não corresponde** à finalidade dos nossos controles econométricos com mudança de referência decenal. Por isso, não extrapolamos automaticamente o Censo 2022 para urbanização e proporção feminina do nosso modelo.

## 2. Quadro operacional replicado

| Pleito | Censo demográfico nas variáveis sociais | População estimada | PIB nominal usado na *proxy* | Observação |
|---|---|---|---|---|
| 2002 | **2000** | 2001 | não disponível de forma comparável no SIDRA5938 | três controles comuns |
| 2006 | **2000** | 2005 | 2004 | quatro controles possíveis |
| 2010 | **2010** | 2009 | 2008 | *mesmo ano*, uso retrospectivo; repetir Censo 2000 como sensibilidade |
| 2014 | **2010** | 2013 | 2012 | mesmo modelo v15 |
| 2018 | **2010** | 2017 | 2016 | mesmo modelo v15 |
| 2022 | **2010** | 2021 | 2020 | continuidade dos controles da v15; uso de Censo 2022 só após padronizar indicadores |

Modelo comum de seis pleitos: log da estimativa de população anterior, proporção urbana e proporção feminina do censo associado, além do benchmark de macrorregião. Este conjunto evita imputar um PIB de 2000 que não está disponível na série SIDRA utilizada.

Sensibilidade apenas 2006–2022: adicionar log de `PIB_t / população_t+1`, denominado **proxy** — não PIB per capita oficial.

**Ressalva temporal:** para 2010, o Censo 2010 é contemporâneo ao pleito e seus resultados podem ter sido disponibilizados somente depois; a associação é retrospectiva. Por transparência, o exercício adicional usa o Censo 2000 para 2010, preservando uma definição anterior ao ano eleitoral. Em ambos, os dados recuperados em 2026 podem incorporar revisões retrospectivas. Nenhum resultado deve ser chamado de previsão eleitoral em tempo real.

## 3. Execução do protocolo

Rotina efetivamente executada e aprovada na integração contínua:
- [Script](../scripts/36_protocolo_censitario_literatura.py)
- [Workflow](../.github/workflows/protocolo_censitario_2002_2022.yml)
- [Grade IBGE de seis eleições e cenário alternativo de 2010](../outputs/protocolo_censitario_2002_2022_v01/controles_municipais_censo_2000_2010.csv)
- [Manifesto com verificações e cobertura](../outputs/protocolo_censitario_2002_2022_v01/manifesto_metodologico.json)

**Total de 5.506 municípios com três controles completos em todos os seis pleitos**, na grade IBGE de 5.570 municípios, antes do cruzamento definitivo com os votos dos anos anteriores. Completos por eleição (três controles): 2002 5.506; 2006 5.506; 2010 5.565; 2014 5.565; 2018 5.565; 2022 5.565. A sensibilidade de 2010 usando Censo 2000 possui 5.506 completos na grade.

Os controles de quatro variáveis permanecem indisponíveis para 2002 e estão completos em 5.506 municípios em 2006, 5.564 em 2010/2014 e 5.565 em 2018/2022. A **amostra eleitoral balanceada definitiva ainda poderá ser menor** após a conciliação histórica da eleição de 2002 e dos registros especiais de 2010 (`ZZ` exterior; `VT` voto em trânsito).

## 4. Limites e integridade

- Não confundir grade IBGE de controles com observações eleitorais conciliadas: nenhuma nova regressão 2002–2022 foi produzida pelo script 36.
- Não inserir 1998 na amostra nem no título dos resultados empíricos. Os arquivos antigos da tentativa de 1998 são mantidos inalterados por rastreabilidade.
- Não inserir voto exterior ou voto em trânsito em municípios sem correspondência territorial oficial.
- Não confundir censos retroativamente utilizados com covariáveis contemporaneamente disponíveis às eleições.
- Não confundir replicação de um **critério metodológico** com replicação integral dos estimadores, variáveis ou amostras dos artigos citados.
- Não modificar a v15 nem bases originais: novas saídas no diretório `outputs/protocolo_censitario_2002_2022_v01/`.
- Não se pode inferir voto individual, efeito causal ou contágio social a partir de informações municipais.

**Passo seguinte, ainda não declarado concluído:** conciliar por ano votos e códigos municipais em 2002, 2006 e 2010, formar a amostra comum e só então executar modelos de três variáveis e sensibilidade de quatro variáveis/2010, com validação espacial e temporal entre eleições.
