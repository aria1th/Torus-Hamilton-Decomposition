# D5 101: Evidence map for the remaining graph-theoretic theorem gaps

## Abstract

The conditional rewrite in `tmp/d5_100_graph_theoretic_hamilton_decomposition_proof_draft_conditional.tex`
replaces the original `Sorry.` blocks by honest theorem-level implications.

What remains external is now sharp:

1. a theorem-level channel classification reducing the full odd-`m`, `d=5`
   problem to the best-seed channel;
2. a concrete graph witness descent package from local D5 representatives to
   torus arcs;
3. a graph return-cycle lift package upgrading the boundary odometer to one
   full-torus orbit of length `m^5`;
4. internalization or stable theorem-level citation of Inputs A--E from `099`.

This note records the current best evidence and observation data for those four
packages, so the next manuscript work can target the right missing theorem
objects rather than reopening broad search.

## 1. Scope

The present note is not itself a new proof of the graph-theoretic Hamilton
decomposition theorem. Its purpose is narrower:

- isolate what is already strongly supported by the current RoundY artifacts;
- state which parts are theorem-level versus compute-only;
- identify the smallest honest remaining packaging gap in each external input.

The relevant manuscript endpoint is the conditional rewrite

- `tmp/d5_100_graph_theoretic_hamilton_decomposition_proof_draft_conditional.tex`

and the current downstream globalization theorem package is

- `theorem/d5_099_one_pass_odd_m_globalization_package.md`.

## 2. Channel classification theorem

### 2.1 Target theorem

The graph-theoretic draft still needs a theorem of the form:

> every odd-`m`, `d=5` instance is either already closed by an earlier channel
> theorem, or reduces to the best-seed channel `R1 -> H_L1`.

The abstract reduction argument is already written in conditional form in
`tmp/d5_100_graph_theoretic_hamilton_decomposition_proof_draft_conditional.tex`.
What is missing is the theorem-level packaging of the channel classification
itself.

### 2.2 Current strongest evidence

The sharpest current evidence comes from the promoted `033` trigger-family note
and the underlying defect-splice artifact:

- `theorem/d5_033_explicit_trigger_family.md`
- `artifacts/d5_defect_splice_transducer_033/data/analysis_summary.json`
- `artifacts/d5_defect_splice_transducer_033/data/best_seed_defect_templates.json`

The artifact summary records the following theorem-shaped observations on the
pilot moduli `m = 5,7,9`:

1. the direct repair result is stable:
   `L3`, `R2`, and `R3` repair directly;
2. only the `R1` channel remains unresolved;
3. the unresolved hole family is exactly `H_L1`;
4. on the extracted unary splice corridor, even the shortest
   `R1 -> H_L1` splice already forces large controller size:
   the recorded lower bounds are `50` at `m=5`, `196` at `m=7`, and `486`
   at `m=9`.

The promoted theorem note `033` already freezes the exact downstream theorem
content used later:

> for the unresolved best-seed channel `R1 -> H_L1`, the target hole family is
> exactly `H_L1 = {(q,w,u,layer) = (m-1,m-1,u,2) : u != 2}`.

So the current evidence is not vague frontier prose. It already singles out the
same best-seed channel and same hole family in both theorem prose and saved
pilot data.

### 2.3 What is still missing

What is still missing is not more pilot evidence that `R1 -> H_L1` is the live
channel. The missing item is a stable theorem statement that promotes:

- "only `R1` remains unresolved after the defect-template quotient"

from artifact / frontier language to a theorem-level reduction theorem with an
explicit quantifier in `m`.

So this gap is primarily theorem packaging, not lack of data.

## 3. Concrete graph witness descent package

### 3.1 Target package

The conditional rewrite isolates the exact graph-level object needed in Section
4:

- a representative space `R`,
- a projection `pi : R -> V`,
- an exact invariant `I`,
- local selected outgoing torus arcs `a_i(r)`,
- and uniqueness of incoming color-`i` arcs.

In the intended D5 use, the invariant should be the globalization invariant
`I = (beta,rho)`, equivalently `I = (beta,delta)` after the raw globalization
theorem from `099`.

### 3.2 Current theorem support

There is already strong support on the invariant side.

1. `theorem/d5_099_one_pass_odd_m_globalization_package.md` proves raw global
   `(beta,delta)` exactness on the true accessible boundary union inside the
   accepted best-seed package.
