# D5 finite-cover normal form 044: theorem, lemmas, and proof notes

## Status labels

- **[C]** computationally checked on the extracted active branch for `m in {5,7,9,11}`
- **[H]** theorem-shaped extrapolation suggested by the checked data but not yet proved uniformly in `m`
- **[O]** open

## Scope

This note packages the current `044` result into manuscript-style statements for the best-seed unresolved branch

- seed pair `left = [2,2,1]`, `right = [1,4,4]`
- unresolved channel `R1 -> H_L1`
- active-union extraction inherited from `037--044`
- checked moduli `m = 5,7,9,11`

It is intentionally split into two levels:

1. a **checked finite-cover theorem** for the active branch, and
2. **proof notes** for how to turn that checked theorem into a uniform argument later.

This note does **not** claim admissible realization of the carry sheet. That remains open.

## Setup

For a checked modulus `m`, let `A_m` be the extracted active branch for the best-seed unresolved corridor, with induced active transition map `F_m`.

For a state `x in A_m`, define:

- grouped base state
  \[
  B(x) = (s(x),u(x),v(x),\lambda(x),f(x)),
  \]
  where `\lambda = layer` and `f in {regular, exceptional}` is the carried family bit;
- carry sheet
  \[
  c(x) = \mathbf 1_{\{q(x)=m-1\}};
  \]
- first future carry time
  \[
  \tau(x) = \min\{t \ge 0 : c(F_m^t x)=1\};
  \]
- next-carry `u`-coordinate
  \[
  U^+(x) = u(F_m^{\tau(x)}x);
  \]
- binary anticipation sheet
  \[
  d(x)=\mathbf 1_{\{U^+(x)\ge m-3\}}.
  \]

When `c(x)=1`, we have `\tau(x)=0`, so `U^+(x)=u(x)`.

We use the shorthand
\[
B+c = (B,c), \qquad B+c+d = (B,c,d).
\]

## Main theorem package

### Theorem A (checked finite-cover normal form) [C]

For each checked modulus `m in {5,7,9,11}`, the best-seed active branch admits the checked normal form
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
with the following properties.

1. **Exceptional trigger descent.** The exceptional fire predicate is a function of `B`.
2. **Regular trigger descent.** The regular fire predicate is not a function of `B`, but it is a function of `B+c`.
3. **Carry-fiber collapse.** Every `B+c` fiber with `c=1` is a singleton.
4. **Residual-support localization.** Every non-singleton `B+c` fiber lies on the regular noncarry region `f = regular`, `c = 0`.
5. **Binary anticipation coordinatization.** On every non-singleton `B+c` fiber, the minimal deterministic cover class is a function of
   \[
   d = \mathbf 1_{\{U^+\ge m-3\}}.
   \]
6. **Deterministic closure.** The active transition law is deterministic on `B+c+d`.

Equivalently: on the checked active branch, the structural object is a grouped base plus a carry sheet plus a binary anticipation cover.

### Corollary B (checked trigger / structure split) [C]

On the checked active branch:

- the **trigger-level** missing lift is exactly the carry sheet `c = 1_{q=m-1}`;
- the **structure-level** residual lift is the binary anticipation sheet
  \[
  d = \mathbf 1_{\{U^+\ge m-3\}}.
  \]

In particular, `d` is not the next local controller target. It is a theorem-level finite-cover coordinate needed only to make the regular noncarry dynamics deterministic.

## Supporting lemmas

### Lemma 1 (regular vs exceptional trigger descent) [C]

For each checked `m`:

- the exceptional fire predicate is a function of `B`;
- the regular fire predicate is not a function of `B`;
- the regular fire predicate is a function of `B+c`.

#### Proof note

This is the direct content of `carry_target_status_044.json`:

- `exceptional_fire_on_B = true`
- `regular_fire_on_B = false`
- `regular_fire_on_Bc = true`

for `m = 5,7,9,11`.

### Lemma 2 (carry-state singleton and residual support) [C]

For each checked `m`:

- every `B+c` fiber with `c=1` is a singleton;
- every non-singleton `B+c` fiber lies on the regular noncarry support.

#### Proof note

This is the content of `binary_anticipation_sheet_044.json`:

- `carry_states_are_singleton_over_Bc = true`
- `support_is_regular_noncarry_only = true`

for `m = 5,7,9,11`.

### Lemma 3 (future-carry low/high dichotomy) [C]

Let `x` lie in a non-singleton `B+c` fiber. Then the checked future-carry `u`-values satisfy
\[
U^+(x) \in \{0,1,m-3,m-2\},
\]
with the expected degeneracy at `m=5`, where the checked set becomes `\{0,m-2\}`.

Moreover, on each checked non-singleton `B+c` fiber, the two branches split into one **low** future-carry value and one **high** future-carry value, so the threshold bit
\[
\mathbf 1_{\{U^+\ge m-3\}}
\]
produces a binary separation of the fiber.

#### Proof note

The checked support tables in `binary_anticipation_sheet_044.json` show:

- `m=5`: allowed `U^+` values `[0,3]`
- `m=7`: allowed `U^+` values `[0,1,4,5]`
- `m=9`: allowed `U^+` values `[0,1,6,7]`
- `m=11`: allowed `U^+` values `[0,1,8,9]`

