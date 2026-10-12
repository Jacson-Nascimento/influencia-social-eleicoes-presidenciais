# Handoff editorial — da v15 (2014–2022) ao manuscrito 2002–2022

**Data:** 12/10/2026. **Autor:** Jacson Cruz do Nascimento.  
**Estado:** Estudo empírico ampliado executado; manuscrito v15 original PRESERVADO. Nenhuma submissão ou reclassificação de artigo realizada.

## Escopo escolhido

Eleições **2002, 2006, 2010, 2014, 2018 e 2022**, apenas **segundo turno presidencial**. Excluir 1998 da análise principal (não houve segundo turno; arquivo nominal TSE histórico incompleto). C e M com identidade C = 1 − |M|, sendo M a margem entre a candidatura PT nº 13 e o outro finalista de cada pleito. Não inferir efeitos causais nem opinião individual.

## Evidências produzidas e versionadas

- [Painel municipal 2002–2022](../outputs/painel_censos_2002_2022_v01/): **5.506 municípios × 6 eleições = 33.036 observações**; chaves TSE/IBGE e documentação das exclusões.
- [36 validações geográficas, 30 temporais, UFs reamostradas 4.999 vezes](../outputs/modelos_seis_eleicoes_censo_precedente_v01/): desenho comum OLS C/M e logit fracionário C, com peso municipal igual ou população anterior.
- [Controles IBGE históricos](../outputs/controles_ibge_historicos_v01/): Censo 2000 para 2002/2006/2010; PIB municipal histórico coletado para 2004 e 2008; estimativas populacionais anteriores às eleições.
- [Sensibilidade Censo 2000 fixo](../outputs/sensibilidade_censo_fixo_2000_v01/): 36 especificações geográficas e 30 temporais reestimadas, idêntica amostra e folds.
- [Sensibilidade Censo 2010 no pleito 2010](../outputs/sensibilidade_censo2010_contemporaneo_v01/): comparação contemporânea apenas como especificação retrospectiva; Censo 2000 antecedente segue principal.
- [Robustez de quatro controles para 2006–2022](../outputs/robustez_historica_full4_2006_2022_v01/): **amostra distinta**, não é substituta do modelo histórico de seis pleitos.

## Resultados geográficos principais (OLS, 5 folds UF, pesos iguais, percentual de melhoria RMSE)

| Eleição | C | M |
|---|---:|---:|
| 2002 | +1,81% | +0,23% |
| 2006 | +0,59% | +1,20% |
| 2010 | −0,59% | +0,08% |
| 2014 | −0,92% | +1,54% |
| 2018 | −1,16% | +0,96% |
| 2022 | −0,54% | +0,09% |

**Todos os IC 95% por reamostragem de UF incluem zero.** Conclusão restrita: não há evidência estável de melhoria de generalização espacial da inclusão de médias socioeconômicas de oito municípios vizinhos após o benchmark local + macrorregião.

## Robustez censitária

- Censo anterior por ano: 2000 para 2002/2006/2010; 2010 para 2014/2018/2022. Principal para não tratar Censo 2010 como informação disponível antes do pleito de 2010.
- Censo 2000 fixo em seis eleições (mesmos modelos/amostra) altera ganhos de M com peso uniforme:
  - **2014:** +1,54% → +0,55%
  - **2018:** +0,96% → +0,27%
  - **2022:** +0,09% → −0,40%
- Em 2010, usar Censo 2010 em vez do Censo 2000 antecedente altera OLS pesos iguais de C −0,59% → −0,31%; M +0,08% → +0,14%. Somente sensibilidade descritiva posterior ao pleito, não ex ante.

## Literatura e fontes editoriais independentes

1. **Ehrl, Philipp (2017).** *Minimum comparable areas for the period 1872–2010: an aggregation of Brazilian municipalities*. *Estudos Econômicos* 47(1), 215–229. DOI https://doi.org/10.1590/0101-416147182phe. Justifica a necessidade de AMCs quando há mudança de fronteiras ou desmembramentos. **A atual amostra de 5.506 municípios com chaves correspondentes não foi transformada formalmente em AMC.**
2. **Soares, Gláucio Ary Dillon; Terron, Sonia Luiza (2008).** *Dois Lulas: a geografia eleitoral da reeleição (explorando conceitos, métodos e técnicas de análise geoespacial)*. *Opinião Pública* 14(2), 269–301. DOI https://doi.org/10.1590/S0104-62762008000200001. Contextualiza geografia eleitoral 2002–2006, não autoriza inferir causalidade social neste estudo.
3. Dados primários oficiais TSE e SIDRA/IBGE, URLs, versões de coleta e SHA registrados em manifestos do repositório.

## Bloqueios científicos/editoriais para transformar em nova versão de submissão

1. **Correspondência territorial:** a amostra comum de 5.506 geocódigos não neutraliza por si só eventuais alterações de limites. Obter e aplicar genealogia municipal/AMC 2000–2010 de fonte confiável, ou justificar formalmente por que o recorte de unidades com código estável é suficiente para a pergunta e limitar inferência espacial.
2. **Revisão da metodologia no corpo principal:** refazer título, abstract somente inglês, amostra, fontes, equações, controle censitário anterior, interpretação de 3 controles, 6 eleições, pesos e esquemas de validação. Atualmente v15 ainda se refere a 2014–2022 e aos 4 controles de outras tabelas.
3. **Substituição disciplinada das tabelas:** destacar resultados com n=5.506 como novos principais. Mover resultados 5.565 (2018/22) e 5.564 (2014–22) para apêndice de replicação com identificação da amostra; **não misturar coeficientes nem ganhos calculados em amostras e regressoras distintas como se fossem diretamente comparáveis**.
4. **Metodologia econômica:** PIB municipal anterior indisponível em série SIDRA comum para 2002; apresentar principal com três atributos e robustez 2006–2022 com quatro atributos como exercício diferente. **Não imputar PIB de 2000.**
5. **Validação temporal:** documentar cinco janelas expansivas, pesos municipais/populacionais e limites dos IC por UF, distinguindo previsão retrospectiva de previsão real ex ante. Considerar rupturas com mudança de candidatos.
6. **Replicabilidade e documentação:** conciliar formalmente notas do TSE para totais 2002/2006/2010 (incluindo ZZ e VT) e atualizar manifesto de proveniência e suplemento do artigo; produzir tabela única de exclusões e hashes antes de submissão.
7. **Qualidade da submissão:** síntese da literatura crítica em prosa, auditoria manual de citações, exame de tabelas, figuras, siglas e resumo; manter a dissertação autoral 2024 como antecedente contextual e manter declaração adequada de ferramentas computacionais/IA.

## Decisão

**Não modificar a versão v15 até a reconciliação editorial e territorial acima.** O novo escopo seis pleitos constitui estudo reestimado, não mera adição de 2002/2006/2010 ao manuscrito de 2014–2022. Recomenda-se rascunho v16 separado e marcado como *em revisão*, após checagens materiais. A contribuição principal é testar a transportabilidade espacial e temporal em seis contextos presidenciais sem extrapolação causal ou inferência individual.
