# D5 278 Route-E Refined Family Large-Odd Gate

This note is the honest follow-up to
[d5_277_routee_refined_family_search.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_277_routee_refined_family_search.md).

Primary files:

- [torus_nd_d5_routee_refined_family_large_odd_gate_278.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_routee_refined_family_large_odd_gate_278.py)
- [d5_278_routee_refined_family_large_odd_gate_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_278_routee_refined_family_large_odd_gate_summary.json)
- [gate_checks.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_278_routee_refined_family_large_odd_gate/gate_checks.json)

## 1. Question

`277` found a better refined family on the checked `7/9` exactness model.

The next honest question is not whether that rule looks nicer on the checked
cycle profiles. It is:

> does the best `277` rule survive the next odd moduli?

## 2. Gate result

It does not.

The best default `277` rule fails exactness already at

- `m = 11`,
- `m = 13`.

The first checked failures are target-not-Latin witnesses. In both cases the
same structural pattern appears: a target of the form

- `(m-1, 6, m-1, 0, m-1)`

receives a repeated incoming color.

So the `277` refinement is real, but it is still a checked-range improvement,
not yet an all-odd theorem family.

## 3. What stabilizes and what does not

The local class set itself is already stable:

- key count on `5,7,9` is `67`,
- key count on `5,7,9,11` is still `67`,
- key count on `5,7,9,11,13` is still `67`.

So no genuinely new local *type* appears after `11`.

But the exactness patterns do still grow:

- `7/9`: `514` patterns,
- `7/9/11`: `552` patterns,
- `7/9/11/13`: `560` patterns.

This is the clean current reading:

- the defect-marker family is close to stable,
- but one more local distinction is still missing from the exactness CSP.

## 4. Meaning for the proof

`278` rules out the most optimistic reading of `277`.

We cannot yet say:

- “the two defect markers from `276` finish the five-color assembly.”

What we can say is sharper and still useful:

- the remaining obstruction is no longer a large search problem,
- and it is no longer a missing global coordinate system,
- it is one more local exactness refinement beyond `g_anchor` and `m_bad`.

So the next theorem/computation target is now very specific:

1. isolate the recurring `11/13` Latin witness family,
2. extract the missing local distinction it exposes,
3. add that distinction to the refined Route-E class family,
4. rerun the finite exactness CSP.

That is a much smaller frontier than the pre-`274` graph-side assembly problem.
