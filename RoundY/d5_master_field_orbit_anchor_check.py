#!/usr/bin/env python3
"""Verify orbit-anchor reconstruction and explicit anchored obstructions.

This script reads the Codex artifact `d5_master_field_quotient_001.tar.gz`,
reconstructs the unique cyclic-equivariant permutation field induced by the
prescribed representative-color anchor, and reports the first outgoing-Latin
obstructions for the two anchored schemas.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path("/mnt/data/master_extract/artifacts/d5_master_field_quotient_001/scripts")
FAMILY_PATH = ROOT / "torus_nd_d5_master_field_quotient_family.py"
OUT_PATH = Path("/mnt/data/d5_master_field_orbit_anchor_summary.json")


def load_family_module():
    spec = importlib.util.spec_from_file_location("mf_orbit_anchor", FAMILY_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def rotate_state(module, state, shift: int):
    return module.rotate_state(state, shift)


def anchored_perm(module, schema, state) -> Tuple[int, int, int, int, int]:
    out: List[int] = []
    for color in range(module.DIM):
        shifted_state = rotate_state(module, state, (-color) % module.DIM)
        a = module.required_color0_output(shifted_state, schema)
        out.append((a + color) % module.DIM)
    return tuple(out)


def is_perm(values: Sequence[int]) -> bool:
    return sorted(values) == list(range(len(values)))


def find_vertex_for_state(module, schema_name: str, target_state, m: int):
    schema = module.SCHEMA_BY_NAME[schema_name]
    for x0 in range(m):
        for x1 in range(m):
            for x2 in range(m):
                for x3 in range(m):
                    for x4 in range(m):
                        coords = (x0, x1, x2, x3, x4)
                        if module.state_for_vertex(coords, m, schema) == target_state:
                            return list(coords)
    return None


def summarize_schema(module, schema_name: str) -> Dict[str, object]:
    schema = module.SCHEMA_BY_NAME[schema_name]
    states = module.schema_state_space(schema_name, (5, 7, 9, 11, 13))
    bad_examples = []
    good_by_layer: Counter[str] = Counter()
    bad_by_layer: Counter[str] = Counter()
    for state in states:
        perm = anchored_perm(module, schema, state)
        if is_perm(perm):
            good_by_layer[str(state[0])] += 1
        else:
            bad_by_layer[str(state[0])] += 1
            if len(bad_examples) < 10:
                anchor_word = [module.required_color0_output(rotate_state(module, state, k), schema) for k in range(module.DIM)]
                bad_examples.append(
                    {
                        "state": [state[0], list(state[1])],
                        "anchor_word": anchor_word,
                        "induced_perm": list(perm),
                        "multiplicity_pattern": sorted(Counter(perm).values(), reverse=True),
                    }
                )
    return {
        "good_outgoing_states_by_layer": dict(good_by_layer),
        "bad_outgoing_states_by_layer": dict(bad_by_layer),
        "bad_outgoing_state_count": int(sum(bad_by_layer.values())),
        "bad_examples": bad_examples,
    }


def main() -> int:
    module = load_family_module()
    summary: Dict[str, object] = {"task_id": "D5-MASTER-FIELD-ORBIT-ANCHOR-CHECK", "schemas": {}}

    for schema_name in module.SCHEMA_BY_NAME:
        summary["schemas"][schema_name] = summarize_schema(module, schema_name)

    explicit_targets = [
        ("stable_anchor_two_atom", (2, (0, 0, 0, 0, 1)), "(m-1,0,0,0,3)"),
        ("unit_anchor_three_atom", (2, (0, 0, 0, 0, 1)), "(0,1,0,1,0)"),
    ]
    for schema_name, target_state, vertex_formula in explicit_targets:
        schema = module.SCHEMA_BY_NAME[schema_name]
        anchor_word = [module.required_color0_output(rotate_state(module, target_state, k), schema) for k in range(module.DIM)]
        induced_perm = anchored_perm(module, schema, target_state)
        summary["schemas"][schema_name]["explicit_universal_obstruction"] = {
            "state": [target_state[0], list(target_state[1])],
            "vertex_formula": vertex_formula,
            "sample_vertices": {str(m): find_vertex_for_state(module, schema_name, target_state, m) for m in (5, 7, 9)},
            "anchor_word": anchor_word,
            "induced_perm": list(induced_perm),
            "is_permutation": is_perm(induced_perm),
        }

    OUT_PATH.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
