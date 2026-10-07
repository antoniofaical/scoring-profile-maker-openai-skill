# Resultado do ensaio independente

Data: 2026-10-07. Resultado: rascunho entregue e tecnicamente válido para o contrato/runtime local conferido. Definição de aderência, revisão humana e calibração continuam pendentes.

## Comportamento observado

O pedido foi aplicado diretamente às instruções locais de `scoring-profile-maker` e à skill disponível `expand-scouting-concept` do plugin concept-expansion 0.1.0. Foram lidos os arquivos reais, sem assumir a correção da integração. A execução foi conduzida pelo agente a partir dos caminhos fornecidos, portanto não comprova ativação automática ou seleção de skill instalada.

A falta de uma definição prévia de score alto levou à decomposição dos problemas em necessidades, caminhos, enunciados, hipóteses e vocabulário. A frase que torna suficiente uma necessidade levou a um único core sobre continuidade funcional do pedido, com categorias auxiliares para as três necessidades e o contexto de pequenas oficinas. Não foi fabricada uma média de três requisitos obrigatórios nem uma fórmula OR não suportada pelo runtime.

O briefing permitiu decisões reversíveis. Não foram feitas perguntas no ensaio. O de-para de outro setor, o tratamento de contexto como auxiliar, a formulação em inglês e os pesos de evidência ficaram explícitos como propostas/hipóteses. Nenhuma aprovação foi preenchida. O material de domínio usado foi apenas o briefing fornecido; as instruções das skills sustentam método e contrato, não fatos do mercado.

A expansão está em `design_notes.md` como **mapa conversacional, parcial e preliminar com IDs locais**, sem `mapa.json` completo. Não se declara validação do mapa pelo contrato do plugin. A ausência de queries e exports atende ao pedido; não equivale a uma expansão completa para busca.

## Verificações realmente executadas

- Geração e leitura dos arquivos concretos em UTF-8; consistência de ID/nome/dimensões entre perfil e briefing.
- `validate_profile.py` com o perfil e `--classifier-root` apontando ao checkout de referência, Python com bytecode desativado. Código de saída 0; schema e invariantes aceitos nos dois runtimes; hashes coincidentes; schema local igual ao embarcado. Commit conferido: `dbd6c4cc4fb35bb820205b500b2bdf67eb84b34b`.
- Sete cálculos sintéticos no módulo puro de scoring do checkout. Especialistas isolados em orçamento, agenda e etapa tiveram 95 quando o único core recebido era 0.95. Core em 0.05 com auxiliares em 1.0 teve score 5. De-para sem menção literal a oficinas manteve 95. Não houve resposta Jev.
- Revisão manual de nove casos: especialista, rótulo temático, habilitador, evidência escassa, de-para, marketing manipulador, documento de orçamento isolado, agenda genérica e etapa visível à equipe. Essa revisão não mede precisão do modelo.
- Campos de `human_review.json` conferidos como nulos. Ausência de `mapa.json` e de exports de queries conferida.
- Integridade antes/depois: 14 arquivos da skill, 9 do plugin e 84 do checkout de referência, sem alteração, adição ou remoção durante este ensaio.

## Problemas e limites observados

Não houve falha técnica impeditiva neste pedido. O ensaio expôs limites que permanecem na proposta:

- `top_weighted` pode diluir suporte: uma unidade com core 0.95 e duas com 0.05 resultaram em 59. Repetições da mesma unidade resultaram em 95. Esse comportamento foi calculado, não presumido; pesos não foram calibrados.
- O core único e as categorias auxiliares são perguntas separadas. O runtime não exige consistência lógica entre suas respostas; o piloto precisa verificar correspondência superficial ou respostas contraditórias.
- De-para funcional pode receber prioridade alta sem evidência de adequação de adoção em pequenas oficinas. Essa interpretação está explicitamente proposta e depende da revisão humana.
- `profile_request.json` segue o modelo de briefing da skill, sem schema formal próprio executado. Sua consistência foi conferida; não se declara validação de schema desse arquivo.
- Não foi executado o validador/exportador de concept-expansion, pois não houve mapa completo nem queries. Não foram realizados busca externa, instalação, coleta de empresas, chamadas pagas, execução Jev, avaliação de precisão ou calibração empírica.

## Arquivos entregues

Todos os arquivos estão exclusivamente em `auditoria/integracao-20261007/ensaio` do repositório da skill:

| Arquivo | Conteúdo |
| --- | --- |
| `profile.json` | Perfil executável de contrato, em estado de rascunho de domínio |
| `profile_request.json` | Briefing normalizado, alvo proposto e política de evidência |
| `design_notes.md` | Briefing original, mapa parcial, fontes locais de método, hipóteses, rastreabilidade, casos e justificativa |
| `human_review.json` | Campos humanos nulos, aprovação pendente |
| `validation.json` | Relatório real de schema/runtime e hashes |
| `validation_execution.json` | Comando, saída, erro e código de saída reais |
| `synthetic_review.json` | Entradas fabricadas e sete cálculos observados |
| `checks.json` | Verificações locais e limites |
| `protected_before.json`, `integrity.json` | Hashes iniciais e comparação de preservação dos arquivos protegidos |
| `prepare_trial.py`, `verify_trial.py` | Procedimento reproduzível do ensaio; executado com Python `-B` |
| `relatorio_ensaio.md` | Este resultado e seus limites |

Hash integral do perfil: `7a8aa9f94818c4d881c3eb7d4a881d58d43cc38f2307bceb5036f0b4e500aee6`.

Hash das perguntas: `184f4c04ba1f170fd6e328b3cd82f9ebe1a77eaaf21571bdb8361bef17c3aec2`.

O ensaio pontual está concluído. Ele verifica a aplicação manual deste fluxo ao pedido fornecido e a validade técnica do perfil produzido. A aprovação da definição e a qualidade de resultados em evidência real permanecem sob controle humano.
