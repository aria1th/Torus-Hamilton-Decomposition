import TorusD4.FullCoordinates
import TorusD4.ReturnDynamics
import TorusD4.Lifts
import Mathlib.Tactic

namespace TorusD4

def KMap : Color → FullCoord m → FullCoord m
  | 0, ((a, b, q0), s) => ((a + 1, b, q0 + 1), s + 1)
  | 1, ((a, b, q0), s) => ((a, b + 1, q0), s + 1)
  | 2, ((a, b, q0), s) => ((a, b, q0 + 1), s + 1)
  | 3, ((a, b, q0), s) => ((a, b, q0), s + 1)

@[simp] theorem KMap_snd (c : Color) (z : FullCoord m) :
    (KMap (m := m) c z).2 = z.2 + 1 := by
  rcases z with ⟨u, s⟩
  rcases u with ⟨a, b, q0⟩
  fin_cases c <;> rfl

@[simp] theorem splitPointEquiv_phi (a b q0 : ZMod m) :
    splitPointEquiv (m := m) (phi a b q0) = ((a, b, q0), (0 : ZMod m)) := by
  simpa [phiLayer_zero] using coordOfPoint_phiLayer (m := m) (a, b, q0) (0 : ZMod m)

@[simp] theorem coordOfPoint_bump (c : Color) (x : Point m) :
    coordOfPoint (m := m) (bump x c) = KMap (m := m) c (coordOfPoint (m := m) x) := by
  fin_cases c
  all_goals
    ext <;> simp [coordOfPoint, KMap, q, S, bump]
    all_goals ring_nf

@[simp] theorem splitPointEquiv_bump (c : Color) (x : Point m) :
    splitPointEquiv (m := m) (bump x c) = KMap (m := m) c (splitPointEquiv (m := m) x) := by
  simpa [splitPointEquiv] using coordOfPoint_bump (m := m) c x

theorem point_eq_phiLayer_of_splitPointEquiv_eq {x : Point m} {u : P0Coord m} {s : ZMod m}
    (h : splitPointEquiv (m := m) x = (u, s)) :
    x = phiLayer (m := m) u s := by
  apply (splitPointEquiv (m := m)).injective
  calc
    splitPointEquiv (m := m) x = (u, s) := h
    _ = splitPointEquiv (m := m) (phiLayer (m := m) u s) := by
          symm
          exact coordOfPoint_phiLayer (m := m) u s

@[simp] theorem zmod_zero_add_one : (0 : ZMod m) + 1 = 1 := by
  norm_num

@[simp] theorem zmod_one_add_one : (1 : ZMod m) + 1 = 2 := by
  norm_num

@[simp] theorem zmod_two_add_one : (2 : ZMod m) + 1 = 3 := by
  norm_num

theorem iterate_two_of_steps {α : Type*} {f : α → α} {x x1 x2 : α}
    (h1 : f x = x1) (h2 : f x1 = x2) :
    (f^[2]) x = x2 := by
  calc
    (f^[2]) x = f (f x) := by
      simp [Function.iterate_succ_apply']
    _ = f x1 := by rw [h1]
    _ = x2 := h2

theorem iterate_three_of_steps {α : Type*} {f : α → α} {x x1 x2 x3 : α}
    (h1 : f x = x1) (h2 : f x1 = x2) (h3 : f x2 = x3) :
    (f^[3]) x = x3 := by
  calc
    (f^[3]) x = f ((f^[2]) x) := by
      simp [Function.iterate_succ_apply']
    _ = f x2 := by rw [iterate_two_of_steps h1 h2]
    _ = x3 := h3

theorem iterate_K0 (n : ℕ) (a b q0 s : ZMod m) :
    ((KMap (m := m) 0)^[n]) ((a, b, q0), s) = ((a + n, b, q0 + n), s + n) := by
  induction n generalizing a b q0 s with
  | zero =>
      simp [KMap]
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [KMap, Nat.cast_add]
      all_goals ring

theorem iterate_K1 (n : ℕ) (a b q0 s : ZMod m) :
    ((KMap (m := m) 1)^[n]) ((a, b, q0), s) = ((a, b + n, q0), s + n) := by
  induction n generalizing a b q0 s with
  | zero =>
      simp [KMap]
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [KMap, Nat.cast_add]
      all_goals ring

theorem iterate_K2 (n : ℕ) (a b q0 s : ZMod m) :
    ((KMap (m := m) 2)^[n]) ((a, b, q0), s) = ((a, b, q0 + n), s + n) := by
  induction n generalizing a b q0 s with
  | zero =>
      simp [KMap]
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [KMap, Nat.cast_add]
      all_goals ring

theorem iterate_K3 (n : ℕ) (a b q0 s : ZMod m) :
    ((KMap (m := m) 3)^[n]) ((a, b, q0), s) = ((a, b, q0), s + n) := by
  induction n generalizing a b q0 s with
  | zero =>
      simp [KMap]
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [KMap, Nat.cast_add]
      all_goals ring

theorem iterate_KMap_snd (c : Color) (n : ℕ) (z : FullCoord m) :
    (((KMap (m := m) c)^[n]) z).2 = z.2 + n := by
  exact snd_iterate_add_one (m := m) (F := KMap (m := m) c) (hstep := KMap_snd (m := m) c) n z

theorem full_natCast_eq_natCast_of_lt [Fact (0 < m)] {a b : ℕ} (ha : a < m) (hb : b < m) :
    (((a : ℕ) : ZMod m) = ((b : ℕ) : ZMod m)) ↔ a = b := by
  constructor
  · intro h
    have h' := (ZMod.natCast_eq_natCast_iff' a b m).1 h
    rwa [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at h'
  · intro h
    simpa [h]

theorem full_natCast_ne_zero_of_pos_lt [Fact (0 < m)] {n : ℕ} (hn0 : 0 < n) (hnm : n < m) :
    ((n : ℕ) : ZMod m) ≠ 0 := by
  intro h
  have h' : n % m = 0 % m := (ZMod.natCast_eq_natCast_iff' n 0 m).1 (by simpa using h)
  rw [Nat.mod_eq_of_lt hnm, Nat.zero_mod] at h'
  exact Nat.ne_of_gt hn0 h'

theorem full_natCast_ne_one_of_two_le_lt [Fact (1 < m)] {n : ℕ} (hn1 : 2 ≤ n) (hnm : n < m) :
    ((n : ℕ) : ZMod m) ≠ 1 := by
  intro h
  have h1m : 1 < m := Fact.out
  have h' : n % m = 1 % m := (ZMod.natCast_eq_natCast_iff' n 1 m).1 (by simpa using h)
  rw [Nat.mod_eq_of_lt hnm, Nat.mod_eq_of_lt h1m] at h'
  omega

theorem full_natCast_ne_two_of_three_le_lt [Fact (2 < m)] {n : ℕ} (hn2 : 3 ≤ n) (hnm : n < m) :
    ((n : ℕ) : ZMod m) ≠ 2 := by
  intro h
  have htwo : (2 : ℕ) < m := by omega
  have h' : n % m = 2 % m := (ZMod.natCast_eq_natCast_iff' n 2 m).1 (by simpa using h)
  rw [Nat.mod_eq_of_lt hnm, Nat.mod_eq_of_lt htwo] at h'
  omega

theorem natCast_sub_three [Fact (0 < m)] (hm : 3 ≤ m) :
    ((m - 3 : ℕ) : ZMod m) = (-3 : ZMod m) := by
  calc
    ((m - 3 : ℕ) : ZMod m) = (m : ZMod m) - 3 := by
      rw [Nat.cast_sub hm]
      norm_num
    _ = (-3 : ZMod m) := by
      simp

theorem witness_phiLayer_canonical [Fact (2 < m)] (u : P0Coord m) {s : ℕ}
    (hs3 : 3 ≤ s) (hsm : s < m) :
    witness (phiLayer (m := m) u s) = canonical := by
  letI : Fact (0 < m) := ⟨by omega⟩
  letI : Fact (1 < m) := ⟨by omega⟩
  have hs0 : (((s : ℕ) : ZMod m)) ≠ 0 := full_natCast_ne_zero_of_pos_lt (m := m) (by omega) hsm
  have hs1 : (((s : ℕ) : ZMod m)) ≠ 1 := full_natCast_ne_one_of_two_le_lt (m := m) (by omega) hsm
  have hs2 : (((s : ℕ) : ZMod m)) ≠ 2 := full_natCast_ne_two_of_three_le_lt (m := m) hs3 hsm
  apply witness_high_layers (x := phiLayer (m := m) u s)
  · simpa [S_phiLayer] using hs0
  · simpa [S_phiLayer] using hs1
  · simpa [S_phiLayer] using hs2

