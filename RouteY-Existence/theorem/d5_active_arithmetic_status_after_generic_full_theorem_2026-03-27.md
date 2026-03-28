# d=5 arithmetic status after the full generic-late cycle theorem
Date: 2026-03-27

## Newly closed

The generic-late active-cycle theorem is now closed in **all** safe moduli `m=3M>=27`, `5∤m`.

The final statement is:

- if `M ≢ 2 (mod 3)`, the generic-late active permutation is a single `M`-cycle;
- if `M ≡ 2 (mod 3)`, writing
  ```text
  Q = (M-2)/3,
  ```
  the cycle lengths are
  ```text
  Q, Q+1, Q+1.
  ```

This is proved by a new reduced arithmetic machine:

- `M=5q+1`: translation on `Z/(7q+1)` with a deleted interval of length `2q`;
- `M=5q+3`: translation on `Z/(5q+4)` with one deleted point;
- `M=5q+4`: translation on `Z/(6q+3)` with a deleted interval of length `q-1`;

together with the previously proved `M=5q+2` branch.

## Practical consequence

The old generic-late arithmetic frontier

```text
M ≡ 1,3,4 (mod 5)
```

is gone.

So in the safe regime `5∤m`, the visibility theorem is now closed for:

- `t=r-1`,
- `t=r`,
- `t=1`,
- **generic late in all congruence classes**.

Since the double-top / `Omega_m` leak theorem was already available for generic late,
the generic-late class is now exactness-ready on the same footing as `t=1` and `t=r-1`.

## What remains

The main unresolved pure color-1 issue in the safe regime is therefore no longer generic-late visibility.
It is the base splice problem:

```text
prove that the induced next-return permutation on B_m is single-cycle,
or prove an equivalent splice certificate.
```

The other remaining global frontier is still the branch `5|m`.
