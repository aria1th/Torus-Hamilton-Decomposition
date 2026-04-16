import TorusD5.Core.Interfaces

namespace TorusD5.Common.M15r9

def IsCommonModulus (m : ℕ) : Prop := ∃ r : ℕ, m = 15 * r + 9

structure TheoremFloor (X Y : Type) (m : ℕ) where
  commonClass : IsCommonModulus m
  Rre : TorusD5.RreInterface m
  Rq : TorusD5.RqInterface m
  betaTilde : TorusD5.BetaTildeInterface X m
  beta : TorusD5.BetaInterface Y m

theorem commonClass_mod_five {m : ℕ} (hm : IsCommonModulus m) : m % 5 = 4 := by
  rcases hm with ⟨r, rfl⟩
  omega

theorem odd_commonClass_of_even_parameter {r : ℕ} (hr : Even r) : Odd (15 * r + 9) := by
  rcases hr with ⟨s, rfl⟩
  refine ⟨15 * s + 4, by ring⟩

theorem even_parameter_of_odd_commonClass {r : ℕ} (hm : Odd (15 * r + 9)) : Even r := by
  have hadd : Odd (15 * r) ↔ Even 9 := (Nat.odd_add.mp hm)
  have hEvenMul : Even (15 * r) := by
    apply Nat.not_odd_iff_even.mp
    intro hOddMul
    have hEvenNine : Even 9 := hadd.mp hOddMul
    exact (by decide : ¬ Even 9) hEvenNine
  rcases Nat.even_mul.mp hEvenMul with hEven15 | hEvenR
  · exact False.elim ((by decide : ¬ Even 15) hEven15)
  · exact hEvenR

theorem commonClass_ge_nine {m : ℕ} (hm : IsCommonModulus m) : 9 ≤ m := by
  rcases hm with ⟨r, rfl⟩
  omega

theorem nine_is_common : IsCommonModulus 9 := by
  exact ⟨0, by norm_num⟩

end TorusD5.Common.M15r9
