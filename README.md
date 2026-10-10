# Dinâmica de influência social e comportamento eleitoral no Brasil

**Autor:** Jacson Cruz do Nascimento  
**ORCID:** https://orcid.org/0009-0006-6535-9569  
**ISNI:** 0000 0005 3052 9869  
**Início:** 8 de outubro de 2026  
**Situação:** etapas descritivas nacional, estadual e municipal executadas; investigação causal e modelos fora da amostra ainda pendentes.

## Objetivo
Investigar padrões de concentração, interação territorial e mudanças agregadas de preferências entre turnos presidenciais, avaliando se medidas espaciais acrescentam capacidade explicativa em relação a modelos simples.

Não há identificação do voto individual. Semelhança territorial não comprova influência social ou contágio. Mudanças agregadas não identificam transferências individuais.

## Projeto independente
Este estudo possui repositório, protocolo, dados, código, testes e eventual DOI próprios. O trabalho anterior de dinâmica de manada organizacional (DOI: https://doi.org/10.5281/zenodo.21985858) é apenas referência conceitual. Os parâmetros dos 60 agentes e seus percentuais simulados não são resultados eleitorais.

Repositório do trabalho anterior: https://github.com/Jacson-Nascimento/dinamica-manada-organizacional

## Fontes públicas
- Resultados 2018: https://dadosabertos.tse.jus.br/dataset/resultados-2018
- Resultados 2022: https://dadosabertos.tse.jus.br/dataset/resultados-2022
- Resultados 2026: https://dadosabertos.tse.jus.br/dataset/resultados-2026
- Boletins de urna 2026: https://dadosabertos.tse.jus.br/dataset/resultados-2026-boletim-de-urna

O licenciamento de cada recurso precisa ser conferido antes de redistribuir bases brutas. Coletas terão manifesto com fonte, ID do recurso, data, bytes e SHA-256.

## Estrutura e replicação
- `docs/`: protocolo, fontes, interpretação e manuscrito.
- `scripts/`: coleta e transformação dos recursos oficiais e auditoria.
- `data/brutos/`: cópias imutáveis de arquivos oficiais, após obtenção.
- `data/controles/`: totais históricos observados e suas fontes.
- `data/tratados/`: derivados abertos.
- `tests/`: testes com dados fictícios.
- `outputs/`: resultados verificados e figuras.

Instalar Python 3.11+ e executar:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/04_conferir_agregados_historicos.py --arquivo data/controles/totalizacao_presidencial_2022_tse.csv --saida outputs/relatorios/auditoria_agregados_2022_v02.json
python scripts/01_coletar_tse.py --dataset resultados-2022 --list
```

A saída v02 serve para preservar o arquivo v01 existente; não sobrepor versões anteriores. Consulte `docs/REPLICACAO.md`.

## Estado da investigação
A base municipal presidencial de 2022 foi coletada do ZIP oficial do TSE, consolidada e conciliada exatamente nos dois turnos. A base de 2018 foi igualmente coletada e disponibilizada **com ressalva**: há diferença de +76 votos no 1º turno entre o arquivo oficial baixado e a totalização histórica de referência; o 2º turno de 2018 conciliou integralmente. Não houve alterações artificiais para ajustar os dados. Ambos os anos cobrem 5.570 municípios brasileiros por turno; locais no exterior (ZZ) são documentados em separado. Nenhuma inferência causal de manada foi validada.

- **Base auditada 2022:** [CSV aberto](data/tratados/votos_presidente_municipio_2022.csv)
- **Base 2018 sob ressalva:** [CSV aberto](data/tratados/votos_presidente_municipio_2018_RESSALVA.csv)
- **Comparativo territorial v02:** [resumo nacional](outputs/comparativo_v02/resumo_nacional_2018_2022.csv) e [resumo por UF](outputs/comparativo_v02/resumo_uf_2018_2022.csv)
- **Relatório técnico:** [avaliação territorial de 2018 e 2022](docs/AVALIACAO_TERRITORIAL_2018_2022_2026-10-10.md)
- **Auditoria 2018:** [JSON com divergências](outputs/relatorios/auditoria_2018_ressalva.json)
- **Auditoria 2022:** [JSON conciliado](outputs/relatorios/auditoria_municipal_2022.json)

As versões anteriores foram preservadas para auditoria. Os ZIPs originais são obtidos pelos links oficiais do TSE, com SHA-256 documentado em `outputs/relatorios/`. Nenhum resultado do modelo organizacional original foi reclassificado como resultado eleitoral.

## Análise espacial exploratória (UF)

Foram avaliadas as 27 UFs com HHI da composição de votos por candidatura, malha IBGE, Moran I global, 9.999 permutações e pesos por k vizinhos (3 a 6). No cenário de referência k=4, a autocorrelação de 2022 no primeiro turno foi I=0,402263, p bruto=0,0009 e p ajustado Holm=0,0036. Os demais testes de referência não apresentaram p ajustado abaixo de 0,05. **Associação espacial não é evidência causal de influência social.**

- [Relatório espacial e sensibilidade](docs/AVALIACAO_ESPACIAL_E_SENSIBILIDADE_2026-10-10.md)
- [Resultados Moran e geometria](outputs/espacial_v01/moran_hhi_ufs_2018_2022.json)
- [Sensibilidade k=3..6](outputs/espacial_v02/sensibilidade_knn_moran.csv)
- [Ajuste Holm](outputs/espacial_v02/holm_quatro_testes.json)

O próximo estágio exige ligação TSE-IBGE validada para malhas municipais históricas e avaliação de modelos espaciais fora da amostra. O estudo **não** apresenta previsão de vencedores ou probabilidades para 2026.

## Avaliação municipal espacial e temporal (10/10/2026)

A partir de votos presidenciais públicos do TSE, da correspondência oficial TSE-IBGE e da malha municipal do IBGE de 2022, foram relacionados 5.570 municípios em 2018 e 2022 sem perdas territoriais. O índice de Moran I do HHI municipal foi positivo nos dois anos e turnos, inclusive após centralização por UF. Para oito vizinhos, os valores brutos variaram de 0,6761 a 0,7898 e os centrados por UF, de 0,4353 a 0,4878. Todos os testes primários tiveram valor-p ajustado Holm de 0,0020. A correlação municipal do HHI entre 2018 e 2022 foi de 0,8083 no primeiro turno e 0,9252 no segundo.

Esses valores **não demonstram manada, transferência individual de votos, causalidade ou previsões eleitorais**. Persistência temporal elevada é um alerta para fatores territoriais não observados. O HHI entre turnos está sujeito ao efeito mecânico da diminuição de candidaturas. A divergência documental de 76 votos no primeiro turno de 2018 permanece preservada e assinalada.

- [Relatório empírico municipal](docs/RELATORIO_MUNICIPAL_ESPACIAL_2026-10-10.md)
- [Protocolo municipal e limites](docs/PROTOCOLO_ESPACIAL_MUNICIPAL_2026-10-10.md)
- [Índices de Moran e sensibilidades](outputs/municipal_v01/moran_municipal_sensibilidade.csv)
- [Correspondência municipal e centroides](outputs/municipal_v01/chaves_tse_ibge_5570_centroides.csv)
- [Estabilidade temporal e mudanças entre turnos](outputs/municipal_v02/persistencia_temporal_e_delta_hhi.json)
- [Manifesto dos dados e hashes](outputs/municipal_v01/manifesto.json)
- [Execução GitHub Actions aprovada](https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/actions/runs/38068129663)

O artigo original de dinâmica de manada é metodologicamente distinto e não foi modificado.
