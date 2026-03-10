import json
import itertools
import importlib.util
import sys
from pathlib import Path

ROOT = Path('/mnt/data/tmp_join/d5_join_quotient_001')
if not ROOT.exists():
    import tarfile
    with tarfile.open('/mnt/data/d5_join_quotient_001.tar.gz', 'r:gz') as tf:
        tf.extractall('/mnt/data/tmp_join')

spec = importlib.util.spec_from_file_location('family', ROOT / 'scripts' / 'torus_nd_d5_master_field_quotient_family.py')
family = importlib.util.module_from_spec(spec)
sys.modules['family'] = family
spec.loader.exec_module(family)

field = json.load(open(ROOT / 'data' / 'best_stable_field.json'))
table = {row['state_id']: row['permutation'] for row in field['anchor_table']['rows']}
m_values_key = (5,7,9,11,13)
summary = {
    'task': 'D5-JOIN-STABLE-FIELD-RETURN-LAW-CHECK',
    'formula_checked': 'R_0(q,w,v,u) = (q+1, w, v+1, u)',
    'm_results': []
}

for m in [5,7,9,11,13]:
    def step(coords):
        return family.color_map_from_table(table, family.SCHEMA_JOIN, m, coords, 0, m_values_key)
    ok = True
    bad_examples = []
    for q,w,v,u in itertools.product(range(m), repeat=4):
        coords = ((-q-w-v-u) % m, q, w, v, u)
        cur = coords
        for _ in range(m):
            cur = step(cur)
        q2,w2,v2,u2 = cur[1],cur[2],cur[3],cur[4]
        target = ((q+1)%m, w, (v+1)%m, u)
        got = (q2,w2,v2,u2)
        if got != target:
            ok = False
            if len(bad_examples) < 10:
                bad_examples.append({'qwuv':[q,w,v,u], 'got':list(got), 'target':list(target)})
    summary['m_results'].append({'m':m,'matches_formula':ok,'bad_examples':bad_examples})

# derive palette by layer
palette = {}
for row in field['anchor_table']['rows']:
    L = str(row['state']['layer_bucket'])
    palette.setdefault(L, {})[row['permutation_name']] = palette.setdefault(L, {}).get(row['permutation_name'], 0) + 1
summary['permutation_palette_by_layer'] = palette
summary['implied_return_displacement'] = 'e_{c+1} + e_{c+3} - 2 e_c'
summary['implied_section_return'] = 'U_0 = id on (w,u)'
summary['implied_monodromy'] = 0

with open('/mnt/data/d5_join_stable_field_return_law_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
