import TorusD4.ReturnDynamics
import Mathlib.Tactic

namespace TorusD4

def G0 (x : P0Coord m) : P0Coord m :=
  let (a, b, q0) := x
  (a - 1, b + 1, q0 - 1)

def G1 (x : P0Coord m) : P0Coord m :=
  let (a, b, q0) := x
  (a + 1, b - 1, q0 + 1)

def G2 (x : P0Coord m) : P0Coord m :=
  let (a, b, q0) := x
  (a, b, q0 - 1)

def G3 (x : P0Coord m) : P0Coord m :=
  let (a, b, q0) := x
  (a, b, q0 + 1)

theorem natCast_ne_zero_of_pos_lt [Fact (1 < m)] {n : ℕ} (hn0 : 0 < n) (hnm : n < m) :
    ((n : ℕ) : ZMod m) ≠ 0 := by
  intro h
  exact Nat.not_dvd_of_pos_of_lt hn0 hnm ((ZMod.natCast_eq_zero_iff n m).1 h)

theorem cast_sub_one_eq_neg_one (hm : 1 ≤ m) : (((m - 1 : ℕ) : ZMod m)) = (-1 : ZMod m) := by
  rw [Nat.cast_sub hm]
  simp

theorem cast_sub_two_eq_neg_two (hm : 2 ≤ m) : (((m - 2 : ℕ) : ZMod m)) = (-2 : ZMod m) := by
  rw [Nat.cast_sub hm]
  simp

theorem neg_two_sub_nat_ne_zero [Fact (1 < m)] {n : ℕ} (hn : n < m - 2) :
    (-2 : ZMod m) - n ≠ 0 := by
  intro h
  have hzero : (((n + 2 : ℕ) : ZMod m)) = 0 := by
    apply neg_eq_zero.mp
    simpa [Nat.cast_add, sub_eq_add_neg, add_assoc, add_left_comm, add_comm] using h
  apply natCast_ne_zero_of_pos_lt (m := m) (n := n + 2) (by omega) (by omega)
  exact hzero

theorem neg_two_sub_nat_ne_neg_one [Fact (1 < m)] {n : ℕ} (hn : n < m - 2) :
    (-2 : ZMod m) - n ≠ (-1 : ZMod m) := by
  intro h
  have hstep : (-1 : ZMod m) - n = 0 := by
    have this := congrArg (fun z : ZMod m => z + 1) h
    ring_nf at this ⊢
    exact this
  have hzero : (((n + 1 : ℕ) : ZMod m)) = 0 := by
    have hneg : (-(((n + 1 : ℕ) : ZMod m))) = 0 := by
      simpa [Nat.cast_add, sub_eq_add_neg, add_assoc, add_left_comm, add_comm] using hstep
    exact neg_eq_zero.mp hneg
  apply natCast_ne_zero_of_pos_lt (m := m) (n := n + 1) (by omega) (by omega)
  exact hzero

theorem one_add_nat_ne_zero [Fact (1 < m)] {n : ℕ} (hn : n < m - 1) :
    (1 : ZMod m) + n ≠ 0 := by
  intro h
  have hzero : (((n + 1 : ℕ) : ZMod m)) = 0 := by
    simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using h
  apply natCast_ne_zero_of_pos_lt (m := m) (n := n + 1) (by omega) (by omega)
  exact hzero

theorem one_add_nat_ne_neg_one [Fact (1 < m)] {n : ℕ} (hn : n < m - 2) :
    (1 : ZMod m) + n ≠ (-1 : ZMod m) := by
  intro h
  have hstep : (2 : ZMod m) + n = 0 := by
    have this := congrArg (fun z : ZMod m => z + 1) h
    ring_nf at this ⊢
    exact this
  have hzero : (((n + 2 : ℕ) : ZMod m)) = 0 := by
    simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using hstep
  apply natCast_ne_zero_of_pos_lt (m := m) (n := n + 2) (by omega) (by omega)
  exact hzero

theorem iterate_G0 (n : ℕ) (a b q0 : ZMod m) :
    ((G0 (m := m)^[n]) (a, b, q0)) = (a - n, b + n, q0 - n) := by
  induction n generalizing a b q0 with
  | zero =>
      simp
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [G0, Nat.cast_add, sub_eq_add_neg] <;> ring

