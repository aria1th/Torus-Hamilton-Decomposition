# D5 084 Theorem Name Map

This note organizes RoundY theorem notes whose filenames are still useful but
too terse, legacy, or researcher-specific.

Its purpose is:

1. to preserve the historical files without breaking references;
2. to record what each such file actually proves or explains;
3. to identify which later canonical note now subsumes it.

This is an organization note, not a new theorem.

## 1. Canonical theorem chain now in force

For the active D5 odd-`m` theorem chain, the canonical stable notes are:

- `theorem/d5_076_bridge_main.md`
- `theorem/d5_076_realization_trackB.md`
- `theorem/d5_076_concrete_bridge_proof.md`
- `theorem/d5_077_tail_length_and_actual_union.md`
- `theorem/d5_079_exceptional_interface_support.md`
- `theorem/d5_080_no_mixed_delta_reduction.md`
- `theorem/d5_081_regular_union_and_gluing_support.md`
- `theorem/d5_082_exceptional_row_reduction.md`
- `theorem/d5_082_frontier_and_theorem_map.md`
- `theorem/d5_083_gluing_flow_and_final_theorem.md`

If a legacy note below overlaps with these, the canonical note should be cited
first.

## 2. Legacy theorem notes still worth knowing

### 2.1 `d5_070.md`

What it is:

- a chain-first exact-reduction theorem note
- the first clean statement that the exact object should start as a marked
  length-`m` chain, not a cycle

Recommended interpretation:

- historical reduction note
- use together with `theorem/d5_070_exact_reduction_chain_first.md`

Now largely subsumed by:

- `theorem/d5_077_tail_length_and_actual_union.md`
- `theorem/d5_082_frontier_and_theorem_map.md`

### 2.2 `d5_072_r2.md`

What it is:

- the symmetry/asymmetry clarification after the coarse bridge was accepted
- the best early statement that the theorem-side clock is globally normalizable
  while the currently checked admissible/local picture remains asymmetric

Recommended interpretation:

- conceptual note
- useful when explaining why global theorem-side symmetry and admissible/local
  asymmetry can coexist

Now largely subsumed by:

- `theorem/d5_079_exceptional_interface_support.md`
- `theorem/d5_082_frontier_and_theorem_map.md`

### 2.3 `d5_072_r3.md`

What it is:

- the clean conditional realization theorem:
  if the global quotient is deterministic and exact for current `epsilon4`,
  then the short-corner detector and canonical clock descend automatically by
  corner-time

Recommended interpretation:

- realization theorem packaging

Now largely subsumed by:

- `theorem/d5_076_realization_trackB.md`

### 2.4 `d5_073.md`

What it is:

- the updated symmetry note after the decorated-bridge sync
- the statement that the true remaining asymmetry is finite decoration, not the
  clock itself

Recommended interpretation:

- historical symmetry phrasing

Now largely subsumed by:

- `theorem/d5_079_exceptional_interface_support.md`

### 2.5 `d5_073_r1.md`

What it is:

- the obstruction theorem for the naive chain-static decorated bridge
  `(beta,a,b)`
- the point where the project learned that static decoration is exact on each
  chain but not deterministic across splices

Recommended interpretation:

- still mathematically useful
- this is the clean source for why the live bridge had to become
  splice-compatible and dynamic

Now largely subsumed by:

- `theorem/d5_076_bridge_main.md`
- `theorem/d5_079_exceptional_interface_support.md`

### 2.6 `works_063_a.md`, `works_063_b.md`, `works_063_c.md`

What they are:

- early route-split working notes that separate theorem, constructive, and
  negative/rigidity viewpoints

Recommended interpretation:

- historical route-organization notes

Now largely subsumed by:

- `theorem/d5_063_route_organization.md`

### 2.7 `d5_078_rA.md`, `d5_078_rB.md`, `d5_078_rC.md`, `d5_078_rD.md`

What they are:

- the four `078` track notes that stabilized the pre-closure bridge language:
  component structure, endpoint compatibility, larger-modulus regular support,
  and safe theorem packaging

Recommended interpretation:

- use the promoted stable copies instead of the `tmp/` originals

Now promoted as:

- `theorem/d5_078_global_component_structure.md`
- `theorem/d5_078_endpoint_compatibility_criterion.md`
- `theorem/d5_078_large_modulus_regular_union_support.md`
- `theorem/d5_078_safe_theorem_language_review.md`

### 2.8 `d5_even_m_reduction_attempt.md`, `d5_even_m_reduction_note.tex`

What they are:

- the first even-`m` reduction/program notes written after the odd-`m` bridge
  closure;
- the place where the even branch was recentered around parity obstruction,
  formal extension of the odd final proof, and a critical-row finite-splice
  program.

Recommended interpretation:

- use the promoted stable copies instead of the `tmp/` originals

Now promoted as:

- `theorem/d5_even_case_strategy_from_d3.md`
- `theorem/d5_even_m_parity_and_critical_row_program.md`
- `theorem/d5_even_m_parity_and_critical_row_program.tex`

## 3. Helpful descriptive aliases already present

Some older content was already re-promoted under better names:

- `works_063_*` -> `theorem/d5_063_route_organization.md`
- `081/082` tmp line -> `theorem/d5_081_regular_union_and_gluing_support.md`,
  `theorem/d5_082_exceptional_row_reduction.md`
- `076–080` tmp line -> the promoted `076`, `077`, `079`, `080` stable notes
- `078` track notes -> the promoted `078` stable notes above

So in most cases the right action is:

- cite the stable descriptive note;
- mention the legacy file only as provenance if needed.

## 4. Recommended citation policy

When writing new theorem notes:

- cite the canonical stable note first;
- cite the legacy terse note only if it contains a distinct argument that is
  not copied into the stable note;
- avoid using bare researcher-note filenames as primary references when a
  stable note exists.

## 5. Bottom line

The main poorly named but still meaningful theorem notes in RoundY are:

- `d5_070.md`
- `d5_072_r2.md`
- `d5_072_r3.md`
- `d5_073.md`
- `d5_073_r1.md`
- `d5_078_rA.md`
- `d5_078_rB.md`
- `d5_078_rC.md`
- `d5_078_rD.md`
- `d5_even_m_reduction_attempt.md`
- `d5_even_m_reduction_note.tex`
- `works_063_a.md`
- `works_063_b.md`
- `works_063_c.md`

They should now be read through this map and, where possible, through the later
stable replacements listed above.
