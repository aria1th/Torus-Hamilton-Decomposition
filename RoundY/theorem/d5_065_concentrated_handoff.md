# D5 Concentrated Handoff 065

This note is a concentrated handoff for the current `d=5` frontier.

It intentionally avoids file-path references inside the body. The goal is to
state the current mathematical picture in one place, with the theorem route,
the positive constructive route, the negative route, and the next targets for
different researchers.

## 1. Current position

The `d=5` problem is no longer a broad search problem.

The branch has split into three clear routes:

1. a theorem route, whose central target is a phase-corner theorem on the
   active best-seed branch;
2. a positive constructive route, whose central target is a canonical cyclic
   controller variable;
3. a rigidity route, whose central target is a bounded-quotient theorem
   showing that any exact local realization must already carry such a cyclic
   clock on its accessible part.

The theorem-side structure is now close to closed in shape. The remaining open
issue is whether the canonical cyclic clock can be realized locally in the
intended admissible class, or whether one can prove that every exact local
scheme must already carry one of comparable size.

## 2. The theorem object

The theorem object should remain minimal:

- `B = (s, u, v, layer, family)`
- `tau`
- `epsilon4`

Auxiliary variables such as `rho`, `alpha`, `delta`, `kappa`, and `beta` are
useful proof or constructive coordinates, but they should not replace
`(B, tau, epsilon4)` in the main theorem statement.

## 3. Main theorem target

The best theorem slogan is:

> On the active best-seed branch, `d=5` is an odometer with one corner.

### Phase-corner theorem

Fix odd `m >= 5` and the best seed. On the active nonterminal branch, define

- `kappa = q + s + v + layer mod m`.

Then the intended theorem is:

1. `kappa' = kappa + 1 mod m`.
2. The current event `epsilon4` is determined by `kappa`, the carry sheet
   `c = 1_{q = m-1}`, and the single corner condition `s = 2`:
   - `kappa = 0 -> wrap`
   - `kappa = 1 -> carry_jump`
   - `kappa = 2 -> other_1000` iff `c = 1`, else `flat`
   - `kappa = 3 -> other_0010` iff `(c = 0 and s = 2)` or `(c = 1 and s != 2)`,
     else `flat`
   - `kappa = 4, ..., m-1 -> flat`
3. Among flat states, the only short reset occurs at the corner `(kappa, s) = (2, 2)`.

This is the conceptual center of the theorem side. The branchwise reset laws
should be treated as corollaries of this machine, not as independent primary
theorems.

### Immediate corollaries

From the phase-corner theorem one should derive:

- countdown law:
  - `tau = 0` on nonflat states
  - on flat states, `tau = 1` at `(kappa, s) = (2, 2)` and `tau = m-kappa`
    otherwise
  - hence `tau' = tau - 1` whenever `tau > 0`
- reset laws:
  - `wrap -> 0`
  - `carry_jump -> 0`, `1`, or `m-2` according to the zero-reset fiber and the
    short case
  - `other_1000 -> m-3` or `0`
  - `other_0010 -> m-4`
- finite-cover compatibility with the chain
  `B <- B+c <- B+c+d`

## 4. Best proof spine

The clean structural proof spine is:

- explicit trigger family
- universal first-exit targets
- pre-exit `B`-region invariance
- mixed-witness scheduler on `B`
- phase-corner theorem

In practice, the strongest current theorem-side route is:

1. use the explicit trigger family for the unresolved channel;
2. use the phase-1 source-residue invariant to derive the two universal
   first-exit targets;
3. show the candidate orbit agrees with the actual active branch up to first
   exit;
4. conclude every pre-exit active current state is `B`-labelled;
5. therefore the mixed witness rule applies exactly there, yielding the
   current-state scheduler in `kappa`;
6. promote that scheduler to the phase-corner theorem.

So the structural branch is now close to closed in logical shape. The main
remaining burden is to write it cleanly and verify the dependencies sharply.

## 5. Positive constructive route

The constructive route has sharpened twice.

### First sharpening: alpha

Starting from source residue

- `rho = u_source + 1`,

the better transport gauge is

- `alpha = rho - u`.

In this gauge:

- `q` and `c` become current-state readouts;
- the explicit formulas for `tau` and `next_tau` no longer need raw `rho` and
  `u` separately;
