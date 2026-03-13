# D5 carry anticipation theorem chain (044–047)

## Status labels

- **[C]** checked computational statement on the extracted active best-seed branch for `m in {5,7,9,11}`
- **[H]** theorem-shaped extrapolation suggested by the checked data but not yet proved uniformly in `m`
- **[O]** open

## Scope

This note packages the current post-`044` carry results into a proof-oriented sequence for the best-seed unresolved branch

- seed pair `L=[2,2,1]`, `R=[1,4,4]`
- unresolved channel `R1 -> H_L1`
- checked active branch extracted in `042–047`
- checked moduli `m = 5,7,9,11`

The goal here is **proof organization**, not a new search. The statements below are written so they can be inserted into a manuscript once the surrounding notation is fixed.

## Fixed notation

Let `A_m` be the checked active best-seed branch for a fixed checked modulus `m`.
Let `F_m : A_m -> A_m` be the induced active transition map.
For `x in A_m`, define:

- grouped base state
  \[
  B(x)=(s(x),u(x),v(x),\lambda(x),f(x)),
  \]
  where `\lambda = layer` and `f in {regular, exceptional}` is the carried family tag;
- carry sheet
  \[
  c(x)=\mathbf 1_{\{q(x)=m-1\}};
  \]
- next-carry time
  \[
  \tau_c(x)=\min\{t\ge 0 : c(F_m^t x)=1\};
  \]
- next-carry `u`-coordinate
  \[
  U^+(x)=u(F_m^{\tau_c(x)}x);
  \]
- binary anticipation sheet
  \[
  d(x)=\mathbf 1_{\{U^+(x)\ge m-3\}}.
  \]

For grouped future transitions, write `dn_t(x)` for the grouped-delta event at time `t` along the active orbit, and let
\[
\delta_{\mathrm{flat}}=(0,0,0,1).
\]
Define the initial flat-run length
\[
\tau(x)=\min\{t\ge 0 : dn_t(x)\neq \delta_{\mathrm{flat}}\}.
\]
Let `epsilon4(x)` be the current `4`-class grouped-delta event label
\[
\epsilon_4(x)\in\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]

Thus `\tau` is the time-to-first-nonflat grouped-delta event, while `\tau_c` is the time-to-next-carry in the raw carry sheet.

## Main checked theorem

### Theorem A (checked finite-sheet anticipation normal form) [C]

For each checked modulus `m in {5,7,9,11}`, the active best-seed branch admits the checked finite-sheet normal form
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
with the following properties.

1. **Exceptional trigger descent.** The exceptional fire predicate is a function of `B`.
2. **Regular trigger descent.** The regular fire predicate is not a function of `B`, but it is a function of `B+c`.
3. **Carry-fiber collapse.** Every `(B+c)`-fiber with `c=1` is a singleton.
4. **Residual-support localization.** Every non-singleton `(B+c)`-fiber lies on the regular noncarry region.
5. **Binary anticipation coordinatization.** The residual deterministic cover over `B+c` is binary and is realized by
   \[
   d=\mathbf 1_{\{U^+\ge m-3\}}.
   \]
6. **Deterministic closure.** The active transition law is deterministic on `B+c+d`.

Moreover, the carry sheet `c` is not a function of the current grouped base `B`, and on the checked branch it is best read as a one-sided anticipation datum over the grouped dynamics rather than as a current grouped-state observable.

### Proof note

Items (1)–(6) are the direct checked content of `042` and `044`:

- `analysis_summary.json` and `carry_slice_trigger_validation_042.json` from `042`
- `analysis_summary.json`, `finite_cover_normal_form_044.json`, `next_carry_coordinatization_044.json`, and `binary_anticipation_sheet_044.json` from `044`

The final sentence uses two ingredients:

- `042` shows `c` is not a function of the current grouped base `B`;
- `046–047` show that `c` is an exact function of a one-sided future grouped-transition sheet.

So the checked structural reading is: grouped base + carry anticipation sheet + binary anticipation cover.

## Support theorem 1: first carry no-go

### Proposition B (first carry-only admissibility no-go) [C]

On the checked active branch, no observable from the first admissible current-edge / short-transition / low-cardinality gauge catalogs realizes the carry sheet `c` exactly. In particular, no exact candidate is found among the checked families built from

- current grouped base `B`,
- one-step grouped transition `B -> B_next`,
- two-step grouped transition `B -> B_next -> B_next2`,
- the first core edge/transition carry catalogs,
- the first low-cardinality anchored gauge-transition catalogs,
- the first targeted point-defect catalogs.

### Proof note

This is exactly the recorded content of `045`:

- `analysis_summary.json`
- `carry_realization_search_summary_045.json`
- `admissibility_obstruction_045.json`
- `exact_obstruction_summary_045.json`

The summary records `0` exact carry realizations across `69,994` tested candidates and explicitly marks the named negative families `B_only`, `B_next`, and `B_next_next2` as false.

### Corollary B.1 (checked local obstruction after 045) [C]

After the first admissible current-edge and short-transition scan, the next local target is not a nearby current observable. The carry sheet must be sought either in a broader lifted gauge or in a deeper one-sided transition sheet.

## Support theorem 2: deep future carry-sheet

### Proposition C (carry as an exact future grouped-transition event) [C]

For each checked modulus `m in {5,7,9,11}`, the carry sheet `c` is already an exact future grouped-transition event on the active grouped base.

More precisely:

1. the minimal exact future grouped-delta horizon is
   \[
   m-3;
   \]
2. the minimal exact future grouped-state horizon is
   \[
   m-2;
   \]
