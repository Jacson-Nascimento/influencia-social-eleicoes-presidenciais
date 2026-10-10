# Inventário de recursos públicos do TSE

**Consulta:** 2026-10-10. **Responsável:** Jacson Cruz do Nascimento.  
**Escopo:** eleições presidenciais, votação nominal por município e zona.

| Ano | ID do recurso TSE | Página oficial | Mimetype informado | Licença exibida |
|---|---|---|---|---|
| 2018 | e1dae37e-c2d6-493c-bf66-437f3788af89 | https://dadosabertos.tse.jus.br/dataset/resultados-2018/resource/e1dae37e-c2d6-493c-bf66-437f3788af89 | application/zip | Creative Commons Attribution |
| 2022 | 40fdcf49-256a-4c81-87cf-711545bd1528 | https://dadosabertos.tse.jus.br/dataset/resultados-2022/resource/40fdcf49-256a-4c81-87cf-711545bd1528 | application/zip | Creative Commons Attribution |

Os IDs foram verificados nas páginas dos recursos. Os arquivos ZIP ainda **não foram transferidos para este repositório**. A presença dos links não comprova download, hash ou conciliação dos respectivos dados.

## Coleta reproduzível

1. Inventariar os recursos com `python scripts/01_coletar_tse.py --dataset resultados-2018 --list` e `--dataset resultados-2022 --list`.
2. Confirmar que os IDs da API correspondem aos identificadores publicados nesta tabela.
3. Baixar pelos IDs exatos com `--download-id`; preservar arquivo original e manifesto com SHA-256, data UTC e URL.
4. Validar ZIP e campos antes do tratamento. Não sobrepor arquivo com conteúdo diferente.
5. Conferir por ano e turno os totais agregados contra a totalização oficial; registrar diferenças e cobertura.

## Advertências

O campo `CSV` exibido no portal descreve o formato lógico; o recurso distribuído aparece com mimetype `application/zip`. O script deve abrir o CSV interno. Os arquivos podem ser grandes; não utilizar leitura parcial em planilhas como evidência de totalização. O desenho do estudo exige atenção à inclusão de ZZ (exterior), mudança do número de candidaturas e compatibilidade de códigos territoriais.

**Estado:** inventário documental de recursos. Coleta completa, validação de conteúdo e estimação espacial pendentes.
