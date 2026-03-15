# D5 078 Global Component Structure

This note promotes the stable structural content of the `078` A-track material
from `tmp/`.

Its role is to freeze the strongest component-geometry picture that was already
visible before the later `079–083` reductions closed the odd-`m` branch inside
the accepted package.

## 1. Main structural conclusion

On the checked actual frozen range `m = 7,9,11`, the saved source-family
windows are not genuine separate components.

After gluing repeated realized `(beta,delta)` states on the complete
`carry_jump -> wrap` chains, the all-source union closes to one deterministic
cycle of size `m^3`.

So on the checked actual range, the source-family windows should be read as
overlapping charts on one total odometer component.

## 2. Regular chart splice law

In the `Theta = 2` gauge, each regular source chart `u != 3` has:

- start label `a_u = m(u+2)-1 mod m^2`,
- chart length `m(m-3)`,
- terminal full-chain label `a_{u-3} - 1`.

So the regular continuation law is exactly:

`u -> u-3 mod m`.

This includes the special regular handoff `6 -> 3`, which enters the
exceptional chart.

## 3. Exceptional continuation already visible

On the checked actual frozen range, the exceptional source-`3` chart does not
jump directly to a new source start.

Its terminal continuation is:

`3 -> (terminal chain of 4) -> 1`,

equivalently in chain labels:

`3m-3 -> 3m-2 -> 3m-1`.

This is the structural precursor of the later `079` exceptional-interface
support note.

## 4. What was still open at this stage

At the `078` stage, the only genuine unresolved structural issue was:

> does the checked exceptional continuation pattern persist on the true larger
> actual unions beyond the frozen `m <= 11` range?

So the problem had already shrunk from a broad globalization question to a
single patched splice question.

## 5. Later status

This note is now historical support.

Its conclusions were later refined by:

- `theorem/d5_079_exceptional_interface_support.md`
- `theorem/d5_081_regular_union_and_gluing_support.md`
- `theorem/d5_082_exceptional_row_reduction.md`

## 6. Promoted references

This note promotes the substance of:

- `tmp/077_d5_trackA_analysis_note.md`
- `tmp/d5_078_rA.md`
