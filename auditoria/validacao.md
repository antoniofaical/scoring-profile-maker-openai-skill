# Validação da entrega — 2026-10-07

## Escopo

Criar uma skill para transformar briefings em perfis do classificador Jev,
incluindo revisão de critérios, política de evidência, pesos, agregação,
versionamento e compatibilidade de respostas. Repositório de execução:
`antoniofaical/scoring-profile-maker-openai-skill`.

O classificador foi consultado somente para leitura no commit
[`dbd6c4cc4fb35bb820205b500b2bdf67eb84b34b`](https://github.com/antoniofaical/startup-theme-adherence-classifier-jev/tree/dbd6c4cc4fb35bb820205b500b2bdf67eb84b34b).
O schema, os modelos e os exemplos estão registrados com URL e SHA-256 em
[`upstream.json`](../skills/scoring-profile-maker/references/upstream.json).
O único ajuste no runtime embarcado é o endereço local do schema, com remoção
do import que deixou de ser necessário.

## Verificações executadas

Ambiente: Python 3.12.14, jsonschema 4.26.0 e PyYAML 6.0.3, em ambiente isolado
da skill. Python 3.11+ é o requisito de compatibilidade, não uma afirmação de
ensaio em todas essas versões.

| Verificação | Evidência | Resultado |
| --- | --- | --- |
| Validador oficial de estrutura de skills | [skill-check.txt](logs/skill-check.txt) | Passou |
| Metadados, links locais e hashes dos recursos | [package-check.txt](logs/package-check.txt) | Passou |
| Testes de contrato, identidade, CLI e pacote | [tests.txt](logs/tests.txt) | 14 testes, nenhuma falha ou teste ignorado |
| CLI oficial, perfil digital twin | [classifier-digital-twin.txt](logs/classifier-digital-twin.txt) | `PROFILE VALID` |
| CLI oficial, perfil GSD | [classifier-gsd.txt](logs/classifier-gsd.txt) | `PROFILE VALID` |
| ZIP determinístico e validador após extração em outro diretório | [tests.txt](logs/tests.txt) | Mesmo hash em duas construções; validador portátil passou |

A suíte verifica três perfis/modelos válidos, as 12 combinações suportadas de
agregação de evidência e score, 20 mutações inválidas, JSON com chaves duplicadas
ou números não finitos, alterações de perguntas e ajustes que preservam as
respostas. O corpus inválido também foi rejeitado pelo runtime original.
As falhas foram verificadas pelo código de saída e pelo relatório da CLI;
não se considerou apenas a presença de mensagens de sucesso.

Os testes de identidade cobrem pesos, thresholds, papel, agregação e ordenação
sem novas perguntas, além de instrução, redação, ID, inclusão e remoção de
perguntas que exigem novas respostas. A mudança do ID do perfil preserva a
identidade das perguntas, mas não a busca de execuções de sites sob o mesmo ID.

## Ensaios independentes

Um agente independente aplicou a skill a três pedidos sem receber os perfis
esperados. O [relatório](ensaios/ensaio_independente/relatorio.md) documenta:

- Criação de um perfil de de-para para cooperativas: um core e cinco auxiliares,
  validado pelo contrato local e pelo runtime original, com nove cenários
  sintéticos de revisão de cálculo.
- Revisão de digital twin: somente peso de sincronização e versão alterados,
  preservando literalmente perguntas e instrução; seis recálculos sintéticos.
- Briefing sem definição observável: saída `generation_error` em vez de perfil
  inventado, rejeitada corretamente pelo validador de perfis.

O ensaio encontrou e corrigiu uma redação ampla demais no perfil de aplicação
(“entradas ou saídas” em vez de “entradas e saídas”). O desenho foi revisto e
recebeu um caso limítrofe adicional. Isso não exigiu mudar as instruções da skill.

O harness também encontrou um conflito UTF-8/CP1252 ao capturar o diagnóstico.
Depois do ensaio independente, o validador foi ajustado para emitir relatórios
UTF-8 e configurar a mesma codificação no subprocesso do runtime. Um teste de
regressão com diagnóstico acentuado e emoji sob ambiente CP1252 passou. Os
artefatos do ensaio foram novamente verificados após esse ajuste, preservando
os resultados e hashes de perfil. O inventário de integridade foi atualizado
nessa reexecução; ele registra ausência de alterações durante o harness, não
ausência da correção feita entre as duas execuções.

O pacote normaliza finais de linha dos arquivos de texto para LF, mantendo o
mesmo conteúdo entre checkouts Windows e outros ambientes. Os ensaios não
comprovam interpretação correta pelo Jev nem precisão em evidências reais.

## Decisões de implementação

- A skill aceita briefing livre; o modelo estruturado registra o resultado da
  interpretação e não é uma etapa de formulário obrigatória.
- Perfis gerados não recebem campos de aprovação, fontes ou notas que o schema
  rejeita. Esses registros ficam separados em `design_notes.md`.
- Três a sete core é uma recomendação. O exemplo GSD com um core impede que essa
  recomendação se torne uma restrição técnica artificial.
- Categorias alternativas são distinguidas de dimensões que precisam coexistir,
  para evitar penalizar soluções especializadas quando uma função já basta.
- O validador distingue contrato embarcado de verificação do runtime fornecido.
  A validação técnica não substitui a revisão semântica nem garante reutilização
  sem conferir as respostas e execuções realmente disponíveis.

## Distribuição e limites

O pacote contém apenas `scoring-profile-maker/` e seus recursos. O ZIP produzido
fica em `dist/`; logs, testes, ambiente virtual e caches ficam fora dele.
O hash do pacote está em [zip.txt](logs/zip.txt).

Não houve chamadas Jev/DeepL, classificação real de empresas nem calibração
empírica. Nenhum perfil foi aprovado por um responsável de domínio durante
esta entrega. Instalação e ativação no aplicativo não foram ensaiadas.
O classificador e os arquivos sincronizados do projeto não foram alterados.

Revisão de domínio e calibração permanecem pendentes para cada perfil gerado.
Um contrato aceito pelo runtime não comprova precisão, cobertura do tema ou
adequação a decisões de alto impacto.
