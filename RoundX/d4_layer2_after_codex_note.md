Problem:
Layer-2의 4개 exceptional row를 primitive object로 볼지, 아니면 더 작은 gate law의 gauge-dependent 전개로 볼지 결정해야 한다. Codex bundle의 질문은 두 가지다: (i) reduced 2-bit family에서 Hamiltonian rule이 얼마나 rigid한가, (ii) 현재 witness보다 더 아름다운 gauge representative가 있는가.

Current target:
1. “4개 예외 row”를 두 hyperplane test 위의 affine gate law로 재해석한다.
2. 현재 witness가 reduced family 안에서 유일한지, 정확히는 어떤 gauge까지 유일한지 정리한다.
3. 가능하면 current witness 대신 line-union gauge를 주인공으로 바꾸어 proof skeleton을 단순화한다.

Known assumptions:
- 고정 low-layer skeleton:
  - S=0: q=0 -> (3,2,1,0), q!=0 -> (1,0,3,2)
  - S=1: canonical (0,1,2,3)
  - S>=3: canonical (0,1,2,3)
- Layer-2는 H={S=2, q=0} 위에서만 비정규일 수 있다.
- H 위 reduced family는 두 bit
  - u = 1_{x0 != 0}
  - v = 1_{x3 = 0}
  만을 보고 Klein-four subgroup <(1 3),(0 2)>의 원소를 고른다.
- Codex bundle README/summary가 주장하는 분류:
  - reduced family 256개 중 survivor는 정확히 4개
  - survivor code는 [0,1,2,3], [1,0,3,2], [2,3,0,1], [3,2,1,0]
  - 이는 하나의 Klein-four gauge orbit를 이룬다.
- Local rerun performed here:
  - full reduced-family classification rerun for m=3..15: same 4 survivors
  - line-union return-formula / odometer verification rerun for m=16..20: all pass
  - so the main computational picture is at least cross-checked, not merely copied.

Attempt A:
  Idea:
  current witness를 “two commuting gates”로 다시 써서, 4개 exceptional row가 실제 primitive data가 아님을 보인다.

  What works:
  - state space를 F2^2로 쓰면 매우 깔끔해진다.
    - odd-swap bit eps_odd in {0,1}
    - even-swap bit eps_even in {0,1}
    - state = (eps_odd, eps_even) in F2^2
  - current witness code [0,1,2,3]는 정확히
    state(u,v) = (u,v)
    이다.
    즉 H 위 truth table은 “input bits를 그대로 swap bits로 읽는다”는 affine law이다.
  - 따라서 current witness의 4 row는 독립 규칙 4개가 아니라, 두 gate
    - odd gate on x0 != 0
    - even gate on x3 = 0
    의 truth-table expansion이다.
  - 이 관점에서 rigid한 것은 literal row-table이 아니라 differential gate pattern이다.
  - Computation says: Hamiltonian survivor는 reduced family 안에서 precisely
    state(u,v) = g + (u,v),   g in F2^2
    꼴뿐이다.
    즉 유일성은 row-table 수준이 아니라 affine gauge-quotient 수준에서 성립한다.

  What works especially well:
  - 4 survivor code는 모두 current witness에 global gauge g를 XOR한 것뿐이다.
  - 그래서 “현재 witness가 본질적으로 맞다”는 말은
    “현재 witness의 gate differential pattern이 맞다”
    로 바꾸어야 정확하다.

  Where it fails:
  - 이것만으로는 current witness 자체를 privileged representative로 만들 수 없다.
  - 오히려 computational evidence는 current witness보다 더 자연스러운 gauge가 있음을 시사한다.
  - 따라서 “4 exceptional rows의 근본적 당위성”을 현재 row-table 자체에서 찾으려는 방향은 좋지 않다.

