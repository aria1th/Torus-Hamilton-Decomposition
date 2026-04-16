#!/usr/bin/env python3

from __future__ import annotations

import shutil
import tarfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STAGING_ROOT = REPO_ROOT / "tmp" / "d5_unified_proof_archive_2026-04-03"
TAR_PATH = REPO_ROOT / "tmp" / "tarfiles" / "d5_unified_proof_archive_2026-04-03.tar"
EXTRACTED_ROOT = REPO_ROOT / "tmp" / "unpacked_tarfiles"


CANONICAL_FILES = [
    "RoundY/README.md",
    "RoundY/current-frontier-and-approach.md",
    "RoundY/instruction_for_codex.md",
    "RoundY/specs/d5_272_routee_assembly_bundle_requirements.md",
    "RoundY/specs/d5_292_residual_compute_request_template.md",
    "RoundY/specs/d5_306_unified_proof_archive_design_2026-04-03.md",
    "RoundY/tex/d5_267_full_d5_working_manuscript_routee_honest.tex",
    "RoundY/tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex",
    "RoundY/tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex",
    "RoundY/theorem/d5_082_frontier_and_theorem_map.md",
    "RoundY/theorem/d5_083_gluing_flow_and_final_theorem.md",
    "RoundY/theorem/d5_083_final_theorem_proof.md",
    "RoundY/theorem/d5_099_one_pass_odd_m_globalization_package.md",
    "RoundY/theorem/d5_106_intended_quotient_identification_and_comparison.md",
    "RoundY/theorem/d5_121_M5_corrected_row_stitching.md",
    "RoundY/theorem/d5_122_M5_all_odd_identification.md",
    "RoundY/theorem/d5_255_transport_honesty_boundary.md",
    "RoundY/theorem/d5_256_independence_internalization_queue.md",
    "RoundY/theorem/d5_268_five_color_assembly_boundary.md",
    "RoundY/theorem/d5_279_one_point_repair_color2_closure.md",
    "RoundY/theorem/d5_280_one_point_repair_color1_line_obstruction.md",
    "RoundY/theorem/d5_281_routee_line_bit_search.md",
    "RoundY/theorem/d5_282_backbone_defect_compression_methodology.md",
    "RoundY/theorem/d5_284_current_working_frontier_after_nonresonant_closure.md",
    "RoundY/theorem/d5_285_residual_assembly_companion_memo.md",
    "RoundY/theorem/d5_286_promoted_collar_complete_local_dynamics.md",
    "RoundY/theorem/d5_287_prime_cyclic_quotient_probe.md",
    "RoundY/theorem/d5_288_next_closable_piece_priority.md",
    "RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md",
    "RoundY/theorem/d5_290_current_assumption_and_gap_audit.md",
    "RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md",
    "RoundY/theorem/d5_293_resonant_support_refinement_search.md",
    "RoundY/theorem/d5_294_residual_package_alignment_after_tar.md",
    "RoundY/theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md",
    "RoundY/theorem/d5_296_resonant_row3_direction_after_visible_grid.md",
    "RoundY/theorem/d5_297_resonant_late_zero_return_atlas.md",
    "RoundY/theorem/d5_298_resonant_late_mod30_routing_note.md",
    "RoundY/theorem/d5_299_resonant_late_first_exact_promotions.md",
    "RoundY/theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md",
    "RoundY/theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md",
    "RoundY/theorem/d5_302_resonant_pure_color1_core_chain.md",
    "RoundY/theorem/d5_303_current_d5_proof_status_overview.md",
    "RoundY/theorem/d5_304_routey_existence_parallel_layer.md",
    "RoundY/theorem/d5_305_current_d5_status_with_routey_existence.md",
]


