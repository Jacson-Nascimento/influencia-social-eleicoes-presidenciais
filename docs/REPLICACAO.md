# Protocolo de replicação

1. Usar Python >= 3.11; `python -m pip install -r requirements.txt`.
2. Testar: `python -m unittest discover -s tests -v`.
3. Inventariar conjuntos no TSE: `python scripts/01_coletar_tse.py --dataset resultados-2022 --list`.
4. Escolher um ID de recurso do inventário. Baixar mantendo arquivo e manifesto com SHA-256.
5. Tratar arquivo municipal: `python scripts/02_tratar_votacao.py --arquivo CAMINHO.zip --ano 2022 --saida data/tratados/votos_2022.csv`.
6. Calcular indicadores: `python scripts/03_indicadores.py --arquivo data/tratados/votos_2022.csv --saida outputs/indicadores_2022.csv`.
7. Auditar totais históricos: `python scripts/04_conferir_agregados_historicos.py --arquivo data/controles/totalizacao_presidencial_2022_tse.csv --saida outputs/relatorios/auditoria_agregados_2022_v02.json`.
8. Conferir totais com TSE e rastrear scripts, entradas, versão e parâmetros.
9. Não estimar transferência individual de votos com agregados nem publicar regressão preditiva sem validação temporal.

**Limite atual:** arquivos municipais oficiais ainda não foram baixados no ambiente de execução.