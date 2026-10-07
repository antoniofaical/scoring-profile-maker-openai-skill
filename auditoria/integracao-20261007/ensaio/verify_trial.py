from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
SKILL = REPO / 'skills/scoring-profile-maker'
PLUGIN = Path(r'C:\Users\anton\.codex\plugins\cache\concept-expansion-local\concept-expansion\0.1.0\skills\expand-scouting-concept')
CLASSIFIER = REPO.parent / 'outputs/scoring-profile-maker-reference'


def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts
    }


command = [sys.executable, '-B', str(SKILL / 'scripts/validate_profile.py'), str(OUT / 'profile.json'), '--classifier-root', str(CLASSIFIER)]
run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'}, timeout=60)
save('validation_execution.json', {'command': command, 'exit_code': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr})
if run.returncode:
    raise SystemExit(run.stderr)
validation = json.loads(run.stdout)
save('validation.json', validation)

sys.path.insert(0, str(CLASSIFIER / 'src'))
from startup_adherence.domain.scoring import build_fit_result

profile = json.loads((OUT / 'profile.json').read_text(encoding='utf-8'))
ids = [criterion['id'] for criterion in profile['criteria']]
core = 'request_continuity_match'


def record(unit, central, **auxiliary):
    return {'evidence_unit': unit, 'probabilities': {key: central if key == core else auxiliary.get(key, 0.0) for key in ids}}


cases = [
    ('S01 especialista orçamento', [record('a', 0.95, quotation_follow_up=0.95)], 95.0),
    ('S02 especialista agenda', [record('a', 0.95, appointment_coordination=0.95)], 95.0),
    ('S03 especialista etapa', [record('a', 0.95, service_stage_visibility=0.95)], 95.0),
    ('S04 core fraco e auxiliares altos', [record('a', 0.05, **{key: 1.0 for key in ids if key != core})], 5.0),
    ('S05 de-para sem setor literal', [record('a', 0.95, appointment_coordination=0.95, small_workshop_context=0.0)], 95.0),
    ('S06 três unidades, uma forte e duas fracas', [record('a', 0.95), record('b', 0.05), record('c', 0.05)], 59.0),
    ('S07 repetições da mesma unidade', [record('a', 0.95), record('a', 0.05), record('a', 0.05)], 95.0),
]
review = []
for name, records, expected in cases:
    result = build_fit_result(subject=name, records=records, profile=profile)
    assert result['fit_score'] == expected, (name, result['fit_score'], expected)
    review.append({'case': name, 'synthetic_inputs': records, 'expected_score': expected, 'observed_score': result['fit_score'], 'evidence_units': result['aggregation']['evidence_units'], 'pass': True})
save('synthetic_review.json', {'scope': 'Cálculo do runtime com valores fabricados. Não são respostas Jev, classificação de empresas ou calibração empírica.', 'cases': review})

request = json.loads((OUT / 'profile_request.json').read_text(encoding='utf-8'))
human = json.loads((OUT / 'human_review.json').read_text(encoding='utf-8'))
assert request['profile_id'] == profile['id']
assert request['profile_name'] == profile['name']
assert len(request['required_dimensions']) == 1
assert len(request['optional_signals']) == 4
assert all(value is None for value in human.values())
assert 'threshold' not in json.dumps(profile)
assert not (OUT / 'mapa.json').exists()
assert not any(OUT.glob('search_queries.*'))
notes = (OUT / 'design_notes.md').read_text(encoding='utf-8')
assert 'mapa preliminar, parcial e conversacional' in notes
assert 'não foi validado por `validar_saida.py`' in notes
before = json.loads((OUT / 'protected_before.json').read_text(encoding='utf-8'))
after = {'skill': snapshot(SKILL), 'plugin': snapshot(PLUGIN), 'classifier': snapshot(CLASSIFIER)}
integrity = {}
for name in before:
    changed = sorted(key for key in before[name].keys() & after[name].keys() if before[name][key] != after[name][key])
    added = sorted(after[name].keys() - before[name].keys())
    removed = sorted(before[name].keys() - after[name].keys())
    integrity[name] = {'files_before': len(before[name]), 'files_after': len(after[name]), 'changed': changed, 'added': added, 'removed': removed, 'unchanged': not (changed or added or removed)}
    assert integrity[name]['unchanged'], name
save('integrity.json', integrity)
save('checks.json', {
    'profile_json_parsed': True,
    'profile_contract_runtime_exit_code': run.returncode,
    'profile_valid': validation['valid'],
    'profile_request_consistency': True,
    'synthetic_calculations_passed': len(review),
    'human_review_fields_null': True,
    'no_map_json_or_query_exports': True,
    'protected_trees_unchanged': True,
    'limits': ['Profile_request usa modelo de briefing sem schema executável próprio; conferência de consistência não é validação formal de schema.', 'Mapa somente nas notas, parcial/preliminar, sem execução dos validadores de concept-expansion.', 'Sem teste instalado de seleção automática da skill, sem respostas Jev e sem calibração de domínio.']
})
with (OUT / 'design_notes.md').open('a', encoding='utf-8') as stream:
    stream.write('\n## Resultado executado do ensaio\n\n')
    stream.write('Validador local: código de saída 0; contrato embarcado e runtime do checkout local aceitam o perfil. Schema do checkout igual ao embarcado.\n\n')
    stream.write(f"Hash integral do perfil: `{validation['profile_sha256']}`. Hash das perguntas: `{validation['question_set_sha256']}`.\n\n")
    stream.write('Sete cálculos sintéticos passaram. Especialistas isolados mantiveram 95; auxiliares em 100 com core em 5 mantiveram score 5; de-para com setor literal ausente manteve 95. Com uma unidade forte e duas fracas, top_weighted retornou 59: a diluição por conteúdo adicional existe e deve ser revista no piloto. Repetições da mesma unidade retornaram 95. Estes valores foram fornecidos manualmente; não comprovam a capacidade de um modelo de reconhecer os casos.\n\n')
    stream.write('Hashes dos arquivos da skill, do plugin e do checkout de referência ficaram iguais, sem novos arquivos nessas árvores. `profile_request.json` foi lido e conferido quanto a ID, nome e dimensões; não há schema separado validado para esse briefing. Todos os campos de `human_review.json` continuam nulos.\n')
print(json.dumps({'valid': validation['valid'], 'synthetic_cases_passed': len(review), 'protected_trees_unchanged': True, 'profile_sha256': validation['profile_sha256'], 'question_set_sha256': validation['question_set_sha256']}, ensure_ascii=False))
