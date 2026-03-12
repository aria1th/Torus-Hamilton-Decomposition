import TorusD3Even.Splice
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

namespace TorusD3Even

local instance : Fact (0 < 3) := ⟨by decide⟩

/-
Color 1, Case I (`m ≡ 0,2 mod 6`) from the splice-integrated manuscript.

This file currently sets up the first splice row

  F11 = (0,2,5,...,m-3)
  F12 = (1,4,7,...,m-1)
  F13 = (3,6,9,...,m-2)

for the subcase `m ≡ 2 mod 6`, together with the common Case-I formulas

  0    ↦ 2
  x    ↦ x + 3    for 1 ≤ x ≤ m - 4
  m-3  ↦ 1
  m-2  ↦ 0
  m-1  ↦ 3.
-/

def T1CaseI [Fact (5 < m)] (x : Fin m) : Fin m :=
  let hm5 : 5 < m := Fact.out
  if hx0 : x.1 = 0 then
    ⟨2, by omega⟩
  else if hxm3 : x.1 = m - 3 then
    ⟨1, by omega⟩
  else if hxm2 : x.1 = m - 2 then
    ⟨0, by omega⟩
  else if hxm1 : x.1 = m - 1 then
    ⟨3, by omega⟩
  else
    ⟨x.1 + 3, by omega⟩

def rho1CaseI [Fact (5 < m)] (x : Fin m) : ℕ :=
  if _hx0 : x.1 = 0 then
    1
  else if _hxm2 : x.1 = m - 2 then
    1
  else if _hxm3 : x.1 = m - 3 then
    m + 3
  else if _hxm1 : x.1 = m - 1 then
    m + 3
  else
    m + 2

theorem eq_six_mul_add_two_of_mod_six_eq_two (hm : m % 6 = 2) :
    ∃ q, m = 6 * q + 2 := by
  refine ⟨m / 6, ?_⟩
  have hdiv := Nat.mod_add_div m 6
  omega

def lenT1CaseIModTwo (m : ℕ) : Fin 3 → ℕ
  | ⟨0, _⟩ => (m - 2) / 3
  | ⟨1, _⟩ => (m - 2) / 3
  | _ => (m - 5) / 3

def pointT1CaseIModTwo [Fact (7 < m)] (j : Fin 3) :
    Fin (lenT1CaseIModTwo m j + 1) → Fin m :=
  match j with
  | ⟨0, _⟩ => fun s =>
      by
        have hm7 : 7 < m := Fact.out
        by_cases hs0 : s.1 = 0
        · exact ⟨0, by omega⟩
        · exact ⟨3 * s.1 - 1, by
            have hsPos : 0 < s.1 := Nat.pos_of_ne_zero hs0
            have hsLe : s.1 ≤ (m - 2) / 3 := Nat.lt_succ_iff.mp s.2
            have hmul : 3 * s.1 ≤ 3 * ((m - 2) / 3) := Nat.mul_le_mul_left 3 hsLe
            have hdiv : 3 * ((m - 2) / 3) ≤ m - 2 := Nat.mul_div_le (m - 2) 3
            omega⟩
  | ⟨1, _⟩ => fun s =>
      by
        have hm7 : 7 < m := Fact.out
        exact ⟨3 * s.1 + 1, by
          have hsLe : s.1 ≤ (m - 2) / 3 := Nat.lt_succ_iff.mp s.2
          have hmul : 3 * s.1 ≤ 3 * ((m - 2) / 3) := Nat.mul_le_mul_left 3 hsLe
          have hdiv : 3 * ((m - 2) / 3) ≤ m - 2 := Nat.mul_div_le (m - 2) 3
          omega⟩
  | ⟨_ + 2, _⟩ => fun s =>
      by
        have hm7 : 7 < m := Fact.out
        exact ⟨3 * s.1 + 3, by
          have hsLe : s.1 ≤ (m - 5) / 3 := Nat.lt_succ_iff.mp s.2
          have hmul : 3 * s.1 ≤ 3 * ((m - 5) / 3) := Nat.mul_le_mul_left 3 hsLe
          have hdiv : 3 * ((m - 5) / 3) ≤ m - 5 := Nat.mul_div_le (m - 5) 3
          omega⟩

def pointT1CaseIModTwoSigma [Fact (7 < m)] :
    SplicePoint (lenT1CaseIModTwo m) → Fin m
  | ⟨j, s⟩ => pointT1CaseIModTwo (m := m) j s

