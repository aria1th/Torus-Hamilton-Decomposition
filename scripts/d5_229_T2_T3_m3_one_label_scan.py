#!/usr/bin/env python3
"""m=3 small-case one-label repair scan for T2 and T3 using the surfaced bundle."""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

BUNDLE_ROOT = Path('/mnt/data/bundlefull/roundy_d5_endpoint_return_model_bundle_20260321_update_197')
OUT_JSON = Path('/mnt/data/d5_229_T2_T3_m3_one_label_scan_summary.json')
TASK_ID = 'D5-T2-T3-M3-ONE-LABEL-SCAN-229'
BIT_NAMES = (
    'pred_changed','pred_left','pred_right','pred_deep',
    'succ_changed','succ_left','succ_right','succ_deep',
    'self_deep','self_stage3',
)
CLASS_LABELS = ('L1','R1','L2','R2','L3','R3')
ROWS = {
    'T2_sigma22': {'left_word': (4,1,4), 'right_word': (2,1,2)},
    'T3_sigma33': {'left_word': (4,4,1), 'right_word': (2,2,1)},
}


def load_helper() -> object:
    spec = importlib.util.spec_from_file_location('scan224', '/mnt/data/d5_224_T2_T3_bundle_obstruction_scan.py')
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


def main() -> None:
    helper = load_helper()
    seed032 = helper._import_seed032(BUNDLE_ROOT)
    prepared = seed032._prepare_m(3, seed032._mixed_rule())
    prepared_by_m = {3: prepared}
    out = {'task_id': TASK_ID, 'bundle_root': str(BUNDLE_ROOT), 'm': 3, 'rows': {}}

    for row_name, spec in ROWS.items():
        left = spec['left_word']
        right = spec['right_word']
        nexts_all, meta = seed032._build_candidate(prepared, w0=0, s0=0, left_word=left, right_word=right, cocycle_defect='none', repair=None)
        labels = meta['labels_by_color'][0]
        pair_counts = helper._pair_counts_for_color0(prepared, nexts_all[0], labels)
        profile = seed032._collision_profile_for_m(prepared, left_word=left, right_word=right)

        gate_total = gate_latin = 0
        bit_total = bit_latin = 0
        for label in CLASS_LABELS:
            base_dir = (left if label.startswith('L') else right)[int(label[1]) - 1]
            for alt_dir in range(5):
                if alt_dir == base_dir:
                    continue
                repair = {'label': label, 'alt_dir': alt_dir}
                for cocycle in ('none','left','right','both'):
                    row = seed032._evaluate_candidate_across_m(prepared_by_m, left_word=left, right_word=right, cocycle_defect=cocycle, repair=repair, m_values=(3,))
                    gate_total += 1
                    gate_latin += int(bool(row['latin_all']))
            for bit_name in BIT_NAMES:
                for bit_value in (0,1):
                    for alt_dir in range(5):
                        if alt_dir == base_dir:
                            continue
                        repair = {'label': label, 'bit_name': bit_name, 'bit_value': bit_value, 'alt_dir': alt_dir}
                        for cocycle in ('none','left','right','both'):
                            row = seed032._evaluate_candidate_across_m(prepared_by_m, left_word=left, right_word=right, cocycle_defect=cocycle, repair=repair, m_values=(3,))
                            bit_total += 1
                            bit_latin += int(bool(row['latin_all']))
        out['rows'][row_name] = {
            'latin_all_colors_base': bool(seed032.incoming_latin_all(nexts_all)),
            'overfull_targets_all_colors': int(profile['overfull_target_count']),
            'changed_label_counts_all_colors': {k:int(v) for k,v in sorted(profile['changed_label_counts'].items())},
            'pair_counts_color0': {str(k): int(v) for k,v in sorted(pair_counts.items(), key=lambda kv: str(kv[0]))},
            'one_gate_latin_count': gate_latin,
            'one_gate_total': gate_total,
            'one_bit_latin_count': bit_latin,
            'one_bit_total': bit_total,
        }

    OUT_JSON.write_text(json.dumps(out, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