COPY_SPECS = [
    {
        "src": REPO_ROOT / "RouteY-Existence",
        "dst": STAGING_ROOT / "20_parallel_routey_existence" / "RouteY-Existence",
        "exclude_dirs": set(),
        "exclude_suffixes": set(),
    },
    {
        "src": EXTRACTED_ROOT / "d5_requested_four_files_2026-03-30",
        "dst": STAGING_ROOT
        / "20_parallel_routey_existence"
        / "supplements"
        / "d5_requested_four_files_2026-03-30",
        "exclude_dirs": set(),
        "exclude_suffixes": set(),
    },
    {
        "src": EXTRACTED_ROOT
        / "d5_current_proof_bundle_curated_2026-04-03"
        / "d5_current_proof_bundle_2026-04-03",
        "dst": STAGING_ROOT
        / "30_current_support_packets"
        / "d5_current_proof_bundle_2026-04-03",
        "exclude_dirs": set(),
        "exclude_suffixes": set(),
    },
    {
        "src": EXTRACTED_ROOT
        / "d5_15r9_full_proof_archive_2026-04-01"
        / "d5_15r9_full_proof_archive_2026-04-01",
        "dst": STAGING_ROOT
        / "30_current_support_packets"
        / "d5_15r9_full_proof_archive_2026-04-01",
        "exclude_dirs": {"90_previous_handoff_summary"},
        "exclude_suffixes": set(),
    },
    {
        "src": EXTRACTED_ROOT
        / "d5_consolidated_standalone_package_2026-03-28_master_c_refresh"
        / "final_d5_consolidated_package_2026-03-27",
        "dst": STAGING_ROOT
        / "40_historical_bundle_extracts"
        / "final_d5_consolidated_package_2026-03-27",
        "exclude_dirs": set(),
        "exclude_suffixes": {".tar", ".tar.gz", ".tgz"},
    },
    {
        "src": EXTRACTED_ROOT
        / "d5_consolidated_support_archive_2026-03-28_v3"
        / "d5_consolidated_support_archive_2026-03-28_v3",
        "dst": STAGING_ROOT
        / "40_historical_bundle_extracts"
        / "d5_consolidated_support_archive_2026-03-28_v3",
        "exclude_dirs": set(),
        "exclude_suffixes": {".tar", ".tar.gz", ".tgz"},
    },
    {
        "src": EXTRACTED_ROOT
        / "roundy_d5_endpoint_return_model_bundle_20260321_update_197"
        / "roundy_d5_endpoint_return_model_bundle_20260321_update_197",
        "dst": STAGING_ROOT
        / "90_archive_provenance"
        / "roundy_d5_endpoint_return_model_bundle_20260321_update_197",
        "exclude_dirs": set(),
        "exclude_suffixes": set(),
    },
]


def reset_output() -> None:
    if STAGING_ROOT.exists():
        shutil.rmtree(STAGING_ROOT)
    STAGING_ROOT.mkdir(parents=True)
    TAR_PATH.parent.mkdir(parents=True, exist_ok=True)
    if TAR_PATH.exists():
        TAR_PATH.unlink()


def copy_file(rel_path: str, prefix: str) -> None:
    src = REPO_ROOT / rel_path
    if not src.exists():
        raise FileNotFoundError(src)
    dst = STAGING_ROOT / prefix / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def should_skip(path: Path, exclude_suffixes: set[str]) -> bool:
    if "__pycache__" in path.parts:
        return True
    if path.suffix == ".pyc":
        return True
    return any(str(path).endswith(suffix) for suffix in exclude_suffixes)


def copy_tree(
    src: Path,
    dst: Path,
    *,
    exclude_dirs: set[str],
    exclude_suffixes: set[str],
) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        if "__pycache__" in rel.parts:
            continue
        if any(part in exclude_dirs for part in rel.parts):
            continue
        if path.is_dir():
            (dst / rel).mkdir(parents=True, exist_ok=True)
            continue
        if should_skip(path, exclude_suffixes):
            continue
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, out)