def indexT1CaseIModTwo [Fact (7 < m)] (hm : m % 6 = 2) (x : Fin m) :
    SplicePoint (lenT1CaseIModTwo m) :=
  if hx0 : x.1 = 0 then
    ⟨(0 : Fin 3), (0 : Fin ((m - 2) / 3 + 1))⟩
  else if hx1 : x.1 % 3 = 1 then
    ⟨(1 : Fin 3), ⟨((x.1 - 1) / 3) % (((m - 2) / 3) + 1), by
      have hm7 : 7 < m := Fact.out
      exact Nat.mod_lt _ (by omega)⟩⟩
  else if hx2 : x.1 % 3 = 2 then
    ⟨(0 : Fin 3), ⟨((x.1 + 1) / 3) % (((m - 2) / 3) + 1), by
      have hm7 : 7 < m := Fact.out
      exact Nat.mod_lt _ (by omega)⟩⟩
  else
    ⟨(2 : Fin 3), ⟨(x.1 / 3 - 1) % (((m - 5) / 3) + 1), by
      have hm7 : 7 < m := Fact.out
      exact Nat.mod_lt _ (by omega)⟩⟩

theorem card_splicePoint_lenT1CaseIModTwo [Fact (7 < m)] (hm : m % 6 = 2) :
    Fintype.card (SplicePoint (lenT1CaseIModTwo m)) = m := by
  rcases eq_six_mul_add_two_of_mod_six_eq_two (m := m) hm with ⟨q, rfl⟩
  have hq : 1 ≤ q := by
    have hm7 : 7 < 6 * q + 2 := Fact.out
    omega
  have hcard :
      Fintype.card (SplicePoint (lenT1CaseIModTwo (6 * q + 2)))
        = ∑ j : Fin 3, (lenT1CaseIModTwo (6 * q + 2) j + 1) := by
    simpa [SplicePoint] using
      (Fintype.card_sigma (α := fun j : Fin 3 => Fin (lenT1CaseIModTwo (6 * q + 2) j + 1)))
  have hdiv6 : 6 * q / 3 = 2 * q := by
    calc
      6 * q / 3 = (3 * (2 * q)) / 3 := by ring_nf
      _ = 2 * q := Nat.mul_div_right (2 * q) (by decide : 0 < 3)
  have h0 : lenT1CaseIModTwo (6 * q + 2) 0 = 2 * q := by
    simp [lenT1CaseIModTwo, hdiv6]
  have h1 : lenT1CaseIModTwo (6 * q + 2) 1 = 2 * q := by
    simp [lenT1CaseIModTwo, hdiv6]
  have h2 : lenT1CaseIModTwo (6 * q + 2) 2 = 2 * q - 1 := by
    have hq' : q ≠ 0 := by omega
    calc
      lenT1CaseIModTwo (6 * q + 2) 2 = (6 * q - 3) / 3 := by simp [lenT1CaseIModTwo]
      _ = (3 * (2 * q - 1)) / 3 := by
            have : 6 * q - 3 = 3 * (2 * q - 1) := by omega
            rw [this]
      _ = 2 * q - 1 := Nat.mul_div_right (2 * q - 1) (by decide : 0 < 3)
  rw [hcard, Fin.sum_univ_three, h0, h1, h2]
  omega

