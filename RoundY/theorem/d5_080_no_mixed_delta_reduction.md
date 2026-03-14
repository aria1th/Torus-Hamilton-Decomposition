# D5 080 No-Mixed-Delta Reduction

This note promotes the stable `080` theorem reduction from `tmp/`.

Its purpose is to record the sharper target that replaced the older direct
tail-length lemma.

## 1. No-mixed-delta lemma

### Lemma 1.1

For each realized boundary label `delta` on the true accessible union, either:

- every realization of `delta` continues, or
- every realization of `delta` is terminal.

This is the **no-mixed-delta** formulation.

## 2. Why it is enough

If two realizations of the same `delta` had different remaining tail lengths,
follow them forward until the first place where one stops and the other
continues. At that later realized label, one would see a mixed-status `delta`.

So:

- no mixed-status `delta`
- implies fixed `delta` has realization-independent tail length
- implies `rho = rho(delta)` globally
- implies raw global `(beta,delta)` is exact.

This is a strictly smaller and cleaner theorem target than tail-length equality
stated directly.

## 3. Best proof split after 080

The right split is:

1. regular no-mixed-delta lemma;
2. exceptional-interface gluing at `3m-2 -> 3m-1`.

If those hold, the full globalization theorem follows.

## 4. Finite proof object

The correct finite object is an **actual-lift end-gluing table**.

It must record, for each noncontinuing cutoff row:

- the cutoff label `delta`,
- same-`delta` continuing witnesses,
- glue evidence on the true accessible union,
- successor / endpoint compatibility.

This is the right proof object because only noncontinuing cutoff rows can create
a new endpoint sheet.

## 5. Safe conclusion after 080

After `080`, the live theorem is no longer:

> prove the whole bridge globalization directly.

It is:

> prove the no-mixed-delta lemma, preferably via actual-lift end-gluing.

## 6. Promoted references

This note promotes the substance of:

- `tmp/d5_080_a.md`
- `tmp/d5_080_rC_critical_lemma_hypotheses.md`
- `tmp/d5_080_d.md`
