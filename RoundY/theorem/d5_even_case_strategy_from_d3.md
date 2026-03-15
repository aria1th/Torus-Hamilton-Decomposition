# D5 Even-m Strategy From The D3 Even Case

This note records the safest current strategy for the unresolved `d=5`,
even-`m` branch by analogy with the solved `d=3`, even-`m` case.

For the theorem-shaped refinement of this strategy, see:

- `theorem/d5_even_m_parity_and_critical_row_program.md`
- `theorem/d5_even_m_parity_and_critical_row_program.tex`
- `theorem/d5_even_m_finite_splice_conditions.md`

That companion note promotes three stronger points:

1. a parity barrier against Kempe-from-canonical in `D_5(m)` for even `m`;
2. a formal extension theorem saying the odd final boundary proof is
   parity-blind once the same upstream package is rebuilt;
3. a critical-row program identifying the likely even analogue of Route E.

## 1. The `d=3` even lesson

The manuscript-level `d=3` even proof is not a direct extension of the odd
affine odometer witness.

Instead, it has the following shape:

1. a parity barrier kills the naive Kempe-from-canonical route;
2. the proof switches to a low-layer repair theorem;
3. after one more first-return reduction, the dynamics become a
   finite-defect / splice version of the same clock-and-carry mechanism.

The important point is methodological:

- after the direct route is obstructed, the right next object is not a broad
  witness search;
- it is a reduced return object with finitely many controlled splice defects.

This is exactly the lesson emphasized in the `d=3` even Route E discussion and
the old Lean-scope decisions: the proof only becomes clean once the
finite-defect / splice layer is abstracted.

## 2. Current `d=5` even status

For `d=5`, even `m`, the current state is much earlier than the odd-`m`
closure.

What is already known:

- the odd-`m` D5 theorem closes through the global bridge
  `(beta,rho)` / raw `(beta,delta)`;
- this is a programmed state-machine theorem, not a fixed witness theorem;
- for the old fixed `26`-move witness, color `0` has an explicit even-`m`
  obstruction:
  invariant families `L_w` produce `m/2`-cycles for every even `m >= 6`;
- the same fixed witness is therefore not the right even-`m` route.

What is not known:

- no accepted even-`m` D5 bridge theorem;
- no even-`m` counterpart of the odd global `(beta,delta)` package;
- no accepted low-layer repair theorem analogous to Route E.

So the even branch should currently be treated as an obstruction-plus-repair
problem, not as a nearly finished extension of the odd proof.

## 3. Strategy options

### Option A. Broad witness search

Search for a fresh even-`m` Hamilton decomposition directly by widening Kempe
or low-layer witness families.

Pros:

- simplest to describe;
- might accidentally find a finite witness for very small even moduli.

Cons:

- repeats the part of the odd D5 program that was most search-heavy;
- ignores the evidence that the old direct route is structurally blocked;
- unlikely to expose the right theorem object.

### Option B. Obstruction first, then repair theorem

Treat the even case the same way `d=3` even was ultimately treated:

1. isolate the obstruction to the naive route;
2. identify a reduced return object;
3. describe the remaining difference from the odd clock as finitely many
   splice/defect packets;
4. only then search for a repair construction.

Pros:

- matches the successful `d=3` even methodology;
- turns the problem into a theorem-shaping problem before reopening search;
- is compatible with the current D5 odd conclusion that the real object is a
  programmed state machine, not a fixed move sequence.

Cons:

- slower at the start;
- may require one extra return reduction before the right section is visible.

### Option C. Defer even `m` completely

Park even `m` until after higher odd-dimension pilot work (`d = 7, 9, ...`).

Pros:

- avoids splitting attention.

Cons:

- loses the chance to reuse the fresh D5 bridge language while it is still
  active;
- risks mixing two different kinds of future work:
  odd-prime generalization and even-case repair.

## 4. Recommendation

Recommend **Option B**.

The `d=3` even case suggests that the right approach is:

- do **not** start with broad even witness search;
- do **not** assume the odd global bridge simply survives parity change;
- first isolate an even-`m` obstruction and a finite-defect / splice repair
  model.

In short:

> Treat `d=5`, even `m`, as a Route-E-style repair problem, not as an odd-case
> globalization problem.

More sharply, the current best theorem target is:

> preserve the bulk boundary odometer, prove the regular source-window splice
> `u -> u-3`, and isolate source `3` as the unique finite splice defect.

## 5. Concrete next steps

The most useful sequence now is:

1. **Obstruction layer**
   Prove or sharpen an even-`m` barrier for the currently natural routes.
   The existing color-`0` invariant-family obstruction is one model for the
   kind of theorem to look for.

2. **Reduced section**
   Find the right even return object.
   It may not be the exact odd boundary union; it may require one further
   return or a lane/transversal reduction as in `d=3` Route E.

3. **Finite-defect model / critical-row extraction**
   On small even moduli (`m = 6, 8, 10, 12`), extract:
   - the bulk clock;
   - the source windows;
   - the defect packets;
   - the splice map between them.

4. **Critical-row repair theorem**
   State the smallest theorem saying that once the regular source-window splice
   is generic and the unique exceptional interface is glued correctly, the
   bulk clock again forces Hamiltonicity.

5. **Only then search for implementations**
   After the splice theorem is visible, search for local rules / witness
   families that realize it.

## 6. What to avoid

- Do not reopen full unrestricted Kempe search on even `m`.
- Do not assume the odd `(beta,delta)` bridge is the correct even theorem
  object without a new reduction.
- Do not begin with Lean or manuscript cleanup for even `m`; the proof object
  is not stable enough yet.

## 7. Bottom line

The best analogy is:

- `d=3` odd: direct odometer;
- `d=3` even: parity obstruction, then finite-defect repair;
- `d=5` odd: bridge/globalization theorem;
- `d=5` even: most likely another finite-defect repair problem.

So the next serious even-`m` question is not
"what new witness works?",
but
"what is the correct even-`m` return object and splice repair theorem?"
