# Auditoria editorial: adequação à revista Opinião Pública (CESOP/Unicamp)

**Periódico de referência editorial PROVISÓRIO:** Opinião Pública (CESOP, Unicamp). Não foi realizada submissão e a escolha da revista deve ser confirmada pelo autor.  
**Normas oficiais consultadas em 10/10/2026:** https://www.cesop.unicamp.br/por/opiniao_publica/submissao  
**Sistema oficial:** https://mc04.manuscriptcentral.com/op-scielo

## Requisitos publicados

| Item | Exigência confirmada | Situação v04 original | Ação |
|---|---|---|---|
| Originalidade | Manuscrito inédito, sem submissão concomitante; admite versões em preprints e perfis acadêmicos | O estudo atual é separado do artigo organizacional; manuscritos preliminares estão no GitHub | Manter histórico de versões e descrever diferença de objeto; confirmar política editorial quanto ao repositório atual |
| Extensão | **7.000–14.000 palavras**, com imagens, notas e referências | v04 cerca de **4.015 palavras** (contagem simples por espaços) | Impedimento objetivo: ampliar argumentação substantiva e revisão sem criar conteúdo artificial |
| Resumo | Até **900 caracteres**, descrevendo objeto, método, achados, implicações e originalidade | v04 aprox. **1.974 caracteres** no resumo | Necessita reescrita; versão curta preparada para o manuscrito v05 |
| Título | Máximo de **20 palavras**, apresentado em **quatro idiomas** | Original 19 palavras, mas só em português | Preparar português, inglês, espanhol e francês |
| Palavras-chave | **Cinco palavras-chave**, apresentadas nos quatro idiomas | Havia seis palavras-chave, apenas português | Fixar cinco conceitos e traduzir |
| Citações | ABNT NBR 10520, sistema autor-data | Mistura de formas; fontes bibliográficas ainda sumárias | Normalizar autor-data e pontuação |
| Referências | ABNT NBR 6023, ordem alfabética, metadados completos | Lista sem ordenação completa e com metadados parciais | Normalizar e conferir DOIs |
| Seções | **Sem numeração**, nomes de seções em negrito e subseções em itálico | Seções numeradas no v04 | Remover os numerais na versão editorial |
| Tabelas/figuras | Título, fonte fora da tabela; mídias em JPEG 300–500 dpi e originais editáveis na aprovação | Tabelas Markdown no GitHub, sem legenda/fonte externa | Normalizar ao montar arquivo de submissão |
| Identificação | Nome, ORCID, afiliação, e-mail e minibiografia do(s) autor(es), patrocinadores se existirem | Nome e ORCID, sem e-mail validado, minibiografia ou fontes de financiamento declaradas | Recolher identificação e preencher somente dados confirmados |
| Dados e replicabilidade | Informar repositório com dados, códigos e métodos utilizados, por exigência se aprovado | GitHub independente e bases tratadas públicas | Repositório já atende à disponibilização básica; conferir documentação de fontes e metadados |
| Formato | **.doc** e submissão via ScholarOne | Google Doc/GitHub Markdown | Exportar e converter para .doc ao final; .docx de trabalho não substitui requisito literal |
| Ética/autoria | Ineditismo e origem de dados demonstráveis | Origem pública documentada; manuscritos anteriores preservados | Conferir declarações exigidas na plataforma no dia de submissão |

## Principais problemas substantivos encontrados

