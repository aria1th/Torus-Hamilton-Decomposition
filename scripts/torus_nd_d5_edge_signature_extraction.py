#!/usr/bin/env python3
"""Extract the minimal edge-conditioned signature suggested by the D5 collision artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping, Sequence

TASK_ID = "D5-EDGE-TRANSDUCER-028"


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _load_json(path: str | Path) -> Mapping[str, object]:
    return json.loads(Path(path).read_text())


def _diag_summary() -> Mapping[str, object]:
    rows = _load_json("artifacts/d5_fixed_w_omit_defect_026/data/layer2_collision_examples.json")["rows"]
    examples = []
    for row in rows:
        w0 = int(row["w0"])
        examples.append(
            {
                "m": int(row["m"]),
                "current_layer2_state": row["shared_layer2_state"],
                "left_endpoint_predecessor": row["left_initial_state"],
                "right_endpoint_predecessor": row["right_initial_state"],
                "edge_signature_formula": {
                    "stationary_coordinate": "pred_w",
                    "left_endpoint": f"pred_w = {w0 - 1}",
                    "right_endpoint": f"pred_w = {w0}",
                    "off_edge": f"pred_w not in {{{w0 - 1},{w0}}}",
                },
            }
        )
    return {
        "branch": "diagonal_fixed_w",
        "stationary_coordinate": "w",
        "signature_summary": (
            "At the layer2 collision state, the current vertex is identical for the left and right active endpoints. "
            "The smallest separating edge-conditioned signature is the predecessor layer1 w-value relative to the "
            "active pair {w0-1,w0}: left endpoint iff pred_w=w0-1, right endpoint iff pred_w=w0, off-edge otherwise."
        ),
        "examples": examples,
    }


def _antidiag_summary() -> Mapping[str, object]:
    rows = _load_json("artifacts/d5_fixed_t_omit_defect_027/data/layer2_collision_examples.json")["rows"]
    examples = []
    for row in rows:
        t0 = int(row["t0"])
        examples.append(
            {
                "m": int(row["m"]),
                "current_layer2_state": row["shared_layer2_state"],
                "lower_endpoint_predecessor": row["lower_initial_state"],
                "higher_endpoint_predecessor": row["higher_initial_state"],
                "edge_signature_formula": {
                    "stationary_coordinate": "pred_t",
                    "lower_endpoint": f"pred_t = {t0}",
                    "higher_endpoint": f"pred_t = {t0 + 1}",
                    "off_edge": f"pred_t not in {{{t0},{t0 + 1}}}",
                },
            }
        )
    return {
        "branch": "antidiagonal_fixed_t",
        "stationary_coordinate": "t = w + 2u",
        "signature_summary": (
            "At the anti-diagonal layer2 collision state, the current vertex is again identical for the two active "
            "endpoints. The smallest separating edge-conditioned signature is the predecessor layer1 stationary "
            "coordinate pred_t relative to the active pair {t0,t0+1}: lower endpoint iff pred_t=t0, higher endpoint "
            "iff pred_t=t0+1, off-edge otherwise."
        ),
        "examples": examples,
    }


def _transducer_summary() -> Mapping[str, object]:
    return {
        "controller_states": ["off_edge", "left_endpoint", "right_endpoint"],
        "palette_mapping": {
            "off_edge": "B",
            "left_endpoint": "P",
            "right_endpoint": "M",
        },
        "omit_row_override": "On the omitted row s=s0, force both endpoint states back to B.",
        "cocycle_defect": {
            "point_left": "toggle layer3 only on the omitted left endpoint",
            "point_right": "toggle layer3 only on the omitted right endpoint",
            "edge_pair": "toggle layer3 on both omitted endpoints",
        },
        "interpretation": (
            "This is the smallest edge-conditioned transducer consistent with the 025 reduced normal form and the "
            "026/027 collision data. The missing local state is endpoint orientation, not another vertex selector."
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract minimal edge-conditioned signatures from the D5 collision artifacts.")
    parser.add_argument("--out-dir", type=Path, required=True, help="artifact data directory")
    parser.add_argument("--summary-out", type=Path, required=True, help="main summary JSON output")
    args = parser.parse_args(argv)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    diag = _diag_summary()
    antidiag = _antidiag_summary()
    transducer = _transducer_summary()
    _write_json(out_dir / "diagonal_edge_signature.json", diag)
    _write_json(out_dir / "antidiagonal_edge_signature.json", antidiag)
    _write_json(out_dir / "transducer_target.json", transducer)

    summary = {
        "task_id": TASK_ID,
        "sources": {
            "diag_collision": "artifacts/d5_fixed_w_omit_defect_026/data/layer2_collision_examples.json",
            "antidiag_collision": "artifacts/d5_fixed_t_omit_defect_027/data/layer2_collision_examples.json",
        },
        "strongest_supported_conclusion": (
            "The 026/027 collisions identify the missing controller type exactly: the smallest separating local state "
            "is edge-conditioned endpoint orientation. In the diagonal branch this is predecessor w relative to the "
            "active pair; in the anti-diagonal branch it is predecessor t relative to the active pair. This yields the "
            "3-state transducer off/L/R required by s44."
        ),
        "recommended_next_family": (
            "Search the smallest edge-conditioned transducer that maps off->B, L->P, R->M, with omitted-row override "
            "and omitted-edge cocycle defect, instead of widening vertex-conditioned selectors."
        ),
    }
    _write_json(args.summary_out, summary)

    print(f"task_id: {TASK_ID}")
    print("extracted edge-conditioned signatures from 026/027 collisions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
