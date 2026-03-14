# D5 083 Gluing Flow And Final Theorem

This note explains the `081–082` flow and states the final theorem target in
the smallest honest form.

It is meant to answer:

> what was reduced in `081–082`, and what theorem closes the old frontier?

For the promoted proof that closes the theorem inside the accepted package, see:

- `theorem/d5_083_final_theorem_proof.md`

## 1. Flow of the reduction

The bridge/globalization problem did **not** close all at once. It compressed in
three clear steps.

### Step 1. Globalization became an end-gluing problem

The older bridge question

`rho = rho(delta)?`

was reduced to a tail-length / endpoint question, and then sharpened again to a
no-mixed-status problem:

- if fixed realized `delta` never has both continuing and terminal lifts,
  then tail length is forced;
- if tail length is forced, then `rho` depends only on `delta`;
- if `rho` depends only on `delta`, then raw global `(beta,delta)` is exact.

So the raw theorem became an **end-gluing theorem** on actual lifts.

### Step 2. The regular sector closed

The next reduction proved that every regular realization of every realized
`delta` continues.

So regular cutoff rows cannot launch a new endpoint sheet.

That means:

- the regular sector contributes no mixed-status ambiguity;
- the regular rows are no longer the live frontier;
- the raw globalization theorem cannot fail for a regular reason.

### Step 3. The whole theorem reduced to one exceptional row

Once the regular sector was closed, the full raw theorem became equivalent to
one remaining question:

- does the **exceptional** cutoff row glue into the regular continuing class?

Because the chart-level exceptional continuation is already pinned to

`3m-3 -> 3m-2 -> 3m-1`,

the whole remaining obstruction can now be phrased as:

- is there any hidden second endpoint sheet over `delta = 3m-1`?

That is the current bottleneck.

## 2. What is already accepted

The following should be treated as accepted.

### 2.1 Safe global bridge

The globally safe theorem object is still

`(beta,rho)`.

### 2.2 Componentwise concrete bridge

On each splice-connected accessible component, the concrete bridge

`(beta,delta)`

is accepted.

### 2.3 Chart-level exceptional landing

The chart / chain-label continuation is fixed at

`3 -> (terminal chain of 4) -> 1`,

equivalently

`3m-3 -> 3m-2 -> 3m-1`.

### 2.4 Regular raw continuation

Every regular realization of every realized `delta` continues.

This is the key reason the full theorem now reduces to the exceptional row.

## 3. What remained open at the end of `082`

At the end of the `082` reduction, only one raw-state gluing statement
remained open:

does every actual lift of the exceptional cutoff `3m-3` land in the regular
continuing class through the interface

`3m-2 -> 3m-1`?

That was the final gluing problem.

## 4. Final theorem

The right theorem target is:

### Final Gluing Theorem

For odd `m` in the accepted D5 regime, every actual lift of the exceptional
cutoff row at `delta = 3m-3` continues through

`3m-2 -> 3m-1`

and lies in the regular continuing endpoint class there.

This theorem is now proved inside the accepted `076–082` package by:

- `theorem/d5_083_final_theorem_proof.md`

## 5. Immediate corollaries

If the Final Gluing Theorem is proved, then:

1. there is no mixed-status `delta` on the true accessible union;
2. fixed realized `delta` determines tail length;
3. fixed realized `delta` determines endpoint class;
4. `rho = rho(delta)` globally;
5. raw global `(beta,delta)` is exact.

So this one theorem is exactly the last upgrade from the safe abstract bridge
to the concrete global bridge.

## 6. Equivalent negative formulation

The same target can be phrased as a no-go statement:

### Hidden-Sheet Exclusion

There is no hidden second endpoint sheet over the regular source-`1` start
label

`delta = 3m-1`.

This is equivalent to the Final Gluing Theorem, because the exceptional row is
already known to land at that interface.

## 7. Likely answer before closure

Before the promoted `083` proof, the evidence pointed to a **positive** answer:

> the exceptional actual-lift gluing should exist, so raw global
> `(beta,delta)` should be exact for odd `m` in `d=5`.

That section is retained here because it records the logic that led to the
final proof note.

### 7.1 Computational pattern for the likely answer

The positive pattern is now very specific.

- On the frozen actual range `m=7,9,11`, the all-source realized
  `(beta,delta)` graph already glues to one deterministic cycle.
- On the larger reconstructed chart model `m=13,15,17,19,21`, every cutoff
  label already has many same-`delta` continuing witnesses.
- The exceptional cutoff `3m-3` lands at the common interface
  `3m-2 -> 3m-1`, not at an isolated label.
- At `3m-2`, the regular source-`4` terminal representative is the only
  terminal regular holder, while many other same-`delta` regular holders
  continue.