theorem index_pointT1CaseIModTwo [Fact (7 < m)] (hm : m % 6 = 2) :
    ∀ p : SplicePoint (lenT1CaseIModTwo m),
      indexT1CaseIModTwo (m := m) hm (pointT1CaseIModTwoSigma (m := m) p) = p := by
  rcases eq_six_mul_add_two_of_mod_six_eq_two (m := m) hm with ⟨q, rfl⟩
  rintro ⟨j, s⟩
  fin_cases j
  · by_cases hs0 : s.1 = 0
    · have hsEq : s = 0 := Fin.ext hs0
      subst hsEq
      simp [indexT1CaseIModTwo, pointT1CaseIModTwoSigma, pointT1CaseIModTwo,
        lenT1CaseIModTwo]
    · have hsPos : 0 < s.1 := Nat.pos_of_ne_zero hs0
      have hx0 : 3 * s.1 - 1 ≠ 0 := by omega
      have hmod1 : (3 * s.1 - 1) % 3 ≠ 1 := by omega
      have hmod2 : (3 * s.1 - 1) % 3 = 2 := by omega
      have hsIdx :
          (⟨((3 * s.1 - 1 + 1) / 3) %
              (lenT1CaseIModTwo (6 * q + 2) 0 + 1),
            Nat.mod_lt _ (Nat.succ_pos _)⟩ :
            Fin (lenT1CaseIModTwo (6 * q + 2) 0 + 1)) = s := by
        apply Fin.ext
        rw [Nat.mod_eq_of_lt s.2]
        omega
      simpa [indexT1CaseIModTwo, pointT1CaseIModTwoSigma, pointT1CaseIModTwo,
        lenT1CaseIModTwo, hs0, hx0, hmod1, hmod2] using
        congrArg (Sigma.mk (0 : Fin 3)) hsIdx
  · have hx0 : 3 * s.1 + 1 ≠ 0 := by omega
    have hmod1 : (3 * s.1 + 1) % 3 = 1 := by omega
    have hsIdx :
        (⟨((3 * s.1 + 1 - 1) / 3) %
            (lenT1CaseIModTwo (6 * q + 2) 1 + 1),
          Nat.mod_lt _ (Nat.succ_pos _)⟩ :
          Fin (lenT1CaseIModTwo (6 * q + 2) 1 + 1)) = s := by
      apply Fin.ext
      rw [Nat.mod_eq_of_lt s.2]
      omega
    simpa [indexT1CaseIModTwo, pointT1CaseIModTwoSigma, pointT1CaseIModTwo,
      lenT1CaseIModTwo, hx0, hmod1] using
      congrArg (Sigma.mk (1 : Fin 3)) hsIdx
  · have hx0 : 3 * s.1 + 3 ≠ 0 := by omega
    have hmod1 : (3 * s.1 + 3) % 3 ≠ 1 := by omega
    have hmod2 : (3 * s.1 + 3) % 3 ≠ 2 := by omega
    have hsIdx :
        (⟨((3 * s.1 + 3) / 3 - 1) %
            (lenT1CaseIModTwo (6 * q + 2) 2 + 1),
          Nat.mod_lt _ (Nat.succ_pos _)⟩ :
          Fin (lenT1CaseIModTwo (6 * q + 2) 2 + 1)) = s := by
      apply Fin.ext
      rw [Nat.mod_eq_of_lt s.2]
      omega
    simpa [indexT1CaseIModTwo, pointT1CaseIModTwoSigma, pointT1CaseIModTwo,
      lenT1CaseIModTwo, hx0, hmod1, hmod2] using
      congrArg (Sigma.mk (2 : Fin 3)) hsIdx

theorem pointT1CaseIModTwo_zero_val [Fact (7 < m)]
    (s : Fin (lenT1CaseIModTwo m 0 + 1)) :
    (pointT1CaseIModTwo (m := m) 0 s).1 = if s.1 = 0 then 0 else 3 * s.1 - 1 := by
  by_cases hs0 : s.1 = 0
  · simp [pointT1CaseIModTwo, lenT1CaseIModTwo, hs0]
  · simp [pointT1CaseIModTwo, lenT1CaseIModTwo, hs0]

theorem pointT1CaseIModTwo_one_val [Fact (7 < m)]
    (s : Fin (lenT1CaseIModTwo m 1 + 1)) :
    (pointT1CaseIModTwo (m := m) 1 s).1 = 3 * s.1 + 1 := by
  simp [pointT1CaseIModTwo, lenT1CaseIModTwo]

theorem pointT1CaseIModTwo_two_val [Fact (7 < m)]
    (s : Fin (lenT1CaseIModTwo m 2 + 1)) :
    (pointT1CaseIModTwo (m := m) 2 s).1 = 3 * s.1 + 3 := by
  simp [pointT1CaseIModTwo, lenT1CaseIModTwo]

/-
Helper layer for the terminal-block wrap proof.
We first evaluate the three block lengths under `m = 6q + 2`, then package
both the three explicit `T1CaseI` endpoint values and the three terminal
points of the splice encoding.
-/
private theorem lenT1CaseIModTwo_zero_eq (q : ℕ) :
    lenT1CaseIModTwo (6 * q + 2) 0 = 2 * q := by
  have hdiv6 : 6 * q / 3 = 2 * q := by
    calc
      6 * q / 3 = (3 * (2 * q)) / 3 := by ring_nf
      _ = 2 * q := Nat.mul_div_right (2 * q) (by decide : 0 < 3)
  simp [lenT1CaseIModTwo, hdiv6]

