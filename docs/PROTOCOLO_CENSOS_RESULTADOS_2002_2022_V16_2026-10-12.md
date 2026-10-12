# Protocolo e resultados da ampliação presidencial 2002–2022 (v16)

**Data:** 12/10/2026. **Autor:** Jacson Cruz do Nascimento (ORCID: 0009-0006-6535-9569).

## Decisão e desenho

- **1998 excluída expressamente**, sem reativação de quaisquer arquivos de 1998.
- **Seis eleições com segundo turno presidencial:** 2002, 2006, 2010, 2014, 2018, 2022.
- **Regra principal de censo (último Censo anterior ao pleito):** Censo 2000 para 2002/2006/2010; Censo 2010 para 2014/2018/2022. Essa escolha evita usar informação censitária posterior em validações cronológicas. A literatura não tem regra universal: há trabalhos que usam dados do Censo 2010 retrospectivamente em eleições anteriores, enquanto outros empregam Censo 2000 para caracterizar eleições do início dos anos 2000. A regra conservadora é uma decisão metodológica do presente trabalho, não suposta cópia literal de um único artigo.
- **Três controles comparáveis em toda a série:** log de população municipal estimada no ano anterior, urbanização e fração feminina do Censo pertinente.
- **Quatro controles de 2006 a 2022:** acrescenta proxy do PIB municipal anterior / população estimada, identificando ambos os anos de referência; indisponibilidade da tabela SIDRA 5938 em 2000 impede inserir essa mesma proxy em 2002 sem outra fonte.
- **Amostras balanceadas:** 5.506 municípios × 6 eleições = 33.036 observações; 5.505 municípios × 5 eleições = 27.525.
- Nenhuma imputação de chaves e covariáveis. O voto no exterior (`ZZ`) e as unidades especiais (`VT`) de 2010 não são municípios.
- **Não alterar v14 ou v15.**

## Antecedentes científicos e sua relação exata com o método

1. *Os custos eleitorais do Bolsa Família: reavaliando seu impacto sobre a eleição presidencial de 2006*. **Opinião Pública**: utiliza informações municipais e censitárias de 2000 para contextualizar resultados de 2002 e 2006; verificar em https://www.scielo.br/j/op/a/JbGw46xjdz5Qhz66SCzsYVL/.
2. *Políticas públicas e o voto: municípios nortistas e as eleições presidenciais brasileiras de 2002 a 2010*. **Revista Eletrônica de Ciência Política**, autores Marcos Felipe Rodrigues de Sousa, Suziany de Oliveira Portéglio e Gustavo César de Macêdo Ribeiro: declara emprego descritivo de dados do Censo 2010 e TSE em eleições 2002–2010; https://revistas.ufpr.br/politica/article/view/70422, DOI https://doi.org/10.5380/recp.v10i1.70422. Essa estratégia retrospectiva **não foi adotada** como base principal, devido ao vazamento de informação censitária posterior aos pleitos.
3. *A importância do crescimento econômico local na escolha do chefe do Executivo no Brasil*. **Revista de Administração Pública**: trabalha com resultados presidenciais de 2002/2006/2010 e indicadores econômicos municipais do IBGE; https://www.scielo.br/j/rap/a/YyBsFzy4y7ZLfjNVnxLyrgL/.

## Testes executados

Foram executadas com sucesso:
- 66 especificações de validação geográfica (amostras de três e quatro controles, OLS e logit fracionário para C).
- 108 especificações de validação temporal (treino com último pleito ou todos os anteriores, OLS e logit fracionário).
- 4.999 reamostragens de unidades da federação para IC exploratórios. Correlação residual entre UFs fronteiriças não é completamente ajustada.
- Sensibilidade de congelar composição demográfica de **Censo 2000 para todo o painel**: 36 validações geográficas e 60 temporais. É um experimento diagnóstico para descontinuidade de mensuração a partir de 2014, não uma caracterização atualizada dos municípios posteriores.
- Conferência de identidade `C = 1 - abs(M)`, ausência de anos de teste nos anos de treinamento, cobertura municipal, chaves e hashes das saídas.

### Ganho RMSE da inclusão de WX(k8), cinco dobras por UF, 3 controles, pesos iguais

| Ano | C | M |
|---|---:|---:|
| 2002 | +1,81% | +0,23% |
| 2006 | +0,59% | +1,20% |
| 2010 | −0,59% | +0,08% |
| 2014 | −0,92% | +1,54% |
| 2018 | −1,16% | +0,96% |
| 2022 | −0,54% | +0,09% |

**Nenhum desses 12 intervalos de 95% exclui zero.** Na especificação com PIB (2006–2022), há alguns intervalos positivos de M, mas seus ganhos não se transferem de maneira regular aos pleitos seguintes.

### Treino cronológico acumulado, 3 controles, pesos iguais

| Teste | C | M |
|---|---:|---:|
| 2002 → 2006 | +0,52% | +0,32% |
| 2002+2006 → 2010 | +1,05% | +1,32% |
| 2002+2006+2010 → 2014 | −1,11% | +1,12% |
| 2002+2006+2010+2014 → 2018 | −0,33% | +1,18% |
| 2002+2006+2010+2014+2018 → 2022 | −0,34% | +2,00% |

Os intervalos do painel com três controles atravessam zero em todos esses pares de resultados.

### Sensibilidade ao Censo congelado

Mantendo características urbanas e proporção feminina do Censo 2000 em todos os anos, C na validação temporal para 2014 passa de −1,11% a −0,31%; para 2022 de −0,34% a +0,04%. Nenhuma série demonstra melhoria de RMSE contextual de modo sistemático em todos os testes. O Censo 2000 fixo é apenas análise de sensibilidade, não substitui a especificação principal.

## Scripts e resultados públicos de replicação

- [Código de construção do painel](../scripts/36_painel_presidencial_2002_2022.py) e [manifesto do painel](../outputs/painel_harmonizado_2002_2022_v01/manifesto.json).
- [Código dos modelos com validação geográfica e temporal](../scripts/37_modelos_seis_eleicoes.py).
- [Comparação geográfica](../outputs/modelos_seis_eleicoes_2002_2022_v01/validacao_geografica_6_e_5_eleicoes.csv), [comparação temporal](../outputs/modelos_seis_eleicoes_2002_2022_v01/validacao_temporal_2002_2022.csv), [SSE temporal por UF](../outputs/modelos_seis_eleicoes_2002_2022_v01/erros_por_uf_validacao_temporal.csv).
- [Código do congelamento do Censo](../scripts/38_sensibilidade_censo_congelado.py) e [comparação de sensibilidade](../outputs/sensibilidade_censo_congelado_2002_2022_v01/comparacao_temporal_censo_fixo_vs_anterior.csv).

**Conclusão documentada:** a expansão melhora o alcance temporal e confirma a sensibilidade dos ganhos ao modelo de controles e ao período de teste; não estabelece causalidade, difusão social ou vantagem contextual universal. Não se substituem as tabelas das versões anteriores: as amostras e especificações mudaram. A preparação de manuscrito de submissão 2002–2022 requer revisão de toda a argumentação, inclusive título e Abstract, e revisão crítica de geocódigos históricos.