- At `3m-1`, the regular source-`1` start already sits inside a completely
  continuing regular holder set.
- No competing local event law has survived; the only remaining possible
  obstruction is a hidden second endpoint sheet over `delta = 3m-1`.

So the data are not merely “compatible” with the positive answer. They now say
that the only way the theorem can fail is by one very specific hidden-sheet
mechanism that has not appeared anywhere in the checked small actual range and
has no visible support in the larger reconstructed pattern.

### 7.2 Short proof for the likely answer

The shortest positive proof route, if correct, is:

1. the regular sector is already closed, so no regular cutoff can create a new
   endpoint sheet;
2. by the accepted structural package, every exceptional actual lift reaches
   the same universal raw first-exit target;
3. therefore all exceptional actual lifts share the same immediate post-exit
   branch;
4. the chart-level continuation of that branch is already pinned to
   `3m-3 -> 3m-2 -> 3m-1`;
5. at `3m-2 -> 3m-1`, the landing lies in the regular continuing interface
   class;
6. hence the exceptional cutoff cannot create a second endpoint sheet;
7. therefore there is no mixed-status `delta`, so tail length is determined by
   `delta`, so `rho = rho(delta)`, and raw global `(beta,delta)` is exact.

The only step in that chain that is not yet fully unconditional in the current
bundle is the raw actual-lift identification in steps `3–5`.

### 7.3 Which earlier theorems already answer the proof steps

The positive proof route is short because most of its steps are already covered
by earlier accepted results.

- **Step 1 is already closed by the regular-union theorem.**
  The note `4.1` proves that every regular realization of every realized
  `delta` continues, so regular cutoff rows cannot launch a new endpoint sheet.

- **Step 2 is already supplied by the structural first-exit package.**
  The `062` / `063B` route identifies universal raw first-exit targets for the
  actual active branch. This is the theorem input that removes raw ambiguity at
  the exceptional exit itself.

- **Step 4 is already supplied at chart level.**
  The promoted `079` exceptional-interface support pins the landing to the common interface
  `3m-3 -> 3m-2 -> 3m-1`, i.e. `3 -> (terminal chain of 4) -> 1`.

- **Step 5 is already supplied on the regular side.**
  At `3m-2`, source `4` is the unique terminal regular representative while
  many same-`delta` regular holders continue, and at `3m-1` the source-`1`
  start lies inside a fully continuing regular holder set. This is exactly the
  regular-interface picture extracted in the promoted `079` and `081` notes.

- **Step 7 is already supplied by the end-gluing / no-mixed-delta reduction.**
  Once the exceptional row is shown to glue into the regular continuing class,
  the promoted `080` and `081b/082` reduction immediately promote this to:
  no mixed-status `delta`,
  tail-length determination,
  `rho = rho(delta)`,
  and raw global `(beta,delta)`.

So, after reviewing the closed inputs, the only genuinely unresolved step is:

- **Step 3–5 at raw actual-lift level**, namely proving that the exceptional
  actual lift really enters that already-known regular interface class and does
  not support a hidden second endpoint sheet.

## 8. Best proof routes

There are two realistic proof routes now.

### Route A. Structural / theorem route

Use:

- the universal raw first-exit theorem,
- the actual post-exit branch,
- and the interface identification

to show that every exceptional actual lift shares the same post-exit raw state
or the same endpoint class as the regular interface.

This is the cleanest theorem route.

### Route B. Raw-state certification route

Export or prove enough actual larger-state gluing data to certify directly:

- actual lifts at the exceptional row,
- their successors,
- and their endpoint-class agreement with the regular interface class.

This is the cleanest compute-support route.

## 9. What is no longer the frontier

Do **not** reopen:

- regular-union ambiguity,
- chart-level exceptional landing,
- local event readout,
- general bridge discovery,
- broad controller search.

Those parts are already reduced away.

## 10. Shortest honest summary

The `081–082` flow says:

- end-gluing is the right raw theorem object;
- regular rows are closed;
- the whole globalization theorem is now one exceptional row;
- proving that row upgrades the global bridge from abstract `(beta,rho)` to raw
  `(beta,delta)`.

## 11. Key references

- `theorem/d5_076_bridge_main.md`
- `theorem/d5_076_realization_trackB.md`
- `theorem/d5_076_concrete_bridge_proof.md`
- `theorem/d5_077_tail_length_and_actual_union.md`
- `theorem/d5_079_exceptional_interface_support.md`
- `theorem/d5_080_no_mixed_delta_reduction.md`
- `theorem/d5_081_regular_union_and_gluing_support.md`
- `checks/d5_081_regular_union_endpoint_table.csv`
- `theorem/d5_082_exceptional_row_reduction.md`
- `theorem/d5_082_frontier_and_theorem_map.md`
