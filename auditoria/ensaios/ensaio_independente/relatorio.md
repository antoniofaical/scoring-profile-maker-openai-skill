# Ensaio independente da scoring-profile-maker

Data: 2026-10-07. Ensaios offline concluídos. Perfis em rascunho; revisão humana e calibração empírica pendentes.

## Resultados observados

1. Pedido das cooperativas: [perfil](pedido_1/profile.json), [briefing](pedido_1/profile_request.json) e [notas](pedido_1/design_notes.md). Um core mede suficiência de qualquer uma das três necessidades. Cinco auxiliares contextualizam funções, setor e autodeclaração. Nenhum gate de maturidade, disponibilidade operacional ou financiamento. O [validador](pedido_1/validation.json) terminou com código 0 e confirmou compatibilidade do perfil com o schema e o runtime do checkout indicado. Os [nove casos sintéticos](pedido_1/synthetic_review.json) conferem aritmética e a intenção do desenho; não medem interpretação do Jev.

2. Pedido de revisão: [perfil 1.1.0 separado](pedido_2/profile.json), [briefing](pedido_2/profile_request.json) e [comparação com baseline](pedido_2/design_notes.md). Apenas o peso de `repeated_synchronization` mudou de 1.0 para 2.0, acompanhado da versão minor. [Comparação literal](pedido_2/literal_comparison.json) e [validação](pedido_2/validation.json) confirmam instrução e todas as perguntas preservadas e hash das perguntas idêntico: `ab8c8def4cdafbacb061a2316ccb1d6d3b7189de010cc9a20b8e49a20b8e0771`. Os [seis recálculos sintéticos](pedido_2/synthetic_recalculation.json) mostram sincronização fraca: 45.08 → 37.59; outra dimensão fraca com sincronização alta: 45.08 → 47.97. Auxiliares altos não elevam core baixo. Respostas antigas reais não foram fornecidas; sua integridade e execução completa não foram verificadas.

3. Pedido vago: [resposta somente JSON](pedido_3/response.json), com `generation_error` e as decisões de domínio ausentes. Nenhum perfil executável foi inventado. A [rejeição pelo validador de perfis](pedido_3/validation.json), código 1, era esperada: o objeto de erro não pertence ao contrato de um perfil.

## Problemas reais e correções

- O primeiro rascunho de aplicação usou “receipts or issues”, mais amplo que “entradas e saídas”. A revisão corrigiu para “receipts and issues”, acrescentou um caso de somente recebimentos e repetiu as verificações. É uma falha de aplicação encontrada e corrigida; a skill não prescreve aquela redação.
- A primeira captura de diagnóstico encontrou `UnicodeDecodeError`: o harness esperava UTF-8 e o subprocesso emitia stderr em CP1252 no Windows. Foi definido `PYTHONIOENCODING=utf-8` no harness e a execução concluiu. A skill não precisou ser alterada.
- O terceiro pedido não define aderência observável, sujeito, uso ou fontes suficientes. A saída de erro é o resultado previsto pela skill, não uma aprovação do pedido vago.
- Os campos de compatibilidade no relatório automático representam condições de identidade. Eles não certificam a existência ou qualidade de respostas salvas. Essa limitação foi explicitada nas notas do pedido 2.

Não foi observada falha não corrigida atribuível à skill nestes três ensaios. Isso não comprova validade de domínio, qualidade universal das perguntas ou prontidão de produção.

## Escopo e evidência

As fontes consultadas foram `SKILL.md`, `references/design.md`, `references/contract.md`, schema, templates, exemplos, procedência e scripts embarcados; no checkout autorizado, somente os módulos de perfil e scoring e seu schema foram lidos/importados. O Python utilizado foi `.venv/Scripts/python.exe` do repositório da skill, com gravação de bytecode desabilitada.

Não houve pesquisa externa, coleta de sites, API paga, classificação de empresas, instalação ou alteração da skill e dos checkouts. A [verificação de integridade](protected_files_integrity.json) registra os hashes dos arquivos conferidos antes e depois e igualdade de todos eles. Esse inventário cobre os arquivos da skill e os três arquivos de runtime/schema usados; não é auditoria integral do checkout.

Pendentes: aprovação humana, evidências reais, piloto rotulado, precisão/recall do Jev, calibração de pesos e agregação, adequação dos produtos ao contexto das cooperativas e replay de respostas antigas reais. O [resumo estruturado](trial_summary.json) e o [harness reexecutável](run_trials.py) permitem continuar a auditoria.
