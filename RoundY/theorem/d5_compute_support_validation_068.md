# D5 Compute Support Validation 068
This note validates the exact reduction object and the canonical clock using the frozen route datasets, without reopening generic local-controller search. It follows the 067 compute-support split.
## 1. Exact reduction object: marked chain before cycle
Using the full frozen active carry dataset from 045 on m=5,7,9,11, every regular carry-jump slice at fixed `(source_u, w)` is an exact marked q-chain of length `m`: `q=0,1,...,m-1`, with `c=0` on the first `m-1` states and `c=1` only at `q=m-1`. These chains occur for `w=2,3,...,m-2`, and each endpoint splices to the next `w`-slice start. So the safer first exact reduction object is a **marked length-m chain**; the cycle requires one more quotienting/identification step across successive `w`-slices.
- m=5: all regular sources satisfy the marked-chain law and all chain endpoints splice correctly to the next w-slice.
- m=7: all regular sources satisfy the marked-chain law and all chain endpoints splice correctly to the next w-slice.
- m=9: all regular sources satisfy the marked-chain law and all chain endpoints splice correctly to the next w-slice.
- m=11: all regular sources satisfy the marked-chain law and all chain endpoints splice correctly to the next w-slice.

## 2. Canonical clock beta on full frozen rows
On the full 047 frozen active dataset for `m=5,7,9,11`, define
```
beta = -(q + s + v + layer) mod m.
```
Then on every nonterminal row the unit drift law `beta' = beta - 1 (mod m)` is exact. On the same rows, `(B,beta)` is exact for the readouts `q`, `c`, `epsilon4`, `tau`, `next_tau`, and `next_B`.
- m=5: `beta' = beta-1` is exact on 216 nonterminal rows; `(B,beta)` is exact for q/c/epsilon4/tau/next_tau/next_B.
- m=7: `beta' = beta-1` is exact on 1212 nonterminal rows; `(B,beta)` is exact for q/c/epsilon4/tau/next_tau/next_B.
- m=9: `beta' = beta-1` is exact on 3952 nonterminal rows; `(B,beta)` is exact for q/c/epsilon4/tau/next_tau/next_B.
- m=11: `beta' = beta-1` is exact on 9780 nonterminal rows; `(B,beta)` is exact for q/c/epsilon4/tau/next_tau/next_B.

## 3. Extension support beyond the full-row range
The extended source-residue support from 049/063a keeps the constructive current formulas exact through `m=19`, so once the canonical clock/source-residue memory is present, the current readouts of `q`, `c`, `tau`, and `next_tau` stay exact through that range. On the larger representative branch support `m=25,27,29`, the predicted scheduler rows also satisfy `beta' = beta-1` exactly.

## 4. Quotient diagnostics on the marked chains
The first 045 feature families separate into two behaviors on the exact marked chains:
- `next_dn` and `dn+next_dn` have only 2 quotient states on every chain and already read carry exactly, **but their chain successor is not deterministic**.
- `B`, `B->B_next`, and `B->B_next->B_next2` induce deterministic quotients, but the quotient size is exactly `m` on each chain.
So the new chain picture cleanly separates **readout exactness** from **transport/determinism**: small quotients can read the marker on a fixed chain, but the exact chain dynamics still force the full m-scale state on deterministic quotients.

## 5. Honest remaining gap
What is still missing computationally is exhaustive larger-modulus validation of the marked-chain/cycle object from regenerated raw rows, and extraction of the accessible quotient for the intended local/admissible class beyond the first 045 catalogs. The current bundle does not include the full raw branch generator needed for that exhaustive extension.