private theorem lenT1CaseIModTwo_one_eq (q : ℕ) :
    lenT1CaseIModTwo (6 * q + 2) 1 = 2 * q := by
  have hdiv6 : 6 * q / 3 = 2 * q := by
    calc
      6 * q / 3 = (3 * (2 * q)) / 3 := by ring_nf
      _ = 2 * q := Nat.mul_div_right (2 * q) (by decide : 0 < 3)
  simp [lenT1CaseIModTwo, hdiv6]

private theorem lenT1CaseIModTwo_two_eq (q : ℕ) :
    lenT1CaseIModTwo (6 * q + 2) 2 = 2 * q - 1 := by
  calc
    lenT1CaseIModTwo (6 * q + 2) 2 = (6 * q - 3) / 3 := by
      simp [lenT1CaseIModTwo]
    _ = (3 * (2 * q - 1)) / 3 := by
          have : 6 * q - 3 = 3 * (2 * q - 1) := by omega
          rw [this]
    _ = 2 * q - 1 := Nat.mul_div_right (2 * q - 1) (by decide : 0 < 3)

@[simp] theorem pointT1CaseIModTwo_zero_zero [Fact (7 < m)] :
    pointT1CaseIModTwo (m := m) 0 0 = ⟨0, by omega⟩ := by
  apply Fin.ext
  simp [pointT1CaseIModTwo, lenT1CaseIModTwo]

@[simp] theorem pointT1CaseIModTwo_one_zero [Fact (7 < m)] :
    pointT1CaseIModTwo (m := m) 1 0 = ⟨1, by omega⟩ := by
  apply Fin.ext
  simp [pointT1CaseIModTwo, lenT1CaseIModTwo]

@[simp] theorem pointT1CaseIModTwo_two_zero [Fact (7 < m)] :
    pointT1CaseIModTwo (m := m) 2 0 = ⟨3, by omega⟩ := by
  apply Fin.ext
  simp [pointT1CaseIModTwo, lenT1CaseIModTwo]

@[simp] theorem T1CaseI_m_sub_three [Fact (5 < m)] :
    T1CaseI (m := m) ⟨m - 3, by omega⟩ = ⟨1, by omega⟩ := by
  have hx0 : m - 3 ≠ 0 := by
    have hm5 : 5 < m := Fact.out
    omega
  have hxm2 : m - 3 ≠ m - 2 := by omega
  have hxm1 : m - 3 ≠ m - 1 := by omega
  apply Fin.ext
  simp [T1CaseI, hx0, hxm2, hxm1]

@[simp] theorem T1CaseI_m_sub_one [Fact (5 < m)] :
    T1CaseI (m := m) ⟨m - 1, by omega⟩ = ⟨3, by omega⟩ := by
  have hx0 : m - 1 ≠ 0 := by
    have hm5 : 5 < m := Fact.out
    omega
  have hxm3 : m - 1 ≠ m - 3 := by omega
  have hxm2 : m - 1 ≠ m - 2 := by omega
  apply Fin.ext
  simp [T1CaseI, hx0, hxm3, hxm2]

@[simp] theorem T1CaseI_m_sub_two [Fact (5 < m)] :
    T1CaseI (m := m) ⟨m - 2, by omega⟩ = ⟨0, by omega⟩ := by
  have hx0 : m - 2 ≠ 0 := by
    have hm5 : 5 < m := Fact.out
    omega
  have hxm3 : m - 2 ≠ m - 3 := by omega
  apply Fin.ext
  simp [T1CaseI, hx0, hxm3]

@[simp] theorem pointT1CaseIModTwo_last_zero [Fact (7 < m)] (hm : m % 6 = 2) :
    pointT1CaseIModTwo (m := m) 0 ⟨lenT1CaseIModTwo m 0, Nat.lt_succ_self _⟩ =
      ⟨m - 3, by omega⟩ := by
  rcases eq_six_mul_add_two_of_mod_six_eq_two (m := m) hm with ⟨q, rfl⟩
  have hq : 1 ≤ q := by
    have hm7 : 7 < 6 * q + 2 := Fact.out
    omega
  have hs0 : lenT1CaseIModTwo (6 * q + 2) 0 ≠ 0 := by
    rw [lenT1CaseIModTwo_zero_eq (q := q)]
    omega
  apply Fin.ext
  rw [pointT1CaseIModTwo_zero_val (m := 6 * q + 2)
      (s := ⟨lenT1CaseIModTwo (6 * q + 2) 0, Nat.lt_succ_self _⟩)]
  simp [hs0]
  rw [lenT1CaseIModTwo_zero_eq (q := q)]
  omega