Attempt B:
  Idea:
  survivor orbit 안에서 가장 작은 support를 갖는 representative를 고르고, 그 rule을 새 주인공으로 본다. 이것이 line-union gauge다.

  What works:
  - line-union gauge는 code [1,0,3,2]이고
    state(u,v) = (1,0) + (u,v) = (1+u, v).
  - 이를 원래 조건으로 쓰면
    - odd gate on x0 = 0
    - even gate on x3 = 0
    - both when both hold
    - otherwise canonical
    이다.
  - 따라서 layer-2 support는
    {x0 = 0} union {x3 = 0}
    로 줄어든다. H 안에서 정확히 두 line의 union이고 크기는 2m-1이다.
  - 같은 orbit의 다른 representative support size는
    - current witness: m^2 - m + 1
    - line-union gauge: 2m - 1
    - even global gauge: m^2 - 1
    - odd+even global gauge: m^2 - m + 1
    이므로, line-union gauge가 유일한 minimal-support representative다.
  - line-union의 verified return formulas are simpler than the current witness:
    R0(a,b,q) =
      (a-1,b,q-1)   if q=0
      (a-2,b+1,q-1) if q=m-1 and b=1
      (a-1,b+1,q-1) otherwise
    R1(a,b,q) =
      (a,b-1,q+1)   if q=0
      (a+1,b-2,q+1) if q=m-1 and a=m-1
      (a+1,b-1,q+1) otherwise
    R2(a,b,q) =
      (a,b+1,q-1)   if q=0
      (a+1,b,q-1)   if q=m-1 and b=2
      (a,b,q-1)     otherwise
    R3(a,b,q) =
      (a+1,b,q+1)   if q=0
      (a,b+1,q+1)   if q=m-1 and a=0
      (a,b,q+1)     otherwise
  - On Q={q=m-1}, the second returns are
    T0(a,b) = (a - 1_{b=1}, b-1)
    T1(a,b) = (a - 1, b - 1_{a=m-1})
    T2(a,b) = (a + 1_{b=2}, b+1)
    T3(a,b) = (a + 1, b + 1_{a=0})
  - affine conjugacies to the standard odometer O(u,v)=(u+1, v+1_{u=0}) can be chosen as
    psi0(a,b)=(1-b,-a)
    psi1(a,b)=(-a-1,-b)
    psi2(a,b)=(b-2,a)
    psi3(a,b)=(a,b)
    so T3 is literally the standard odometer already in (a,b)-coordinates.

  Why this is aesthetically better:
  - current witness: bulk of H carries an odd swap, so the support is “almost everything”.
  - line-union gauge: bulk of H is canonical, and the defect sits on two obvious lines.
  - the second-return story survives intact, but one color map becomes exactly the odometer in native coordinates.

  Where it fails:
  - all-m proof of the reduced-family classification is still open.
  - all-m proof for line-union Hamiltonicity is not yet written in the note, although the bundle gives formulas verified computationally.
  - we still need a clean handwritten derivation of the line-union R_c and T_c formulas from the layer rules.

Candidate lemmas:
- [P] Gate-law lemma:
  On H, represent the layer-2 tuple by a swap-state s(x) in F2^2. For the current witness,
  s(x) = (1_{x0 != 0}, 1_{x3 = 0}).
- [C] Reduced-family classification lemma:
  In the 256-rule reduced family, the Hamiltonian rules on the tested range are exactly
  s(u,v)=g+(u,v), g in F2^2.
- [P] Minimal-support gauge lemma:
  Among the four affine-gauge representatives g+(u,v), the unique support-minimizer is g=(1,0), i.e. the line-union gauge.
- [P] Line-union first-return lemma:
  The explicit R_c formulas above hold on P0 under the line-union rule.
- [P] Line-union second-return lemma:
  The explicit T_c formulas above hold on Q={q=m-1}.
- [P] Odometer conjugacy lemma:
  The above psi_c satisfy psi_c o T_c = O o psi_c.
- [P] Lift lemmas:
  one-cycle on Q => one-cycle on P0 => one-cycle on V.
- [O] Conceptual uniqueness lemma:
  prove, without exhaustive search, that any Hamiltonian reduced-family rule must satisfy s(u,v)=g+(u,v).

Needed computations/search:
- Short term: no larger search is essential to continue the proof write-up.
- Still useful:
  1. a tiny symbolic checker that derives the line-union R_c formulas directly from the layer rules,
  2. a compact table comparing the four gauge representatives (code, support, native odometer coordinates, symmetry),
  3. if desired, a broader search beyond the reduced 2-bit family to test whether any non-affine dependence on H can also be Hamiltonian.

Next branching options:
1. Proof-first route:
   Rewrite the theorem using the line-union gauge as the main witness and turn the verified R_c/T_c formulas into a complete handwritten proof.
2. Exposition-first route:
   Keep the current witness in the theorem statement, but add a proposition saying the layer-2 mechanism is unique modulo Klein-four gauge and that the line-union gauge is the minimal-support representative.
3. Classification route:
   Try to prove the computational statement
   s(u,v)=g+(u,v)
   from return-map constraints, eliminating exhaustive search from this part.
4. Aesthetic route:
   Reframe the section entirely around “affine gate law on H” and mention row-tables only as one gauge expansion.

Claim status labels:
  [P] proved or directly derivable from the current proof architecture with routine algebra
  [C] computationally verified (bundle + local rerun), but not yet written as a proof
  [H] strong structural interpretation suggested by the data
  [F] formulation should be abandoned as misleading
  [O] open
