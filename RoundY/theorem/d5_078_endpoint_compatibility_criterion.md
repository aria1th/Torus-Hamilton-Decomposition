# D5 078 Endpoint Compatibility Criterion

This note promotes the stable theorem-level reduction from the `078`
B-track material in `tmp/`.

Its role is to state the cleanest bridge-globalization criterion available
before the later `080–083` closure.

## 1. Endpoint form of the globalization question

Let `U` range over actual splice-connected accessible components in the regular
full-chain union.

Because the accepted componentwise concrete bridge has successor
`delta -> delta+1`, each finite component has a well-defined right endpoint
`r(U)` in `Z/m^2 Z`, while a total component has endpoint `infty`.

Then:

> `rho = rho(delta)` globally if and only if every realized `delta` appears
> only in components with the same right endpoint.

Equivalently:

> raw global `(beta,delta)` fails exactly when the same realized `delta`
> occurs in two actual components with different forward endpoints.

So the globalization question is an endpoint-compatibility problem, not a new
local event-readout problem.

## 2. Tail-length interpretation

Using the accepted `077` reduction, endpoint compatibility is equivalent to
tail-length compatibility.

At fixed realized `delta`, the padded future word can vary only through the
remaining full-chain tail length.

So the same criterion can be restated as:

> `rho = rho(delta)` globally if and only if fixed realized `delta` has
> component-independent remaining tail length.

## 3. Conditional positive and negative forms

### Positive form

If every relevant actual component is total, then all tail lengths are
infinite, hence `rho = rho(delta)` globally.

### Negative form

If the saved source-family windows were genuine finite components, then raw
global `(beta,delta)` would fail immediately because the same realized `delta`
would already appear with different endpoints.

So the note isolates a clean theorem fork without reopening any local bridge
analysis.

## 4. Later status

This criterion remains mathematically correct, but it is now historical support
for the later closure.

Its role was to reduce the bridge problem to one explicit geometric statement.
That reduction was then sharpened by:

- `theorem/d5_080_no_mixed_delta_reduction.md`
- `theorem/d5_081_regular_union_and_gluing_support.md`
- `theorem/d5_082_exceptional_row_reduction.md`

## 5. Promoted references

This note promotes the substance of:

- `tmp/d5_078_rB.md`