2. `theorem/d5_076_concrete_bridge_proof.md` supplies the componentwise
   concrete bridge:
   - intrinsic boundary digit `delta = q + m sigma`,
   - splice law `delta -> delta + 1`,
   - current event `epsilon4` as a function of `(beta,delta)`,
   - realized boundary image as a forward interval or the full odometer.
3. `theorem/d5_068_realization.md` already isolates the exact general descent
   object:
   the lifted realization `R_m` over the visible quotient, together with the
   criterion that descent means the phase fiber over each visible state is a
   singleton.

So the theorem-side issue is no longer whether there exists an exact invariant.
It is whether that invariant is enough to define graph-level outgoing arc
selectors and prove incoming uniqueness.

### 3.3 Current observation data

The best compute support here is:

- `artifacts/d5_exact_reduction_support_068b/data/analysis_summary.json`
- `artifacts/d5_exact_reduction_support_068b/data/accessible_quotient_on_chain.json`
- `artifacts/d5_exact_reduction_support_068b/data/beta_exactness_extension.json`
- `artifacts/d5_exact_reduction_support_068b/data/branch_support_extension.json`
- `artifacts/d5_exact_reduction_support_068b/data/marked_chain_validation.json`

The summary records:

- exhaustive full-row exactness on `m = 13,15,17,19,21`;
- larger branch-local support on `m = 31,33,35,37,39,41`;
- exact unit drift of the canonical clock `beta`;
- exact readout of `q`, `c`, `epsilon4`, `tau`, `next_tau`, and `next_B`
  from `(B,beta)` on the checked full-row range.

The most useful structural observation inside
`accessible_quotient_on_chain.json` is:

- the smaller candidate quotients `next_dn` and `dn_plus_next_dn` fail
  deterministic successor exactness on every checked full-row modulus;
- the marked chain candidates `B`, `B_next`, and `B_next2` succeed, each with
  deterministic successor exactness and exact carry readout;
- their verified chain size is exactly `m` on the checked range.

This is already very close to the right graph-descent heuristic:

> if one wants a graph-level selector package, the visible representative space
> is probably not a tiny one-step quotient. The smallest stable deterministic
> object already looks like a marked length-`m` chain.

### 3.4 What is still missing

The missing theorem is therefore very specific. One still needs to write down:

1. the actual representative space `R`;
2. the projection `pi : R -> V`;
3. the five local selected arcs `a_i(r)`;
4. the theorem that these local arcs depend only on the invariant
   `(beta,delta)`;
5. the theorem that each color has exactly one incoming selected arc at each
   torus vertex.

That is a graph packaging gap, not an invariant-exactness gap.

## 4. Graph return-cycle lift package

### 4.1 Target package

The conditional rewrite isolates a clean Hamiltonicity package:

- choose a section `S_i` for each color factor `F_i`;
- prove every `F_i`-orbit returns to `S_i`;
- prove consecutive returns are exactly `m^3` steps apart;
- identify the first-return map on `S_i` with the full odometer
  `delta -> delta + 1` on `Z/m^2 Z`;
- prove each return segment has `m^3` distinct vertices.

Once those hold, the return-cycle criterion from the conditional rewrite gives a
Hamilton cycle of length `m^5`.

### 4.2 Current theorem support

There is already strong odometer support in lower-dimensional or reduced forms.

1. `tmp/d5_100_graph_theoretic_hamilton_decomposition_proof_draft_conditional.tex`
   contains the general return-cycle criterion:
   first-return single cycle plus exact return spacing implies one full cycle.
2. `RoundY/d5_color3_skew_product_note_v1.md` gives a genuine D5 graph-level
   precedent:
   first-return reduction, section return, monodromy criterion, and lift back
   to a Hamilton cycle for color `3`.
3. `theorem/d5_beta_clock_realization_lifted_phase_20260313_067.md` proves that
   on the exact lifted active corridor the canonical clock is already
   `beta = -Theta`, so the phase itself is no longer conjectural.

So there is already a manuscript pattern for:

- return-section reduction,
- exact odometer on the section,
- and lift back to a full graph cycle.

What remains is to supply the D5 best-seed full-torus version.

### 4.3 Current observation data

The best observation data comes from two earlier artifacts.

#### (a) Reduced grouped-return odometer

Artifact:

- `artifacts/d5_mixed_skew_odometer_normal_form_018/data/analysis_summary.json`
- `artifacts/d5_mixed_skew_odometer_normal_form_018/data/saved_vs_direct_comparison.json`
- `artifacts/d5_mixed_skew_odometer_normal_form_018/data/control_comparison.json`

Verified observations:

1. on saved tables `m = 5,7,9,11,13`, the reduced grouped return is exactly
   the odometer `s -> s + 1`;
2. the same formulas persist under direct replay for `m = 15,17,19`;
3. the grouped cocycle is exactly
   `phi(s) = 2 + 1_{s=1} - 2*1_{s=2} - 1_{s=3}`;
4. after gauge change it becomes the one-defect cocycle `-2*1_{s=2}`;
5. the control witnesses `cycle_007` and `anti_mixed_010` do not collapse to
   the same `s`-only grouped model.

This does not yet prove the full graph return-cycle lift, but it is strong
evidence that the active D5 dynamics already sit on a rigid odometer-type base
rather than on a chaotic multi-parameter return object.

#### (b) Raw lifted corridor odometer

Artifact:

- `artifacts/d5_lifted_corridor_carrier_target_037/data/analysis_summary.json`
- `artifacts/d5_lifted_corridor_carrier_target_037/data/raw_visibility_summary.json`
- `artifacts/d5_lifted_corridor_carrier_target_037/data/carrier_target_summary.json`

Verified observations on `m = 5,7,9,11`:

1. the lifted corridor state is already visible on raw current coordinates;
2. the raw triple `(q,w,layer)` follows an exact odometer rule;
3. the raw odometer coordinate `chi` increments by one on every traced step;
4. the regular and exceptional first exits occur at universal target phases;
5. the target gap matches the expected formula on every checked modulus.

Again, this is not yet the full graph return-cycle theorem. But it is direct
evidence that the corridor lift already behaves like an exact odometer with
uniform return targets.

### 4.4 What is still missing

The remaining graph lift package is now very sharp:

1. define the full-torus section `S_i`;
2. identify the `m^3` return spacing;
3. prove that the boundary odometer `delta -> delta+1` is the actual first
   return on that section;
4. prove that return segments are simple and therefore contribute `m^3`
   distinct vertices.

So the remaining work is not "find another odometer." It is "lift the existing
odometer to the full torus and control the return geometry."

## 5. Inputs A--E: internalization and stable citation status

The one-pass globalization note `099` keeps five inputs explicit. Their current
best status is as follows.

| Input | Current best stable source | Current status |
|---|---|---|
| A. exact trigger family for `H_L1` | `theorem/d5_033_explicit_trigger_family.md` plus artifact `033` | Stable theorem citation already exists. First-principles defect-template rebuild is still external. |
| B. coarse patch facts used before first exit | `theorem/d5_098_compact_cleanup_033_062_structural_block.md` together with `theorem/d5_first_exit_target_proof_062.md` | Mostly internalized in the compact structural block. The remaining externality is small and theorem-shaped. |
| C. componentwise concrete bridge | `theorem/d5_076_concrete_bridge_proof.md` plus artifact `068B` support | Stable theorem citation exists, with strong checked data on full rows and larger branch slices. |
| D. regular chart and endpoint support | `theorem/d5_095_compact_reproof_079_chart_interface_landing.md`, `theorem/d5_096_compact_reproof_081_regular_closure.md`, `checks/d5_077_compact_interval_summary.json`, `checks/d5_081_regular_union_endpoint_table.csv` | The regular-side support is already close to manuscript order. Remaining issue is theorem packaging, not lack of checked data. |
| E. exceptional source-`3` interior continuation | currently spread across `076` componentwise splice law, `092`, and `099` | This is the least cleanly isolated input. It likely wants one short standalone lemma promoted from the existing chart/interior continuation argument. |

The practical conclusion is:

- A, C, and most of D already have stable theorem-level homes;
- B is largely absorbed by `098`;
- E is the one input that still wants the most explicit standalone theorem
  statement if `099` is to become manuscript-order self-contained.

## 6. Recommended next steps

The current data suggest the following order.

1. Write the theorem-level channel classification note:
   package "only the best-seed channel remains" as a stable theorem, citing the
   `033` pilot artifact honestly.
2. Write the graph witness descent note:
   define representatives, projection, local arc selectors, and incoming
   uniqueness, using `(beta,delta)` as the exact invariant.
3. Write the graph return-cycle lift note:
   define the full-torus section `S_i`, prove exact return spacing, and identify
   the section return with the odometer.
4. Add one short standalone lemma for Input E:
   exceptional interior source-`3` continuation before the cutoff.

That order matches the current evidence base: the invariant side is already
strong, the odometer side is already strongly observed, and the real remaining
burden is theorem packaging at graph level.
