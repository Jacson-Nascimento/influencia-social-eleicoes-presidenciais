# Protocolo de pesquisa

**Autor:** Jacson Cruz do Nascimento. **Início:** 2026-10-08. **Versão:** 0.2.

## Questão
Em que medida indicadores espaciais e modelos de interação social melhoram a capacidade de explicar mudanças agregadas de voto entre turnos presidenciais em comparação com modelos de referência?

## Universo
Município, ano, turno e candidatura. Bases retrospectivas de 2018 e 2022; 2026 apenas com informações disponíveis no respectivo corte temporal. Identificar votos no exterior, alterações territoriais e mudanças de códigos.

## Variáveis
ANO_ELEICAO, NR_TURNO, SG_UF, CD_MUNICIPIO, NR_CANDIDATO, QT_VOTOS_NOMINAIS. Calcular frações nominais, HHI, entropia, número efetivo de candidaturas e maior fração municipal. Comparecimento, abstenção, brancos e nulos devem vir de bases próprias, nunca inferidos de votos nominais.

## Hipóteses
H0: incorporar medidas de interação não melhora o desempenho fora da amostra frente a modelos de referência.
H1: algumas especificações espaciais podem melhorar o ajuste fora da amostra, controladas características territoriais.

## Procedimento
1. Inventariar recursos oficiais e suas licenças, URLs, IDs, datas de acesso, tamanhos e hashes.
2. Baixar fontes sem sobrescrever originais e conferir campos, turnos, cobertura e totais com o TSE.
3. Construir indicadores agregados, verificar padronização das unidades territoriais e denominações.
4. Especificar matrizes de contiguidade a partir de malhas públicas do IBGE e tratar municípios isolados.
5. Comparar referências estatísticas com extensões espaciais, por cortes temporais válidos.
6. Documentar erros, calibração, dependência espacial, sensibilidade e eventuais falhas.
7. Liberar scripts, dados derivados autorizados, dicionário e artefatos de reprodução.

## Limitações
Similaridade territorial não comprova influência social causal. Concentração muda mecanicamente com o número de candidaturas. Não atribuir valor moral de acerto/erro a preferências eleitorais. Não inferir mudanças individuais a partir de dados agregados. Poucas eleições não equivalem a milhares de eleições independentes.

Não transplantar parâmetros originais do artigo sobre dinâmica de manada para o eleitorado. Não publicar resultados experimentais como observações empíricas. A análise de 2026 será descritiva, com incerteza e limitações explícitas.