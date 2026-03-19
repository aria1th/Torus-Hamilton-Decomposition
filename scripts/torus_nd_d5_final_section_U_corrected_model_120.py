#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from torus_nd_d5_selector_star_common_119 import selector_perm_star

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = REPO_ROOT / "RoundY" / "checks" / "d5_120_final_section_U_corrected_model_summary.json"

EXACT_MODULI = [11, 13, 15, 17, 19, 21]
EXACT_SPOT_CHECKS = [23, 25]
MODEL_ONLY_SCAN_MAX = 101

def apply_F_color4(m: int, x: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    y = list(x)
    p = selector_perm_star(m, tuple(y))
    j = p[4]
    y[j] = (y[j] + 1) % m
    return tuple(y)


def correction_diffs(m: int) -> list[int]:
    if m < 11 or m % 2 == 0:
        raise ValueError(f"correction formula is only intended for odd m >= 11, got m={m}")
    return [3, 3, 3, 1, 3] + [2] * (m - 7) + [1, 0]


def correction_c(m: int) -> list[int]:
    c = [0] * m
    for a, value in {0: 0, 1: 3, 2: 6, 3: 9, 4: 10, m - 1: 0}.items():
        c[a] = value % m
    for a in range(5, m - 1):
        c[a] = (2 * a + 3) % m
    return c


def exact_transformed_map(m: int) -> dict[tuple[int, int], tuple[int, int]]:
    c = correction_c(m)
    transformed = {}
    steps = m ** 3
    for a in range(m):
        for v in range(m):
            b = (v - c[a]) % m
            x = (a, b, (-a) % m, 0, (-b) % m)
            y = x
            for _ in range(steps):
                y = apply_F_color4(m, y)
            ap = y[0]
            vp = (y[1] + c[ap]) % m
            transformed[(a, v)] = (ap, vp)
    return transformed


def model_rule(m: int, a: int, v: int) -> tuple[str, tuple[int, int]]:
    if a == 0:
        if v == (m - 8) % m:
            return ("row0_same_m_minus_8", (0, (v - 2) % m))
        if v == m - 1:
            return ("row0_same_m_minus_1", (0, (v - 2) % m))
        return ("row0_to_row1_affine", (1, (2 * v + 6) % m))

    if 1 <= a <= 6:
        if a == 1 and v == 4 % m:
            return ("row1_special_to_row7", (7 % m, 2 % m))
        if v == (2 * a + 2) % m:
            return ("line_A_same", (a, (v - 2) % m))
        if v == (2 * a - 10) % m:
            return ("line_B_early_same", (a, (v - 2) % m))
        return ("bulk", ((a + 1) % m, v))

    if a == 7:
        if v == (2 * a + 2) % m:
            return ("line_A_same", (a, (v - 2) % m))
        return ("bulk", ((a + 1) % m, v))

    if a == 8:
        if v == (2 * a - 12) % m:
            return ("row8_special_to_row0", (0, m - 2))
        if v == (2 * a + 2) % m:
            return ("line_A_same", (a, (v - 2) % m))
        return ("bulk", ((a + 1) % m, v))

    if 9 <= a <= m - 2:
        if v == (2 * a + 2) % m:
            return ("line_A_same", (a, (v - 2) % m))
        if v == (2 * a - 12) % m:
            return ("line_B_late_same", (a, (v - 2) % m))
        return ("bulk", ((a + 1) % m, v))

    if v == 0:
        return ("row_last_same_zero", (a, (v - 2) % m))
    if v == (m - 14) % m:
        return ("row_last_same_m_minus_14", (a, (v - 2) % m))
    if v == 4 % m:
        return ("row_last_special_to_row1", (1, 4 % m))
    if v == 2 % m:
        return ("row_last_special_to_row0_m_minus_1", (0, m - 1))
    if v % 2 == 1:
        return ("row_last_odd_half_to_row0", (0, ((v + (m - 6)) // 2) % m))
    return ("row_last_even_half_to_row0", (0, (v // 2 - 3) % m))


def defect_formula_records(m: int) -> list[dict[str, object]]:
    records = []
    for a in range(m):
        for v in range(m):
            kind, image = model_rule(m, a, v)
            if image == ((a + 1) % m, v):
                continue
            records.append(
                {
                    "state": [a, v],
                    "image": [image[0], image[1]],
                    "type": kind,
                }
            )
    records.sort(key=lambda item: (item["state"][0], item["state"][1]))
    return records


def verify_model_against_exact(m: int, transformed: dict[tuple[int, int], tuple[int, int]]) -> dict[str, object]:
    mismatches = []
    type_counts = Counter()
    defect_count = 0
    for a in range(m):
        for v in range(m):
            kind, image = model_rule(m, a, v)
            if image != ((a + 1) % m, v):
                defect_count += 1
                type_counts[kind] += 1
            if image != transformed[(a, v)]:
                mismatches.append(
                    {
                        "state": [a, v],
                        "model_image": [image[0], image[1]],
                        "exact_image": [transformed[(a, v)][0], transformed[(a, v)][1]],
                        "type": kind,
                    }
                )
                if len(mismatches) >= 20:
                    break
        if len(mismatches) >= 20:
            break
    return {
        "exact_match": not mismatches,
        "mismatch_count": len(mismatches),
        "sample_mismatches": mismatches,
        "defect_count": defect_count,
        "defect_count_matches_formula_4m_minus_7": defect_count == 4 * m - 7,
        "defect_type_counts": dict(sorted(type_counts.items())),
    }


def cycle_summary(m: int, transformed: dict[tuple[int, int], tuple[int, int]]) -> dict[str, object]:
    states = [(a, v) for a in range(m) for v in range(m)]
    idx = {state: i for i, state in enumerate(states)}
    perm = [idx[transformed[state]] for state in states]
    visited = [False] * len(states)
    lengths = []
    for i in range(len(states)):
        if visited[i]:
            continue
        cur = i
        length = 0
        while not visited[cur]:
            visited[cur] = True
            cur = perm[cur]
            length += 1
        lengths.append(length)
    lengths.sort(reverse=True)
    distribution = Counter(lengths)
    return {
        "cycle_count": len(lengths),
        "largest_cycle": lengths[0],
        "distribution": {str(k): v for k, v in sorted(distribution.items(), reverse=True)},
        "hamilton": len(lengths) == 1,
    }


def row0_first_return(transformed: dict[tuple[int, int], tuple[int, int]], m: int) -> dict[str, object]:
    records = []
    time_dist = Counter()
    translation_ok = True
    for v0 in range(m):
        cur = (0, v0)
        steps = 0
        while True:
            cur = transformed[cur]
            steps += 1
            if cur[0] == 0:
                break
        target_v = (v0 - 2) % m
        if cur[1] != target_v:
            translation_ok = False
        records.append({"start_v": v0, "return_v": cur[1], "steps": steps})
        time_dist[steps] += 1
    return {
        "translation_minus_two": translation_ok,
        "step_distribution": {str(k): v for k, v in sorted(time_dist.items())},
        "records": records,
    }


def row0_hit_summary(transformed: dict[tuple[int, int], tuple[int, int]], m: int) -> dict[str, object]:
    max_steps = 0
    witness = None
    for a in range(m):
        for v in range(m):
            cur = (a, v)
            for step in range(1, 20 * m):
                cur = transformed[cur]
                if cur[0] == 0:
                    if step > max_steps:
                        max_steps = step
                        witness = {"state": [a, v], "landing": [cur[0], cur[1]], "steps": step}
                    break
            else:
                return {
                    "all_states_hit_row0": False,
                    "max_steps": None,
                    "witness": {"state": [a, v]},
                }
    return {
        "all_states_hit_row0": True,
        "max_steps": max_steps,
        "max_steps_matches_2m_minus_4": max_steps == 2 * m - 4,
        "witness": witness,
    }


def model_map(m: int) -> dict[tuple[int, int], tuple[int, int]]:
    return {(a, v): model_rule(m, a, v)[1] for a in range(m) for v in range(m)}


def model_only_scan(max_m: int) -> dict[str, object]:
    per_modulus = {}
    for m in range(11, max_m + 1, 2):
        transformed = model_map(m)
        cycle = cycle_summary(m, transformed)
        row0 = row0_first_return(transformed, m)
        hits = row0_hit_summary(transformed, m)
        per_modulus[str(m)] = {
            "hamilton": cycle["hamilton"],
            "row0_translation_minus_two": row0["translation_minus_two"],
            "all_states_hit_row0": hits["all_states_hit_row0"],
        }
    return {
        "max_m": max_m,
        "all_hamilton": all(item["hamilton"] for item in per_modulus.values()),
        "all_row0_translation_minus_two": all(item["row0_translation_minus_two"] for item in per_modulus.values()),
        "all_states_hit_row0": all(item["all_states_hit_row0"] for item in per_modulus.values()),
        "per_modulus": per_modulus,
    }


def exact_block(m: int) -> dict[str, object]:
    transformed = exact_transformed_map(m)
    verify = verify_model_against_exact(m, transformed)
    defects = defect_formula_records(m)
    row0 = row0_first_return(transformed, m)
    hits = row0_hit_summary(transformed, m)
    cycle = cycle_summary(m, transformed)
    return {
        "correction_diffs": correction_diffs(m),
        "correction_c": correction_c(m),
        "model_verification": verify,
        "defect_records": defects,
        "row0_first_return": row0,
        "row0_hit_summary": hits,
        "cycle_summary": cycle,
    }


def main() -> None:
    exact = {str(m): exact_block(m) for m in EXACT_MODULI}
    spots = {str(m): exact_block(m) for m in EXACT_SPOT_CHECKS}
    summary = {
        "scope": {
            "source_selector": "Sel* from scripts/torus_nd_d5_selector_star_common_119.py",
            "object": "U_m = (F_4^*)^(m^3)|P2 in corrected row coordinates (a,v)",
            "requested_exact_moduli": EXACT_MODULI,
            "extra_exact_spot_checks": EXACT_SPOT_CHECKS,
            "model_only_scan_max_m": MODEL_ONLY_SCAN_MAX,
        },
        "correction_formula": {
            "diff_pattern": "[3,3,3,1,3] + [2]^(m-7) + [1,0]",
            "closed_form": {
                "c(0..4)": [0, 3, 6, 9, 10],
                "c(a) for 5 <= a <= m-2": "2a + 3 mod m",
                "c(m-1)": 0,
            },
        },
        "exact_verification": exact,
        "extra_exact_spot_checks": spots,
        "model_only_scan": model_only_scan(MODEL_ONLY_SCAN_MAX),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2))
    print(OUT_JSON)


if __name__ == "__main__":
    main()