- the post-entry birth is universal: `alpha = 1`.

So the first constructive reformulation is:

> build a local carrier `alpha` with universal birth and the correct
> one-phase decrement behavior.

### Second sharpening: beta

The current best constructive coordinate is

- `beta = alpha - (s + v + layer) - J`,

where `J = 1_{epsilon4 = carry_jump}`.

This gives:

- `q = -beta - s - v - layer mod m`
- `c = 1_{beta + s + v + layer = 1}`

so `q` and `c` are exact from `(B, beta)` alone.

Moreover, the checked support says:

- `beta' = beta - 1 mod m`

on every recorded transition in the checked range.

This is the main constructive compression:

> the positive route is best viewed as realizing a universal cyclic clock with
> unit drift.

The key convergence point is:

> the phase-corner theorem and the `beta` controller are the same machine in
> two gauges.

So the positive route is no longer a free design problem. It is the local
realization problem for the canonical controller already implicit in the
theorem route.

### Best positive target

The strongest clean positive theorem target now is:

> There exists a local/admissible controller variable `beta` on the active
> branch such that:
> - `beta` is born at a universal post-entry value;
> - `beta' = beta - 1 mod m` at every active step;
> - `q`, `c`, `epsilon4`, `tau`, and `next_tau` are exact current functions of
>   `(B, beta)`.

If proved, that would close the positive route more cleanly than the older
source-residue language.

## 6. Rigidity route

The negative branch should no longer be phrased as "bounded horizon fails."

The right target is an exact bounded-quotient theorem.

### Cyclic-section principle

Assume one has a cyclic return section

- `Sigma_m = {x_0, ..., x_{m-1}}`

with return map

- `R(x_q) = x_{q+1}`

and carry label

- `c(x_q) = 1` exactly at one distinguished residue.

Then the carry observable is generating on that section: any exact semiconjugate
quotient that still recovers carry must separate all residues. In particular,
any exact quotient must have at least `m` states.

This is stronger than the old witness-pair lower bound. It says not only that
bounded lookahead fails, but that any bounded exact quotient fails.

### Best rigidity target

The real negative theorem should therefore be:

> prove that the intended local/admissible class factors through a bounded
> finite cover of the active cyclic section.

Once that reduction exists, the cyclic-section principle forces a lower bound
of order `m` on any exact carrier, ruling out uniformly bounded local schemes.

This also explains why an `m`-valued positive carrier such as `alpha` or
`beta` is not just convenient but structurally natural.

So this branch does not really compete with the positive route. It supports
it by showing that any exact realization must already contain a cyclic clock on
its accessible exact part.

## 7. Checked support

The current checked support can be summarized briefly as follows:

- the structural branch support extends well beyond the earliest pilot range,
  including branch-local support on larger odd moduli;
- the stronger constructive formulas through source residue remain exact through
  `m = 19`;
- the `beta` drift picture is exact on the checked transition data;
- no current evidence points to a structural failure of the phase-corner view.

So the route is no longer blocked by noisy empirical uncertainty. It is blocked
by proof closure and local realizability.

## 8. Recommended division of labor

### Researcher A: theorem route

Aim:

- finish the phase-corner theorem cleanly;
- make countdown, reset, and finite-cover compatibility corollaries;
- keep the theorem object minimal.

### Researcher B: positive constructive route

Aim:

- realize the `beta` clock directly, or realize `alpha` and straighten it to
  `beta`;
- focus on universal birth and unit-drift transport.

### Researcher C: negative route

Aim:

- define the intended local/admissible class precisely;
- prove bounded finite-cover reduction;
- apply the cyclic-section injectivity/lower-bound argument.

### Researcher D: compute support only

Aim:

- do not reopen broad search;
- only test identities that directly support one of the three proof branches.

## 9. Honest remaining open point

The problem is not fully solved.

What now seems likely is:

- the theorem side is close to a stable manuscript theorem;
- the positive route has compressed to a clean cyclic-clock realization
  problem;
- the rigidity route has compressed to a bounded-quotient theorem that
  supports the same cyclic-clock picture as the positive route.

So the real remaining question is:

> can the intended local class realize the canonical cyclic clock, or does the
> bounded-quotient rigidity theorem force any exact realization to use an
> `m`-scale carrier that the intended class cannot provide?

That is the clean current frontier.