3. the exact future signature can be compressed to
   \[
   B + \tau + \eta,
   \]
   where `\tau` is the initial flat-run length for `dn=(0,0,0,1)` and `\eta` is the first nonflat grouped-delta event after that run.

### Proof note

This is the direct checked content of `046`:

- `analysis_summary.json`
- `minimal_future_horizons.json`
- `first_nonflat_signature_summary.json`
- `failure_at_H_minus_1_tables.json`

The summary records the horizon pattern
\[
2,4,6,8 = m-3
\]
for grouped-delta windows and
\[
3,5,7,9 = m-2
\]
for grouped-state windows on `m = 5,7,9,11`.

### Corollary C.1 (carry sheet is already an anticipation event) [C]

On the checked active branch, the carry sheet is not merely a hidden current bit. It is exactly encoded by the first nonflat future event in the grouped dynamics.

## Support theorem 3: exact checked-range coding

### Proposition D (boundary sharpening and exact checked-range coding) [C]

On the checked active branch for `m=5,7,9,11`, the future signature of Proposition C sharpens as follows.

1. Every ambiguity in `B+tau` lies at the boundary `tau=0`.
2. The `tau=0` boundary class is genuinely `3`-class minimal, with current grouped-delta partition
   \[
   \{\mathrm{wrap},\ \mathrm{carry\_jump},\ \mathrm{other}\}.
   \]
3. The first exact checked-range quotient is
   \[
   B + \min(\tau,8) + \epsilon_4.
   \]
4. Equivalently, the first exact checked-range transition-sheet coding is
   \[
   B + \epsilon_4(\text{current}) + \text{next 7 future flat/nonflat bits after the current step}.
   \]
5. No smaller checked-range tau truncation or threshold quotient survives on `m=5,7,9,11`.

### Proof note

This is the direct checked content of `047`:

- `analysis_summary.json`
- `quotient_exactness_summary.json`
- `representative_ambiguous_rows.json`
- `representative_exact_rows.json`

The summary records:

- all `B+tau` ambiguity occurs at `tau=0`;
- the boundary partition is genuinely `3`-class minimal;
- the first exact checked-range quotient is `B + min(tau,8) + epsilon4`;
- the first exact checked-range transition-sheet coding is `B + epsilon4 + future_binary_after_current_window_length_7`.

### Corollary D.1 (tau is the live hidden datum; epsilon4 is boundary correction) [C]

On the checked active branch, the live hidden datum for the carry sheet is `tau`, while `epsilon4` enters only as a boundary correction at `tau=0`.

## Combined theorem-shaped reading

### Corollary E (checked carry-anticipation formulation) [C]

Combining Theorem A with Propositions B–D, the carry mechanism on the checked active best-seed branch is best read in the following way:

1. the structural object is the finite-sheet normal form
   \[
   B \leftarrow B+c \leftarrow B+c+d;
   \]
2. the first residual trigger-level lift is the carry sheet `c`;
3. the carry sheet is not available in the first admissible current/short-transition catalogs;
4. the carry sheet is, however, an exact one-sided anticipation datum on the grouped base;
5. on the checked range, that anticipation datum is exactly coded by
   \[
   B + \min(\tau,8) + \epsilon_4,
   \]
   equivalently by current `B`, current `epsilon4`, and the next `7` future flat/nonflat bits.

This is the cleanest checked bridge from the search branch to the proof branch.

## Proof organization for a manuscript

A clean manuscript order is:

1. **Finite-sheet normal form theorem** (`042` + `044`):
   \[
   B \leftarrow B+c \leftarrow B+c+d.
   \]
2. **Negative admissibility proposition** (`045`):
   no first current-edge / short-transition / low-cardinality gauge family realizes `c`.
3. **Carry anticipation proposition** (`046`):
   `c` is the first exact future grouped-transition event.
4. **Boundary sharpening proposition** (`047`):
   the live hidden datum is `tau`, with `epsilon4` only a boundary correction.
5. **Open theorem-level target**:
   admissibly realize the anticipation datum coding `c`.

This order keeps the distinction clear:

- `d` belongs to the structural finite cover;
- `c` belongs to the trigger-level missing lift;
- `tau` is the theorem-friendly anticipation coordinate underlying `c`.

## Open theorem statements

### Conjectural Theorem F (uniform anticipation normal form) [H]

For every odd modulus `m >= 5` on the best-seed active branch, the checked normal form persists:
\[
B \leftarrow B+c \leftarrow B+c+d,
\qquad
c = \mathbf 1_{\{q=m-1\}},
\qquad
d = \mathbf 1_{\{U^+\ge m-3\}}.
\]
Moreover, the carry sheet is a one-sided anticipation datum on the grouped base.

### Conjectural Theorem G (uniform carry-event coding) [H]

There is a symbolic description of the grouped-delta future on the active branch such that:

1. `c` is determined by the first nonflat future grouped-delta event;
2. the exact horizon is `m-3` in grouped-delta time and `m-2` in grouped-state time;
3. the only boundary ambiguity occurs at `tau=0` and is resolved by the `3`-class current event partition
   \[
   \{\mathrm{wrap},\ \mathrm{carry\_jump},\ \mathrm{other}\}.
   \]

These are the natural theorem-level upgrades of `046–047`.

## What remains open [O]

1. Prove Theorems F and G uniformly in odd `m`.
2. Find an admissible coding of the carry sheet `c` or of the equivalent anticipation datum `(tau, epsilon4)`.
3. Integrate that admissible coding with the checked controller logic to close the local branch.
4. After that, fold the whole package into the d3/d4/d5 odometer narrative.