@[simp] theorem pointT1CaseIModTwo_last_one [Fact (7 < m)] (hm : m % 6 = 2) :
    pointT1CaseIModTwo (m := m) 1 ⟨lenT1CaseIModTwo m 1, Nat.lt_succ_self _⟩ =
      ⟨m - 1, by omega⟩ := by
  rcases eq_six_mul_add_two_of_mod_six_eq_two (m := m) hm with ⟨q, rfl⟩
  apply Fin.ext
  rw [pointT1CaseIModTwo_one_val (m := 6 * q + 2)
      (s := ⟨lenT1CaseIModTwo (6 * q + 2) 1, Nat.lt_succ_self _⟩)]
  rw [lenT1CaseIModTwo_one_eq (q := q)]
  omega

@[simp] theorem pointT1CaseIModTwo_last_two [Fact (7 < m)] (hm : m % 6 = 2) :
    pointT1CaseIModTwo (m := m) 2 ⟨lenT1CaseIModTwo m 2, Nat.lt_succ_self _⟩ =
      ⟨m - 2, by omega⟩ := by
  rcases eq_six_mul_add_two_of_mod_six_eq_two (m := m) hm with ⟨q, rfl⟩
  apply Fin.ext
  rw [pointT1CaseIModTwo_two_val (m := 6 * q + 2)
      (s := ⟨lenT1CaseIModTwo (6 * q + 2) 2, Nat.lt_succ_self _⟩)]
  rw [lenT1CaseIModTwo_two_eq (q := q)]
  omega

