# Protocolo da variável dependente: competitividade eleitoral

**Projeto:** Geografia da competitividade eleitoral no Brasil, eleições presidenciais 2018 e 2022.  
**Autor:** Jacson Cruz do Nascimento. **Data:** 10/10/2026.  
**Natureza:** estudo empírico observacional com dados públicos, não causal.

## Pergunta de pesquisa

Em que medida as características socioeconômicas dos municípios e de seus vizinhos explicam as diferenças territoriais de competitividade nas eleições presidenciais brasileiras de 2018 e 2022?

O artigo anterior de dinâmica de manada organizacional não é a base empírica do novo estudo. Não há transposição de seus parâmetros ou classificação de preferências de voto em acerto/erro.

## Indicador principal: segundo turno

Defina `a_i` como votos nominais da candidatura 13 e `b_i` como votos nominais da outra candidatura finalista em um município. O total é `T_i = a_i+b_i`. A variável principal será:

`C_i = 1 - abs(a_i - b_i)/T_i = 2 * min(a_i, b_i)/T_i`.

Ela assume 0 quando uma candidatura recebe 100% dos votos válidos nominais do município e 1 em empate absoluto (50% e 50%). Quanto maior `C`, mais equilibrada é a disputa entre os dois finalistas, não havendo juízo normativo sobre preferências.

O indicador complementar **direcional** é a margem assinada da candidatura nº 13 contra a outra finalista:

`M_i = (a_i-b_i)/T_i`, variando de -1 a +1. `C_i = 1 - abs(M_i)`.

- 2018: nº 13, Fernando Haddad (PT), versus nº 17, Jair Bolsonaro (PSL).
- 2022: nº 13, Luiz Inácio Lula da Silva (PT), versus nº 22, Jair Bolsonaro (PL).

A candidatura nº 13 pertence ao PT nos dois pleitos, mas **não corresponde à mesma pessoa**. A análise direcional será estratificada por eleição e não interpretada como mudança individual de voto.

O índice C é **não ponderado por município** nos modelos principais. Calcular sensibilidade ponderada pela quantidade de votos válidos e informar explicitamente o peso é uma etapa futura, não pressuposta nos resultados atuais.

## Primeiro turno: análises complementares

O número de candidatos difere entre eleições. Não se deve interpretar variação de HHI como mudança imediata de competitividade. Os indicadores serão:

1. Competitividade condicional entre as **duas candidaturas mais votadas em cada município**: `1 - abs(v1-v2)/(v1+v2)`, podendo essas candidaturas diferir dos finalistas nacionais.
2. Cobertura dos dois primeiros: `(v1+v2)/votos_validos`; municípios com os mesmos valores de competitividade condicional podem ter coberturas muito diferentes.
3. Número efetivo de candidaturas: `1/HHI`, registrando o número de candidaturas positivas.
4. Margem assinada nacional da candidatura 13 versus o oponente que disputará o segundo turno, **calculada como parcela do total válido do primeiro turno**, para descrever direção sem confundir com a disputa entre os dois líderes locais.

## Regras de auditoria

- Exigir cobertura integral de 5.570 municípios por turno/eleição antes de qualquer estimação.
- Verificar que os finalistas do segundo turno são exatamente as candidaturas documentadas e que sua soma reproduz os totais nacionais conferidos (2018: 104.838.753 e 2022: 118.552.353, incluindo exterior; o arquivo municipal analisado exclui o exterior, portanto conciliar internamente e separar controle nacional/exterior).
- **Atenção:** os dados municipais excluem UF ZZ, e por isso NÃO é correto exigir que sua soma iguale o total nacional que inclui votos no exterior. O fluxo deve verificar a conciliação nacional sobre a base completa antes da exclusão e documentar a diferença do exterior. 
- Aplicar correspondência TSE-IBGE previamente validada, preservar os cinco municípios sem variáveis de Censo 2010 e não imputá-los.
- Preservar arquivos de votação, HHI, cálculos anteriores, manifests e documentação de versões anteriores, sem alterações.
- O primeiro turno de 2018 permanece com ressalva documental de +76 votos perante notícia histórica de totalização.

## Comparação dos modelos

Desfecho central: índice de competitividade do **segundo turno**. Modelos em cada eleição: efeitos UF + atributos municipais; extensão UF + atributos municipais + contexto de vizinhos com k=8, sensibilidades k=4/12. Testar desempenho fora da amostra deixando UFs inteiras fora do treino e usando uma amostra comum. Comparar modelos sem efeitos fixos na avaliação inter-UF. Incluir análise da margem assinada separadamente.

Evitar alegação de previsão ex ante: indicadores IBGE foram obtidos em versões publicadas em 2026, potencialmente revisadas. Concentração, competitividade e preferência direcional são objetos estatísticos diferentes. A associação geográfica não demonstra influência social causal.

## Critério editorial de conclusão

Redigir o manuscrito em torno da competitividade, justificar os novos indicadores e comparar literatura pertinente com citações verificadas. Dados e scripts abertos; sem resultados inventados, sem referências não verificadas e sem alegação de originalidade por mera detecção de autocorrelação.
