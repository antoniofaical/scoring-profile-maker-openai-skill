# Integração com concept-expansion — 2026-10-07

## Mudança e razão

Versão da skill: 0.2.0. O usuário pediu que a expansão ajudasse a definir os
critérios quando ele ainda não sabe o que deve representar um score alto.
A revisão acrescenta uma etapa de descoberta do alvo antes de considerar
essa ausência bloqueante. Um briefing sem problema ou propósito suficiente
continua podendo exigir uma decisão concreta de escopo.

O fluxo é: briefing → necessidades → caminhos/funções → proposta de aderência
→ critérios → perfil. As hipóteses permanecem propostas, e aprovação humana
permanece sob controle do usuário. O contrato e o cálculo do classificador não
foram alterados.

## Implementação

- `SKILL.md`: aciona o fluxo quando o alvo estiver indefinido ou houver pedido
  de integração; reutiliza expansões adequadas existentes.
- `references/concept-expansion.md`: instruções de composição, seleção dos
  ramos, definição proposta do score e rastreabilidade por IDs.
- A skill de expansão é descoberta no catálogo do ambiente. Não é copiada,
  instalada ou alterada por esta integração. Sem o plugin disponível, a skill
  explicita a limitação e trabalha preliminarmente com o material fornecido.
- Um pedido de critérios não obriga geração de queries ou busca de empresas.
  Um mapa nas notas é identificado como conversacional; a validação do contrato
  completo de expansão só é declarada quando efetivamente executada.

Referências lidas do plugin concept-expansion 0.1.0: `SKILL.md`,
`references/metodologia.md` e `references/contrato-saida.md`, no catálogo local.
A passagem das entidades da expansão ao perfil é uma decisão deste projeto,
documentada separadamente das regras de ambas as skills.

## Verificações técnicas

- [14 testes passaram](logs/tests.txt), incluindo contrato do classificador,
  identidade das respostas e execução do validador após extração do ZIP.
- [Validador de skills](logs/skill-check.txt): passou.
- [Metadados, links e integridade do contrato](logs/package-check.txt): passaram.
- [Pacote 0.2.0](logs/zip.txt): produzido e verificado como determinístico.

## Atualização instalada

Os 12 arquivos da instalação anterior foram comparados com o commit original
antes da atualização e correspondiam à versão publicada. A instalação anterior
foi preservada em uma cópia local temporária fora dos artefatos de distribuição.

Foram atualizados somente `SKILL.md` e a nova referência de integração em
`C:\Users\anton\.codex\skills\scoring-profile-maker`. O validador de skills
passou no destino, e os 13 arquivos instalados correspondem à fonte atualizada,
normalizando finais de linha na comparação.

## Ensaio de aplicação independente

O [ensaio](ensaio/relatorio_ensaio.md) aplicou as instruções das duas skills a
um briefing sobre perda de pedidos em pequenas oficinas, sem definição prévia
de score alto. Produziu briefing, mapa parcial nas notas e perfil válido no
contrato embarcado e no runtime do checkout de referência. A definição proposta
preservou a suficiência de atender uma necessidade, usando um core comum e
categorias auxiliares. Foram revisados nove casos semânticos e executados sete
cálculos sintéticos; campos humanos permaneceram nulos.

A inspeção dos arquivos confirmou rastreabilidade por IDs, hipóteses explícitas,
ausência de queries e preservação das árvores protegidas. O ensaio foi iniciado
com os caminhos das skills: não comprova seleção automática no ambiente instalado.
O mapa conversacional não foi declarado validado no contrato completo do plugin.

O cálculo sintético mostrou diluição de suporte por `top_weighted` quando uma
unidade forte recebe duas unidades fracas. As perguntas core e auxiliares também
não têm consistência lógica imposta pelo runtime. Esses limites foram registrados
para o piloto; os valores fabricados não comprovam precisão ou calibração.

Não houve chamadas pagas, classificação de empresas, alterações no classificador
ou no plugin concept-expansion. Os critérios derivados de uma expansão ainda
precisam de revisão de domínio e calibração para uso decisório.
