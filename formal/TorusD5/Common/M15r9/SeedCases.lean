import TorusD5.Common.M15r9.StablePacket
import Mathlib.Data.Finset.Basic

namespace TorusD5.Common.M15r9

def stableLowSeeds : Finset ℕ := {39, 69, 129}
def appendixOutliers : Finset ℕ := {9}

def IsSeedAppendixModulus (m : ℕ) : Prop :=
  m ∈ stableLowSeeds ∨ m ∈ appendixOutliers

theorem stableLowSeeds_are_common {m : ℕ} (hm : m ∈ stableLowSeeds) : IsCommonModulus m := by
  simp only [stableLowSeeds, Finset.mem_insert, Finset.mem_singleton] at hm
  rcases hm with rfl | rfl | rfl
  · exact ⟨2, by norm_num⟩
  · exact ⟨4, by norm_num⟩
  · exact ⟨8, by norm_num⟩

theorem appendixOutlier_is_common {m : ℕ} (hm : m ∈ appendixOutliers) : IsCommonModulus m := by
  simp only [appendixOutliers, Finset.mem_singleton] at hm
  subst m
  exact nine_is_common

end TorusD5.Common.M15r9
