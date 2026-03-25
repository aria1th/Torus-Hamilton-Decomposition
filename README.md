# Hamilton decompositions of low-dimensional directed tori

This repository now contains the full low-dimensional program around directed
torus Hamilton decompositions:

- `d=3`: solved manuscript for all `m >= 3`
- `d=4`: solved in the same return-map / odometer language, with Lean
  formalization
- composite dimensions: theorem-level product reduction now shows that every
  dimension of the form `2^alpha 3^beta` with `alpha + beta >= 1` is already
  forced, including `d=6,8,9,12,16,18,...`; more generally, all composite
  dimensions follow once the prime dimensions are settled
- `d=5`: odd `m` now closes inside the accepted theorem package via the global
  bridge `(beta,rho)` / raw `(beta,delta)`; even `m` remains open and is
  currently best treated as a finite-defect / splice repair problem rather
  than as a broad witness-search branch

The original core manuscript in this bundle is:

*Hamilton decompositions of the directed 3-torus `D(m)`: explicit constructions
for all `m >= 3`* by Sanghyun Park.

## Current repository status

The repo is no longer just the original `d=3` manuscript bundle.

- `tex/` and the main manuscript files still center the finished `d=3` paper
- `RoundX/` contains the finished `d=4` proof program
- `RoundComposite/` contains the theorem-level composite-dimension product
  reduction and prime-to-composite closure note
- `formal/` contains the Lean development, including a complete `d=4`
  formalization, the completed `d=3` formal split
  (`TorusD3Odd`, `TorusD3Even`, `TorusD3Odometer`), and conservative `d=5`
  extracted-model support
- `RoundY/` contains the closed odd-`m` D5 theorem package, the open even-`m`
  branch, and the current generalization / screening notes

For the current research-facing status, start with:

- [RESEARCH_HIGHLIGHTS.md](RESEARCH_HIGHLIGHTS.md)
- [RESEARCH_PROGRESSION.md](RESEARCH_PROGRESSION.md)
- [RoundY/README.md](RoundY/README.md)
- [formal/README.md](formal/README.md)

## Context

The problem studied here is the same directed `3`-torus decomposition problem
highlighted in Donald Knuth's note *Claude's Cycles* (dated February 28, 2026;
revised March 6, 2026):

https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf

Knuth's note frames the question of decomposing the arcs of the digraph on
`(Z/mZ)^3` into three directed Hamilton cycles, discusses an odd-`m`
construction found in AI-assisted exploration, and records the state of the
even case during that period. The manuscript in this bundle gives a full
mathematical treatment for all `m >= 3`, including:

- explicit odd constructions;
- a parity obstruction for Kempe-from-canonical approaches in the even case;
- the Route E construction for even `m >= 6`;
- a separate finite witness for `m = 4`.

## Repository structure

```
.
├── README.md
├── RESEARCH_HIGHLIGHTS.md    ← 현재 연구 하이라이트
├── RESEARCH_PROGRESSION.md   ← 전체 연구 진행 타임라인
├── CITATION.cff
├── LICENSE
├── .gitignore
│
├── tex/                      ← 논문 .tex/.pdf 버전들
│   ├── d3torus_..._editorial_revision.tex        (v1)
│   ├── d3torus_..._reworked_forced_repair.tex     (rework v1)
│   ├── d3torus_..._reworked_forced_repair_v2.tex  (rework v2)
│   ├── d3torus_..._splice_integrated.tex
│   ├── d3torus_..._appendices.tex
│   └── d3torus_..._appendices_upload.{tex,pdf}
│
├── reviews/                  ← 리뷰 및 구조 제안
│   ├── review_a.md, review_b.md
│   ├── suggestion_c.md, suggestion_d.md
│   └── proof_progress_suggestion_d{,_round2,_round3}.md
│
├── Round2/                   ← 다단계 레프리 리포트
│   ├── proof-stages/         ← Gemini/GPT 5.4 Pro 증명 재구성 기록
│   ├── stage1/               ← 비교 리포트
│   ├── stage2/               ← Thinking/DeepThink 리포트
│   ├── stage3/               ← 7.5/10 리포트
│   └── stage4/               ← 8/10 리포트 + v3 원고
│
├── RoundX/                   ← d=4 일반화 작업
│   ├── codex_job_request{,_2,_3}.md
│   ├── d4_line_union_general_theorem_proof_final.{tex,md}
│   └── d3torus_..._v5.tex    (최종 submission 후보)
│
├── RoundComposite/           ← composite-dimension product reduction
│   ├── README.md
│   ├── TODO.md
│   ├── Result.md
│   └── d_composite_product_reduction.tex
│
├── RoundY/                   ← d=5 현재 frontier
│   ├── README.md
│   ├── current-frontier-and-approach.md
│   ├── theorem/
│   └── autonomous/
│
├── formal/                   ← Lean formalization
│   ├── README.md
│   ├── TorusD3Even/
│   ├── TorusD3Odd/
│   ├── TorusD3Odometer/
│   ├── TorusD4/
│   └── TorusD5/
│
├── 4d_generalization/        ← 4D 연구 메모
│
├── scripts/                  ← Python 탐색/검증 스크립트
│   ├── torus_nd_*.py
│   └── proof_progress_round{2,3}_checks.py
│
├── anc/                      ← 검증 스크립트 번들 (논문 보조)
├── artifacts/                ← 계산 결과물 (JSON, tar.gz)
├── candidates/               ← 후보 탐색 스크립트
├── traces/                   ← 탐색 단계 기록
│
├── Hamilton decompositions.pdf
└── SuppInfo_d3torus_complete_m_ge_3.zip
```

## Main manuscript

The current main TeX document used for the D3 arXiv submission is:

- `arxiv_uploads/2026-03-25_cases/d3_review_candidates/v8_d3_only/d3torus_complete_m_ge_3_odometer_revision_v8_rewrite.tex`
  — current upload-ready D3-only source.

Earlier working-lineage manuscript versions remain in `tex/`:

- `d3torus_complete_m_ge_3_editorial_revision.tex` — original v1 source.
- `d3torus_complete_m_ge_3_editorial_revision_reworked_forced_repair_v2.tex` —
  revised version with "deductive surgery" narrative.
- `RoundX/d3torus_complete_m_ge_3_editorial_revision_v5.tex` —
  older submission-era milestone from the D3/D4 branch.

## Supporting information

The files in `anc/` are verification aids only. They are not part of the
formal proofs in the manuscript.

Typical use:

```bash
cd anc
python run_even_artifact_suite.py
```

## d=4 generalization (RoundX)

The `RoundX/` directory contains the complete proof that the directed 4-torus
`D_4(m)` admits a Hamilton decomposition for all `m >= 3`, using a
line-union gauge witness:

- `d4_line_union_general_theorem_proof_final.tex` — full LaTeX proof.
- `d4_line_union_general_theorem_proof_final.md` — Markdown version.

The proof relies on a two-level return map → odometer conjugacy structure.
See `RESEARCH_PROGRESSION.md` for the full narrative of how this was discovered.

## Composite dimensions (RoundComposite)

The `RoundComposite/` directory contains a theorem-level product reduction for
composite dimensions:

- `d_composite_product_reduction.tex` proves the square lemma for `d=2`;
- it proves multiplicative closure
  `D_a(m)` and `D_b(m)` solved for all `m` `=> D_{ab}(m)` solved for all `m`;
- therefore every dimension `2^alpha 3^beta` with `alpha + beta >= 1` is now
  unconditionally closed from the already-solved `d=2,3,4` cases;
- more generally, all composite dimensions follow formally once the prime
  dimensions are settled.

This is currently a theorem-level existence result, not yet a tiny local
witness-table construction and not yet Lean-formalized.

## d=5 frontier (RoundY)

The `RoundY/` directory contains the current `d=5` program.

The odd-`m` branch is now closed inside the accepted theorem package:

- theorem-level object: abstract bridge `(beta,rho)`;
- concrete verifiable model: global raw `(beta,delta)`;
- final promoted proof chain:
  `033 -> 062 -> 076 -> 077 -> 079 -> 081 -> 082 -> 083`.

The even-`m` branch is still open. The current recommendation is **not** to
reopen broad witness search immediately, but to treat it by analogy with the
solved `d=3` even case:

- use the parity barrier to rule out Kempe-from-canonical;
- identify the right reduced return object;
- extract a finite-defect / splice repair theorem;
- sharpen that to a critical-row theorem on source windows;
- only then search for implementations.

So the live D5 research question is no longer the old odd-`m` globalization
gap. It is mainly:

- manuscript / audit cleanup for the odd-`m` theorem package;
- even-`m` repair-theorem discovery;
- and pilot validation that the theorem-guided screening method still works on
  manageable higher odd dimensions such as `d = 7, 9, ...`.

Start with:

- `RoundY/README.md`
- `RoundY/current-frontier-and-approach.md`
- `RoundY/theorem/d5_088_exact_verifiable_solution_for_odd_m.md`
- `RoundY/theorem/d5_even_case_strategy_from_d3.md`
- `RoundY/theorem/d5_even_m_parity_and_critical_row_program.md`
- `RoundY/TODO.md`

For a concrete theorem-guided screening example derived from the odd-`m`
methodology, see:

- `RoundY/specs/d5_089_odd_m_search_screen_example.md`
- `scripts/torus_nd_d5_odd_m_candidate_screen.py`

## Lean formalization checkpoint

The `formal/` tree now contains:

- a complete `d=4` formalization;
- a complete `d=3` even Route E package;
- the completed current `d=3` odometer rewrite:
  `Color2Full`,
  `Color1FullCaseI`,
  `Color1FullCaseII`,
  `Color0FullCaseI`,
  `Color0FullCaseII`,
  and
  `Color0FullCaseIIModFour`;
- the pre-existing odd-`m` `d=3` closure in `TorusD3Odd`, so small odd cases
  such as `m = 3` are already covered there rather than needing a separate
  odometer-side reproof;
- the extracted-model / specification scaffolding for `d=5`.

So the live formal scope question is no longer whether the current `d=3`
odometer rewrite closes. It does. The remaining formal work is cleanup,
presentation, and any future abstraction/refactor passes, while `d=5` Lean
remains a support/specification branch rather than the main research frontier.

## Research progression

See [`RESEARCH_PROGRESSION.md`](RESEARCH_PROGRESSION.md) for a detailed
chronological account of the full research arc, including:

- AI-assisted proof restructuring (orbit tracing → height comparison → finite splice)
- Multi-stage referee feedback loop (6/10 → 8/10)
- d=4 generalization breakthrough
- d=5 reduction from broad search to the bridge/globalization theorem, closure
  of the odd-`m` branch, and the current even-`m` repair strategy

## AI tooling disclosure

During the development of this manuscript and the broader low-dimensional
research program, the author used GPT-5.4, GPT-5.4 Pro, Codex 5.3, Gemini 3.1
Deep Think, and Opus 4.6 for exploratory case analysis, theorem packaging,
candidate proof directions, validation-code assistance, internal critique, and
language revision. The author independently reviewed and edited all outputs and
takes full responsibility for the final content.

## Citation and license

Citation metadata is provided in `CITATION.cff`. The repository is released
under the MIT License; see `LICENSE`.