theorem iterate_G1 (n : ℕ) (a b q0 : ZMod m) :
    ((G1 (m := m)^[n]) (a, b, q0)) = (a + n, b - n, q0 + n) := by
  induction n generalizing a b q0 with
  | zero =>
      simp
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [G1, Nat.cast_add, sub_eq_add_neg] <;> ring

theorem iterate_G2 (n : ℕ) (a b q0 : ZMod m) :
    ((G2 (m := m)^[n]) (a, b, q0)) = (a, b, q0 - n) := by
  induction n generalizing a b q0 with
  | zero =>
      simp
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [G2, Nat.cast_add, sub_eq_add_neg] <;> ring

theorem iterate_G3 (n : ℕ) (a b q0 : ZMod m) :
    ((G3 (m := m)^[n]) (a, b, q0)) = (a, b, q0 + n) := by
  induction n generalizing a b q0 with
  | zero =>
      simp
  | succ n ih =>
      rw [Function.iterate_succ_apply', ih]
      ext <;> simp [G3, Nat.cast_add] <;> ring

theorem R0_eq_G0_of {a b q0 : ZMod m} (hq0 : q0 ≠ 0) (hq1 : q0 ≠ (-1 : ZMod m)) :
    R0 (m := m) (a, b, q0) = G0 (m := m) (a, b, q0) := by
  simp [R0, G0, hq0, hq1]

theorem R1_eq_G1_of {a b q0 : ZMod m} (hq0 : q0 ≠ 0) (hq1 : q0 ≠ (-1 : ZMod m)) :
    R1 (m := m) (a, b, q0) = G1 (m := m) (a, b, q0) := by
  simp [R1, G1, hq0, hq1]

theorem R2_eq_G2_of {a b q0 : ZMod m} (hq0 : q0 ≠ 0) (hq1 : q0 ≠ (-1 : ZMod m)) :
    R2 (m := m) (a, b, q0) = G2 (m := m) (a, b, q0) := by
  simp [R2, G2, hq0, hq1]

theorem R3_eq_G3_of {a b q0 : ZMod m} (hq0 : q0 ≠ 0) (hq1 : q0 ≠ (-1 : ZMod m)) :
    R3 (m := m) (a, b, q0) = G3 (m := m) (a, b, q0) := by
  simp [R3, G3, hq0, hq1]

theorem R0_sliceQ [Fact (1 < m)] (u : QCoord m) :
    R0 (m := m) (sliceQ (m := m) u) =
      (u.1 - 1 - delta m (u.2 = (1 : ZMod m)), u.2 + 1, (-2 : ZMod m)) := by
  rcases u with ⟨a, b⟩
  have hneg1 : (-1 : ZMod m) ≠ 0 := neg_ne_zero.mpr one_ne_zero
  by_cases hb : b = (1 : ZMod m)
  · simp [sliceQ, R0, delta, hneg1, hb]
    constructor <;> ring
  · simp [sliceQ, R0, delta, hneg1, hb]
    ring

theorem R1_sliceQ [Fact (1 < m)] (u : QCoord m) :
    R1 (m := m) (sliceQ (m := m) u) =
      (u.1 + 1, u.2 - 1 - delta m (u.1 = (-1 : ZMod m)), (0 : ZMod m)) := by
  rcases u with ⟨a, b⟩
  have hneg1 : (-1 : ZMod m) ≠ 0 := neg_ne_zero.mpr one_ne_zero
  by_cases ha : a = (-1 : ZMod m)
  · simp [sliceQ, R1, delta, hneg1, ha]
    ring
  · simp [sliceQ, R1, delta, hneg1, ha]

theorem R2_sliceQ [Fact (1 < m)] (u : QCoord m) :
    R2 (m := m) (sliceQ (m := m) u) =
      (u.1 + delta m (u.2 = (2 : ZMod m)), u.2, (-2 : ZMod m)) := by
  rcases u with ⟨a, b⟩
  have hneg1 : (-1 : ZMod m) ≠ 0 := neg_ne_zero.mpr one_ne_zero
  by_cases hb : b = (2 : ZMod m)
  · simp [sliceQ, R2, delta, hneg1, hb]
    ring
  · simp [sliceQ, R2, delta, hneg1, hb]
    ring

theorem R3_sliceQ [Fact (1 < m)] (u : QCoord m) :
    R3 (m := m) (sliceQ (m := m) u) =
      (u.1, u.2 + delta m (u.1 = (0 : ZMod m)), (0 : ZMod m)) := by
  rcases u with ⟨a, b⟩
  have hneg1 : (-1 : ZMod m) ≠ 0 := neg_ne_zero.mpr one_ne_zero
  by_cases ha : a = (0 : ZMod m)
  · simp [sliceQ, R3, delta, hneg1, ha]
  · simp [sliceQ, R3, delta, hneg1, ha]

@[simp] theorem R0_at_q0 (a b : ZMod m) :
    R0 (m := m) (a, b, (0 : ZMod m)) = (a - 1, b, (-1 : ZMod m)) := by
  simp [R0]

@[simp] theorem R1_at_q0 (a b : ZMod m) :
    R1 (m := m) (a, b, (0 : ZMod m)) = (a, b - 1, (1 : ZMod m)) := by
  simp [R1]

@[simp] theorem R2_at_q0 (a b : ZMod m) :
    R2 (m := m) (a, b, (0 : ZMod m)) = (a, b + 1, (-1 : ZMod m)) := by
  simp [R2]

@[simp] theorem R3_at_q0 (a b : ZMod m) :
    R3 (m := m) (a, b, (0 : ZMod m)) = (a + 1, b, (1 : ZMod m)) := by
  simp [R3]

theorem iterate_R0_from_neg2 [Fact (1 < m)] :
    ∀ n (a b : ZMod m), n ≤ m - 2 →
      ((R0 (m := m)^[n]) (a, b, (-2 : ZMod m))) = (a - n, b + n, (-2 : ZMod m) - n)
  | 0, a, b, _ => by simp
  | n + 1, a, b, hn => by
      have hn' : n < m - 2 := Nat.lt_of_succ_le hn
      rw [Function.iterate_succ_apply', iterate_R0_from_neg2 n a b (Nat.le_of_succ_le hn)]
      have hq0 : (-2 : ZMod m) - n ≠ 0 := neg_two_sub_nat_ne_zero (m := m) hn'
      have hq1 : (-2 : ZMod m) - n ≠ (-1 : ZMod m) := neg_two_sub_nat_ne_neg_one (m := m) hn'
      rw [R0_eq_G0_of (m := m) hq0 hq1]
      ext <;> simp [G0, Nat.cast_add, sub_eq_add_neg] <;> ring

theorem iterate_R1_from_pos1 [Fact (1 < m)] :
    ∀ n (a b : ZMod m), n ≤ m - 2 →
      ((R1 (m := m)^[n]) (a, b, (1 : ZMod m))) = (a + n, b - n, (1 : ZMod m) + n)
  | 0, a, b, _ => by simp
  | n + 1, a, b, hn => by
      have hn0 : n < m - 2 := Nat.lt_of_succ_le hn
      rw [Function.iterate_succ_apply', iterate_R1_from_pos1 n a b (Nat.le_of_succ_le hn)]
      have hq0 : (1 : ZMod m) + n ≠ 0 := by
        apply one_add_nat_ne_zero (m := m)
        omega
      have hq1 : (1 : ZMod m) + n ≠ (-1 : ZMod m) := one_add_nat_ne_neg_one (m := m) hn0
      rw [R1_eq_G1_of (m := m) hq0 hq1]
      ext <;> simp [G1, Nat.cast_add, sub_eq_add_neg] <;> ring

theorem iterate_R2_from_neg2 [Fact (1 < m)] :
    ∀ n (a b : ZMod m), n ≤ m - 2 →
      ((R2 (m := m)^[n]) (a, b, (-2 : ZMod m))) = (a, b, (-2 : ZMod m) - n)
  | 0, a, b, _ => by simp
  | n + 1, a, b, hn => by
      have hn' : n < m - 2 := Nat.lt_of_succ_le hn
      rw [Function.iterate_succ_apply', iterate_R2_from_neg2 n a b (Nat.le_of_succ_le hn)]
      have hq0 : (-2 : ZMod m) - n ≠ 0 := neg_two_sub_nat_ne_zero (m := m) hn'
      have hq1 : (-2 : ZMod m) - n ≠ (-1 : ZMod m) := neg_two_sub_nat_ne_neg_one (m := m) hn'
      rw [R2_eq_G2_of (m := m) hq0 hq1]
      ext <;> simp [G2, Nat.cast_add, sub_eq_add_neg] <;> ring

theorem iterate_R3_from_pos1 [Fact (1 < m)] :
    ∀ n (a b : ZMod m), n ≤ m - 2 →
      ((R3 (m := m)^[n]) (a, b, (1 : ZMod m))) = (a, b, (1 : ZMod m) + n)
  | 0, a, b, _ => by simp
  | n + 1, a, b, hn => by
      have hn0 : n < m - 2 := Nat.lt_of_succ_le hn
      rw [Function.iterate_succ_apply', iterate_R3_from_pos1 n a b (Nat.le_of_succ_le hn)]
      have hq0 : (1 : ZMod m) + n ≠ 0 := by
        apply one_add_nat_ne_zero (m := m)
        omega
      have hq1 : (1 : ZMod m) + n ≠ (-1 : ZMod m) := one_add_nat_ne_neg_one (m := m) hn0
      rw [R3_eq_G3_of (m := m) hq0 hq1]
      ext <;> simp [G3, Nat.cast_add] <;> ring

theorem iterate_m_R0_sliceQ_eq_sliceQ_T0 (hm : 3 ≤ m) (u : QCoord m) :
    ((R0 (m := m)^[m]) (sliceQ (m := m) u)) = sliceQ (m := m) (T0 (m := m) u) := by
  letI : Fact (1 < m) := ⟨by omega⟩
  have hm2 : 2 ≤ m := by omega
  have hm1a : m - 1 = (m - 2) + 1 := by omega
  have hm1b : 1 + (m - 1) = m := by omega
  rcases u with ⟨a, b⟩
  have hsplitPre :
      ((R0 (m := m)^[(m - 2) + 1]) (sliceQ (m := m) (a, b))) =
        ((R0 (m := m)^[m - 2]) (R0 (m := m) (sliceQ (m := m) (a, b)))) := by
    simpa using
      (Function.iterate_add_apply (R0 (m := m)) (m - 2) 1 (sliceQ (m := m) (a, b)))
  have hpre :
      ((R0 (m := m)^[m - 1]) (sliceQ (m := m) (a, b))) =
        ((R0 (m := m)^[m - 2]) (a - 1 - delta m (b = (1 : ZMod m)), b + 1, (-2 : ZMod m))) := by
    calc
      ((R0 (m := m)^[m - 1]) (sliceQ (m := m) (a, b)))
          = ((R0 (m := m)^[(m - 2) + 1]) (sliceQ (m := m) (a, b))) := by simp [hm1a]
      _ = ((R0 (m := m)^[m - 2]) (R0 (m := m) (sliceQ (m := m) (a, b)))) := hsplitPre
      _ = ((R0 (m := m)^[m - 2]) (a - 1 - delta m (b = (1 : ZMod m)), b + 1, (-2 : ZMod m))) := by
            rw [R0_sliceQ (m := m) (u := (a, b))]
  have hstate :
      ((R0 (m := m)^[m - 2]) (a - 1 - delta m (b = (1 : ZMod m)), b + 1, (-2 : ZMod m))) =
        (a + 1 - delta m (b = (1 : ZMod m)), b - 1, (0 : ZMod m)) := by
    rw [iterate_R0_from_neg2 (m := m) (m - 2) (a - 1 - delta m (b = (1 : ZMod m))) (b + 1) le_rfl]
    ext <;> simp [cast_sub_two_eq_neg_two (m := m) hm2] <;> ring
  have hsplit :
      ((R0 (m := m)^[1 + (m - 1)]) (sliceQ (m := m) (a, b))) =
        R0 (m := m) (((R0 (m := m)^[m - 1]) (sliceQ (m := m) (a, b)))) := by
    simpa using
      (Function.iterate_add_apply (R0 (m := m)) 1 (m - 1) (sliceQ (m := m) (a, b)))
  calc
    ((R0 (m := m)^[m]) (sliceQ (m := m) (a, b)))
        = ((R0 (m := m)^[1 + (m - 1)]) (sliceQ (m := m) (a, b))) := by simp [hm1b]
    _ = R0 (m := m) (((R0 (m := m)^[m - 1]) (sliceQ (m := m) (a, b)))) := hsplit
    _ = R0 (m := m) ((R0 (m := m)^[m - 2]) (a - 1 - delta m (b = (1 : ZMod m)), b + 1, (-2 : ZMod m))) := by
          rw [hpre]
    _ = R0 (m := m) (a + 1 - delta m (b = (1 : ZMod m)), b - 1, (0 : ZMod m)) := by
          rw [hstate]
    _ = (a - delta m (b = (1 : ZMod m)), b - 1, (-1 : ZMod m)) := by
          simp [R0]
          ring
    _ = sliceQ (m := m) (T0 (m := m) (a, b)) := by
          simp [sliceQ, T0]

theorem iterate_m_R1_sliceQ_eq_sliceQ_T1 (hm : 3 ≤ m) (u : QCoord m) :
    ((R1 (m := m)^[m]) (sliceQ (m := m) u)) = sliceQ (m := m) (T1 (m := m) u) := by
  letI : Fact (1 < m) := ⟨by omega⟩
  have hm2 : 2 ≤ m := by omega
  have hmSplit : (m - 2) + 2 = m := by omega
  rcases u with ⟨a, b⟩
  have htwo :
      ((R1 (m := m)^[2]) (sliceQ (m := m) (a, b))) =
        (a + 1, b - 1 - delta m (a = (-1 : ZMod m)) - 1, (1 : ZMod m)) := by
    calc
      ((R1 (m := m)^[2]) (sliceQ (m := m) (a, b)))
          = R1 (m := m) (R1 (m := m) (sliceQ (m := m) (a, b))) := by
              simpa using
                (Function.iterate_add_apply (R1 (m := m)) 1 1 (sliceQ (m := m) (a, b)))
      _ = R1 (m := m) (a + 1, b - 1 - delta m (a = (-1 : ZMod m)), (0 : ZMod m)) := by
            rw [R1_sliceQ (m := m) (u := (a, b))]
      _ = (a + 1, b - 1 - delta m (a = (-1 : ZMod m)) - 1, (1 : ZMod m)) := by
            simp [R1]
  have hsplit :
      ((R1 (m := m)^[(m - 2) + 2]) (sliceQ (m := m) (a, b))) =
        ((R1 (m := m)^[m - 2]) (((R1 (m := m)^[2]) (sliceQ (m := m) (a, b))))) := by
    simpa using
      (Function.iterate_add_apply (R1 (m := m)) (m - 2) 2 (sliceQ (m := m) (a, b)))
  have hiter :
      ((R1 (m := m)^[m - 2]) (a + 1, b - 1 - delta m (a = (-1 : ZMod m)) - 1, (1 : ZMod m))) =
        (a + 1 + ((m : ZMod m) - 2), b - 1 - delta m (a = (-1 : ZMod m)) - 1 - ((m : ZMod m) - 2),
          (1 : ZMod m) + ((m : ZMod m) - 2)) := by
    simpa [Nat.cast_sub hm2] using
      (iterate_R1_from_pos1 (m := m) (m - 2)
        (a + 1) (b - 1 - delta m (a = (-1 : ZMod m)) - 1) le_rfl)
  calc
    ((R1 (m := m)^[m]) (sliceQ (m := m) (a, b)))
        = ((R1 (m := m)^[(m - 2) + 2]) (sliceQ (m := m) (a, b))) := by simp [hmSplit]
    _ = ((R1 (m := m)^[m - 2]) (((R1 (m := m)^[2]) (sliceQ (m := m) (a, b))))) := hsplit
    _ = ((R1 (m := m)^[m - 2]) (a + 1, b - 1 - delta m (a = (-1 : ZMod m)) - 1, (1 : ZMod m))) := by
          rw [htwo]
    _ = (a + 1 + ((m : ZMod m) - 2), b - 1 - delta m (a = (-1 : ZMod m)) - 1 - ((m : ZMod m) - 2),
          (1 : ZMod m) + ((m : ZMod m) - 2)) := hiter
    _ = sliceQ (m := m) (T1 (m := m) (a, b)) := by
          ext <;> simp [sliceQ, T1] <;> ring

theorem iterate_m_R2_sliceQ_eq_sliceQ_T2 (hm : 3 ≤ m) (u : QCoord m) :
    ((R2 (m := m)^[m]) (sliceQ (m := m) u)) = sliceQ (m := m) (T2 (m := m) u) := by
  letI : Fact (1 < m) := ⟨by omega⟩
  have hm2 : 2 ≤ m := by omega
  have hm1a : m - 1 = (m - 2) + 1 := by omega
  have hm1b : 1 + (m - 1) = m := by omega
  rcases u with ⟨a, b⟩
  have hsplitPre :
      ((R2 (m := m)^[(m - 2) + 1]) (sliceQ (m := m) (a, b))) =
        ((R2 (m := m)^[m - 2]) (R2 (m := m) (sliceQ (m := m) (a, b)))) := by
    simpa using
      (Function.iterate_add_apply (R2 (m := m)) (m - 2) 1 (sliceQ (m := m) (a, b)))
  have hpre :
      ((R2 (m := m)^[m - 1]) (sliceQ (m := m) (a, b))) =
        ((R2 (m := m)^[m - 2]) (a + delta m (b = (2 : ZMod m)), b, (-2 : ZMod m))) := by
    calc
      ((R2 (m := m)^[m - 1]) (sliceQ (m := m) (a, b)))
          = ((R2 (m := m)^[(m - 2) + 1]) (sliceQ (m := m) (a, b))) := by simp [hm1a]
      _ = ((R2 (m := m)^[m - 2]) (R2 (m := m) (sliceQ (m := m) (a, b)))) := hsplitPre
      _ = ((R2 (m := m)^[m - 2]) (a + delta m (b = (2 : ZMod m)), b, (-2 : ZMod m))) := by
            rw [R2_sliceQ (m := m) (u := (a, b))]
  have hstate :
      ((R2 (m := m)^[m - 2]) (a + delta m (b = (2 : ZMod m)), b, (-2 : ZMod m))) =
        (a + delta m (b = (2 : ZMod m)), b, (0 : ZMod m)) := by
    rw [iterate_R2_from_neg2 (m := m) (m - 2) (a + delta m (b = (2 : ZMod m))) b le_rfl]
    ext <;> simp [cast_sub_two_eq_neg_two (m := m) hm2] <;> ring
  have hsplit :
      ((R2 (m := m)^[1 + (m - 1)]) (sliceQ (m := m) (a, b))) =
        R2 (m := m) (((R2 (m := m)^[m - 1]) (sliceQ (m := m) (a, b)))) := by
    simpa using
      (Function.iterate_add_apply (R2 (m := m)) 1 (m - 1) (sliceQ (m := m) (a, b)))
  calc
    ((R2 (m := m)^[m]) (sliceQ (m := m) (a, b)))
        = ((R2 (m := m)^[1 + (m - 1)]) (sliceQ (m := m) (a, b))) := by simp [hm1b]
    _ = R2 (m := m) (((R2 (m := m)^[m - 1]) (sliceQ (m := m) (a, b)))) := hsplit
    _ = R2 (m := m) ((R2 (m := m)^[m - 2]) (a + delta m (b = (2 : ZMod m)), b, (-2 : ZMod m))) := by
          rw [hpre]
    _ = R2 (m := m) (a + delta m (b = (2 : ZMod m)), b, (0 : ZMod m)) := by
          rw [hstate]
    _ = (a + delta m (b = (2 : ZMod m)), b + 1, (-1 : ZMod m)) := by
          simp [R2]
    _ = sliceQ (m := m) (T2 (m := m) (a, b)) := by
          simp [sliceQ, T2]

theorem iterate_m_R3_sliceQ_eq_sliceQ_T3 (hm : 3 ≤ m) (u : QCoord m) :
    ((R3 (m := m)^[m]) (sliceQ (m := m) u)) = sliceQ (m := m) (T3 (m := m) u) := by
  letI : Fact (1 < m) := ⟨by omega⟩
  have hm2 : 2 ≤ m := by omega
  have hmSplit : (m - 2) + 2 = m := by omega
  rcases u with ⟨a, b⟩
  have htwo :
      ((R3 (m := m)^[2]) (sliceQ (m := m) (a, b))) =
        (a + 1, b + delta m (a = (0 : ZMod m)), (1 : ZMod m)) := by
    calc
      ((R3 (m := m)^[2]) (sliceQ (m := m) (a, b)))
          = R3 (m := m) (R3 (m := m) (sliceQ (m := m) (a, b))) := by
              simpa using
                (Function.iterate_add_apply (R3 (m := m)) 1 1 (sliceQ (m := m) (a, b)))
      _ = R3 (m := m) (a, b + delta m (a = (0 : ZMod m)), (0 : ZMod m)) := by
            rw [R3_sliceQ (m := m) (u := (a, b))]
      _ = (a + 1, b + delta m (a = (0 : ZMod m)), (1 : ZMod m)) := by
            simp [R3]
  have hsplit :
      ((R3 (m := m)^[(m - 2) + 2]) (sliceQ (m := m) (a, b))) =
        ((R3 (m := m)^[m - 2]) (((R3 (m := m)^[2]) (sliceQ (m := m) (a, b))))) := by
    simpa using
      (Function.iterate_add_apply (R3 (m := m)) (m - 2) 2 (sliceQ (m := m) (a, b)))
  have hiter :
      ((R3 (m := m)^[m - 2]) (a + 1, b + delta m (a = (0 : ZMod m)), (1 : ZMod m))) =
        (a + 1, b + delta m (a = (0 : ZMod m)), (1 : ZMod m) + ((m : ZMod m) - 2)) := by
    simpa [Nat.cast_sub hm2] using
      (iterate_R3_from_pos1 (m := m) (m - 2)
        (a + 1) (b + delta m (a = (0 : ZMod m))) le_rfl)
  calc
    ((R3 (m := m)^[m]) (sliceQ (m := m) (a, b)))
        = ((R3 (m := m)^[(m - 2) + 2]) (sliceQ (m := m) (a, b))) := by simp [hmSplit]
    _ = ((R3 (m := m)^[m - 2]) (((R3 (m := m)^[2]) (sliceQ (m := m) (a, b))))) := hsplit
    _ = ((R3 (m := m)^[m - 2]) (a + 1, b + delta m (a = (0 : ZMod m)), (1 : ZMod m))) := by
          rw [htwo]
    _ = (a + 1, b + delta m (a = (0 : ZMod m)), (1 : ZMod m) + ((m : ZMod m) - 2)) := hiter
    _ = sliceQ (m := m) (T3 (m := m) (a, b)) := by
          ext <;> simp [sliceQ, T3] <;> ring

theorem iterate_m_sliceQ_eq_sliceQ_TMap (hm : 3 ≤ m) (c : Color) (u : QCoord m) :
    ((RMap (m := m) c)^[m]) (sliceQ (m := m) u) = sliceQ (m := m) (TMap (m := m) c u) := by
  fin_cases c
  · simpa [RMap, TMap] using iterate_m_R0_sliceQ_eq_sliceQ_T0 (m := m) hm u
  · simpa [RMap, TMap] using iterate_m_R1_sliceQ_eq_sliceQ_T1 (m := m) hm u
  · simpa [RMap, TMap] using iterate_m_R2_sliceQ_eq_sliceQ_T2 (m := m) hm u
  · simpa [RMap, TMap] using iterate_m_R3_sliceQ_eq_sliceQ_T3 (m := m) hm u

theorem secondReturnOfRMap_eq_TMap (hm : 3 ≤ m) (c : Color) (u : QCoord m) :
    secondReturnOfRMap (m := m) c u = TMap (m := m) c u := by
  have h := iterate_m_sliceQ_eq_sliceQ_TMap (m := m) hm c u
  simpa [secondReturnOfRMap] using congrArg (abCoord (m := m)) h

end TorusD4
