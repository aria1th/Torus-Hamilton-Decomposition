#!/usr/bin/env python3
import json, pathlib, sys, collections

BASE = pathlib.Path('/mnt/data/phasealign_ex/d5_theta_ab_phase_align_001')
if not BASE.exists():
    BASE.mkdir(parents=True, exist_ok=True)
    raise SystemExit('Expected extracted bundle at /mnt/data/phasealign_ex/d5_theta_ab_phase_align_001')

sys.path.append(str(BASE / 'scripts'))
import torus_nd_d5_master_field_quotient_family as fam

search = json.loads((BASE / 'data' / 'search_summary.json').read_text())
fields = search['schema_results'][0]['feasible_fields']
state_space_key = (5, 7, 9, 11, 13)
states = fam.schema_state_space(fam.SCHEMA_PHASE_ALIGN.name, state_space_key)
state_to_id = {s: i for i, s in enumerate(states)}
perms = [{int(r['state_id']): tuple(r['permutation']) for r in f['anchor_table']['rows']} for f in fields]

strict_ids = [0,1,2,3,4]
clean_ids = [5,6,7,8,9]

def realized_states(moduli):
    out = set()
    for m in moduli:
        for x0 in range(m):
            for x1 in range(m):
                for x2 in range(m):
                    for x3 in range(m):
                        for x4 in range(m):
                            sid = state_to_id[fam.state_for_vertex((x0,x1,x2,x3,x4), m, fam.SCHEMA_PHASE_ALIGN)]
                            out.add(sid)
    return out

pilot_realized = realized_states([5,7,9])

summary = {
    'task_id': 'D5-PHASE-ALIGN-PILOT-GRAMMAR-ANALYSIS',
    'pilot_realized_state_count': len(pilot_realized),
    'layer_counts_on_pilot_realized': dict(collections.Counter(states[sid][0] for sid in pilot_realized)),
    'classes': {},
}

for class_name, ids in [('strict_collapse', strict_ids), ('clean_nonclock', clean_ids)]:
    class_tables = [perms[i] for i in ids]
    # check rigidity on pilot-realized states
    disagreements = []
    for sid in sorted(pilot_realized):
        vals = {tbl[sid] for tbl in class_tables}
        if len(vals) > 1:
            disagreements.append({'state_id': sid, 'state': {'layer_bucket': states[sid][0], 'signature': list(states[sid][1])}, 'permutations': [list(v) for v in sorted(vals)]})
            if len(disagreements) >= 20:
                break
    rep = class_tables[0]
    layer_perm_hist = collections.Counter((str(states[sid][0]), ''.join(map(str, rep[sid]))) for sid in pilot_realized)
    # exact displacement law on pilot m values
    return_laws = {}
    for m in [5,7,9]:
        disp_hist = collections.Counter()
        for q in range(m):
            for w in range(m):
                for v in range(m):
                    for u in range(m):
                        cur = ((-q-w-v-u) % m, q, w, v, u)
                        for _ in range(m):
                            cur = fam.color_map_from_table(rep, fam.SCHEMA_PHASE_ALIGN, m, cur, 0, state_space_key)
                        got = (cur[1], cur[2], cur[3], cur[4])
                        disp = ((got[0]-q) % m, (got[1]-w) % m, (got[2]-v) % m, (got[3]-u) % m)
                        disp_hist[disp] += 1
        return_laws[str(m)] = {str(k): v for k, v in sorted(disp_hist.items())}
    summary['classes'][class_name] = {
        'field_indices': ids,
        'pilot_realized_disagreement_count': len(disagreements),
        'pilot_realized_disagreement_examples': disagreements,
        'layer_permutation_histogram_on_pilot_realized': {f'layer={layer}|perm={perm}': count for (layer, perm), count in layer_perm_hist.items()},
        'pilot_return_displacement_histogram': return_laws,
    }

# cross-class difference on pilot-realized states
strict = perms[strict_ids[0]]
clean = perms[clean_ids[0]]
diff_states = [sid for sid in sorted(pilot_realized) if strict[sid] != clean[sid]]
summary['cross_class_pilot_difference_count'] = len(diff_states)
summary['cross_class_pilot_difference_layer_histogram'] = dict(collections.Counter(states[sid][0] for sid in diff_states))
summary['cross_class_pilot_difference_examples'] = [
    {
        'state_id': sid,
        'state': {'layer_bucket': states[sid][0], 'signature': list(states[sid][1])},
        'strict_perm': list(strict[sid]),
        'clean_perm': list(clean[sid]),
    }
    for sid in diff_states[:20]
]

out = pathlib.Path('/mnt/data/d5_phase_align_pilot_grammar_analysis_summary.json')
out.write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2)[:4000])