The recorded pair counts are always of low/high type:

- `m=7`: `[0,4]`, `[0,5]`, `[1,5]`
- `m=9`: `[0,6]`, `[0,7]`, `[1,7]`
- `m=11`: `[0,8]`, `[0,9]`, `[1,9]`

so the threshold at `m-3` is the natural binary quotient on the checked ambiguous support.

### Lemma 4 (binary anticipation refines the 2-sheet cover) [C]

For each checked `m`, the minimal deterministic cover over `B+c` is binary, and its cover class is a function of
\[
d = \mathbf 1_{\{U^+\ge m-3\}}.
\]

#### Proof note

The binary nature of the residual cover over `B+c` is inherited from `043`.
The new `044` refinement is that `next_carry_coordinatization_044.json` records

- `cover_class_is_function_of_Bc_plus_feature = true`
- `collision_key_count = 0`

for the feature `1_{next carry u >= m-3}` on `m = 5,7,9,11`.

Thus the checked binary feature `d` realizes the checked residual 2-sheet cover.

### Lemma 5 (deterministic closure on `B+c+d`) [C]

For each checked `m`, the induced active transition law is deterministic on `B+c+d`.

#### Proof note

This is the content of `finite_cover_normal_form_044.json`, which records

- `transition_on_Bc_plus_d.is_deterministic = true`
- `nondeterministic_key_count = 0`

for all checked `m`.

## Proof sketch of Theorem A

Fix `m in {5,7,9,11}`.

1. By Lemma 1, the fire predicates descend exactly as claimed:
   exceptional fire to `B`, regular fire to `B+c` but not to `B`.
2. By Lemma 2, every ambiguity over `B+c` is confined to the regular noncarry region, while all carry fibers are already singleton.
3. By Lemma 3, on the ambiguous support the first future-carry `u`-value lies in a low/high pair, so the threshold bit
   \[
   d = \mathbf 1_{\{U^+\ge m-3\}}
   \]
   is a natural binary refinement.
4. By Lemma 4, that refinement exactly matches the checked residual 2-sheet cover over `B+c`.
5. By Lemma 5, adjoining `d` makes the active transition law deterministic.

Therefore the checked active branch factors as
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
with trigger descent and deterministic closure exactly as stated.

## Notes for a future uniform proof

The checked theorem is already manuscript-worthy as a computational normal form, but a uniform proof in `m` still needs symbolic work. The cleanest route looks like this.

### Note 1. Keep the trigger and structural levels separate.

The verified roles are now distinct:

- `c = 1_{q=m-1}` is the exact **trigger-level** lift;
- `d = 1_{U^+\ge m-3}` is the exact **structure-level** residual cover.

This separation should be preserved in any manuscript proof. The next local realization target remains `c`, not `d`.

### Note 2. A uniform proof should be built on the raw odometer model, not on generic cover labels.

The future-carry coordinate is meaningful because the active branch already has an explicit raw odometer / skew-odometer description from `037--040`. A uniform proof should likely proceed by:

1. writing the first future-carry map symbolically on the regular noncarry branch;
2. showing that only two continuation types occur over each ambiguous `B+c` fiber;
3. proving that these two types are exactly separated by the threshold `U^+ \ge m-3`.

### Note 3. The real conjectural upgrade is not “recover raw `q`.”

The checked normal form suggests the right theorem statement is:

> the best-seed D5 active branch is a grouped skew-odometer base with a carry sheet and a binary anticipation cover.

That is cleaner than a raw-coordinate formulation and matches the d3/d4 narrative better.

### Note 4. What still needs proof beyond the checked moduli.

The following statement is strongly supported but still unproved uniformly.

#### Conjectural Theorem C [H]

For every odd modulus `m >= 5` on the best-seed active branch, the same normal form holds:
\[
B \leftarrow B+c \leftarrow B+c+d,
\qquad
c = \mathbf 1_{\{q=m-1\}},
\qquad
d = \mathbf 1_{\{U^+\ge m-3\}}.
\]

To prove this uniformly, it would suffice to establish symbolically that:

1. exceptional fire descends to `B`;
2. regular fire descends to `B+c` but not `B`;
3. all non-singleton `B+c` fibers lie on regular noncarry states;
4. every ambiguous `B+c` fiber has exactly two continuation types;
5. these two types are separated by the next-carry threshold `U^+ \ge m-3`.

### Note 5. What remains open.

- **[O]** admissible realization of the carry sheet `c = 1_{q=m-1}`;
- **[O]** uniform symbolic proof of Theorem A beyond `m = 5,7,9,11`;
- **[O]** any need to realize `d` admissibly (currently not the recommended next local branch).

## Manuscript wording suggestion

A compact paper-level sentence that is faithful to the checked data is:

> On the extracted best-seed active branch for `m=5,7,9,11`, the unresolved D5 dynamics admit a checked finite-cover normal form `B <- B+c <- B+c+d`, where `B=(s,u,v,layer,family)`, `c=1_{q=m-1}` is the exact trigger lift, and `d=1_{next carry u >= m-3}` is a binary anticipation sheet supported only on regular noncarry states. Exceptional fire descends to `B`, regular fire descends to `B+c`, and the active transition law closes deterministically on `B+c+d`.
