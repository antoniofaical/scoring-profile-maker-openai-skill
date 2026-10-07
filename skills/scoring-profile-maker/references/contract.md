# Contrato e versionamento

Compatibilidade embarcada: `profile_schema_version = 1`, no commit registrado em
[upstream.json](upstream.json). O [schema](profile.schema.json) foi copiado sem
modificação do classificador. O validador embarca o runtime desse commit com
apenas o endereço local do schema adaptado. O runtime do checkout solicitado
prevalece em uma verificação de outra revisão.

## Campos aceitos

| Campo | Regra |
| --- | --- |
| `profile_schema_version` | `1` |
| `id` | ID estável, regex `^[a-z][a-z0-9_]*$` |
| `version` | String segura para paths; SemVer é recomendação |
| `name` | Nome não vazio |
| `description` | Texto opcional |
| `instruction` | Política comum de evidência, não vazia |
| `criteria` | Lista não vazia, IDs únicos e pelo menos um core |
| `evidence_aggregation` | `method`: `top_weighted`, `mean` ou `maximum`; `top_weights` opcionais, positivos |
| `score_aggregation` | `method`: `weighted_mean`, `weighted_geometric`, `minimum` ou `weighted_geometric_bottleneck` |

Um critério exige `id`, `role` e `instructions`. Core aceita `weight` positivo,
padrão 1. Auxiliar aceita `threshold` entre 0 e 1. Não use peso em auxiliares nem
threshold em core. No método misto, os campos são `geometric_weight` e
`bottleneck_weight`, não negativos e não ambos zero; os padrões são 0.5 cada.
O schema define combinações aceitas desses campos, inclusive quando omitidos.

Objetos rejeitam campos extras. Coloque fundamentação, fontes, casos de teste,
aprovação e calibração em um documento separado. Não adicione ao JSON
`question_set_sha256`, `status`, `sources`, fórmulas livres, score, respostas Jev
ou um limiar de aprovação global.

## Identidade e reutilização

`profile_sha256` identifica o JSON integral canonicalizado. `question_set_sha256`
identifica somente `instruction` e as perguntas `{id: {type: "noul", instructions}}`.
A ordem dos critérios não muda este último hash. Pesos, papéis, thresholds,
descrição, ID do perfil e versão não entram no hash das perguntas.

| Mudança | Versão recomendada | Perguntas compatíveis? |
| --- | --- | --- |
| Nenhuma | Preservar | Sim |
| Nome/descrição/documentação | Patch | Sim |
| Pesos, papel, thresholds ou agregação | Minor | Sim, se IDs e textos forem idênticos |
| Instrução comum, texto/ID de pergunta, inclusão/remoção | Major | Não |
| Novo alvo com nova identidade | Novo ID; começar em `1.0.0` | Depende das perguntas; não presume reutilização de sites |

Não reutilize IDs de critérios para outro significado. Registre o motivo e o
efeito de alterações. Revisão que preserve respostas deve manter literalmente
os textos; pequenas correções de pontuação alteram o hash.

No replay de texto, perguntas compatíveis são condição necessária. As respostas
salvas precisam ainda ter os hashes certos, critérios completos e modelo
consistente. No modo de sites, `score` procura uma execução completa de outra
versão do mesmo ID com o mesmo hash de perguntas; ID diferente não encontra a
execução pelo mesmo caminho. A coleta pode ser reutilizada, mas isso não garante
reutilização das respostas. Não declare custo zero sem verificar o modo e os
arquivos efetivamente disponíveis.

## Script embarcado

`scripts/validate_profile.py` valida schema e invariantes do runtime, recusa JSON
com chaves duplicadas e números não finitos, e imprime hashes e comparação
opcional com baseline. O código de saída é 0 para contrato válido e 1 para falha;
erros de argumentos usam 2. Divergência de runtime fornecido também é falha.

`--classifier-root` importa somente o módulo de domínio no `src/` desse checkout
em um subprocesso, valida o perfil e compara hashes. Não instala dependências,
não chama APIs e não grava no checkout. Uma diferença no arquivo de schema é
reportada. Uma validação bem-sucedida declara compatibilidade do perfil avaliado,
nunca equivalência de todos os perfis possíveis em versões diferentes.

O relatório de baseline descreve a fronteira técnica e sugere um nível de
versionamento; não decide equivalência semântica do tema. Verifique versão e
identidade na revisão humana. O validador não decide atomicidade, validade de
domínio, precisão do Jev, adequação dos pesos nem prontidão de produção.
