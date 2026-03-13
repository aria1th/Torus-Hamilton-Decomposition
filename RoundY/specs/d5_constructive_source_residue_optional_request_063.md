# Optional Narrow Compute Request 063A

Target only the constructive route through transported source residue `rho`.
Do **not** reopen theorem-side `(B,tau,epsilon4)` searches.

## Goal
Stress-test the explicit current-state formulas from `063` on the extended
`049/050` support range.

## Inputs
- source-residue refinement `049`
- theorem scheduler / branch support `058–062`
- checked-range explicit formulas from `063`

## Requested checks

1. **Extended tau formula check**
   Validate through `m = 13,15,17,19` whether
   \[
   \delta = \rho-(s+u+v+\lambda),\qquad a=1_{\{\rho=u+1\}}
   \]
   gives the exact piecewise formula
   \[
   \tau =
   \begin{cases}
   0, & \delta=0,\\
   \delta, & 1\le \delta\le m-4,\\
   0 \text{ or } m-3, & \delta=m-3 \text{ by the }(a,s)\text{-corner rule},\\
   0,1,\text{ or }m-2, & \delta=m-2 \text{ by the }(a,s)\text{-corner rule}.
   \end{cases}
   \]

2. **Extended next_tau formula check**
   Validate through the same range whether the branchwise formula from `063`
   remains exact on `(s,u,layer,rho,epsilon4)`.

3. **Constructive-route compression**
   Test whether the full current-state constructive route can now be summarized
   as:
   - current `rho` transport,
   - current `delta` computation,
   - piecewise current formulas for `c`, `tau`, and `next_tau`.

## Deliverables
- exactness summary JSON by modulus
- first collision witness if any formula fails
- a yes/no note on whether the constructive route is now stable through `m=19`

## Not needed
- no generic local scan
- no theorem-side proof search
- no attempt to realize `rho` locally yet
