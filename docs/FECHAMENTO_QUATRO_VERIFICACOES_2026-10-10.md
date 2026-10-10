# Fechamento das quatro verificações pré-submissão: competitividade eleitoral de 2018 e 2022

**Autor:** Jacson Cruz do Nascimento. ORCID https://orcid.org/0009-0006-6535-9569. **Data:** 10/10/2026.  
**Status:** verificações computacionais e revisão comparativa executadas; pendências editoriais e de identificação restantes.

## 1. Pesos demográficos anteriores às eleições

Estimativas populacionais oficiais do IBGE de 2017 e de 2021 foram utilizadas respectivamente como peso nas regressões e na avaliação do desfecho eleitoral de 2018 e 2022. As versões foram recuperadas via SIDRA em 2026 e podem ter revisão retrospectiva. Ponderação populacional é diferente da ponderação por votos nominais válidos observados.

Para o desfecho de competitividade `C=1-|v13-vop|/(v13+vop)`, a inclusão de médias socioeconômicas dos oito vizinhos reduziu o erro agregado em 1,92% em 2018 e em 4,99% em 2022 quando os municípios tinham peso igual; **com pesos populacionais, o ganho tornou-se −3,26% e +0,40%, respectivamente**. Para a margem assinada, os ganhos sem pesos de +17,09% e +18,53% se converteram em −0,89% e −1,87%, respectivamente.

Conclusão: a contribuição do contexto dos vizinhos não é robusta à ponderação populacional anterior. O sinal positivo de R² in-sample em regressões aninhadas não corrige essa instabilidade fora da amostra.

## 2. Influência de capitais e grandes municípios

As 27 capitais foram identificadas pelo catálogo oficial de municípios do IBGE, preservado em versão comprimida e com hash SHA-256 registrado. Os códigos IBGE foram cruzados sem aproximação, e as matrizes de oito vizinhos foram reconstruídas nas quatro amostras. A amostra sem capitais tem 26 UFs, pois o DF contém uma única unidade municipal.

| Critério de exclusão | Municípios usados | Ganho CV ponderado por população, C 2018 | C 2022 | Margem 2018 | Margem 2022 |
|---|---:|---:|---:|---:|---:|
| Todos | 5.565 | −3,26% | +0,40% | −0,89% | −1,87% |
| Capitais | 5.538 | −2,18% | −1,05% | +6,25% | +4,73% |
| Maiores 1% (56) | 5.509 | −1,93% | −1,34% | +11,52% | +10,43% |
| Maiores 5% (279) | 5.286 | +0,17% | +0,94% | +14,95% | +15,62% |

A ponderação e a presença das grandes cidades mudam substantivamente as conclusões, sobretudo sobre a direção da votação. O resultado é um **teste de heterogeneidade**, não uma estimativa causal do efeito de excluir grandes municípios. As exclusões mudam simultaneamente os indivíduos da amostra, a divisão em folds por UF e a rede de vizinhos. Em 2018 a população da amostra estimada é 207.614.682 e em 2022 é 213.269.184; os 279 maiores concentram parcela expressiva da população e sua exclusão altera o estimando.

## 3. Literatura existente e originalidade

Foi verificado o núcleo bibliográfico na página editorial dos periódicos, incluindo:

- Braga e Zolnerkevic (2020), *Padrões de votação no tempo e no espaço*, *Opinião Pública*: https://periodicos.sbu.unicamp.br/ojs/index.php/op/article/view/8659514
- Alkmim e Terron (2022), *O Brasil é realmente um país polarizado?*, *Estudos Avançados*: https://doi.org/10.1590/s0103-4014.2022.36106.002
- Masullo e Silva Junior (2024), *Geografia do voto*, *Revista do Departamento de Geografia*: https://doi.org/10.11606/eISSN.2236-2878.rdg.2024.207979
- Resende e Azevedo (2025), *Conjuntura de fronteira e voto nas eleições presidenciais de 2022*, *Caderno de Geografia*: https://doi.org/10.5752/P.2318-2962.2025v35n83p1195
- Nicolau (2026), *Ascensão urbana e recuo metropolitano*, *Estudos Avançados*: https://doi.org/10.1590/s0103-4014.2026.40117.005

A literatura já trata de padrões espaciais da votação, importância das cidades e efeitos contextuais. A contribuição plausível deste artigo deve ser descrita como **avaliação incremental de competitividade versus margem assinada e sensibilidade dos ganhos socioespaciais à ponderação e ao porte municipal**, sob replicação aberta. Não reivindicar inovação por mero uso de Moran ou por associação geográfica. O confronto foi realizado com resumos e metadados oficiais; a avaliação editorial definitiva ainda deve incluir leitura metodológica integral dos principais antecedentes.

## 4. Auditoria das bases e ressalva de 2018

A base derivada da votação municipal por candidato no primeiro turno de 2018 totaliza 107.050.749 votos nominais válidos; a publicação histórica de totalização oficial do TSE registra 107.050.673. A diferença de 76 votos resulta de +20 votos na candidatura 17, +46 na candidatura 13 e +10 no agregado das demais candidaturas. O total percentual é de aproximadamente 0,000071% da referência de 2018.

**A causa documental exata segue não identificada.** A base original foi preservada, sem imputações ou ajuste arbitrário. O resultado do segundo turno de 2018 e os dois turnos de 2022 foram conciliados exatamente com os controles oficiais, incluindo resultados por candidatura e a parcela do exterior.

Como o desfecho primário do artigo é a competitividade do segundo turno, a divergência está restrita à análise complementar de primeiro turno de 2018. Não se deve declarar conciliação integral de todos os arquivos eleitorais, mas a ressalva documentada não implica divergência numérica no desfecho principal.

## 5. Recomendações para submissão

1. Manter os resultados positivos e negativos em todas as tabelas, sem seleção oportunista da ponderação, das UFs ou de k.
2. Discutir heterogeneidade por porte, inferência ecológica e limitações das validações transdutivas/geográficas.
3. Fechar o caráter **descritivo e associativo** do artigo, sem insinuar causalidade social, identificação individual ou previsão de eleições futuras.
4. Antes de submeter: inspecionar referências integralmente, verificar exigências da revista, rever normalização de equações e tabelas, realizar checagem editorial de licenças/fontes e aprimorar modelagem da dependência espacial de resíduos e covariáveis.

## Artefatos de replicação

- [Manuscrito consolidado v04](MANUSCRITO_COMPETITIVIDADE_V04_2026-10-10.md)
- [Matriz de antecedentes](REVISAO_LITERATURA_COMPETITIVIDADE_2026-10-10.md)
- [Resultados de robustez com pesos populacionais e capitais](../outputs/robustez_demografica_v01/robustez_pesos_populacao_e_grandes_cidades.csv)
- [Catálogo oficial IBGE congelado](../data/ibge_brutos/localidades_v01/municipios_ibge_api.json.gz)
- [Capitais identificadas](../outputs/robustez_demografica_v01/capitais_identificadas_ibge.csv)
- [Manifesto demográfico](../outputs/robustez_demografica_v01/manifesto.json)
- [Auditoria eleitoral independente](../outputs/auditoria_documental_final_v01/reconciliacao_candidatos_e_totais.csv)
- [Manifesto da auditoria eleitoral](../outputs/auditoria_documental_final_v01/manifesto_auditoria_2018_2022.json)

Executado em GitHub Actions, mantendo intactos os artigos e versões anteriores.
