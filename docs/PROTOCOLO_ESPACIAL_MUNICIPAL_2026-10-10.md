# Protocolo da avaliação espacial municipal

Responsável: Jacson Cruz do Nascimento. Pesquisa acadêmica independente.
Etapa: extensão municipal dos resultados exploratórios por UF, sem previsão de resultados eleitorais.

## Fontes públicas identificadas
- Correspondência oficial TSE e IBGE, gerada em 04/10/2026: https://dadosabertos.tse.jus.br/dataset/codigos-oficiais-de-uf-e-municipios-segundo-o-tse-e-o-ibge
- Arquivo de correspondência original: https://cdn.tse.jus.br/estatistica/sead/odsele/municipio_tse_ibge/municipio_tse_ibge.zip
- Malha municipal digital IBGE 2022: https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/BR_Municipios_2022.zip
- Votos municipais TSE de 2018 e 2022: dados agregados neste repositório com ressalva documentada de 76 votos no primeiro turno de 2018.

## Regras de qualidade
1. Não parear por nomes parecidos nem excluir perdas silenciosamente.
2. Exigir correspondência única e completa de todos os 5.570 municípios presentes nos dois turnos e anos.
3. Excluir a UF ZZ das análises municipais brasileiras. Os registros exteriores permanecem nas bases eleitorais originais.
4. Conferir integridade dos ZIPs, registrar SHA-256, publicar scripts, chaves e índices derivados.
5. Não reescrever séries originais, mesmo se a conciliação histórica diferir.
6. Não converter evidências de associação espacial em efeitos causais sem desenho identificador.

## Especificação exploratória
Variável: HHI das participações de votos nominais das candidaturas em cada município/turno. Vizinhança: k vizinhos pelo centroide geométrico da malha IBGE 2022, usando distância aproximada sobre a esfera, k=8 como referência e k=4/12 como sensibilidades.

Testes de Moran global: permutação irrestrita (associação bruta) e permutação estratificada por UF após centralização dos valores de HHI dentro de cada UF. Esta segunda especificação pergunta se há padrão espacial residual após diferenças de nível entre as UFs. As permutações não simulam eleitores.

Inferência: 1.999 permutações bicaudais por especificação e correção Holm por quatro comparações ano/turno no k de referência, separada por família de ajuste. As versões k=4 e k=12 são diagnósticos de sensibilidade, não confirmatórios.

A comparação entre 2018 e 2022 é exploratória: o número de candidaturas difere e altera mecanicamente a distribuição do HHI. Não estimar transferência individual de votos nem chances de vitória.

## Critérios de encerramento
Resultados só são classificados como concluídos se a execução integral do GitHub Actions passar, a correspondência for completa e os relatórios mostrarem os valores observados sem preenchimentos artificiais. Qualquer divergência deverá ficar documentada. A malha de 2022 aplicada a 2018 constitui uma limitação histórica, assim como a correspondência TSE-IBGE gerada em 2026.
