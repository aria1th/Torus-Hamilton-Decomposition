# Hamilton decompositions of low-dimensional directed tori

This repository now contains the full low-dimensional program around directed
torus Hamilton decompositions:

- `d=3`: solved manuscript for all `m >= 3`
- `d=4`: solved in the same return-map / odometer language, with Lean
  formalization
- `d=5`: active frontier, currently reduced to an exact-bridge /
  globalization question: abstract bridge `(beta,rho)` versus the strongest
  checked concrete model `(beta,q,sigma)` / `(beta,delta)`

The original core manuscript in this bundle is:

*Hamilton decompositions of the directed 3-torus `D(m)`: explicit constructions
for all `m >= 3`* by Sanghyun Park.

## Current repository status

The repo is no longer just the original `d=3` manuscript bundle.

- `tex/` and the main manuscript files still center the finished `d=3` paper
- `RoundX/` contains the finished `d=4` proof program
- `formal/` contains the Lean development, including a complete `d=4`
  formalization, a complete `d=3` even Route E package, an active `d=3`
  odometer rewrite, and conservative `d=5` extracted-model support
- `RoundY/` contains the live `d=5` frontier

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

The latest manuscript versions are in `tex/`:

- `d3torus_complete_m_ge_3_editorial_revision.tex` — original v1 source.
- `d3torus_complete_m_ge_3_editorial_revision_reworked_forced_repair_v2.tex` —
  revised version with "deductive surgery" narrative.
- The submission-ready candidate is `RoundX/d3torus_complete_m_ge_3_editorial_revision_v5.tex`.

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

## d=5 frontier (RoundY)

The `RoundY/` directory contains the current `d=5` research frontier.
This case is still open, but the question is now much narrower than a generic
search problem. The theorem-level bridge is now best stated as the abstract
right-congruence object `(beta,rho)`, the strongest checked concrete model is
the dynamic boundary odometer `(beta,q,sigma)` / `(beta,delta)`, and the
remaining gap is whether raw global `(beta,delta)` works on the full
accessible union or only componentwise.

Start with:

- `RoundY/README.md`
- `RoundY/current-frontier-and-approach.md`
- `RoundY/theorem/d5_076_unified_handoff.md`
- `RoundY/theorem/d5_077_globalization_handoff.md`

## Lean formalization checkpoint

The `formal/` tree now contains:

- a complete `d=4` formalization;
- a complete `d=3` even Route E package;
- an active `d=3` odometer rewrite, with `Color2Full`, `Color1FullCaseI`,
  `Color1FullCaseII`, and `Color0FullCaseI` complete, while
  `Color0FullCaseII` is the current frontier;
- the extracted-model / specification scaffolding for `d=5`.

So the live formal scope question is no longer whether the color-1 odometer
rewrite closes. It does. The active `d=3` Lean frontier is now the remaining
upper-lane and dispatcher work in color-0 Case II, while `d=5` Lean remains a
support/specification branch rather than the main research frontier.

## Research progression

See [`RESEARCH_PROGRESSION.md`](RESEARCH_PROGRESSION.md) for a detailed
chronological account of the full research arc, including:

- AI-assisted proof restructuring (orbit tracing → height comparison → finite splice)
- Multi-stage referee feedback loop (6/10 → 8/10)
- d=4 generalization breakthrough
- d=5 reduction from broad search to the current abstract-bridge /
  globalization frontier

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