theorem splitPointEquiv_colorMap_phiLayer_canonical [Fact (2 < m)] (c : Color) (u : P0Coord m)
    {s : ℕ} (hs3 : 3 ≤ s) (hsm : s < m) :
    splitPointEquiv (m := m) (colorMap (m := m) c (phiLayer (m := m) u s)) =
      KMap (m := m) c (u, s) := by
  have hw : witness (phiLayer (m := m) u s) = canonical :=
    witness_phiLayer_canonical (m := m) u hs3 hsm
  simpa [colorMap, hw, canonical] using splitPointEquiv_bump (m := m) c (phiLayer (m := m) u s)

theorem splitPointEquiv_colorMap_phi_q_zero (c : Color) (a b : ZMod m) :
    splitPointEquiv (m := m) (colorMap (m := m) c (phi a b 0)) =
      KMap (m := m) (reverse c) (((a, b, (0 : ZMod m)), (0 : ZMod m))) := by
  have hw : witness (phi a b (0 : ZMod m)) = reverse := by
    simp [witness]
  calc
    splitPointEquiv (m := m) (colorMap (m := m) c (phi a b 0))
        = KMap (m := m) (reverse c) (splitPointEquiv (m := m) (phi a b 0)) := by
            simpa [colorMap, hw] using splitPointEquiv_bump (m := m) (reverse c) (phi a b 0)
    _ = KMap (m := m) (reverse c) (((a, b, (0 : ZMod m)), (0 : ZMod m))) := by
          rw [splitPointEquiv_phi]

theorem splitPointEquiv_colorMap_phi_q_ne_zero (c : Color) (a b q0 : ZMod m) (hq0 : q0 ≠ 0) :
    splitPointEquiv (m := m) (colorMap (m := m) c (phi a b q0)) =
      KMap (m := m) (swap01Swap23 c) (((a, b, q0), (0 : ZMod m))) := by
  have hw : witness (phi a b q0) = swap01Swap23 := by
    simp [witness, hq0]
  calc
    splitPointEquiv (m := m) (colorMap (m := m) c (phi a b q0))
        = KMap (m := m) (swap01Swap23 c) (splitPointEquiv (m := m) (phi a b q0)) := by
            simpa [colorMap, hw] using splitPointEquiv_bump (m := m) (swap01Swap23 c) (phi a b q0)
    _ = KMap (m := m) (swap01Swap23 c) (((a, b, q0), (0 : ZMod m))) := by
          rw [splitPointEquiv_phi]

theorem splitPointEquiv_colorMap_phiLayer_one [Fact (1 < m)] (c : Color) (u : P0Coord m) :
    splitPointEquiv (m := m) (colorMap (m := m) c (phiLayer (m := m) u 1)) =
      KMap (m := m) c (u, (1 : ZMod m)) := by
  have hw : witness (phiLayer (m := m) u 1) = canonical := by
    simpa [S_phiLayer] using witness_layer1 (m := m) (x := phiLayer (m := m) u 1) (by simp)
  simpa [colorMap, hw, canonical] using splitPointEquiv_bump (m := m) c (phiLayer (m := m) u 1)

theorem splitPointEquiv_colorMap_phiLayer_two_q_ne_zero [Fact (2 < m)] (c : Color) (u : P0Coord m)
    (hq0 : u.2.2 ≠ 0) :
    splitPointEquiv (m := m) (colorMap (m := m) c (phiLayer (m := m) u 2)) =
      KMap (m := m) c (u, (2 : ZMod m)) := by
  have hm2 : 2 < m := Fact.out
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  letI : Fact (1 < m) := ⟨lt_trans (by decide : 1 < 2) hm2⟩
  have htwo0 : (2 : ZMod m) ≠ 0 := full_natCast_ne_zero_of_pos_lt (m := m) (n := 2) (by decide) hm2
  have htwo1 : (2 : ZMod m) ≠ 1 := full_natCast_ne_one_of_two_le_lt (m := m) (n := 2) (by decide) hm2
  have hw : witness (phiLayer (m := m) u 2) = canonical := by
    simp [witness, S_phiLayer, q_phiLayer, htwo0, htwo1, hq0]
  simpa [colorMap, hw, canonical] using splitPointEquiv_bump (m := m) c (phiLayer (m := m) u 2)

def layer2Dir (c : Color) (a b : ZMod m) : Color :=
  match c with
  | 0 => if b = (2 : ZMod m) then 2 else 0
  | 1 => if a = (0 : ZMod m) then 3 else 1
  | 2 => if b = (2 : ZMod m) then 0 else 2
  | 3 => if a = (0 : ZMod m) then 1 else 3

theorem witness_phiLayer_two_q_zero [Fact (2 < m)] (a b : ZMod m) :
    witness (phiLayer (m := m) (a, b, (0 : ZMod m)) 2) =
      if a = (0 : ZMod m) then
        if b = (2 : ZMod m) then swap13Swap02 else swap13
      else if b = (2 : ZMod m) then
        swap02
      else
        canonical := by
  have hm2 : 2 < m := Fact.out
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  letI : Fact (1 < m) := ⟨lt_trans (by decide : 1 < 2) hm2⟩
  have htwo0 : (2 : ZMod m) ≠ 0 := full_natCast_ne_zero_of_pos_lt (m := m) (n := 2) (by decide) hm2
  have htwo1 : (2 : ZMod m) ≠ 1 := full_natCast_ne_one_of_two_le_lt (m := m) (n := 2) (by decide) hm2
  by_cases ha : a = (0 : ZMod m)
  · by_cases hb : b = (2 : ZMod m)
    · have hx3 : (2 : ZMod m) - b = 0 := by simpa [hb]
      simp [witness, S_phiLayer, q_phiLayer, phiLayer_apply_0, phiLayer_apply_3, htwo0, htwo1, ha, hb, hx3]
    · have hx3 : (2 : ZMod m) - b ≠ 0 := by
        intro hx3
        exact hb ((sub_eq_zero_iff_eq (x := (2 : ZMod m)) (c := b)).mp hx3).symm
      simp [witness, S_phiLayer, q_phiLayer, phiLayer_apply_0, phiLayer_apply_3, htwo0, htwo1, ha, hb, hx3]
  · by_cases hb : b = (2 : ZMod m)
    · have hx3 : (2 : ZMod m) - b = 0 := by simpa [hb]
      simp [witness, S_phiLayer, q_phiLayer, phiLayer_apply_0, phiLayer_apply_3, htwo0, htwo1, ha, hb, hx3]
    · have hx3 : (2 : ZMod m) - b ≠ 0 := by
        intro hx3
        exact hb ((sub_eq_zero_iff_eq (x := (2 : ZMod m)) (c := b)).mp hx3).symm
      simp [witness, S_phiLayer, q_phiLayer, phiLayer_apply_0, phiLayer_apply_3, htwo0, htwo1, ha, hb, hx3]