def write_text(rel_path: str, text: str) -> None:
    dst = STAGING_ROOT / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def stage_canonical_roundy() -> None:
    for rel_path in CANONICAL_FILES:
        copy_file(rel_path, "10_canonical_roundy")


def stage_external_trees() -> None:
    for spec in COPY_SPECS:
        copy_tree(
            spec["src"],
            spec["dst"],
            exclude_dirs=spec["exclude_dirs"],
            exclude_suffixes=spec["exclude_suffixes"],
        )


def render_start_here() -> str:
    return """# Start Here

This unified archive is organized by authority level.

## 1. Canonical current proof frontier

Read these first:

1. `10_canonical_roundy/RoundY/README.md`
2. `10_canonical_roundy/RoundY/current-frontier-and-approach.md`
3. `10_canonical_roundy/RoundY/instruction_for_codex.md`
4. `10_canonical_roundy/RoundY/theorem/d5_284_current_working_frontier_after_nonresonant_closure.md`
5. `10_canonical_roundy/RoundY/tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex`
6. `10_canonical_roundy/RoundY/theorem/d5_285_residual_assembly_companion_memo.md`
7. `10_canonical_roundy/RoundY/tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex`
8. `10_canonical_roundy/RoundY/theorem/d5_286_promoted_collar_complete_local_dynamics.md`
9. `10_canonical_roundy/RoundY/theorem/d5_299_resonant_late_first_exact_promotions.md`
10. `10_canonical_roundy/RoundY/theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md`
11. `10_canonical_roundy/RoundY/theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md`
12. `10_canonical_roundy/RoundY/theorem/d5_302_resonant_pure_color1_core_chain.md`
13. `10_canonical_roundy/RoundY/theorem/d5_303_current_d5_proof_status_overview.md`
14. `10_canonical_roundy/RoundY/theorem/d5_305_current_d5_status_with_routey_existence.md`

## 2. Parallel existence / seam-surgery lane

Read next when you need the parallel arithmetic lane:

1. `20_parallel_routey_existence/RouteY-Existence/README.md`
2. `20_parallel_routey_existence/RouteY-Existence/status/MAIN_FLOW.md`
3. `20_parallel_routey_existence/RouteY-Existence/status/CURRENT_STATUS.md`
4. `20_parallel_routey_existence/supplements/d5_requested_four_files_2026-03-30/`

## 3. Current extracted support packets

- `30_current_support_packets/d5_current_proof_bundle_2026-04-03/`
- `30_current_support_packets/d5_15r9_full_proof_archive_2026-04-01/`

Treat these as support and certification packets, not as replacements for the
canonical RoundY frontier docs above.

## 4. Historical extracts

- `40_historical_bundle_extracts/` contains March 28 historical/support bundles
- `90_archive_provenance/` contains the older March 21 endpoint/model archive

Use those only when you need provenance, older guide layers, or pre-frontier
model history.

## 5. Important boundary

Do not treat older bundle-local `README`, `START_HERE`, or summary files as
authoritative over the `10_canonical_roundy/` material. The unified archive is
ordered so that current RoundY stays canonical.
"""


