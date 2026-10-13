# Handoff operacional — estudo eleitoral 2002–2022 (13/10/2026)

**Documento completo em Word (8 páginas):**  
[HANDOFF_CONTINUIDADE_ARTIGO_ELEITORAL_2002_2022_2026-10-13.docx — Google Drive](https://docs.google.com/document/d/1E_hgDurh4tSloBXDh1v-kA43zVfwQhzB/edit)

**Pasta do projeto:** [01.05 — Influência social e comportamento eleitoral / 02_PROTOCOLO_E_REFERENCIAS](https://drive.google.com/drive/folders/1DGc1e-35ljw5cNsvOF2AWIF9wWJsSkeb)

**Autor:** Jacson Cruz do Nascimento (ORCID 0009-0006-6535-9569).  
**Estado:** estudo empírico de seis eleições executado e versionado; manuscrito integral 2002–2022 **ainda não finalizado nem submetido**.

## Decisões que NÃO devem ser revertidas sem comando do autor

- Escopo: segundo turno presidencial de **2002, 2006, 2010, 2014, 2018 e 2022**. **1998 expressamente excluído**. Não usar suas tabelas antigas nem apagar os registros já produzidos.
- Manuscritos **v14 (2018–2022)** e **v15 (2014–2022)** preservados sem edição. A futura **v16** será reescrita para 2002–2022.
- Principal: **5.506 municípios comuns, 33.036 observações**; três controles locais (log da população pré-eleitoral; urbanização e proporção de mulheres do Censo antecedente) + macrorregião, versus inclusão das médias desses controles nos oito vizinhos mais próximos.
- Censo: **2000 para 2002/2006/2010**, **2010 para 2014/2018/2022**. Censo 2010 aplicado à eleição de 2010 é sensibilidade retrospectiva, não benchmark cronologicamente antecedente. Outra sensibilidade fixa Censo 2000 nos seis pleitos.
- PIB apenas em robustez distinta **2006–2022 com 5.505 municípios e quatro controles**, pois não foi obtido o PIB de 2000 da mesma série SIDRA 5938. Não imputar.
- Resultados descritivos: **nenhum dos 12 IC 95% de ganho RMSE geográfico (6 pleitos × C/M, pesos iguais) exclui zero no modelo principal**. Não afirmar efeito causal ou contágio social.
- Conservar a dissertação de 2024 como referência contextual e manter a declaração editorial de uso de IA conforme as normas aplicáveis.

## Fontes de verdade: ler antes de trabalhar

1. [Este Word de continuidade](https://docs.google.com/document/d/1E_hgDurh4tSloBXDh1v-kA43zVfwQhzB/edit).
2. [Fechamento analítico de seis eleições](FECHAMENTO_ANALITICO_SEIS_ELEICOES_E_PLANO_V16_2026-10-12.md).
3. [Painel e manifesto das seis eleições](../outputs/painel_censos_2002_2022_v01/manifesto.json).
4. [Manifesto dos modelos censo antecedente](../outputs/modelos_seis_eleicoes_censo_precedente_v01/manifesto.json).
5. [Validação geográfica](../outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_geografica_2002_2022.csv) e [validação temporal](../outputs/modelos_seis_eleicoes_censo_precedente_v01/validacao_temporal_2002_2022.csv).
6. [Cobertura de votos](../outputs/cobertura_amostra_2002_2022_v01/cobertura_votos_amostra_comum.csv).
7. [Protocolo de censo e literatura](PROTOCOLO_CENSOS_RESULTADOS_2002_2022_V16_2026-10-12.md).

## Roteiro prioritário

1. Confrontar totais 2002/2006/2010 com publicações históricas do TSE, separando **ZZ** (exterior), **VT** (2010) e MT **91065** (2002, 869 votos não imputados).
2. Verificar mudanças de limites municipais, genealogia e eventual **área mínima comparável (AMC)**; mesma chave ≠ mesmos limites ao longo do tempo.
3. Examinar PIB 2000 na série histórica **distinta** do IBGE 1999–2002 e sua comparabilidade; se inadequado, manter principal de três controles.
4. Conferir hashes, amostras, fórmulas C/M, RMSE, bootstrap 4.999 por UF e treinamento apenas com pleitos anteriores.
5. Preparar **novo Word v16** com título, Abstract **somente em inglês**, seis eleições, tabelas com IC no corpo, discussão metodológica e apêndice. Nunca transpor resultados de amostras 5.565/5.564 para a nova 5.506 como se fossem intercambiáveis.
6. Realizar avaliação editorial, conferência independente das fontes e diagramação; publicar/compartilhar dados conforme licenças e somente submeter após comando explícito do autor.

**Nota:** o arquivo Word vinculado é o documento mais completo; este Markdown serve apenas para localização e início de nova conversa. Nenhuma base, coeficiente ou manuscrito anterior foi alterado ao criar este registro.
