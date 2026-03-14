# D5 083 Final Theorem Proof

This note promotes the strongest `083` proof from `tmp/` into the stable
RoundY theorem chain.

Its role is narrow:

1. prove the final exceptional-row gluing theorem **within the accepted
   `076–082` package**;
2. make explicit which imported earlier theorems are being used;
3. separate the now-closed in-package D5 theorem from the smaller remaining
   task of auditing imported dependencies before broader generalization.

## Scope

This note proves the final theorem targeted in
`theorem/d5_083_gluing_flow_and_final_theorem.md`, relative to the accepted
structural package already imported by the `083` bundle.

Concretely, it uses as accepted inputs:

1. the componentwise concrete bridge and odometer splice law
   `delta -> delta+1`;
2. the `077` tail-length reduction:
   at fixed realized `delta`, the only possible ambiguity is remaining
   full-chain tail length;
3. the `081` regular-union theorem:
   every regular realization of every realized `delta` continues;
4. the `079` chart/interface theorem:
   the exceptional continuation is pinned in chain labels to
   `3m-3 -> 3m-2 -> 3m-1`;
5. the structural `062` first-exit theorem:
   on the actual active branch, the candidate orbit equals the true orbit up to
   first exit, and the exceptional family exits at the universal raw target
   `T_exc = (m-2,m-1,1)` by direction `1`.

The only upstream dependency not re-proved here is the explicit `H_{L1}`
trigger formula, now isolated at
`theorem/d5_033_explicit_trigger_family.md`,
which is exactly the accepted dependency already named by `062`.

## Executive theorem

### Theorem A

For odd `m` in the accepted D5 regime, every actual lift of the exceptional
cutoff row `delta = 3m-3` continues through

`3m-2 -> 3m-1`

and lies in the regular continuing endpoint class there.

Consequently:

1. there is no mixed-status realized `delta`;
2. fixed realized `delta` determines tail length;
3. fixed realized `delta` determines endpoint class / future word;
4. `rho = rho(delta)` globally;
5. raw global `(beta,delta)` is exact.

## Proof

The accepted `077` reduction says that, once the concrete bridge `(beta,delta)`
is in place componentwise, two realizations of the same `delta` can differ only
by remaining full-chain tail length.

So to prove the final theorem it is enough to show that every actual accessible
realization has infinite forward tail. If every realization has tail length
`infty`, then equal `delta` automatically gives equal tail length, hence equal
endpoint class / future word. In particular, the exceptional interface
realization at `3m-1` and the regular source-`1` start realization at the same
label must be in the same endpoint class.

The proof therefore splits into totality.

### 1. Every regular full chain has a forward successor

This is exactly the promoted `081` regular-union theorem: every regular
realization of every realized `delta` continues on the true larger regular
accessible union. So no regular full chain is terminal.

### 2. Every exceptional full chain before the cutoff has a forward successor

Inside the exceptional source-`3` chart, all nonterminal exceptional chains are
interior chart occurrences. Therefore they continue internally by the accepted
componentwise odometer splice law `delta -> delta+1`.

So the only exceptional chain that still needs work is the terminal
exceptional cutoff chain at `delta = 3m-3`.

### 3. The exceptional cutoff chain has a forward successor

By the accepted `062` first-exit theorem, on the actual active branch:

- the true orbit agrees with the candidate orbit up to first `H_{L1}` exit;
- for the exceptional family, the first exit is always the universal raw target
  `T_exc = (m-2,m-1,1)`;
- the exit direction is always `1`.

Therefore every actual lift of the exceptional cutoff reaches the same raw exit
state and leaves it in the same branch direction. By determinism of the raw
system, every such actual lift has the same immediate post-exit continuation.

The accepted `079` interface theorem pins the corresponding chain-label
continuation to

`3m-3 -> 3m-2 -> 3m-1`.

Therefore every actual lift of the exceptional cutoff has an actual forward
successor, and its next two full-chain labels are forced to be `3m-2`, then
`3m-1`. So the exceptional cutoff chain is not terminal.

### 4. Hence every accessible component is total

Take any accessible full chain `C`.

- If `C` is regular, Section 1 gives a forward successor.
- If `C` is exceptional but not the cutoff chain, Section 2 gives a forward
  successor.
- If `C` is the exceptional cutoff chain, Section 3 gives a forward successor.

Thus every accessible full chain has an accessible forward successor.

Now suppose some splice-connected accessible component were finite. Then its
realized boundary image would be a finite forward orbit segment in `Z/m^2 Z`,
so it would have a right-end chain with no forward successor. But no accessible
full chain is terminal. Contradiction.

Hence every splice-connected accessible component is total.

### 5. Global tail-length constancy and the raw global bridge

Since every accessible component is total, every realized state has remaining
full-chain tail length `infty`.

By the accepted `077` tail-length reduction, fixed realized `delta` can differ
only by tail length. Therefore fixed realized `delta` has realization-
independent tail length, namely `infty`.

Hence fixed realized `delta` determines:

- the endpoint class,
- the padded future current-event word,
- and therefore the abstract right-congruence class `rho`.

So `rho = rho(delta)` globally, and therefore raw global `(beta,delta)` is
exact.

This also rules out mixed-status `delta`: a mixed-status row would give at
least one finite tail and at least one infinite tail at the same realized
label, contradicting the previous paragraph.

### 6. Recovering the exact exceptional gluing statement

Let `E_+` be the exceptional realization at `delta = 3m-1` reached from the
cutoff row, and let `R_+` be the regular source-`1` start realization at the
same label.

By Section 3, `E_+` exists and is reached through

`3m-3 -> 3m-2 -> 3m-1`.

By Sections 4 and 5, both `E_+` and `R_+` have infinite remaining tail length.
By the accepted `077` reduction, equal realized `delta` and equal tail length
force the same endpoint class / future word.

Therefore `E_+` and `R_+` lie in the same endpoint class. Pulling back one full
chain gives the same conclusion at `3m-2`.

So every actual lift of the exceptional cutoff row glues into the regular
continuing endpoint class through the interface `3m-2 -> 3m-1`.

## Honest dependency statement

This note closes D5 odd-`m` **within the accepted `083` package**.

What it really uses is:

- the promoted regular-union theorem;
- the promoted chart/interface theorem;
- the promoted `077` tail-length reduction;
- the accepted structural `062` universal first-exit theorem.

If one wants to expose every upstream dependency, then the only extra clause is
that `062` itself depends on the promoted trigger-family theorem
`theorem/d5_033_explicit_trigger_family.md`. That is not a new gap in the
gluing proof; it is simply the accepted structural input already named by the
`082/083` frontier notes.

## Conclusion

The correct final verdict is:

> Within the accepted `076–082` theorem package, the Final Gluing Theorem is
> proved, and raw global `(beta,delta)` follows.

The next task is therefore not a new D5 bottleneck but a dependency audit:
decide which imported accepted theorems should be re-packaged or rechecked
before treating the odd-`m` D5 theorem as fully ready for wider
generalization.