def render_crosswalk() -> str:
    return """# Source Crosswalk

## Included sources

- `RoundY/` selected current docs
  - status: canonical
  - reason: current D5 proof frontier and theorem-order reading

- `RouteY-Existence/`
  - status: parallel support
  - reason: curated existence / seam-surgery lane already promoted from the
    March 28 support archive

- `d5_requested_four_files_2026-03-30`
  - status: parallel supplement
  - reason: small `15r+9` residue-specific replay/check packet

- `d5_current_proof_bundle_curated_2026-04-03`
  - status: current support packet
  - reason: latest role-organized extracted bundle around the active April
    support work

- `d5_15r9_full_proof_archive_2026-04-01`
  - status: current baseline annex
  - reason: preserves the April 1 theorem floor plus scope/exclusion and
    missing-reference metadata

- `d5_consolidated_standalone_package_2026-03-28_master_c_refresh`
  - status: historical/support
  - reason: preserves the March 28 bridge bundle, late exact packet, and older
    guide layers

- `d5_consolidated_support_archive_2026-03-28_v3`
  - status: historical/support
  - reason: raw ancestor archive behind the later `RouteY-Existence` curation

- `roundy_d5_endpoint_return_model_bundle_20260321_update_197`
  - status: archive provenance
  - reason: older mixed-model / endpoint-return support chain

## Omitted or absorbed sources

- `d5_15r9_proof_handoff_bundle_2026-04-01`
  - omitted as a standalone subtree
  - reason: its substantive April 1 files are already preserved inside
    `d5_15r9_full_proof_archive_2026-04-01`; keeping both would create a
    second conflicting wrapper for the same packet

## Recomposition rule

The raw tar files were unpacked first and then recomposed into this archive.
Nested `.tar` files were not kept as primary content in the new bundle.
Historical provenance is preserved by source-scoped extracted directories.
"""


def all_staged_files() -> list[Path]:
    return sorted(path for path in STAGING_ROOT.rglob("*") if path.is_file())


def render_manifest() -> str:
    files = all_staged_files()
    manifest_rel = Path("00_guides/MANIFEST.md")
    if manifest_rel not in [path.relative_to(STAGING_ROOT) for path in files]:
        listed_files = [path.relative_to(STAGING_ROOT) for path in files] + [manifest_rel]
    else:
        listed_files = [path.relative_to(STAGING_ROOT) for path in files]
    top_levels = [
        "00_guides",
        "10_canonical_roundy",
        "20_parallel_routey_existence",
        "30_current_support_packets",
        "40_historical_bundle_extracts",
        "90_archive_provenance",
    ]
    lines = ["# Manifest", ""]
    lines.append(f"Total files: {len(listed_files)}")
    lines.append("")
    lines.append("## Top-level counts")
    for name in top_levels:
        root = STAGING_ROOT / name
        count = sum(1 for path in root.rglob("*") if path.is_file())
        if name == "00_guides" and manifest_rel not in [path.relative_to(STAGING_ROOT) for path in files]:
            count += 1
        lines.append(f"- `{name}/`: {count} files")
    lines.append("")
    lines.append("## Files")
    for rel_path in sorted(listed_files):
        lines.append(f"- `{rel_path.as_posix()}`")
    lines.append("")
    return "\n".join(lines)


def stage_guides() -> None:
    write_text("00_guides/START_HERE.md", render_start_here())
    write_text("00_guides/SOURCE_CROSSWALK.md", render_crosswalk())
    copy_file(
        "RoundY/specs/d5_306_unified_proof_archive_design_2026-04-03.md",
        "00_guides",
    )
    design_src = (
        STAGING_ROOT
        / "00_guides"
        / "RoundY"
        / "specs"
        / "d5_306_unified_proof_archive_design_2026-04-03.md"
    )
    design_dst = STAGING_ROOT / "00_guides" / "DESIGN.md"
    design_dst.write_text(design_src.read_text(encoding="utf-8"), encoding="utf-8")
    shutil.rmtree(STAGING_ROOT / "00_guides" / "RoundY")
    write_text("00_guides/MANIFEST.md", render_manifest())


def build_tar() -> int:
    with tarfile.open(TAR_PATH, "w") as archive:
        archive.add(STAGING_ROOT, arcname=STAGING_ROOT.name, recursive=True)
    with tarfile.open(TAR_PATH, "r") as archive:
        return len(archive.getmembers())


def main() -> None:
    reset_output()
    stage_canonical_roundy()
    stage_external_trees()
    stage_guides()
    member_count = build_tar()
    file_count = len(all_staged_files())
    print(f"staging: {STAGING_ROOT}")
    print(f"tar: {TAR_PATH}")
    print(f"files: {file_count}")
    print(f"tar members: {member_count}")


if __name__ == "__main__":
    main()
