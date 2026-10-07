# Notas de desenho — pedido 1

Rascunho de 2026-10-07. Revisão humana: pendente. Calibração empírica: pendente.

## Alvo e decisões

O pedido do ensaio é a fonte de domínio: uma função documentada correspondente a qualquer uma das três necessidades basta para priorizar investigação. Não foi acrescentado gate de maturidade, operação ou financiamento. A disponibilidade real e a adequação à cooperativa devem ser verificadas posteriormente; não foram inferidas.

O único core `functional_de_para_fit` mede a relação comum entre função de solução e necessidade de destino. As três alternativas estão definidas na instrução e na pergunta; não formam três requisitos cumulativos. Esse desenho segue `references/design.md`, seção “Core, auxiliares e de-para”. Os auxiliares `inventory_movements`, `lot_traceability` e `replenishment_orders` identificam os destinos de aplicação; `agricultural_sector_context` e `cooperative_target_self_claim` contextualizam setor e autodeclaração. Eles não alteram o score. Não foram propostos limiares de flags porque o pedido só solicita contexto.

`weighted_mean` com um core de peso 1.0 não penaliza especialização em uma só necessidade. `top_weighted` e pesos [0.6, 0.25, 0.15] são hipótese inicial recomendada em `references/design.md`, seção “Agregação das evidências”, sem calibração. Com um bloco, o runtime normaliza o peso para 1. Texto em várias páginas pode repetir a mesma alegação; URLs ou IDs distintos não comprovam independência. Uma alegação forte de marketing ainda pode dominar caso o modelo a aceite indevidamente.

## Evidência e revisão

Sites públicos das empresas são a fonte admitida pelo briefing. Descrições específicas de funções podem sustentar o de-para; rótulos e promessas amplas isoladas não podem. Nenhum site foi consultado e nenhuma empresa foi classificada. O perfil mede suporte documental, não qualidade, sucesso ou implantação.

`synthetic_review.json` contém nove casos fictícios: estoque no varejo sem agricultura, rastreabilidade isolada, reposição isolada, três funções, setor sem função, marketing enganoso, evidência escassa, lote sem vínculo e recebimentos sem saídas. Os quatro casos funcionais recebem 90 quando se atribui manualmente 0.9 ao core; setor e autodeclaração em 1 não elevam core zero. São expectativas semânticas e conferências aritméticas; não são resultados Jev nem teste de interpretação de textos.

A revisão semântica encontrou uma abrangência indevida no primeiro rascunho produzido neste ensaio: “receipts or issues” admitia apenas uma direção de movimentação, enquanto o pedido diz “entradas e saídas”. Foi corrigido para “receipts and issues” na instrução e perguntas antes da entrega. Isso limita falsos positivos de uma solução que só registra recebimentos. A skill não prescrevia essa redação; foi uma falha de aplicação corrigida durante a revisão, com novo caso limítrofe e validação repetida.

Risco de falso positivo: descrição genérica de ERP interpretada como uma das funções; autodeclaração detalhada incorreta. Risco de falso negativo: coleta incompleta ou função descrita por terminologia diferente. A pergunta abrangente precisa de piloto rotulado para verificar se o modelo entende a suficiência das alternativas e a política de evidência. Agregação de evidência não resolve alegações falsas ou ausência de informação.

## Verificação real e pendências

O validador local, com Python do ambiente do repositório e jsonschema, terminou com código 0; `validation.json` registra schema, invariantes, hashes e compatibilidade com o runtime do checkout indicado. A execução real do runtime de scoring com registros sintéticos conferiu os nove resultados aritméticos; não foram feitas chamadas de API.

Não validado empiricamente: leitura do perfil pelo Jev, precisão/recall, pesos, ordenação de empresas reais, tradução, qualidade da coleta, adequação setorial e disponibilidade dos produtos. Não existe aprovação humana documentada. Nenhuma resposta antiga existe para este perfil novo; a reutilização não foi exercitada.

Hash do perfil: `150a12b596c3c43c62653c66417d37439d5a094f15826b2043102244625f3afd`. Hash das perguntas: `5db5ceababbf91cb933f1299b01d2491db268b8a9ab8797b91d0d333a10465e6`. Runtime conferido: `dbd6c4cc4fb35bb820205b500b2bdf67eb84b34b`; esta revisão de commit não certifica checkout limpo.
