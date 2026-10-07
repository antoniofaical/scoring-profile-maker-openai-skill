# Scoring Profile Maker

Skill para criar e revisar perfis de scoring do
[startup-theme-adherence-classifier-jev](https://github.com/antoniofaical/startup-theme-adherence-classifier-jev).
Transforma o briefing em critérios e perguntas verificáveis, gera o JSON do
classificador e registra as escolhas de pesos, agregação e versionamento.

## Uso

A skill está em `skills/scoring-profile-maker/`. Disponibilize essa pasta no
diretório de skills do seu cliente Codex ou instale a partir deste repositório
com o instalador de skills do cliente. O caminho da skill no repositório é
`skills/scoring-profile-maker`. A criação deste pacote não instala nem ativa a
skill automaticamente.

Exemplo de solicitação após a instalação:

> Use $scoring-profile-maker para criar um perfil de aderência para soluções que
> coordenem encaminhamentos de pacientes. Use evidências dos sites das empresas.
> A presença do nome de uma doença não deve aumentar o score. Quero priorizar
> soluções para investigação e receber o JSON compatível e a justificativa.

Por padrão, a entrega contém `profile.json`, `profile_request.json` e
`design_notes.md`. Um pedido de somente JSON é respeitado. Um perfil anterior
pode ser fornecido para revisão e análise de reutilização das respostas.

## Verificação local

Python 3.11+:

```text
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/check_package.py
python tools/package_skill.py
```

O último comando gera `dist/scoring-profile-maker-0.1.0.zip`, com a skill e seus
recursos, sem ambiente virtual, caches, testes ou auditoria. Para usar somente
o validador, instale `requirements.txt`.

```text
python skills/scoring-profile-maker/scripts/validate_profile.py caminho/profile.json
python skills/scoring-profile-maker/scripts/validate_profile.py caminho/novo.json --baseline caminho/anterior.json
python skills/scoring-profile-maker/scripts/validate_profile.py caminho/profile.json --classifier-root caminho/classificador
```

As verificações não executam Jev nem DeepL. O contrato de origem, com commit e
hashes, está em `skills/scoring-profile-maker/references/upstream.json`.
Os resultados desta entrega estão em [auditoria/validacao.md](auditoria/validacao.md).

Validade técnica não prova validade do tema ou precisão de classificação. A
skill entrega um rascunho revisável; aprovação de domínio e calibração empírica
permanecem sob controle humano.