1. A versão v04 continha um parágrafo de resultados depois da introdução e antes da fundamentação, deslocado em relação ao fluxo argumentativo. Foi identificado como erro editorial de estrutura; precisa integrar Resumo/Resultados/Discussão, não permanecer como parágrafo solto.
2. Competitividade simétrica `C=1-|M|` e margem assinada `M` não têm a mesma interpretação: dois municípios com vantagem de partidos opostos podem ter a mesma competitividade.
3. R² in-sample aumenta mecanicamente em modelos OLS aninhados. O contraste mais relevante é o RMSE em UFs omitidas e sua incerteza espacial.
4. A heterogeneidade de ganhos entre municípios pequenos e grandes precisa aparecer no resumo, na discussão e nas conclusões.
5. Os dados IBGE de 2017/2021 têm anos de referência anteriores aos pleitos, mas foram consultados nas versões de 2026, possivelmente revisadas. Não são dados com vintage comprovadamente disponível antes da eleição.
6. Os 76 votos de divergência no primeiro turno de 2018 devem aparecer em **nota metodológica explícita**, sem inventar uma causa e sem atribuir influência sobre os indicadores do segundo turno.
7. O primeiro turno de 2018 só aparece como análise complementar; não é necessário alterar votos ou excluir a observação do artigo principal, desde que a ressalva fique visível.
8. A inferência de coeficientes baseada apenas em erro iid ou em permutação ingênua de resíduos não é suficiente com dependência espacial. Análises de incerteza por 27 UFs e Conley 100/250 km foram executadas, com resultados potencialmente diferentes.
9. A revisão da literatura atualizada não deve chamar análise de padrões espaciais, margens eleitorais ou uso de modelos espaciais de descoberta inédita, pois obras anteriores já os abordam.

## Resumo português condensado, destinado ao formulário (verificar caracteres)

Analisa-se se características socioeconômicas dos municípios e de seus vizinhos ajudam a explicar a competitividade do segundo turno presidencial no Brasil em 2018 e 2022. Com dados TSE/IBGE, estimam-se regressões locais e contextuais para 5.565 municípios, com validação por estados omitidos. O contexto melhora o erro quando os municípios têm peso igual, mas os ganhos deixam de ser estáveis com ponderação populacional; o porte das cidades altera os resultados. O artigo distingue competitividade de direção do voto e documenta a sensibilidade da inferência, sem atribuir causalidade a efeitos de vizinhança.

## Quatro títulos e palavras-chave (proposta editorial)

**Português:** Geografia da competitividade eleitoral no Brasil: contexto socioeconômico e eleições presidenciais de 2018 e 2022  
**English:** Geography of Electoral Competitiveness in Brazil: Socioeconomic Context and the 2018 and 2022 Presidential Elections  
**Español:** Geografía de la competitividad electoral en Brasil: contexto socioeconómico y elecciones presidenciales de 2018 y 2022  
**Français:** Géographie de la compétitivité électorale au Brésil : contexte socioéconomique et élections présidentielles de 2018 et 2022

**PT:** competitividade eleitoral; geografia eleitoral; municípios brasileiros; contexto socioeconômico; validação espacial.  
**EN:** electoral competitiveness; electoral geography; Brazilian municipalities; socioeconomic context; spatial validation.  
**ES:** competitividad electoral; geografía electoral; municipios brasileños; contexto socioeconómico; validación espacial.  
**FR:** compétitivité électorale ; géographie électorale ; municipalités brésiliennes ; contexte socioéconomique ; validation spatiale.

## Parecer editorial

**Situação:** tecnicamente avançado, mas não afirmar que está pronto para submissão enquanto a versão final não atender à extensão mínima, aos metadados completos, à normalização de tabelas e ao arquivo .doc exigido.

**Nota de 2018 (a reproduzir integralmente na versão final):** “Na auditoria dos arquivos oficiais de votação nominal referentes ao primeiro turno presidencial de 2018, a soma extraída da base atualmente distribuída pelo TSE foi 107.050.749 votos válidos, 76 votos acima dos 107.050.673 registrados na publicação histórica de totalização. A diferença compreende 20 votos da candidatura nº 17, 46 da candidatura nº 13 e 10 das demais candidaturas. Não foi possível determinar documentalmente a causa dessa divergência. Nenhum dado foi corrigido ou imputado. A ressalva limita-se à análise complementar do primeiro turno de 2018, não afetando os resultados principais, calculados com segundos turnos conciliados.” 
