# Comparação com baseline — pedido 2

Rascunho de 2026-10-07. Revisão humana: pendente. Baseline preservado em `references/examples/digital_twin.json`.

Somente `repeated_synchronization.weight` mudou de 1.0 para 2.0 e a versão de 1.0.0 para 1.1.0. O ID `digital_twin`, todos os critérios, papéis, thresholds, instrução, perguntas, nome, descrição e agregações foram preservados. A versão minor segue `references/contract.md`, seção “Identidade e reutilização”. A razão do peso é a instrução explícita do ensaio, não uma descoberta de domínio.

O validador local terminou com código 0 e o runtime do checkout conferiu os mesmos hashes. `literal_comparison.json` confirma igualdade literal da instrução e de todas as perguntas, hash das perguntas idêntico, e ausência de alterações além do peso e da versão. `validation.json` contém a comparação automática com baseline.

Hash de perguntas nas duas versões: `ab8c8def4cdafbacb061a2316ccb1d6d3b7189de010cc9a20b8e49a20b8e0771`.
Hash integral baseline: `3463891b88223936cee611c583bf31a89555d51cad16f003308e2720f1ca78e2`.
Hash integral revisão: `335a88fdef37d7d19205c9522c9044a7e50d7b9e39f8d952b8c843b3357b69f1`.
SHA-256 dos bytes do arquivo baseline: `a727473becc964384c9ecbd75432a8d8dedaa706fbcf2b4f949892d5391bc190`.

## Efeito do peso — cálculo com entradas sintéticas idênticas

| Caso | Baseline | Revisão | Delta |
| --- | ---: | ---: | ---: |
| equilibrado | 80.0 | 80.0 | 0.0 |
| sincronizacao_fraca | 45.08 | 37.59 | -7.49 |
| outra_dimensao_fraca | 45.08 | 47.97 | 2.89 |
| auxiliares_altos_core_baixo | 10.0 | 10.0 | 0.0 |
| auxiliares_baixos_core_baixo | 10.0 | 10.0 | 0.0 |
| sincronizacao_zero | 0.0 | 0.0 | 0.0 |

O maior peso aumenta a penalização quando a sincronização está fraca e aumenta o resultado quando a sincronização está forte e outra dimensão está fraca. O mínimo conserva peso 0.4; o peso alterado atua na parte geométrica 0.6. Valores equilibrados mantêm o resultado. Auxiliares não elevam o score. Core zero zera o resultado. Essa conferência usa o código real do classificador, com valores escolhidos manualmente; não valida empiricamente a interpretação das perguntas nem a utilidade do peso 2.0. Ver `synthetic_recalculation.json`.

## Reutilização e limites

Foi preservada a condição de identidade das perguntas para replay de texto, e o ID permite a busca de uma execução de sites compatível. Os nomes dos campos automáticos de compatibilidade não significam que os arquivos antigos foram verificados. Respostas antigas reais não foram fornecidas; não foi confirmado se possuem hashes corretos, critérios completos, modelo consistente ou execução de sites concluída. Logo, o ensaio comprova a fronteira técnica e o recálculo sintético, não um replay de registros reais ou custo zero. Essas condições seguem `references/contract.md`.

O construto do baseline foi mantido; não foi revalidado com fontes externas. Calibração, precisão do Jev e revisão humana continuam pendentes.
