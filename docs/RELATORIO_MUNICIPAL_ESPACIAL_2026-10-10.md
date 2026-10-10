# Associação espacial e persistência da concentração eleitoral municipal, 2018 e 2022

Autor: Jacson Cruz do Nascimento  
ORCID: https://orcid.org/0009-0006-6535-9569  
Relatório técnico, versão 1.0. Referência: 10/10/2026.

## Objetivo e dados

Avaliar se padrões espaciais de concentração de votos identificados em escala estadual persistem na escala dos 5.570 municípios brasileiros e se os indicadores são estáveis entre 2018 e 2022. Bases de votos nominais por município e zona do Tribunal Superior Eleitoral, vinculadas pelos códigos TSE-IBGE de documento oficial gerado em 04/10/2026 e pela malha municipal digital IBGE de 2022. Correspondência territorial integral e sem aproximação por nomes. ZZ (exterior) excluído somente da matriz municipal. Mantida a ressalva documental de +76 votos em 2018, primeiro turno, entre a base distribuída e a totalização histórica.

Correspondência: https://dadosabertos.tse.jus.br/dataset/codigos-oficiais-de-uf-e-municipios-segundo-o-tse-e-o-ibge  
Malha: https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Municipios_2022.zip

## Método

HHI = soma dos quadrados das parcelas de votos nominais válidos de cada candidatura no município. Autocorrelação global de Moran I, centroides da geometria oficial e vizinhança por 8 municípios mais próximos (referência), com sensibilidades para k=4 e k=12. Permutação bicaudal com 1.999 repetições; análise bruta e residual após centralizar os valores de HHI por UF, esta com permutação restrita a cada UF. Holm aplicado aos quatro testes de referência dentro de cada família. Resolução mínima do valor-p: 0,0005.

## Moran municipal, oito vizinhos

| Eleição | Turno | Moran I bruto | Moran I centrado por UF |
|---|---|---:|---:|
| 2018 | 1º | 0,676123 | 0,435290 |
| 2018 | 2º | 0,715548 | 0,487566 |
| 2022 | 1º | 0,789798 | 0,485353 |
| 2022 | 2º | 0,756175 | 0,487826 |

O valor-p bruto de permutação foi 0,0005 em cada teste e o ajustado por Holm foi 0,0020 nos testes principais. São indicadores de associação espacial, não de influência interpessoal causal.

## Sensibilidade da vizinhança

| Ano/turno | Moran bruto, k=4/8/12 | Moran centrado UF, k=4/8/12 |
|---|---|---|
| 2018/1º | 0,707397 / 0,676123 / 0,657477 | 0,482980 / 0,435290 / 0,402079 |
| 2018/2º | 0,744698 / 0,715548 / 0,697456 | 0,535918 / 0,487566 / 0,454258 |
| 2022/1º | 0,811415 / 0,789798 / 0,775725 | 0,536913 / 0,485353 / 0,450469 |
| 2022/2º | 0,781615 / 0,756175 / 0,738960 | 0,539902 / 0,487826 / 0,451541 |

A associação positiva permaneceu nas três configurações, em ambos os anos e turnos. O primeiro turno de 2018, não significativo na escala de 27 UFs em teste anterior, apresenta associação na escala municipal, ilustrando a sensibilidade da inferência à unidade espacial de agregação (MAUP).

## Persistência entre eleições

| Comparação HHI 2018 x 2022 | Primeiro turno | Segundo turno |
|---|---:|---:|
| Correlação Pearson | 0,808331 | 0,925187 |
| Correlação Spearman | 0,753348 | 0,887418 |
| Pearson após centralizar por UF | 0,814711 | 0,909539 |

A estrutura municipal apresenta correlação temporal elevada. Essa persistência é compatível com explicações territoriais relativamente estáveis, que devem ser confrontadas antes de atribuir variações observadas à influência coletiva.

## Mudança de concentração entre turnos

| Medida | 2018 | 2022 |
|---|---:|---:|
| Mediana municipal de HHI segundo menos primeiro turno | 0,172514 | 0,058533 |
| Moran bruto do delta, k=8 | 0,741589 | 0,667800 |
| Moran centrado UF do delta, k=8 | 0,448147 | 0,439601 |

Os quatro testes de delta apresentaram valor-p bruto 0,0005, mas o aumento do HHI entre turnos decorre parcialmente da redução mecânica do número de candidaturas.

## Conclusão restrita e limitações

A semelhança geográfica e sua permanência entre eleições não identificam transmissão de preferência entre eleitores, transferência individual de votos ou comportamento de manada. A autocorrelação também pode refletir educação, renda, urbanização, religião, história política regional e outros determinantes omitidos. A centralização por UF remove apenas diferenças médias estaduais e não todos os fatores de confusão. Centroides de malha de 2022 aplicados a 2018 e correspondência atualizada em 2026 impõem limitação temporal. A divergência de 76 votos no primeiro turno de 2018 não foi artificialmente eliminada.

A etapa seguinte deve incorporar covariáveis territoriais públicas e validação de modelos fora da amostra. O modelo organizacional original permanece estudo independente, e seus parâmetros não são considerados estimativas do eleitorado.

## Replicação

Repositório: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais  
Script espacial: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/blob/main/scripts/10_espacial_municipal.py  
Script de estabilidade: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/blob/main/scripts/11_persistencia_hhi_municipal.py  
Base de Moran: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/blob/main/outputs/municipal_v01/moran_municipal_sensibilidade.csv  
Persistência: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/blob/main/outputs/municipal_v02/persistencia_temporal_e_delta_hhi.json  
Manifesto: https://github.com/Jacson-Nascimento/influencia-social-eleicoes-presidenciais/blob/main/outputs/municipal_v01/manifesto.json

Os arquivos de votos e geocódigos derivados estão abertos no repositório. As fontes originais permanecem atribuídas ao TSE e ao IBGE.