theorem witnessDir_phiLayer_two_q_zero [Fact (2 < m)] (c : Color) (a b : ZMod m) :
    (witness (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) c =
      layer2Dir (m := m) c a b := by
  rw [witness_phiLayer_two_q_zero (m := m) a b]
  fin_cases c <;>
    by_cases ha : a = (0 : ZMod m) <;>
    by_cases hb : b = (2 : ZMod m) <;>
    simp [layer2Dir, ha, hb, swap13Swap02, swap13Swap02Fun, swap13, swap13Fun,
      swap02, swap02Fun, canonical]

theorem splitPointEquiv_colorMap_phiLayer_two_q_zero [Fact (2 < m)] (c : Color) (a b : ZMod m) :
    splitPointEquiv (m := m) (colorMap (m := m) c (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) =
      KMap (m := m) (layer2Dir (m := m) c a b) (((a, b, (0 : ZMod m)), (2 : ZMod m))) := by
  calc
    splitPointEquiv (m := m) (colorMap (m := m) c (phiLayer (m := m) (a, b, (0 : ZMod m)) 2))
        = KMap (m := m) ((witness (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) c)
            (((a, b, (0 : ZMod m)), (2 : ZMod m))) := by
              simpa [colorMap] using
                splitPointEquiv_bump (m := m)
                  ((witness (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) c)
                  (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)
    _ = KMap (m := m) (layer2Dir (m := m) c a b) (((a, b, (0 : ZMod m)), (2 : ZMod m))) := by
          rw [witnessDir_phiLayer_two_q_zero (m := m) c a b]

theorem iterate_colorMap_phiLayer_three [Fact (2 < m)] (c : Color) (u : P0Coord m) :
    ∀ n, n ≤ m - 3 →
      ((colorMap (m := m) c)^[n]) (phiLayer (m := m) u 3) =
        phiLayer (m := m) (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).1
          (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).2
  | 0, _ => by simp
  | n + 1, hn => by
      have hn' : n ≤ m - 3 := Nat.le_of_succ_le hn
      have hs3 : 3 ≤ n + 3 := by omega
      have hsm : n + 3 < m := by omega
      rw [Function.iterate_succ_apply', iterate_colorMap_phiLayer_three (m := m) c u n hn']
      have hsnd :
          (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).2 = ((n + 3 : ℕ) : ZMod m) := by
        simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
          iterate_KMap_snd (m := m) c n (u, (3 : ZMod m))
      have hsnd' :
          (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).2 = (n : ZMod m) + 3 := by
        calc
          (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).2 = ((n + 3 : ℕ) : ZMod m) := hsnd
          _ = (n : ZMod m) + 3 := by
                rw [Nat.cast_add]
                norm_num
      apply (splitPointEquiv (m := m)).injective
      calc
        splitPointEquiv (m := m)
            (colorMap (m := m) c
              (phiLayer (m := m) (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).1
                (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).2))
            = KMap (m := m) c
                ((((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).1, ((n + 3 : ℕ) : ZMod m)) := by
                  rw [hsnd]
                  exact splitPointEquiv_colorMap_phiLayer_canonical (m := m) c
                    (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).1 hs3 hsm
        _ = KMap (m := m) c
              ((((KMap (m := m) c)^[n]) (u, (3 : ZMod m))).1, (n : ZMod m) + 3) := by
                rw [Nat.cast_add]
                norm_num
        _ = KMap (m := m) c (((KMap (m := m) c)^[n]) (u, (3 : ZMod m))) := by
              rw [← hsnd']
        _ = ((KMap (m := m) c)^[n + 1]) (u, (3 : ZMod m)) := by
              symm
              exact Function.iterate_succ_apply' (KMap (m := m) c) n (u, (3 : ZMod m))
        _ = splitPointEquiv (m := m)
              (phiLayer (m := m) (((KMap (m := m) c)^[n + 1]) (u, (3 : ZMod m))).1
                (((KMap (m := m) c)^[n + 1]) (u, (3 : ZMod m))).2) := by
                  symm
                  exact coordOfPoint_phiLayer (m := m)
                    (((KMap (m := m) c)^[n + 1]) (u, (3 : ZMod m))).1
                    (((KMap (m := m) c)^[n + 1]) (u, (3 : ZMod m))).2

theorem iterate_colorMap_phiLayer_three_max [Fact (2 < m)] (c : Color) (u : P0Coord m) :
    ((colorMap (m := m) c)^[m - 3]) (phiLayer (m := m) u 3) =
      phiLayer (m := m) (((KMap (m := m) c)^[m - 3]) (u, (3 : ZMod m))).1
        (((KMap (m := m) c)^[m - 3]) (u, (3 : ZMod m))).2 := by
  exact iterate_colorMap_phiLayer_three (m := m) c u (m - 3) le_rfl

theorem firstReturn_eq_R0 [Fact (2 < m)] (u : P0Coord m) :
    ((colorMap (m := m) 0)^[m]) (phiLayer (m := m) u 0) =
      phiLayer (m := m) (R0 (m := m) u) 0 := by
  have hm2 : 2 < m := Fact.out
  have hm : 3 ≤ m := by omega
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  letI : Fact (1 < m) := ⟨lt_trans (by decide : 1 < 2) hm2⟩
  rcases u with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · have h1coord :
        splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0)) =
          (((a, b, (0 : ZMod m)), (1 : ZMod m))) := by
      simpa [phiLayer_zero, KMap, reverse, reverseFun, hq0] using
        splitPointEquiv_colorMap_phi_q_zero (m := m) (c := 0) a b
    have h1 :
        colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a, b, (0 : ZMod m)) 1 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
    have h2coord :
        splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b, (0 : ZMod m)) 1)) =
          (((a + 1, b, (1 : ZMod m)), (2 : ZMod m))) := by
      simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 0)
        ((a, b, (0 : ZMod m)))
    have h2 :
        colorMap (m := m) 0 (phiLayer (m := m) (a, b, (0 : ZMod m)) 1) =
          phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 2 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
    have h3coord :
        splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 2)) =
          (((a + 2, b, (2 : ZMod m)), (3 : ZMod m))) := by
      have h1ne : (1 : ZMod m) ≠ 0 := one_ne_zero
      simpa [KMap, add_assoc] using splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 0)
        ((a + 1, b, (1 : ZMod m))) h1ne
    have h3 :
        colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 2) =
          phiLayer (m := m) (a + 2, b, (2 : ZMod m)) 3 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
    have h2iter :
        ((colorMap (m := m) 0)^[2]) (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 2 := by
      exact iterate_two_of_steps h1 h2
    have h3iter :
        ((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a + 2, b, (2 : ZMod m)) 3 := by
      exact iterate_three_of_steps h1 h2 h3
    have hk :
        ((KMap (m := m) 0)^[m - 3]) ((a + 2, b, (2 : ZMod m)), (3 : ZMod m)) =
          (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
      calc
        ((KMap (m := m) 0)^[m - 3]) ((a + 2, b, (2 : ZMod m)), (3 : ZMod m))
            = ((a + 2 + (((m - 3 : ℕ) : ZMod m)), b, (2 : ZMod m) + (((m - 3 : ℕ) : ZMod m))),
                (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                  simpa using iterate_K0 (m := m) (m - 3) (a + 2) b (2 : ZMod m) (3 : ZMod m)
        _ = ((a - 1, b, (-1 : ZMod m)), (0 : ZMod m)) := by
              have hsub3 : ((m - 3 : ℕ) : ZMod m) = (-3 : ZMod m) := natCast_sub_three (m := m) hm
              ext <;> rw [hsub3] <;> ring
        _ = (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
              simp [R0, hq0]
    calc
      ((colorMap (m := m) 0)^[m]) (phiLayer (m := m) (a, b, q0) 0)
          = ((colorMap (m := m) 0)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
              rw [Nat.sub_add_cancel hm]
      _ = ((colorMap (m := m) 0)^[m - 3]) (((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
            simpa using Function.iterate_add_apply (colorMap (m := m) 0) (m - 3) 3
              (phiLayer (m := m) (a, b, q0) 0)
      _ = ((colorMap (m := m) 0)^[m - 3]) (phiLayer (m := m) (a + 2, b, (2 : ZMod m)) 3) := by
            rw [h3iter]
      _ = phiLayer (m := m)
            (((KMap (m := m) 0)^[m - 3]) ((a + 2, b, (2 : ZMod m)), (3 : ZMod m))).1
            (((KMap (m := m) 0)^[m - 3]) ((a + 2, b, (2 : ZMod m)), (3 : ZMod m))).2 := by
              exact iterate_colorMap_phiLayer_three_max (m := m) 0 (a + 2, b, (2 : ZMod m))
      _ = phiLayer (m := m) (R0 (m := m) (a, b, q0)) 0 := by
            rw [hk]
  · by_cases hqneg1 : q0 = (-1 : ZMod m)
    · by_cases hb1 : b = (1 : ZMod m)
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a, b + 1, (-1 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 0) a b q0 hq0
        have h1 :
            colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b + 1, (-1 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b + 1, (-1 : ZMod m)) 1)) =
              (((a + 1, b + 1, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap, hqneg1] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 0)
            ((a, b + 1, (-1 : ZMod m)))
        have h2 :
            colorMap (m := m) 0 (phiLayer (m := m) (a, b + 1, (-1 : ZMod m)) 1) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have h3coord :
            splitPointEquiv (m := m)
              (colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2)) =
              (((a + 1, b + 1, (1 : ZMod m)), (3 : ZMod m))) := by
          have hb2 : b + 1 = (2 : ZMod m) := by
            rw [hb1]
            norm_num
          simpa [layer2Dir, KMap, hb2] using
            splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 0) (a + 1) (b + 1)
        have h3 :
            colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a + 1, b + 1, (1 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h2iter :
            ((colorMap (m := m) 0)^[2]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2 := by
          exact iterate_two_of_steps h1 h2
        have h3iter :
            ((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b + 1, (1 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 0)^[m - 3]) ((a + 1, b + 1, (1 : ZMod m)), (3 : ZMod m)) =
              (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 0)^[m - 3]) ((a + 1, b + 1, (1 : ZMod m)), (3 : ZMod m))
                = ((a + 1 + (((m - 3 : ℕ) : ZMod m)), b + 1, (1 : ZMod m) + (((m - 3 : ℕ) : ZMod m))),
                    (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                      simpa using iterate_K0 (m := m) (m - 3) (a + 1) (b + 1) (1 : ZMod m) (3 : ZMod m)
            _ = ((a - 2, b + 1, (-2 : ZMod m)), (0 : ZMod m)) := by
                  have hsub3 : ((m - 3 : ℕ) : ZMod m) = (-3 : ZMod m) := natCast_sub_three (m := m) hm
                  ext <;> rw [hsub3] <;> ring
            _ = (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  ext <;> simp [R0, hqneg1, hb1] <;> ring
        calc
          ((colorMap (m := m) 0)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 0)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 0)^[m - 3]) (((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 0) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 0)^[m - 3]) (phiLayer (m := m) (a + 1, b + 1, (1 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 0)^[m - 3]) ((a + 1, b + 1, (1 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 0)^[m - 3]) ((a + 1, b + 1, (1 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 0 (a + 1, b + 1, (1 : ZMod m))
          _ = phiLayer (m := m) (R0 (m := m) (a, b, q0)) 0 := by
                rw [hk]
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a, b + 1, (-1 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 0) a b q0 hq0
        have h1 :
            colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b + 1, (-1 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b + 1, (-1 : ZMod m)) 1)) =
              (((a + 1, b + 1, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap, hqneg1] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 0)
            ((a, b + 1, (-1 : ZMod m)))
        have h2 :
            colorMap (m := m) 0 (phiLayer (m := m) (a, b + 1, (-1 : ZMod m)) 1) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have h3coord :
            splitPointEquiv (m := m)
              (colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2)) =
              (((a + 2, b + 1, (1 : ZMod m)), (3 : ZMod m))) := by
          have hb2 : b + 1 ≠ (2 : ZMod m) := by
            intro hb2
            apply hb1
            have hb1' : b = (1 : ZMod m) := by
              calc
                b = (2 : ZMod m) - 1 := by
                  simpa using congrArg (fun t : ZMod m => t - 1) hb2
                _ = 1 := by
                  norm_num
            exact hb1'
          simpa [layer2Dir, KMap, hb2, add_assoc] using
            splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 0) (a + 1) (b + 1)
        have h3 :
            colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a + 2, b + 1, (1 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h2iter :
            ((colorMap (m := m) 0)^[2]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2 := by
          exact iterate_two_of_steps h1 h2
        have h3iter :
            ((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 2, b + 1, (1 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, (1 : ZMod m)), (3 : ZMod m)) =
              (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, (1 : ZMod m)), (3 : ZMod m))
                = ((a + 2 + (((m - 3 : ℕ) : ZMod m)), b + 1, (1 : ZMod m) + (((m - 3 : ℕ) : ZMod m))),
                    (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                      simpa using iterate_K0 (m := m) (m - 3) (a + 2) (b + 1) (1 : ZMod m) (3 : ZMod m)
            _ = ((a - 1, b + 1, (-2 : ZMod m)), (0 : ZMod m)) := by
                  have hsub3 : ((m - 3 : ℕ) : ZMod m) = (-3 : ZMod m) := natCast_sub_three (m := m) hm
                  ext <;> rw [hsub3] <;> ring
            _ = (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  ext <;> simp [R0, hqneg1, hb1] <;> ring
        calc
          ((colorMap (m := m) 0)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 0)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 0)^[m - 3]) (((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 0) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 0)^[m - 3]) (phiLayer (m := m) (a + 2, b + 1, (1 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, (1 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, (1 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 0 (a + 2, b + 1, (1 : ZMod m))
          _ = phiLayer (m := m) (R0 (m := m) (a, b, q0)) 0 := by
                rw [hk]
    · have h1coord :
          splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0)) =
            (((a, b + 1, q0), (1 : ZMod m))) := by
        simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun] using
          splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 0) a b q0 hq0
      have h1 :
          colorMap (m := m) 0 (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a, b + 1, q0) 1 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
      have h2coord :
          splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a, b + 1, q0) 1)) =
            (((a + 1, b + 1, q0 + 1), (2 : ZMod m))) := by
        simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 0)
          ((a, b + 1, q0))
      have h2 :
          colorMap (m := m) 0 (phiLayer (m := m) (a, b + 1, q0) 1) =
            phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
      have hq1ne : q0 + 1 ≠ (0 : ZMod m) := by
        intro hzero
        exact hqneg1 (eq_neg_iff_add_eq_zero.mpr hzero)
      have h3coord :
          splitPointEquiv (m := m) (colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2)) =
            (((a + 2, b + 1, q0 + 2), (3 : ZMod m))) := by
        simpa [KMap, add_assoc] using splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 0)
          ((a + 1, b + 1, q0 + 1)) hq1ne
      have h3 :
          colorMap (m := m) 0 (phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2) =
            phiLayer (m := m) (a + 2, b + 1, q0 + 2) 3 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
      have h2iter :
          ((colorMap (m := m) 0)^[2]) (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2 := by
        exact iterate_two_of_steps h1 h2
      have h3iter :
          ((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a + 2, b + 1, q0 + 2) 3 := by
        exact iterate_three_of_steps h1 h2 h3
      have hk :
          ((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, q0 + 2), (3 : ZMod m)) =
            (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
        calc
          ((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, q0 + 2), (3 : ZMod m))
              = ((a + 2 + (((m - 3 : ℕ) : ZMod m)), b + 1, q0 + 2 + (((m - 3 : ℕ) : ZMod m))),
                  (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                    simpa [add_assoc] using iterate_K0 (m := m) (m - 3) (a + 2) (b + 1) (q0 + 2) (3 : ZMod m)
          _ = ((a - 1, b + 1, q0 - 1), (0 : ZMod m)) := by
                have hsub3 : ((m - 3 : ℕ) : ZMod m) = (-3 : ZMod m) := natCast_sub_three (m := m) hm
                ext <;> rw [hsub3] <;> ring
          _ = (R0 (m := m) (a, b, q0), (0 : ZMod m)) := by
                simp [R0, hq0, hqneg1]
      calc
        ((colorMap (m := m) 0)^[m]) (phiLayer (m := m) (a, b, q0) 0)
            = ((colorMap (m := m) 0)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                rw [Nat.sub_add_cancel hm]
        _ = ((colorMap (m := m) 0)^[m - 3]) (((colorMap (m := m) 0)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
              simpa using Function.iterate_add_apply (colorMap (m := m) 0) (m - 3) 3
                (phiLayer (m := m) (a, b, q0) 0)
        _ = ((colorMap (m := m) 0)^[m - 3]) (phiLayer (m := m) (a + 2, b + 1, q0 + 2) 3) := by
              rw [h3iter]
        _ = phiLayer (m := m)
              (((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, q0 + 2), (3 : ZMod m))).1
              (((KMap (m := m) 0)^[m - 3]) ((a + 2, b + 1, q0 + 2), (3 : ZMod m))).2 := by
                exact iterate_colorMap_phiLayer_three_max (m := m) 0 (a + 2, b + 1, q0 + 2)
        _ = phiLayer (m := m) (R0 (m := m) (a, b, q0)) 0 := by
              rw [hk]

theorem firstReturn_eq_R3 [Fact (2 < m)] (u : P0Coord m) :
    ((colorMap (m := m) 3)^[m]) (phiLayer (m := m) u 0) =
      phiLayer (m := m) (R3 (m := m) u) 0 := by
  have hm2 : 2 < m := Fact.out
  have hm : 3 ≤ m := by omega
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  letI : Fact (1 < m) := ⟨lt_trans (by decide : 1 < 2) hm2⟩
  rcases u with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · have h1coord :
        splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0)) =
          (((a + 1, b, (1 : ZMod m)), (1 : ZMod m))) := by
      simpa [phiLayer_zero, KMap, reverse, reverseFun, hq0] using
        splitPointEquiv_colorMap_phi_q_zero (m := m) (c := 3) a b
    have h1 :
        colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 1 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
    have h2coord :
        splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 1)) =
          (((a + 1, b, (1 : ZMod m)), (2 : ZMod m))) := by
      simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 3)
        ((a + 1, b, (1 : ZMod m)))
    have h2 :
        colorMap (m := m) 3 (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 1) =
          phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 2 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
    have h3coord :
        splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 2)) =
          (((a + 1, b, (1 : ZMod m)), (3 : ZMod m))) := by
      have h1ne : (1 : ZMod m) ≠ 0 := one_ne_zero
      simpa [KMap] using splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 3)
        ((a + 1, b, (1 : ZMod m))) h1ne
    have h3 :
        colorMap (m := m) 3 (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 2) =
          phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 3 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
    have h3iter :
        ((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 3 := by
      exact iterate_three_of_steps h1 h2 h3
    have hk :
        ((KMap (m := m) 3)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m)) =
          (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
      calc
        ((KMap (m := m) 3)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m))
            = ((a + 1, b, (1 : ZMod m)), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                simpa using iterate_K3 (m := m) (m - 3) (a + 1) b (1 : ZMod m) (3 : ZMod m)
        _ = ((a + 1, b, (1 : ZMod m)), (0 : ZMod m)) := by
              rw [natCast_sub_three (m := m) hm]
              ring
        _ = (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
              simp [R3, hq0]
    calc
      ((colorMap (m := m) 3)^[m]) (phiLayer (m := m) (a, b, q0) 0)
          = ((colorMap (m := m) 3)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
              rw [Nat.sub_add_cancel hm]
      _ = ((colorMap (m := m) 3)^[m - 3]) (((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
            simpa using Function.iterate_add_apply (colorMap (m := m) 3) (m - 3) 3
              (phiLayer (m := m) (a, b, q0) 0)
      _ = ((colorMap (m := m) 3)^[m - 3]) (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 3) := by
            rw [h3iter]
      _ = phiLayer (m := m)
            (((KMap (m := m) 3)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m))).1
            (((KMap (m := m) 3)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m))).2 := by
              exact iterate_colorMap_phiLayer_three_max (m := m) 3 (a + 1, b, (1 : ZMod m))
      _ = phiLayer (m := m) (R3 (m := m) (a, b, q0)) 0 := by
            rw [hk]
  · by_cases hqneg1 : q0 = (-1 : ZMod m)
    · by_cases ha0 : a = (0 : ZMod m)
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a, b, (0 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 3) a b q0 hq0
        have h1 :
            colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 1)) =
              (((a, b, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 3)
            ((a, b, (0 : ZMod m)))
        have h2 :
            colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 1) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have h3coord :
            splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) =
              (((a, b + 1, (0 : ZMod m)), (3 : ZMod m))) := by
          simpa [layer2Dir, KMap, ha0] using
            splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 3) a b
        have h3 :
            colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a, b + 1, (0 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h3iter :
            ((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b + 1, (0 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 3)^[m - 3]) ((a, b + 1, (0 : ZMod m)), (3 : ZMod m)) =
              (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 3)^[m - 3]) ((a, b + 1, (0 : ZMod m)), (3 : ZMod m))
                = ((a, b + 1, (0 : ZMod m)), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                    simpa using iterate_K3 (m := m) (m - 3) a (b + 1) (0 : ZMod m) (3 : ZMod m)
            _ = ((a, b + 1, (0 : ZMod m)), (0 : ZMod m)) := by
                  rw [natCast_sub_three (m := m) hm]
                  ring
            _ = (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  simp [R3, hqneg1, ha0]
        calc
          ((colorMap (m := m) 3)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 3)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 3)^[m - 3]) (((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 3) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 3)^[m - 3]) (phiLayer (m := m) (a, b + 1, (0 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 3)^[m - 3]) ((a, b + 1, (0 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 3)^[m - 3]) ((a, b + 1, (0 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 3 (a, b + 1, (0 : ZMod m))
          _ = phiLayer (m := m) (R3 (m := m) (a, b, q0)) 0 := by
                rw [hk]
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a, b, (0 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 3) a b q0 hq0
        have h1 :
            colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 1)) =
              (((a, b, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 3)
            ((a, b, (0 : ZMod m)))
        have h2 :
            colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 1) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have h3coord :
            splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) =
              (((a, b, (0 : ZMod m)), (3 : ZMod m))) := by
          simpa [layer2Dir, KMap, ha0] using
            splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 3) a b
        have h3 :
            colorMap (m := m) 3 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h3iter :
            ((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 3)^[m - 3]) ((a, b, (0 : ZMod m)), (3 : ZMod m)) =
              (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 3)^[m - 3]) ((a, b, (0 : ZMod m)), (3 : ZMod m))
                = ((a, b, (0 : ZMod m)), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                    simpa using iterate_K3 (m := m) (m - 3) a b (0 : ZMod m) (3 : ZMod m)
            _ = ((a, b, (0 : ZMod m)), (0 : ZMod m)) := by
                  rw [natCast_sub_three (m := m) hm]
                  ring
            _ = (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  simp [R3, hqneg1, ha0]
        calc
          ((colorMap (m := m) 3)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 3)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 3)^[m - 3]) (((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 3) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 3)^[m - 3]) (phiLayer (m := m) (a, b, (0 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 3)^[m - 3]) ((a, b, (0 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 3)^[m - 3]) ((a, b, (0 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 3 (a, b, (0 : ZMod m))
          _ = phiLayer (m := m) (R3 (m := m) (a, b, q0)) 0 := by
                rw [hk]
    · have h1coord :
          splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0)) =
            (((a, b, q0 + 1), (1 : ZMod m))) := by
        simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun] using
          splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 3) a b q0 hq0
      have h1 :
          colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a, b, q0 + 1) 1 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
      have h2coord :
          splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0 + 1) 1)) =
            (((a, b, q0 + 1), (2 : ZMod m))) := by
        simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 3)
          ((a, b, q0 + 1))
      have h2 :
          colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0 + 1) 1) =
            phiLayer (m := m) (a, b, q0 + 1) 2 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
      have hq1ne : q0 + 1 ≠ (0 : ZMod m) := by
        intro hzero
        exact hqneg1 (eq_neg_iff_add_eq_zero.mpr hzero)
      have h3coord :
          splitPointEquiv (m := m) (colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0 + 1) 2)) =
            (((a, b, q0 + 1), (3 : ZMod m))) := by
        simpa [KMap] using splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 3)
          ((a, b, q0 + 1)) hq1ne
      have h3 :
          colorMap (m := m) 3 (phiLayer (m := m) (a, b, q0 + 1) 2) =
            phiLayer (m := m) (a, b, q0 + 1) 3 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
      have h3iter :
          ((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a, b, q0 + 1) 3 := by
        exact iterate_three_of_steps h1 h2 h3
      have hk :
          ((KMap (m := m) 3)^[m - 3]) ((a, b, q0 + 1), (3 : ZMod m)) =
            (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
        calc
          ((KMap (m := m) 3)^[m - 3]) ((a, b, q0 + 1), (3 : ZMod m))
              = ((a, b, q0 + 1), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                  simpa using iterate_K3 (m := m) (m - 3) a b (q0 + 1) (3 : ZMod m)
          _ = ((a, b, q0 + 1), (0 : ZMod m)) := by
                rw [natCast_sub_three (m := m) hm]
                ring
          _ = (R3 (m := m) (a, b, q0), (0 : ZMod m)) := by
                simp [R3, hq0, hqneg1]
      calc
        ((colorMap (m := m) 3)^[m]) (phiLayer (m := m) (a, b, q0) 0)
            = ((colorMap (m := m) 3)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                rw [Nat.sub_add_cancel hm]
        _ = ((colorMap (m := m) 3)^[m - 3]) (((colorMap (m := m) 3)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
              simpa using Function.iterate_add_apply (colorMap (m := m) 3) (m - 3) 3
                (phiLayer (m := m) (a, b, q0) 0)
        _ = ((colorMap (m := m) 3)^[m - 3]) (phiLayer (m := m) (a, b, q0 + 1) 3) := by
              rw [h3iter]
        _ = phiLayer (m := m)
              (((KMap (m := m) 3)^[m - 3]) ((a, b, q0 + 1), (3 : ZMod m))).1
              (((KMap (m := m) 3)^[m - 3]) ((a, b, q0 + 1), (3 : ZMod m))).2 := by
                exact iterate_colorMap_phiLayer_three_max (m := m) 3 (a, b, q0 + 1)
        _ = phiLayer (m := m) (R3 (m := m) (a, b, q0)) 0 := by
              rw [hk]

theorem firstReturn_eq_R2 [Fact (2 < m)] (u : P0Coord m) :
    ((colorMap (m := m) 2)^[m]) (phiLayer (m := m) u 0) =
      phiLayer (m := m) (R2 (m := m) u) 0 := by
  have hm2 : 2 < m := Fact.out
  have hm : 3 ≤ m := by omega
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  letI : Fact (1 < m) := ⟨lt_trans (by decide : 1 < 2) hm2⟩
  rcases u with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · have h1coord :
        splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0)) =
          (((a, b + 1, (0 : ZMod m)), (1 : ZMod m))) := by
      simpa [phiLayer_zero, KMap, reverse, reverseFun, hq0] using
        splitPointEquiv_colorMap_phi_q_zero (m := m) (c := 2) a b
    have h1 :
        colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a, b + 1, (0 : ZMod m)) 1 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
    have h2coord :
        splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b + 1, (0 : ZMod m)) 1)) =
          (((a, b + 1, (1 : ZMod m)), (2 : ZMod m))) := by
      simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 2)
        ((a, b + 1, (0 : ZMod m)))
    have h2 :
        colorMap (m := m) 2 (phiLayer (m := m) (a, b + 1, (0 : ZMod m)) 1) =
          phiLayer (m := m) (a, b + 1, (1 : ZMod m)) 2 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
    have h3coord :
        splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b + 1, (1 : ZMod m)) 2)) =
          (((a, b + 1, (2 : ZMod m)), (3 : ZMod m))) := by
      have h1ne : (1 : ZMod m) ≠ 0 := one_ne_zero
      simpa [KMap] using splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 2)
        ((a, b + 1, (1 : ZMod m))) h1ne
    have h3 :
        colorMap (m := m) 2 (phiLayer (m := m) (a, b + 1, (1 : ZMod m)) 2) =
          phiLayer (m := m) (a, b + 1, (2 : ZMod m)) 3 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
    have h3iter :
        ((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a, b + 1, (2 : ZMod m)) 3 := by
      exact iterate_three_of_steps h1 h2 h3
    have hk :
        ((KMap (m := m) 2)^[m - 3]) ((a, b + 1, (2 : ZMod m)), (3 : ZMod m)) =
          (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
      calc
        ((KMap (m := m) 2)^[m - 3]) ((a, b + 1, (2 : ZMod m)), (3 : ZMod m))
            = ((a, b + 1, (2 : ZMod m) + (((m - 3 : ℕ) : ZMod m))), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                simpa using iterate_K2 (m := m) (m - 3) a (b + 1) (2 : ZMod m) (3 : ZMod m)
        _ = ((a, b + 1, (-1 : ZMod m)), (0 : ZMod m)) := by
              rw [natCast_sub_three (m := m) hm]
              ring
        _ = (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
              simp [R2, hq0]
    calc
      ((colorMap (m := m) 2)^[m]) (phiLayer (m := m) (a, b, q0) 0)
          = ((colorMap (m := m) 2)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
              rw [Nat.sub_add_cancel hm]
      _ = ((colorMap (m := m) 2)^[m - 3]) (((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
            simpa using Function.iterate_add_apply (colorMap (m := m) 2) (m - 3) 3
              (phiLayer (m := m) (a, b, q0) 0)
      _ = ((colorMap (m := m) 2)^[m - 3]) (phiLayer (m := m) (a, b + 1, (2 : ZMod m)) 3) := by
            rw [h3iter]
      _ = phiLayer (m := m)
            (((KMap (m := m) 2)^[m - 3]) ((a, b + 1, (2 : ZMod m)), (3 : ZMod m))).1
            (((KMap (m := m) 2)^[m - 3]) ((a, b + 1, (2 : ZMod m)), (3 : ZMod m))).2 := by
              exact iterate_colorMap_phiLayer_three_max (m := m) 2 (a, b + 1, (2 : ZMod m))
      _ = phiLayer (m := m) (R2 (m := m) (a, b, q0)) 0 := by
            rw [hk]
  · by_cases hqneg1 : q0 = (-1 : ZMod m)
    · by_cases hb2 : b = (2 : ZMod m)
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a, b, (-1 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 2) a b q0 hq0
        have h1 :
            colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b, (-1 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, (-1 : ZMod m)) 1)) =
              (((a, b, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 2)
            ((a, b, (-1 : ZMod m)))
        have h2 :
            colorMap (m := m) 2 (phiLayer (m := m) (a, b, (-1 : ZMod m)) 1) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have h3coord :
            splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) =
              (((a + 1, b, (1 : ZMod m)), (3 : ZMod m))) := by
          simpa [layer2Dir, KMap, hb2] using
            splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 2) a b
        have h3 :
            colorMap (m := m) 2 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h3iter :
            ((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 2)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m)) =
              (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 2)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m))
                = ((a + 1, b, (1 : ZMod m) + (((m - 3 : ℕ) : ZMod m))), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                    simpa using iterate_K2 (m := m) (m - 3) (a + 1) b (1 : ZMod m) (3 : ZMod m)
            _ = ((a + 1, b, (-2 : ZMod m)), (0 : ZMod m)) := by
                  rw [natCast_sub_three (m := m) hm]
                  ring
            _ = (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  ext <;> simp [R2, hqneg1, hb2] <;> ring
        calc
          ((colorMap (m := m) 2)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 2)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 2)^[m - 3]) (((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 2) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 2)^[m - 3]) (phiLayer (m := m) (a + 1, b, (1 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 2)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 2)^[m - 3]) ((a + 1, b, (1 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 2 (a + 1, b, (1 : ZMod m))
          _ = phiLayer (m := m) (R2 (m := m) (a, b, q0)) 0 := by
                rw [hk]
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a, b, (-1 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 2) a b q0 hq0
        have h1 :
            colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b, (-1 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, (-1 : ZMod m)) 1)) =
              (((a, b, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 2)
            ((a, b, (-1 : ZMod m)))
        have h2 :
            colorMap (m := m) 2 (phiLayer (m := m) (a, b, (-1 : ZMod m)) 1) =
              phiLayer (m := m) (a, b, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have h3coord :
            splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2)) =
              (((a, b, (1 : ZMod m)), (3 : ZMod m))) := by
          simpa [layer2Dir, KMap, hb2] using
            splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 2) a b
        have h3 :
            colorMap (m := m) 2 (phiLayer (m := m) (a, b, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a, b, (1 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h3iter :
            ((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a, b, (1 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 2)^[m - 3]) ((a, b, (1 : ZMod m)), (3 : ZMod m)) =
              (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 2)^[m - 3]) ((a, b, (1 : ZMod m)), (3 : ZMod m))
                = ((a, b, (1 : ZMod m) + (((m - 3 : ℕ) : ZMod m))), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                    simpa using iterate_K2 (m := m) (m - 3) a b (1 : ZMod m) (3 : ZMod m)
            _ = ((a, b, (-2 : ZMod m)), (0 : ZMod m)) := by
                  rw [natCast_sub_three (m := m) hm]
                  ring
            _ = (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  ext <;> simp [R2, hqneg1, hb2] <;> ring
        calc
          ((colorMap (m := m) 2)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 2)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 2)^[m - 3]) (((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 2) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 2)^[m - 3]) (phiLayer (m := m) (a, b, (1 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 2)^[m - 3]) ((a, b, (1 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 2)^[m - 3]) ((a, b, (1 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 2 (a, b, (1 : ZMod m))
          _ = phiLayer (m := m) (R2 (m := m) (a, b, q0)) 0 := by
                rw [hk]
    · have h1coord :
          splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0)) =
            (((a, b, q0), (1 : ZMod m))) := by
        simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun] using
          splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 2) a b q0 hq0
      have h1 :
          colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a, b, q0) 1 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
      have h2coord :
          splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 1)) =
            (((a, b, q0 + 1), (2 : ZMod m))) := by
        simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 2)
          ((a, b, q0))
      have h2 :
          colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0) 1) =
            phiLayer (m := m) (a, b, q0 + 1) 2 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
      have hq1ne : q0 + 1 ≠ (0 : ZMod m) := by
        intro hzero
        exact hqneg1 (eq_neg_iff_add_eq_zero.mpr hzero)
      have h3coord :
          splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0 + 1) 2)) =
            (((a, b, q0 + 2), (3 : ZMod m))) := by
        calc
          splitPointEquiv (m := m) (colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0 + 1) 2))
              = (((a, b, q0 + 1 + 1), (3 : ZMod m))) := by
                  simpa [KMap] using
                    splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 2)
                      ((a, b, q0 + 1)) hq1ne
          _ = (((a, b, q0 + 2), (3 : ZMod m))) := by
                congr 1
                ring
      have h3 :
          colorMap (m := m) 2 (phiLayer (m := m) (a, b, q0 + 1) 2) =
            phiLayer (m := m) (a, b, q0 + 2) 3 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
      have h3iter :
          ((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a, b, q0 + 2) 3 := by
        exact iterate_three_of_steps h1 h2 h3
      have hk :
          ((KMap (m := m) 2)^[m - 3]) ((a, b, q0 + 2), (3 : ZMod m)) =
            (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
        calc
          ((KMap (m := m) 2)^[m - 3]) ((a, b, q0 + 2), (3 : ZMod m))
              = ((a, b, q0 + 2 + (((m - 3 : ℕ) : ZMod m))), (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                  simpa using iterate_K2 (m := m) (m - 3) a b (q0 + 2) (3 : ZMod m)
          _ = ((a, b, q0 - 1), (0 : ZMod m)) := by
                rw [natCast_sub_three (m := m) hm]
                ring
          _ = (R2 (m := m) (a, b, q0), (0 : ZMod m)) := by
                simp [R2, hq0, hqneg1]
      calc
        ((colorMap (m := m) 2)^[m]) (phiLayer (m := m) (a, b, q0) 0)
            = ((colorMap (m := m) 2)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                rw [Nat.sub_add_cancel hm]
        _ = ((colorMap (m := m) 2)^[m - 3]) (((colorMap (m := m) 2)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
              simpa using Function.iterate_add_apply (colorMap (m := m) 2) (m - 3) 3
                (phiLayer (m := m) (a, b, q0) 0)
        _ = ((colorMap (m := m) 2)^[m - 3]) (phiLayer (m := m) (a, b, q0 + 2) 3) := by
              rw [h3iter]
        _ = phiLayer (m := m)
              (((KMap (m := m) 2)^[m - 3]) ((a, b, q0 + 2), (3 : ZMod m))).1
              (((KMap (m := m) 2)^[m - 3]) ((a, b, q0 + 2), (3 : ZMod m))).2 := by
                exact iterate_colorMap_phiLayer_three_max (m := m) 2 (a, b, q0 + 2)
        _ = phiLayer (m := m) (R2 (m := m) (a, b, q0)) 0 := by
              rw [hk]

theorem firstReturn_eq_R1 [Fact (2 < m)] (u : P0Coord m) :
    ((colorMap (m := m) 1)^[m]) (phiLayer (m := m) u 0) =
      phiLayer (m := m) (R1 (m := m) u) 0 := by
  have hm2 : 2 < m := Fact.out
  have hm : 3 ≤ m := by omega
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  letI : Fact (1 < m) := ⟨lt_trans (by decide : 1 < 2) hm2⟩
  rcases u with ⟨a, b, q0⟩
  by_cases hq0 : q0 = 0
  · have h1coord :
        splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0)) =
          (((a, b, (1 : ZMod m)), (1 : ZMod m))) := by
      simpa [phiLayer_zero, KMap, reverse, reverseFun, hq0] using
        splitPointEquiv_colorMap_phi_q_zero (m := m) (c := 1) a b
    have h1 :
        colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a, b, (1 : ZMod m)) 1 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
    have h2coord :
        splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a, b, (1 : ZMod m)) 1)) =
          (((a, b + 1, (1 : ZMod m)), (2 : ZMod m))) := by
      simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 1)
        ((a, b, (1 : ZMod m)))
    have h2 :
        colorMap (m := m) 1 (phiLayer (m := m) (a, b, (1 : ZMod m)) 1) =
          phiLayer (m := m) (a, b + 1, (1 : ZMod m)) 2 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
    have h1ne : (1 : ZMod m) ≠ 0 := one_ne_zero
    have h3coord :
        splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a, b + 1, (1 : ZMod m)) 2)) =
          (((a, b + 2, (1 : ZMod m)), (3 : ZMod m))) := by
      calc
        splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a, b + 1, (1 : ZMod m)) 2))
            = (((a, b + 1 + 1, (1 : ZMod m)), (3 : ZMod m))) := by
                simpa [KMap] using splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 1)
                  ((a, b + 1, (1 : ZMod m))) h1ne
        _ = (((a, b + 2, (1 : ZMod m)), (3 : ZMod m))) := by
              congr 1
              ring
    have h3 :
        colorMap (m := m) 1 (phiLayer (m := m) (a, b + 1, (1 : ZMod m)) 2) =
          phiLayer (m := m) (a, b + 2, (1 : ZMod m)) 3 := by
      exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
    have h3iter :
        ((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
          phiLayer (m := m) (a, b + 2, (1 : ZMod m)) 3 := by
      exact iterate_three_of_steps h1 h2 h3
    have hk :
        ((KMap (m := m) 1)^[m - 3]) ((a, b + 2, (1 : ZMod m)), (3 : ZMod m)) =
          (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
      calc
        ((KMap (m := m) 1)^[m - 3]) ((a, b + 2, (1 : ZMod m)), (3 : ZMod m))
            = ((a, b + 2 + (((m - 3 : ℕ) : ZMod m)), (1 : ZMod m)),
                (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                  simpa using iterate_K1 (m := m) (m - 3) a (b + 2) (1 : ZMod m) (3 : ZMod m)
        _ = ((a, b - 1, (1 : ZMod m)), (0 : ZMod m)) := by
              rw [natCast_sub_three (m := m) hm]
              ring
        _ = (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
              simp [R1, hq0]
    calc
      ((colorMap (m := m) 1)^[m]) (phiLayer (m := m) (a, b, q0) 0)
          = ((colorMap (m := m) 1)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
              rw [Nat.sub_add_cancel hm]
      _ = ((colorMap (m := m) 1)^[m - 3]) (((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
            simpa using Function.iterate_add_apply (colorMap (m := m) 1) (m - 3) 3
              (phiLayer (m := m) (a, b, q0) 0)
      _ = ((colorMap (m := m) 1)^[m - 3]) (phiLayer (m := m) (a, b + 2, (1 : ZMod m)) 3) := by
            rw [h3iter]
      _ = phiLayer (m := m)
            (((KMap (m := m) 1)^[m - 3]) ((a, b + 2, (1 : ZMod m)), (3 : ZMod m))).1
            (((KMap (m := m) 1)^[m - 3]) ((a, b + 2, (1 : ZMod m)), (3 : ZMod m))).2 := by
              exact iterate_colorMap_phiLayer_three_max (m := m) 1 (a, b + 2, (1 : ZMod m))
      _ = phiLayer (m := m) (R1 (m := m) (a, b, q0)) 0 := by
            rw [hk]
  · by_cases hqneg1 : q0 = (-1 : ZMod m)
    · by_cases haneg1 : a = (-1 : ZMod m)
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a + 1, b, (0 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 1) a b q0 hq0
        have h1 :
            colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b, (0 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b, (0 : ZMod m)) 1)) =
              (((a + 1, b + 1, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 1)
            ((a + 1, b, (0 : ZMod m)))
        have h2 :
            colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b, (0 : ZMod m)) 1) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have ha1zero : a + 1 = (0 : ZMod m) := by
          simpa [haneg1]
        have h3coord :
            splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2)) =
              (((a + 1, b + 1, (0 : ZMod m)), (3 : ZMod m))) := by
          simpa [layer2Dir, KMap, ha1zero] using
            splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 1) (a + 1) (b + 1)
        have h3 :
            colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h3iter :
            ((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 1, (0 : ZMod m)), (3 : ZMod m)) =
              (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 1, (0 : ZMod m)), (3 : ZMod m))
                = ((a + 1, b + 1 + (((m - 3 : ℕ) : ZMod m)), (0 : ZMod m)),
                    (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                      simpa using iterate_K1 (m := m) (m - 3) (a + 1) (b + 1) (0 : ZMod m) (3 : ZMod m)
            _ = ((a + 1, b - 2, (0 : ZMod m)), (0 : ZMod m)) := by
                  rw [natCast_sub_three (m := m) hm]
                  ring
            _ = (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  simp [R1, hq0, hqneg1, haneg1]
        calc
          ((colorMap (m := m) 1)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 1)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 1)^[m - 3]) (((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 1) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 1)^[m - 3]) (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 1, (0 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 1, (0 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 1 (a + 1, b + 1, (0 : ZMod m))
          _ = phiLayer (m := m) (R1 (m := m) (a, b, q0)) 0 := by
                rw [hk]
      · have h1coord :
            splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0)) =
              (((a + 1, b, (0 : ZMod m)), (1 : ZMod m))) := by
          simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun, hqneg1] using
            splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 1) a b q0 hq0
        have h1 :
            colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b, (0 : ZMod m)) 1 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
        have h2coord :
            splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b, (0 : ZMod m)) 1)) =
              (((a + 1, b + 1, (0 : ZMod m)), (2 : ZMod m))) := by
          simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 1)
            ((a + 1, b, (0 : ZMod m)))
        have h2 :
            colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b, (0 : ZMod m)) 1) =
              phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
        have ha1ne : a + 1 ≠ (0 : ZMod m) := by
          intro hzero
          exact haneg1 (eq_neg_iff_add_eq_zero.mpr hzero)
        have h3coord :
            splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2)) =
              (((a + 1, b + 2, (0 : ZMod m)), (3 : ZMod m))) := by
          calc
            splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2))
                = (((a + 1, b + 1 + 1, (0 : ZMod m)), (3 : ZMod m))) := by
                    simpa [layer2Dir, KMap, ha1ne] using
                      splitPointEquiv_colorMap_phiLayer_two_q_zero (m := m) (c := 1) (a + 1) (b + 1)
            _ = (((a + 1, b + 2, (0 : ZMod m)), (3 : ZMod m))) := by
                  congr 1
                  ring
        have h3 :
            colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, (0 : ZMod m)) 2) =
              phiLayer (m := m) (a + 1, b + 2, (0 : ZMod m)) 3 := by
          exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
        have h3iter :
            ((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
              phiLayer (m := m) (a + 1, b + 2, (0 : ZMod m)) 3 := by
          exact iterate_three_of_steps h1 h2 h3
        have hk :
            ((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, (0 : ZMod m)), (3 : ZMod m)) =
              (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
          calc
            ((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, (0 : ZMod m)), (3 : ZMod m))
                = ((a + 1, b + 2 + (((m - 3 : ℕ) : ZMod m)), (0 : ZMod m)),
                    (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                      simpa using iterate_K1 (m := m) (m - 3) (a + 1) (b + 2) (0 : ZMod m) (3 : ZMod m)
            _ = ((a + 1, b - 1, (0 : ZMod m)), (0 : ZMod m)) := by
                  rw [natCast_sub_three (m := m) hm]
                  ring
            _ = (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
                  simp [R1, hq0, hqneg1, haneg1]
        calc
          ((colorMap (m := m) 1)^[m]) (phiLayer (m := m) (a, b, q0) 0)
              = ((colorMap (m := m) 1)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                  rw [Nat.sub_add_cancel hm]
          _ = ((colorMap (m := m) 1)^[m - 3]) (((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
                simpa using Function.iterate_add_apply (colorMap (m := m) 1) (m - 3) 3
                  (phiLayer (m := m) (a, b, q0) 0)
          _ = ((colorMap (m := m) 1)^[m - 3]) (phiLayer (m := m) (a + 1, b + 2, (0 : ZMod m)) 3) := by
                rw [h3iter]
          _ = phiLayer (m := m)
                (((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, (0 : ZMod m)), (3 : ZMod m))).1
                (((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, (0 : ZMod m)), (3 : ZMod m))).2 := by
                  exact iterate_colorMap_phiLayer_three_max (m := m) 1 (a + 1, b + 2, (0 : ZMod m))
          _ = phiLayer (m := m) (R1 (m := m) (a, b, q0)) 0 := by
                rw [hk]
    · have h1coord :
          splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0)) =
            (((a + 1, b, q0 + 1), (1 : ZMod m))) := by
        simpa [phiLayer_zero, KMap, swap01Swap23, swap01Swap23Fun] using
          splitPointEquiv_colorMap_phi_q_ne_zero (m := m) (c := 1) a b q0 hq0
      have h1 :
          colorMap (m := m) 1 (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a + 1, b, q0 + 1) 1 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h1coord
      have h2coord :
          splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b, q0 + 1) 1)) =
            (((a + 1, b + 1, q0 + 1), (2 : ZMod m))) := by
        simpa [KMap] using splitPointEquiv_colorMap_phiLayer_one (m := m) (c := 1)
          ((a + 1, b, q0 + 1))
      have h2 :
          colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b, q0 + 1) 1) =
            phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h2coord
      have hq1ne : q0 + 1 ≠ (0 : ZMod m) := by
        intro hzero
        exact hqneg1 (eq_neg_iff_add_eq_zero.mpr hzero)
      have h3coord :
          splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2)) =
            (((a + 1, b + 2, q0 + 1), (3 : ZMod m))) := by
        calc
          splitPointEquiv (m := m) (colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2))
              = (((a + 1, b + 1 + 1, q0 + 1), (3 : ZMod m))) := by
                  simpa [KMap] using splitPointEquiv_colorMap_phiLayer_two_q_ne_zero (m := m) (c := 1)
                    ((a + 1, b + 1, q0 + 1)) hq1ne
          _ = (((a + 1, b + 2, q0 + 1), (3 : ZMod m))) := by
                congr 1
                ring
      have h3 :
          colorMap (m := m) 1 (phiLayer (m := m) (a + 1, b + 1, q0 + 1) 2) =
            phiLayer (m := m) (a + 1, b + 2, q0 + 1) 3 := by
        exact point_eq_phiLayer_of_splitPointEquiv_eq (m := m) h3coord
      have h3iter :
          ((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0) =
            phiLayer (m := m) (a + 1, b + 2, q0 + 1) 3 := by
        exact iterate_three_of_steps h1 h2 h3
      have hk :
          ((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, q0 + 1), (3 : ZMod m)) =
            (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
        calc
          ((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, q0 + 1), (3 : ZMod m))
              = ((a + 1, b + 2 + (((m - 3 : ℕ) : ZMod m)), q0 + 1),
                  (3 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) := by
                    simpa using iterate_K1 (m := m) (m - 3) (a + 1) (b + 2) (q0 + 1) (3 : ZMod m)
          _ = ((a + 1, b - 1, q0 + 1), (0 : ZMod m)) := by
                rw [natCast_sub_three (m := m) hm]
                ring
          _ = (R1 (m := m) (a, b, q0), (0 : ZMod m)) := by
                simp [R1, hq0, hqneg1]
      calc
        ((colorMap (m := m) 1)^[m]) (phiLayer (m := m) (a, b, q0) 0)
            = ((colorMap (m := m) 1)^[m - 3 + 3]) (phiLayer (m := m) (a, b, q0) 0) := by
                rw [Nat.sub_add_cancel hm]
        _ = ((colorMap (m := m) 1)^[m - 3]) (((colorMap (m := m) 1)^[3]) (phiLayer (m := m) (a, b, q0) 0)) := by
              simpa using Function.iterate_add_apply (colorMap (m := m) 1) (m - 3) 3
                (phiLayer (m := m) (a, b, q0) 0)
        _ = ((colorMap (m := m) 1)^[m - 3]) (phiLayer (m := m) (a + 1, b + 2, q0 + 1) 3) := by
              rw [h3iter]
        _ = phiLayer (m := m)
              (((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, q0 + 1), (3 : ZMod m))).1
              (((KMap (m := m) 1)^[m - 3]) ((a + 1, b + 2, q0 + 1), (3 : ZMod m))).2 := by
                exact iterate_colorMap_phiLayer_three_max (m := m) 1 (a + 1, b + 2, q0 + 1)
        _ = phiLayer (m := m) (R1 (m := m) (a, b, q0)) 0 := by
              rw [hk]

theorem firstReturn_eq_RMap [Fact (2 < m)] (c : Color) (u : P0Coord m) :
    ((colorMap (m := m) c)^[m]) (phiLayer (m := m) u 0) =
      phiLayer (m := m) (RMap (m := m) c u) 0 := by
  fin_cases c
  · simpa [RMap] using firstReturn_eq_R0 (m := m) u
  · simpa [RMap] using firstReturn_eq_R1 (m := m) u
  · simpa [RMap] using firstReturn_eq_R2 (m := m) u
  · simpa [RMap] using firstReturn_eq_R3 (m := m) u

end TorusD4
