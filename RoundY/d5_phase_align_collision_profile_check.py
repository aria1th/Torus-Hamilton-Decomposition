#!/usr/bin/env python3
"""Analyze how much the proposed phase_align bit resolves hidden-phase collisions."""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

SCRIPT_DIR = Path('/mnt/data/d5_dynamic_collapse_core_001_extracted/d5_dynamic_collapse_core_001/scripts')
sys.path.append(str(SCRIPT_DIR))

from torus_nd_d5_master_field_quotient_family import SCHEMA_JOIN, color_map_from_table, state_for_vertex

STATE_SPACE_KEY = (5, 7, 9, 11, 13)
FIELD_JSON = Path('/mnt/data/d5_dynamic_collapse_core_001_extracted/d5_dynamic_collapse_core_001/data/input_best_stable_field.json')
OUT_JSON = Path('/mnt/data/d5_phase_align_collision_profile_summary.json')


def delta(coords, m: int) -> int:
    return (coords[3] - coords[1]) % m


def phase_align(coords, m: int) -> int:
    return int(delta(coords, m) == 0)


def main() -> None:
    field = json.loads(FIELD_JSON.read_text())
    table = {int(row['state_id']): tuple(row['permutation']) for row in field['anchor_table']['rows']}

    per_m = []
    for m in (5, 7, 9, 11, 13):
        visited = defaultdict(set)
        visited_bit = defaultdict(set)
        example_by_bit = {}
        for q in range(m):
            for w in range(m):
                for v in range(m):
                    for u in range(m):
                        cur = ((-q - w - v - u) % m, q, w, v, u)
                        for _ in range(m):
                            state = state_for_vertex(cur, m, SCHEMA_JOIN)
                            d = delta(cur, m)
                            b = phase_align(cur, m)
                            visited[state].add(d)
                            visited_bit[(state, b)].add(d)
                            example_by_bit.setdefault((state, b), tuple(cur))
                            cur = color_map_from_table(table, SCHEMA_JOIN, m, cur, 0, STATE_SPACE_KEY)
        orig_multi = sum(1 for vals in visited.values() if len(vals) > 1)
        split_multi = sum(1 for vals in visited_bit.values() if len(vals) > 1)
        full_nonzero = sum(1 for vals in visited_bit.values() if len(vals) == m - 1)
        almost_full = sum(1 for vals in visited_bit.values() if m - 3 <= len(vals) < m - 1)
        by_layer = Counter()
        support_hist = Counter()
        examples = []
        for (state, b), vals in visited_bit.items():
            if len(vals) <= 1:
                continue
            by_layer[str(state[0])] += 1
            support_hist[len(vals)] += 1
            if len(examples) < 12:
                examples.append({
                    'state': {'layer_bucket': state[0], 'signature': list(state[1])},
                    'phase_align': b,
                    'delta_values': sorted(vals),
                    'example_vertex': list(example_by_bit[(state, b)]),
                })
        per_m.append({
            'm': m,
            'original_multi_delta_state_count': orig_multi,
            'remaining_multi_delta_state_count_after_phase_align_split': split_multi,
            'fraction_remaining': (split_multi / orig_multi) if orig_multi else 0.0,
            'full_nonzero_support_state_count': full_nonzero,
            'almost_full_nonzero_support_state_count': almost_full,
            'remaining_multi_delta_by_layer': dict(sorted(by_layer.items())),
            'remaining_support_histogram': {str(k): v for k, v in sorted(support_hist.items())},
            'examples': examples,
        })

    OUT_JSON.write_text(json.dumps({'task_id': 'D5-PHASE-ALIGN-COLLISION-PROFILE-001', 'per_m': per_m}, indent=2))


if __name__ == '__main__':
    main()