theorem pointT1CaseIModTwoSigma_injective [Fact (7 < m)] :
    Function.Injective (pointT1CaseIModTwoSigma (m := m)) := by
  rintro ⟨j, s⟩ ⟨j', s'⟩ h
  have hv :
      (pointT1CaseIModTwo (m := m) j s).1 = (pointT1CaseIModTwo (m := m) j' s').1 :=
    congrArg Fin.val h
  fin_cases j <;> fin_cases j'
  · by_cases hs0 : s.1 = 0
    · by_cases hs'0 : s'.1 = 0
      · have hsEq : s = 0 := Fin.ext hs0
        have hs'Eq : s' = 0 := Fin.ext hs'0
        subst hsEq; subst hs'Eq
        rfl
      · have hsEq : s = 0 := Fin.ext hs0
        subst hsEq
        have hv' : 0 = 3 * s'.1 - 1 := by
          simpa [pointT1CaseIModTwo_zero_val, hs'0] using hv
        omega
    · by_cases hs'0 : s'.1 = 0
      · have hs'Eq : s' = 0 := Fin.ext hs'0
        subst hs'Eq
        have hv' : 3 * s.1 - 1 = 0 := by
          simpa [pointT1CaseIModTwo_zero_val, hs0] using hv
        omega
      · have hv : 3 * s.1 - 1 = 3 * s'.1 - 1 := by
          simpa [pointT1CaseIModTwo_zero_val, hs0, hs'0] using hv
        have hsval : s.1 = s'.1 := by omega
        have hfin : s = s' := Fin.ext hsval
        cases hfin
        rfl
  · by_cases hs0 : s.1 = 0
    · have hsEq : s = 0 := Fin.ext hs0
      subst hsEq
      have hv' : 0 = 3 * s'.1 + 1 := by
        simpa [pointT1CaseIModTwo_zero_val, pointT1CaseIModTwo_one_val] using hv
      omega
    · have hsPos : 0 < s.1 := Nat.pos_of_ne_zero hs0
      have hv' : 3 * s.1 - 1 = 3 * s'.1 + 1 := by
        simpa [pointT1CaseIModTwo_zero_val, hs0, pointT1CaseIModTwo_one_val] using hv
      omega
  · by_cases hs0 : s.1 = 0
    · have hsEq : s = 0 := Fin.ext hs0
      subst hsEq
      have hv' : 0 = 3 * s'.1 + 3 := by
        simpa [pointT1CaseIModTwo_zero_val, pointT1CaseIModTwo_two_val] using hv
      omega
    · have hv : 3 * s.1 - 1 = 3 * s'.1 + 3 := by
        simpa [pointT1CaseIModTwo_zero_val, hs0, pointT1CaseIModTwo_two_val] using hv
      omega
  · have hv' : 3 * s.1 + 1 = if s'.1 = 0 then 0 else 3 * s'.1 - 1 := by
      simpa [pointT1CaseIModTwo_one_val, pointT1CaseIModTwo_zero_val] using hv
    by_cases hs'0 : s'.1 = 0
    · rw [if_pos hs'0] at hv'
      omega
    · rw [if_neg hs'0] at hv'
      omega
  · have hv : 3 * s.1 + 1 = 3 * s'.1 + 1 := by
      simpa [pointT1CaseIModTwo_one_val] using hv
    have hsval : s.1 = s'.1 := by omega
    have hfin : s = s' := Fin.ext hsval
    cases hfin
    rfl
  · have hv : 3 * s.1 + 1 = 3 * s'.1 + 3 := by
      simpa [pointT1CaseIModTwo_one_val, pointT1CaseIModTwo_two_val] using hv
    omega
  · have hv' : 3 * s.1 + 3 = if s'.1 = 0 then 0 else 3 * s'.1 - 1 := by
      simpa [pointT1CaseIModTwo_two_val, pointT1CaseIModTwo_zero_val] using hv
    by_cases hs'0 : s'.1 = 0
    · rw [if_pos hs'0] at hv'
      omega
    · rw [if_neg hs'0] at hv'
      omega
  · have hv : 3 * s.1 + 3 = 3 * s'.1 + 1 := by
      simpa [pointT1CaseIModTwo_two_val, pointT1CaseIModTwo_one_val] using hv
    omega
  · have hv : 3 * s.1 + 3 = 3 * s'.1 + 3 := by
      simpa [pointT1CaseIModTwo_two_val] using hv
    have hsval : s.1 = s'.1 := by omega
    have hfin : s = s' := Fin.ext hsval
    cases hfin
    rfl

noncomputable def spliceEquivT1CaseIModTwo [Fact (7 < m)] (hm : m % 6 = 2) :
    SplicePoint (lenT1CaseIModTwo m) ≃ Fin m := by
  let f := pointT1CaseIModTwoSigma (m := m)
  have hinj : Function.Injective f := pointT1CaseIModTwoSigma_injective (m := m)
  have hcard : Fintype.card (SplicePoint (lenT1CaseIModTwo m)) = Fintype.card (Fin m) := by
    simpa using card_splicePoint_lenT1CaseIModTwo (m := m) hm
  exact Equiv.ofBijective f ((Fintype.bijective_iff_injective_and_card f).2 ⟨hinj, hcard⟩)

@[simp] theorem spliceEquivT1CaseIModTwo_apply [Fact (7 < m)] (hm : m % 6 = 2)
    (p : SplicePoint (lenT1CaseIModTwo m)) :
    spliceEquivT1CaseIModTwo (m := m) hm p = pointT1CaseIModTwoSigma (m := m) p := by
  rfl

theorem pointT1CaseIModTwo_step [Fact (5 < m)] [Fact (7 < m)] {j : Fin 3}
    (s : Fin (lenT1CaseIModTwo m j + 1)) (hs : s.1 + 1 < lenT1CaseIModTwo m j + 1) :
    T1CaseI (m := m) (pointT1CaseIModTwo (m := m) j s) =
      pointT1CaseIModTwo (m := m) j ⟨s.1 + 1, hs⟩ := by
  fin_cases j
  · by_cases hs0 : s.1 = 0
    · have hsEq : s = 0 := Fin.ext hs0
      subst hsEq
      apply Fin.ext
      simp [pointT1CaseIModTwo, T1CaseI, lenT1CaseIModTwo]
    · have hsPos : 0 < s.1 := Nat.pos_of_ne_zero hs0
      have hsLe : s.1 + 1 ≤ (m - 2) / 3 := Nat.lt_succ_iff.mp hs
      have hmul : 3 * (s.1 + 1) ≤ 3 * ((m - 2) / 3) := Nat.mul_le_mul_left 3 hsLe
      have hdiv : 3 * ((m - 2) / 3) ≤ m - 2 := Nat.mul_div_le (m - 2) 3
      have hx0 : 3 * s.1 - 1 ≠ 0 := by omega
      have hxm3 : 3 * s.1 - 1 ≠ m - 3 := by omega
      have hxm2 : 3 * s.1 - 1 ≠ m - 2 := by omega
      have hxm1 : 3 * s.1 - 1 ≠ m - 1 := by omega
      have hs1nz : s.1 + 1 ≠ 0 := by omega
      apply Fin.ext
      simp [pointT1CaseIModTwo, T1CaseI, lenT1CaseIModTwo, hs0, hs1nz, hx0, hxm3, hxm2, hxm1]
      omega
  · have hsLe : s.1 + 1 ≤ (m - 2) / 3 := Nat.lt_succ_iff.mp hs
    have hmul : 3 * (s.1 + 1) ≤ 3 * ((m - 2) / 3) := Nat.mul_le_mul_left 3 hsLe
    have hdiv : 3 * ((m - 2) / 3) ≤ m - 2 := Nat.mul_div_le (m - 2) 3
    have hx0 : 3 * s.1 + 1 ≠ 0 := by omega
    have hxm3 : 3 * s.1 + 1 ≠ m - 3 := by omega
    have hxm2 : 3 * s.1 + 1 ≠ m - 2 := by omega
    have hxm1 : 3 * s.1 + 1 ≠ m - 1 := by omega
    apply Fin.ext
    simp [pointT1CaseIModTwo, T1CaseI, lenT1CaseIModTwo, hx0, hxm3, hxm2, hxm1]
    omega
  · have hsLe : s.1 + 1 ≤ (m - 5) / 3 := Nat.lt_succ_iff.mp hs
    have hmul : 3 * (s.1 + 1) ≤ 3 * ((m - 5) / 3) := Nat.mul_le_mul_left 3 hsLe
    have hdiv : 3 * ((m - 5) / 3) ≤ m - 5 := Nat.mul_div_le (m - 5) 3
    have hx0 : 3 * s.1 + 3 ≠ 0 := by omega
    have hxm3 : 3 * s.1 + 3 ≠ m - 3 := by omega
    have hxm2 : 3 * s.1 + 3 ≠ m - 2 := by omega
    have hxm1 : 3 * s.1 + 3 ≠ m - 1 := by omega
    apply Fin.ext
    simp [pointT1CaseIModTwo, T1CaseI, lenT1CaseIModTwo, hx0, hxm3, hxm2, hxm1]
    omega

theorem pointT1CaseIModTwo_wrap [Fact (5 < m)] [Fact (7 < m)] (hm : m % 6 = 2) :
    ∀ j : Fin 3,
      T1CaseI (m := m)
        (pointT1CaseIModTwo (m := m) j ⟨lenT1CaseIModTwo m j, Nat.lt_succ_self _⟩) =
      pointT1CaseIModTwo (m := m) (nextBlock j) 0 := by
  intro j
  fin_cases j
  · rw [pointT1CaseIModTwo_last_zero (m := m) hm, T1CaseI_m_sub_three (m := m)]
    simpa [nextBlock] using (pointT1CaseIModTwo_one_zero (m := m)).symm
  · rw [pointT1CaseIModTwo_last_one (m := m) hm, T1CaseI_m_sub_one (m := m)]
    simpa [nextBlock] using (pointT1CaseIModTwo_two_zero (m := m)).symm
  · rw [pointT1CaseIModTwo_last_two (m := m) hm, T1CaseI_m_sub_two (m := m)]
    simpa [nextBlock] using (pointT1CaseIModTwo_zero_zero (m := m)).symm

theorem cycleOn_T1CaseIModTwo [Fact (5 < m)] [Fact (7 < m)] (hm : m % 6 = 2) :
    TorusD4.CycleOn m (T1CaseI (m := m)) ⟨0, by omega⟩ := by
  have hcycle :=
    cycleOn_of_spliceBlocks
      (len := lenT1CaseIModTwo m)
      (e := spliceEquivT1CaseIModTwo (m := m) hm)
      (T := T1CaseI (m := m))
      (hstep := by
        intro j s hs
        simpa using pointT1CaseIModTwo_step (m := m) (j := j) s hs)
      (hwrap := by
        intro j
        simpa using pointT1CaseIModTwo_wrap (m := m) hm j)
  simpa [spliceStart, spliceEquivT1CaseIModTwo, pointT1CaseIModTwoSigma,
    pointT1CaseIModTwo, lenT1CaseIModTwo] using hcycle

end TorusD3Even
