import itertools, json, pathlib, sys, tarfile, tempfile
from collections import Counter

TAR = pathlib.Path('/mnt/data/d5_fresh_cyclic_qclock_vfiber_001.tar.gz')

with tempfile.TemporaryDirectory() as td:
    with tarfile.open(TAR, 'r:gz') as tf:
        tf.extractall(td)
    base = pathlib.Path(td) / 'artifacts' / 'd5_fresh_cyclic_qclock_vfiber_001'
    sys.path.insert(0, str(base / 'scripts'))
    from torus_nd_d5_fresh_cyclic_qclock_family import deserialize_candidate, full_step_color, candidate_name

    cands = json.load(open(base / 'data' / 'handoff_candidates.json'))

    def analyze(spec, m):
        verts = list(itertools.product(range(m), repeat=5))
        # outgoing direction multiset per vertex
        outgoing_bad = 0
        outgoing_patterns = Counter()
        incoming_dirs = {v: [] for v in verts}
        for v in verts:
            dirs = []
            for c in range(5):
                nxt = full_step_color(spec, c, v, m)
                diff = [(nxt[i] - v[i]) % m for i in range(5)]
                d = diff.index(1)
                dirs.append(d)
                incoming_dirs[nxt].append(d)
            pat = tuple(sorted(dirs))
            if pat != (0, 1, 2, 3, 4):
                outgoing_bad += 1
                outgoing_patterns[pat] += 1
        incoming_bad = 0
        incoming_patterns = Counter()
        for v, dirs in incoming_dirs.items():
            pat = tuple(sorted(dirs))
            if pat != (0, 1, 2, 3, 4):
                incoming_bad += 1
                incoming_patterns[pat] += 1
        return {
            'm': m,
            'vertex_count': len(verts),
            'outgoing_bad_vertices': outgoing_bad,
            'outgoing_good_fraction': (len(verts) - outgoing_bad) / len(verts),
            'incoming_bad_vertices': incoming_bad,
            'incoming_good_fraction': (len(verts) - incoming_bad) / len(verts),
            'top_outgoing_bad_patterns': [
                {'pattern': list(p), 'count': c}
                for p, c in outgoing_patterns.most_common(10)
            ],
            'top_incoming_bad_patterns': [
                {'pattern': list(p), 'count': c}
                for p, c in incoming_patterns.most_common(10)
            ],
        }

    out = {'task': 'D5-MASTER-FIELD-LATIN-CHECK-001', 'results': []}
    for item in cands:
        spec = deserialize_candidate(item['candidate'])
        out['results'].append({
            'candidate_name': candidate_name(spec),
            'm5': analyze(spec, 5),
            'm7': analyze(spec, 7),
        })

json.dump(out, open('/mnt/data/d5_master_field_latin_check_summary.json', 'w'), indent=2)
print('saved /mnt/data/d5_master_field_latin_check_summary.json')
