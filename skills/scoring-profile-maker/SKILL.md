---
name: scoring-profile-maker
description: Cria e revisa perfis JSON de scoring para o startup-theme-adherence-classifier-jev a partir de briefings de scouting, temas ou definições de aderência. Quando o significado do score ainda não estiver definido, usa concept-expansion disponível para propor necessidades, critérios e um alvo observável. Não executa classificação de empresas nem busca de fornecedores.
---

# Scoring Profile Maker

Transforme a demanda em um contrato de avaliação compatível com o classificador
[startup-theme-adherence-classifier-jev](https://github.com/antoniofaical/startup-theme-adherence-classifier-jev).
O score mede o suporte nas evidências fornecidas à definição de aderência;
não é uma probabilidade de qualidade, sucesso ou adequação clínica da empresa.

## Entenda a decisão

Leia o briefing e os arquivos pertinentes antes de propor critérios. Se houver
perfil anterior, leia-o e preserve seu ID e os IDs dos critérios que mantêm o
significado. Escolha entre reutilizar, revisar ou criar um perfil: um novo lote
de empresas com os mesmos critérios reutiliza o perfil existente.

Extraia: sujeito avaliado, definição observável de aderência plena, uso do score,
evidências disponíveis, exclusões, tratamento de evidência ausente e possibilidade
de uma dimensão forte compensar uma fraca. A partir de uma expansão de scouting,
use necessidades e funções relevantes; queries e palavras-chave não são
automaticamente critérios de aderência.

O usuário não precisa saber previamente o que um score alto significa. Quando
essa definição faltar, ou o usuário pedir integração com concept-expansion, leia
[references/concept-expansion.md](references/concept-expansion.md) e aplique o
fluxo de descoberta do alvo antes de escrever o perfil. Reutilize uma expansão
existente que cubra a demanda; um perfil claro não exige uma nova expansão.

Distinga aderência direta ao tema de potencial de aplicação funcional (de-para).
No de-para, avalie funções documentadas que correspondam à necessidade de destino;
a menção literal ao tema pode ser auxiliar. Não infira adaptabilidade, validação
clínica ou disponibilidade de produto a partir de uma função genérica.

Use o contexto já fornecido. Pergunte apenas por decisões ausentes que mudariam
os critérios ou a lógica do score, agrupando as perguntas críticas. Enquanto
aguarda, organize o briefing e as questões em aberto. Se não for possível definir
o alvo mesmo após a expansão, entregue esse estado e não fabrique um perfil executável. Propostas
razoáveis de pesos iguais e escolhas de agregação podem constar como hipóteses
explícitas de um rascunho; não obrigue o usuário a preencher um formulário.

O modelo [assets/profile_request.template.json](assets/profile_request.template.json)
serve para registrar o briefing normalizado quando houver entrega em arquivos.
Substitua seus exemplos e descreva hipóteses ou pendências fora do JSON do perfil.

## Desenhe critérios e cálculo

Leia [references/design.md](references/design.md) para escolher critérios,
políticas de evidência e agregações. Use critérios atômicos, verificáveis nas
fontes disponíveis e com alta resposta significando maior suporte ao critério.
Separe `core` (altera o score) de `auxiliary` (contexto e flags).

Não acrescente requisitos de maturidade, financiamento, geografia, doença,
regulação ou operação só porque aparecem em um exemplo. Use exemplos apenas
pela estrutura e pela lógica que forem pertinentes à demanda atual.

Leia [references/contract.md](references/contract.md) e o
[schema](references/profile.schema.json) antes de escrever o JSON. Use o
[modelo](assets/profile.template.json) como estrutura; substitua todos os valores
de exemplo e remova critérios que a demanda não exige. Não inclua notas,
fontes, aprovação humana ou campos não previstos pelo schema no perfil.

Para uma revisão, compare as perguntas e a instrução literalmente: até mudanças
de redação ou tradução alteram a identidade das respostas. Consulte a seção de
versionamento em `references/contract.md`. Um novo tema pode exigir novo ID;
ajustes do mesmo alvo preservam o ID e recebem uma versão apropriada.

## Valide e revise

Execute o validador local com Python 3.11+ e `jsonschema` disponível:

```text
python <skill>/scripts/validate_profile.py <perfil.json>
python <skill>/scripts/validate_profile.py <perfil.json> --baseline <anterior.json>
```

Substitua os caminhos pelos caminhos reais. O script lê arquivos, imprime um
relatório JSON e não faz chamadas de rede. Se houver checkout autorizado de
leitura do classificador, acrescente `--classifier-root <checkout>` para conferir
o runtime desse checkout. O relatório distingue o contrato embarcado da versão
efetivamente verificada. A CLI oficial também oferece:

```text
python <checkout>/fit.py --profile <perfil.json> --validate-profile
```

Se uma dependência ou o runtime não estiver disponível, informe precisamente
o que foi e não foi executado. Não declare validação técnica por simples inspeção.
Use o contrato embarcado sem rede quando suficiente; se o usuário solicitar
compatibilidade com outra revisão, confira seu schema e runtime antes de afirmar
compatibilidade. A procedência do contrato está em
[references/upstream.json](references/upstream.json).

Revise semanticamente cada critério, sua fonte no briefing, redundância,
direção, evidência admissível e falsos positivos/negativos. Contraponha casos
positivos, negativos, limítrofes, com evidência escassa e com marketing enganoso.
Para critérios funcionais, inclua uma solução útil que não menciona o tema.
Em revisões de pesos, confira também cenários de uma dimensão fraca e auxiliares
altos. Valores simulados ilustram o cálculo; não são respostas Jev, teste de
precisão ou calibração empírica.

Corrija os problemas encontrados e repita as verificações afetadas. Os limiares
auxiliares e pesos propostos permanecem hipóteses até calibração. A revisão humana
e um piloto rotulado pertencem ao responsável pelo domínio; registre seu estado
real e nunca preencha aprovação em nome de uma pessoa.

## Entregue

Por padrão, entregue `profile.json`, `profile_request.json` e `design_notes.md`
em uma pasta da tarefa. Se houver perfil anterior, preserve seu arquivo e entregue
a revisão separadamente. Não escreva no repositório do classificador sem autorização.

Em `design_notes.md`, registre o alvo, o vínculo de cada critério ao briefing,
as escolhas de pesos/agregação, fontes e hipóteses, os casos de revisão, os
resultados reais da validação (incluindo hashes), o impacto sobre reutilização
de respostas e as pendências de revisão humana/calibração. Referencie as fontes
junto das escolhas que sustentam; não invente justificativas externas.
Se usar expansão, registre também seus IDs de origem, os ramos selecionados e
adiados, a definição proposta de score alto e quais hipóteses ainda precisam de
revisão. Preserve os campos humanos da expansão e do perfil anterior.

Respeite pedidos de somente JSON, de outra estrutura de arquivos ou de uma
resposta curta no chat. Nesses casos, mantenha a revisão internamente e entregue
o formato solicitado sem acrescentar campos ao perfil. Se a saída for somente
JSON e faltarem decisões essenciais, use `{"generation_error": ["decisão ausente"]}`
em vez de um perfil inventado; esse objeto não é um perfil válido.

Comunique em português e identifique a saída como rascunho quando não houver
aprovação humana documentada. Apresente os arquivos, as verificações concluídas
e o que ainda precisa de revisão. Criar o perfil não autoriza rodar Jev, DeepL,
crawl, scoring em lote ou instalar a skill.
