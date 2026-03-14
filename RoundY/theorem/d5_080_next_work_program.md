# D5 080 Next Work Program

This note explains the current D5 work program after the accepted `079`
frontier note and the `080` follow-up reductions.

It is meant to answer one practical question:

> what should we work on next, and in what order?

## 1. Global context

The broader composite-dimension reduction is already in place:

- `d=2` is closed in `RoundComposite/`;
- `d=3` and `d=4` are already closed elsewhere in the repo;
- therefore every dimension built only from prime factors `2` and `3` is
  already closed by product reduction.

So the current low-dimensional bottleneck is genuinely on the unresolved prime
side, especially `d=5`.

That means D5 should now be treated as a high-leverage prime input to the
broader program, not as one branch among many equally open directions.

## 2. Accepted current state

The following should now be treated as accepted working context.

### 2.1 Safe theorem object

The safest global bridge is still

`(beta,rho)`.

This remains the correct theorem object for a globally unconditional statement.

### 2.2 Strongest concrete model

The strongest accepted concrete model is componentwise

`(beta,delta)`,

equivalently `(beta,q,sigma)` with `delta = q + m sigma`.

Accepted componentwise package:

- uniform splice law,
- uniform current-event readout,
- boundary image is a `+1` orbit segment in `Z/m^2 Z`.

### 2.3 What `079` changed

The exceptional splice is no longer the main live gap.

At chart / chain-label level it is now pinned to the interface

`3 -> (terminal chain of 4) -> 1`.

So the open problem is no longer “find the bridge” or “locate the exceptional
splice.” The open problem is globalization.

## 3. The sharpened `080` target

After `080`, the best next target is slightly smaller than the old critical
lemma.

### Old critical lemma

If two realized states have the same `delta`, then they have the same remaining
full-chain tail length.

### Better target from `080`

**No-mixed-delta lemma.**

For every realized `delta` on the true accessible union, either:

- every realization of `delta` continues, or
- every realization of `delta` is terminal.

This is enough because if two realizations of the same `delta` had different
tail lengths, then following them forward until the first divergence would
produce a later realized `delta'` with mixed continuation status.

So:

- no mixed-status `delta`
- implies same tail length
- implies `rho = rho(delta)`
- implies raw global `(beta,delta)` is exact.

This is now the best single theorem target.

## 4. Recommended proof split

The cleanest work split now is:

### 4.1 Regular-union lemma

Prove that on the true larger regular accessible union, fixed realized `delta`
has realization-independent continuation status.

This is the main structural theorem target.

Equivalent safe formulations:

- no mixed-status `delta` on the regular union;
- all regular realizations of a fixed `delta` have the same endpoint class;
- the regular union contributes no new tail-length ambiguity.

### 4.2 Exceptional-interface gluing

Prove that the exceptional realization glues into the same class at the shared
interface

`3m-2 -> 3m-1`.

After `079`, this is much smaller than before. The issue is no longer where the
exceptional branch lands, but whether its landing lies in the same endpoint
class as the regular one at that interface.

### 4.3 Global upgrade

Once the regular-union lemma and the exceptional-interface gluing are both
proved, the bridge upgrades immediately:

- `rho = rho(delta)` globally;
- raw global `(beta,delta)` is exact.

## 5. Best finite proof object

The most useful finite proof object suggested by `080` is an **end-gluing
table**.

The idea is:

- interior continuing occurrences cannot create a new endpoint class;
- so only noncontinuing chart occurrences can possibly create a new
  globalization obstruction.

That means we do not need a full table over all `delta` unless this compressed
approach fails.

### End-gluing table rows

1. one row for each regular terminal label

`e_u = m(u-1)-2`

2. one exceptional row at

`3m-3`

### What each row must show

For each row, identify:

- a same-`delta` continuing witness,
- and evidence that the terminal occurrence and the continuing witness are in
  the same endpoint class.

If every row glues, then the no-mixed-delta lemma follows.

## 6. Compute work that is worth doing

Compute should now be completely targeted.

### Best compute object

A **delta-fiber status table** on the true larger accessible union.

For each realized `delta`, record:

- number of actual realizations,
- which realizations continue,
- which terminate,
- next `delta` when continuation exists,
- optional endpoint id / future-word hash.

### Minimal pass condition

For every realized `delta`:

- `cont_count(delta)` is either `0` or `occ_count(delta)`, never mixed;
- `next_delta_set(delta)` is empty or exactly `{delta+1}`.

That is exactly the no-mixed-delta lemma in data form.

### If raw larger-state export is too expensive

Use the smaller backup object:

- the end-gluing table only,
- plus a tiny exceptional-interface table for `3m-2` and `3m-1`.

## 7. Work order

This is the recommended order.

1. Keep the global theorem abstract as `(beta,rho)`.
2. Work first on the regular no-mixed-delta lemma.
3. Then prove exceptional-interface gluing at `3m-2 -> 3m-1`.
4. Only after that upgrade the theorem to raw global `(beta,delta)`.
5. Treat compute only as support for these two lemma-level tasks.

## 8. What not to reopen

Do not reopen:

- broad witness search,
- tiny-controller search,
- local event-readout discovery,
- chart-level exceptional landing discovery,
- composite-dimension side work,
- even-`m` speculation.

Those are no longer the bottleneck.

## 9. Success criteria

The current D5 branch should be considered materially advanced if we obtain
either of the following:

### Strong success

A proof of the no-mixed-delta lemma on the true accessible union.

### Moderate success

A proof of:

- the regular no-mixed-delta lemma,
- and the exceptional-interface gluing lemma.

This would already force the global bridge upgrade.

## 10. Bottom line

The current D5 branch is now very close in a specific sense:

- the local rule is identified,
- the componentwise bridge is identified,
- the exceptional splice is essentially pinned,
- and the only remaining serious gap is whether fixed realized `delta`
  determines continuation status on the true accessible union.

So the best next work target is:

> prove the no-mixed-delta lemma, first on the regular union and then across
> the exceptional interface.
