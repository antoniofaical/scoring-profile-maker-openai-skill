# Da expansão à definição de aderência

Use este fluxo quando o usuário tem um tema ou problema, mas ainda não sabe o
que deve caracterizar um score alto. O objetivo é descobrir uma definição
observável útil à decisão, em vez de exigir que o usuário forneça o construto
pronto. Não expanda novamente um briefing que já tenha alvo claro ou uma expansão
adequada disponível.

## Acione a capacidade disponível

Procure `concept-expansion:expand-scouting-concept` no catálogo do ambiente,
também identificável como `expand-scouting-concept` no plugin concept-expansion.
Leia seu `SKILL.md` e as referências pertinentes pelo caminho do catálogo.
Uma @menção ao plugin indica essa capacidade; não é um endereço de arquivo.

Se ela estiver disponível, use-a na mesma tarefa com o briefing original e o
objetivo de definir critérios de avaliação. Respeite o escopo solicitado: para
um pedido de critérios, faça a expansão conceitual pertinente e registre o mapa
em notas; não imponha uma busca de empresas ou uma lista de queries ao usuário.
Se o usuário também pedir expansão completa ou queries, execute o fluxo completo
e os validadores da skill de expansão. Um mapa parcial nas notas não equivale a
um `mapa.json` validado no contrato completo.

Se o plugin não estiver disponível, informe a limitação e aplique a passagem
conceitual descrita abaixo ao material fornecido. Não afirme que executou o
plugin nem o instale por conta própria. A integração é uma dependência opcional,
não um requisito para perfis com alvo já definido.

## Descubra o alvo com o usuário

1. Recupere tema, problema, beneficiário, contexto e decisão desejada. Registre
   ausências e sentidos alternativos. “Não sei o que é score alto” é uma razão
   para explorar o alvo, não uma pendência bloqueante por si só.
2. Expanda os eixos pertinentes em necessidades e caminhos funcionais. Distinga
   resultado desejado, capacidade candidata e hipótese sobre a ligação entre eles.
   Fundamente afirmações especializadas quando houver acesso a fontes; sem
   fundamentação suficiente, identifique a expansão como preliminar.
3. Selecione as necessidades que ajudam a decisão. Preserve as outras como
   adiadas ou fora do perfil, com justificativa. Não converta todos os ramos
   exploratórios em exigências cumulativas sobre cada empresa.
4. Proponha, em linguagem simples: “Para este perfil, score alto significa que
   as evidências mostram [função observável] que corresponde a [necessidade]
   no contexto [definido], com [dimensões pertinentes]”. Distingua aderência
   direta e potencial de de-para. Não apresente potencial como eficácia provada.
5. Dê ao usuário uma decisão concreta somente se interpretações incompatíveis
   mudarem o que será avaliado: por exemplo, cobrir uma função vs. entregar uma
   jornada inteira. Não devolva a pergunta abstrata “o que é score alto?”.
   Quando o briefing sustenta um sentido útil e reversível, continue com um
   rascunho e explique a hipótese; não exija confirmação para produzir o rascunho.

Quando faltarem até problema, finalidade ou contexto capazes de distinguir
sentidos, mantenha alternativas e formule as decisões mínimas pendentes. Não
resolva uma escolha incompatível silenciosamente nem fabrique aprovação humana.

## Transforme o mapa em critérios

Use a cadeia: briefing → necessidade → caminho/capacidade → evidência admissível
→ pergunta → papel no perfil → cálculo. São relações muitos-para-muitos.
Registre o vínculo para cada critério, inclusive se nasceu diretamente do
briefing ou de uma síntese de várias necessidades.

| Origem na expansão | Uso no perfil |
| --- | --- |
| `briefing.objetivo`, `contexto`, `escopo` | Alvo e uso do score; escopo proposto permanece proposto |
| `necessidades[].resultado` | Resultado de destino para definir aderência e de-para |
| `caminhos[].capacidade`, `ligacao`, `papel` | Função observável e tipo de relação; ligação hipotética permanece hipótese |
| `enunciados[].suporte`, `fontes` | Fundamentação e limites nas notas; não provas sobre cada empresa |
| `pendencias` e sentidos alternativos | Decisões abertas e limites do rascunho |
| `vocabulario`, `queries` | Apoio lexical e contexto de descoberta; não prova funcional nem core automático |

Preserve IDs existentes, como `N...` e `C...`, nos vínculos das notas. O critério
recebe um ID `snake_case` do contrato do classificador; não substitua nem renumere
IDs do mapa. Não acrescente campos ao perfil para guardar IDs de origem.
Não altere `revisao_humana` ou transforme `suporte.classe = hipotese` em fato
por ter gerado uma pergunta.

Para um mapa conversacional sem IDs, atribua identificadores locais estáveis
nas notas e deixe claro que não é um mapa canônico validado. Registre seleção
e descarte de forma que outra tarefa possa reconstruir as escolhas.

Necessidades alternativas que individualmente bastam pedem uma definição comum
de aderência e categorias auxiliares, ou perfis separados se forem construtos
incompatíveis. Dimensões complementares realmente necessárias podem ser core
conjuntos. Escolha a agregação em `design.md` depois dessa distinção.
Não invente fórmulas OR no JSON: o classificador tem um conjunto fechado de
métodos. Explique qualquer limite de representação antes de aproximar o alvo.

Não confunda caminho habilitador com solução completa. Preserve essa distinção
em perguntas ou auxiliares conforme a decisão. Restrições de maturidade,
geografia, financiamento e regulação só entram no score quando forem parte
do alvo escolhido e puderem ser observadas nas evidências admitidas.

## Entrega e verificação

Preencha `profile_request.json` com o alvo proposto, dimensões escolhidas e
política de compensação. Registre hipóteses e origem separadamente em
`design_notes.md`; fontes e aprovação não pertencem ao JSON do perfil.

Inclua nas notas uma tabela com: ID do critério, ID de necessidade/caminho ou
trecho do briefing, função avaliada, evidência admissível, papel, justificativa
e estado do suporte. Declare a definição de score alto como proposta enquanto
não existir aprovação documentada. O usuário pode rever a definição com um
exemplo concreto, sem precisar desenhar pesos ou fórmulas.

Revise: uma solução especializada que cobre uma necessidade suficiente; um
rótulo temático sem função; um habilitador; evidência escassa; uma solução útil
de outro setor quando de-para for admissível. Não trate pontuações sintéticas
como calibração. Execute a validação normal do perfil. Validade do mapa, validade
técnica do perfil e aprovação da definição são três verificações distintas.

## Procedência

Integração construída a partir do plugin concept-expansion 0.1.0, consultado em
2026-10-07: `SKILL.md`, `references/metodologia.md` e
`references/contrato-saida.md` de `expand-scouting-concept` no catálogo local.
Sua metodologia organiza briefing, necessidades, caminhos e suporte; a passagem
ao scoring descrita aqui é uma escolha de integração deste projeto.
As regras executáveis do perfil continuam as do classificador em `upstream.json`.
