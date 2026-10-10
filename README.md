# Dinâmica de influência social e comportamento eleitoral no Brasil

**Autor:** Jacson Cruz do Nascimento  
**ORCID:** https://orcid.org/0009-0006-6535-9569  
**ISNI:** 0000 0005 3052 9869  
**Início:** 8 de outubro de 2026  
**Situação:** projeto empírico em preparação; sem estimação eleitoral.

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
O controle nacional da eleição de 2022 foi reconciliado aritmeticamente. A base municipal completa ainda não foi obtida neste ambiente; não há estimativas de influência social, relações causais ou projeções do segundo turno presidencial de 2026. Nenhum resultado do modelo organizacional original foi reclassificado como resultado eleitoral.