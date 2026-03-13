import TorusD3Odometer.Color1FullCaseI

namespace TorusD3Odometer

open TorusD4

theorem natCast_ne_natCast_of_lt [Fact (0 < m)] {a b : ℕ}
    (ha : a < m) (hb : b < m) (hab : a ≠ b) :
    ((a : ℕ) : ZMod m) ≠ ((b : ℕ) : ZMod m) := by
  intro h
  have h' : a % m = b % m := (ZMod.natCast_eq_natCast_iff' a b m).1 h
  rw [Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] at h'
  exact hab h'

def dir1FromLayerZero (dir0 : P0Coord m → Color) (z : FullCoord m) : Color :=
  let (u, s) := z
  if s = 0 then
    dir0 u
  else if s = 1 then
    0
  else
    1

def fullMapColor1 (dir0 : P0Coord m → Color) (z : FullCoord m) : FullCoord m :=
  KMap (m := m) (dir1FromLayerZero (m := m) dir0 z) z

def returnMapColor1 (dir0 : P0Coord m → Color) (u : P0Coord m) : P0Coord m :=
  match dir0 u with
  | 0 => (u.1 + 2, u.2)
  | 1 => (u.1 + 1, u.2)
  | _ => (u.1 + 1, u.2 + 1)

@[simp] theorem fullMapColor1_snd (dir0 : P0Coord m → Color) (z : FullCoord m) :
    (fullMapColor1 (m := m) dir0 z).2 = z.2 + 1 := by
  simp [fullMapColor1, KMap_snd]

theorem fullMapColor1_of_s_ne_zero_one (dir0 : P0Coord m → Color) {u : P0Coord m} {s : ZMod m}
    (hs0 : s ≠ 0) (hs1 : s ≠ 1) :
    fullMapColor1 (m := m) dir0 (u, s) = KMap (m := m) 1 (u, s) := by
  simp [fullMapColor1, dir1FromLayerZero, hs0, hs1]

theorem iterate_fullMapColor1_from_two [Fact (5 < m)] (dir0 : P0Coord m → Color) :
    ∀ n u, n ≤ m - 2 →
      ((fullMapColor1 (m := m) dir0)^[n]) (u, (2 : ZMod m)) =
        ((KMap (m := m) 1)^[n]) (u, (2 : ZMod m))
  | 0, u, _ => by simp
  | n + 1, u, hn => by
      have hcur_lt : n + 2 < m := by
        have hm5 : 5 < m := Fact.out
        omega
      have hn' : n ≤ m - 2 := Nat.le_of_succ_le hn
      have hs0 : (2 : ZMod m) + n ≠ 0 := by
        simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
          natCast_ne_zero_of_pos_lt (m := m) (n := n + 2) (by omega) hcur_lt
      have hs1 : (2 : ZMod m) + n ≠ 1 := by
        simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
          natCast_ne_one_of_two_le_lt (m := m) (n := n + 2) (by omega) hcur_lt
      calc
        ((fullMapColor1 (m := m) dir0)^[n + 1]) (u, (2 : ZMod m))
            = fullMapColor1 (m := m) dir0 (((fullMapColor1 (m := m) dir0)^[n]) (u, (2 : ZMod m))) := by
                rw [Function.iterate_succ_apply']
        _ = fullMapColor1 (m := m) dir0 (((KMap (m := m) 1)^[n]) (u, (2 : ZMod m))) := by
              rw [iterate_fullMapColor1_from_two (m := m) dir0 n u hn']
        _ = fullMapColor1 (m := m) dir0 (u, (2 : ZMod m) + n) := by
              rw [iterate_KMap1]
        _ = KMap (m := m) 1 (u, (2 : ZMod m) + n) := by
              simpa using fullMapColor1_of_s_ne_zero_one (m := m) dir0 (u := u) hs0 hs1
        _ = ((KMap (m := m) 1)^[n + 1]) (u, (2 : ZMod m)) := by
              symm
              rw [Function.iterate_succ_apply', iterate_KMap1]

theorem iterate_m_sub_two_fullMapColor1 [Fact (5 < m)] (dir0 : P0Coord m → Color) (u : P0Coord m) :
    (((fullMapColor1 (m := m) dir0)^[m - 2]) (u, (2 : ZMod m))) = slicePoint (0 : ZMod m) u := by
  have hm2 : 2 ≤ m := by
    have hm5 : 5 < m := Fact.out
    omega
  calc
    (((fullMapColor1 (m := m) dir0)^[m - 2]) (u, (2 : ZMod m)))
        = ((KMap (m := m) 1)^[m - 2]) (u, (2 : ZMod m)) := by
            rw [iterate_fullMapColor1_from_two (m := m) dir0 (m - 2) u le_rfl]
    _ = (u, (2 : ZMod m) + (((m - 2 : ℕ) : ZMod m))) := by
          rw [iterate_KMap1]
    _ = slicePoint (0 : ZMod m) u := by
          ext <;> simp [slicePoint, Nat.cast_sub hm2]
          all_goals ring

theorem fullMapColor1_step_zero_of_dir0 (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 0) :
    fullMapColor1 (m := m) dir0 (slicePoint (0 : ZMod m) u) = ((u.1 + 1, u.2), (1 : ZMod m)) := by
  simp [fullMapColor1, dir1FromLayerZero, hdir, KMap, slicePoint]

theorem fullMapColor1_step_zero_of_dir1 (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 1) :
    fullMapColor1 (m := m) dir0 (slicePoint (0 : ZMod m) u) = (u, (1 : ZMod m)) := by
  simp [fullMapColor1, dir1FromLayerZero, hdir, KMap, slicePoint]

theorem fullMapColor1_step_zero_of_dir2 (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 2) :
    fullMapColor1 (m := m) dir0 (slicePoint (0 : ZMod m) u) = ((u.1, u.2 + 1), (1 : ZMod m)) := by
  simp [fullMapColor1, dir1FromLayerZero, hdir, KMap, slicePoint]

theorem fullMapColor1_step_one [Fact (5 < m)] (dir0 : P0Coord m → Color) (u : P0Coord m) :
    fullMapColor1 (m := m) dir0 (u, (1 : ZMod m)) = ((u.1 + 1, u.2), (2 : ZMod m)) := by
  ext <;> simp [fullMapColor1, dir1FromLayerZero, KMap, one_ne_zero (m := m)]
  ring

theorem iterate_two_fullMapColor1_of_dir0 [Fact (5 < m)] (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 0) :
    (((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u)) =
      ((u.1 + 2, u.2), (2 : ZMod m)) := by
  calc
    (((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u))
        = fullMapColor1 (m := m) dir0 (fullMapColor1 (m := m) dir0 (slicePoint (0 : ZMod m) u)) := by
            simp [Function.iterate_succ_apply']
    _ = fullMapColor1 (m := m) dir0 (((u.1 + 1, u.2), (1 : ZMod m))) := by
          rw [fullMapColor1_step_zero_of_dir0 (m := m) dir0 hdir]
    _ = ((u.1 + 2, u.2), (2 : ZMod m)) := by
          rw [fullMapColor1_step_one (m := m) dir0 (u := (u.1 + 1, u.2))]
          ring

theorem iterate_two_fullMapColor1_of_dir1 [Fact (5 < m)] (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 1) :
    (((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u)) =
      ((u.1 + 1, u.2), (2 : ZMod m)) := by
  calc
    (((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u))
        = fullMapColor1 (m := m) dir0 (fullMapColor1 (m := m) dir0 (slicePoint (0 : ZMod m) u)) := by
            simp [Function.iterate_succ_apply']
    _ = fullMapColor1 (m := m) dir0 (u, (1 : ZMod m)) := by
          rw [fullMapColor1_step_zero_of_dir1 (m := m) dir0 hdir]
    _ = ((u.1 + 1, u.2), (2 : ZMod m)) := by
          simpa using fullMapColor1_step_one (m := m) dir0 u

theorem iterate_two_fullMapColor1_of_dir2 [Fact (5 < m)] (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 2) :
    (((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u)) =
      ((u.1 + 1, u.2 + 1), (2 : ZMod m)) := by
  calc
    (((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u))
        = fullMapColor1 (m := m) dir0 (fullMapColor1 (m := m) dir0 (slicePoint (0 : ZMod m) u)) := by
            simp [Function.iterate_succ_apply']
    _ = fullMapColor1 (m := m) dir0 (((u.1, u.2 + 1), (1 : ZMod m))) := by
          rw [fullMapColor1_step_zero_of_dir2 (m := m) dir0 hdir]
    _ = ((u.1 + 1, u.2 + 1), (2 : ZMod m)) := by
          simpa using fullMapColor1_step_one (m := m) dir0 (u := (u.1, u.2 + 1))

theorem iterate_m_fullMapColor1_of_dir0 [Fact (5 < m)] (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 0) :
    (((fullMapColor1 (m := m) dir0)^[m]) (slicePoint (0 : ZMod m) u)) =
      slicePoint (0 : ZMod m) (u.1 + 2, u.2) := by
  have hm2 : 2 ≤ m := by
    have hm5 : 5 < m := Fact.out
    omega
  calc
    (((fullMapColor1 (m := m) dir0)^[m]) (slicePoint (0 : ZMod m) u))
        = (((fullMapColor1 (m := m) dir0)^[m - 2])
            ((((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u)))) := by
              simpa [Nat.sub_add_cancel hm2] using
                (Function.iterate_add_apply (f := fullMapColor1 (m := m) dir0) (m := m - 2) (n := 2)
                  (slicePoint (0 : ZMod m) u))
    _ = (((fullMapColor1 (m := m) dir0)^[m - 2]) (((u.1 + 2, u.2), (2 : ZMod m)))) := by
          rw [iterate_two_fullMapColor1_of_dir0 (m := m) dir0 hdir]
    _ = slicePoint (0 : ZMod m) (u.1 + 2, u.2) := iterate_m_sub_two_fullMapColor1 (m := m) dir0 _

theorem iterate_m_fullMapColor1_of_dir1 [Fact (5 < m)] (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 1) :
    (((fullMapColor1 (m := m) dir0)^[m]) (slicePoint (0 : ZMod m) u)) =
      slicePoint (0 : ZMod m) (u.1 + 1, u.2) := by
  have hm2 : 2 ≤ m := by
    have hm5 : 5 < m := Fact.out
    omega
  calc
    (((fullMapColor1 (m := m) dir0)^[m]) (slicePoint (0 : ZMod m) u))
        = (((fullMapColor1 (m := m) dir0)^[m - 2])
            ((((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u)))) := by
              simpa [Nat.sub_add_cancel hm2] using
                (Function.iterate_add_apply (f := fullMapColor1 (m := m) dir0) (m := m - 2) (n := 2)
                  (slicePoint (0 : ZMod m) u))
    _ = (((fullMapColor1 (m := m) dir0)^[m - 2]) (((u.1 + 1, u.2), (2 : ZMod m)))) := by
          rw [iterate_two_fullMapColor1_of_dir1 (m := m) dir0 hdir]
    _ = slicePoint (0 : ZMod m) (u.1 + 1, u.2) := iterate_m_sub_two_fullMapColor1 (m := m) dir0 _

theorem iterate_m_fullMapColor1_of_dir2 [Fact (5 < m)] (dir0 : P0Coord m → Color) {u : P0Coord m}
    (hdir : dir0 u = 2) :
    (((fullMapColor1 (m := m) dir0)^[m]) (slicePoint (0 : ZMod m) u)) =
      slicePoint (0 : ZMod m) (u.1 + 1, u.2 + 1) := by
  have hm2 : 2 ≤ m := by
    have hm5 : 5 < m := Fact.out
    omega
  calc
    (((fullMapColor1 (m := m) dir0)^[m]) (slicePoint (0 : ZMod m) u))
        = (((fullMapColor1 (m := m) dir0)^[m - 2])
            ((((fullMapColor1 (m := m) dir0)^[2]) (slicePoint (0 : ZMod m) u)))) := by
              simpa [Nat.sub_add_cancel hm2] using
                (Function.iterate_add_apply (f := fullMapColor1 (m := m) dir0) (m := m - 2) (n := 2)
                  (slicePoint (0 : ZMod m) u))
    _ = (((fullMapColor1 (m := m) dir0)^[m - 2]) (((u.1 + 1, u.2 + 1), (2 : ZMod m)))) := by
          rw [iterate_two_fullMapColor1_of_dir2 (m := m) dir0 hdir]
    _ = slicePoint (0 : ZMod m) (u.1 + 1, u.2 + 1) := iterate_m_sub_two_fullMapColor1 (m := m) dir0 _

theorem iterate_m_fullMapColor1_slicePoint_zero [Fact (5 < m)] (dir0 : P0Coord m → Color) (u : P0Coord m) :
    (((fullMapColor1 (m := m) dir0)^[m]) (slicePoint (0 : ZMod m) u)) =
      slicePoint (0 : ZMod m) (returnMapColor1 (m := m) dir0 u) := by
  by_cases hdir0 : dir0 u = 0
  · simpa [returnMapColor1, hdir0] using iterate_m_fullMapColor1_of_dir0 (m := m) dir0 (u := u) hdir0
  by_cases hdir1 : dir0 u = 1
  · simpa [returnMapColor1, hdir0, hdir1] using iterate_m_fullMapColor1_of_dir1 (m := m) dir0 (u := u) hdir1
  have hdir2 : dir0 u = 2 := by
    apply Fin.ext
    have hlt : (dir0 u).1 < 3 := (dir0 u).2
    interval_cases hval : (dir0 u).1
    · exact False.elim (hdir0 (Fin.ext hval))
    · exact False.elim (hdir1 (Fin.ext hval))
    · rfl
  simpa [returnMapColor1, hdir0, hdir1, hdir2] using
    iterate_m_fullMapColor1_of_dir2 (m := m) dir0 (u := u) hdir2

def dir1CaseIILayerZero (u : P0Coord m) : Color :=
  let i : ZMod m := u.1
  let k : ZMod m := u.2
  if (i = 0 ∧ k = 0) ∨
      (i + k = (-1 : ZMod m) ∧ i ≠ 0 ∧ i ≠ (1 : ZMod m) ∧ i ≠ (-2 : ZMod m) ∧ i ≠ (-1 : ZMod m)) ∨
      (i = (1 : ZMod m) ∧ k = 0) ∨
      (i = (-2 : ZMod m) ∧ k = 0) ∨
      (i = (-1 : ZMod m) ∧ k = (-1 : ZMod m)) then
    0
  else if (i = 0 ∧ k ≠ 0 ∧ k ≠ (-1 : ZMod m)) ∨
      (i = (1 : ZMod m) ∧ k ≠ 0) ∨
      (i = (2 : ZMod m) ∧ k = (-2 : ZMod m)) ∨
      (i = (2 : ZMod m) ∧ k = (-1 : ZMod m)) ∨
      (i = (-2 : ZMod m) ∧ k = (1 : ZMod m)) then
    1
  else
    2

def dir1CaseII (z : FullCoord m) : Color :=
  dir1FromLayerZero (m := m) (dir1CaseIILayerZero (m := m)) z

def fullMap1CaseII (z : FullCoord m) : FullCoord m :=
  fullMapColor1 (m := m) (dir1CaseIILayerZero (m := m)) z

def returnMap1CaseII (u : P0Coord m) : P0Coord m :=
  returnMapColor1 (m := m) (dir1CaseIILayerZero (m := m)) u

@[simp] theorem fullMap1CaseII_snd (z : FullCoord m) :
    (fullMap1CaseII (m := m) z).2 = z.2 + 1 := by
  simpa [fullMap1CaseII] using
    fullMapColor1_snd (m := m) (dir0 := dir1CaseIILayerZero (m := m)) z

theorem iterate_m_fullMap1CaseII_slicePoint_zero [Fact (5 < m)] (u : P0Coord m) :
    ((fullMap1CaseII (m := m)^[m]) (slicePoint (0 : ZMod m) u)) =
      slicePoint (0 : ZMod m) (returnMap1CaseII (m := m) u) := by
  simpa [fullMap1CaseII, returnMap1CaseII] using
    iterate_m_fullMapColor1_slicePoint_zero (m := m) (dir1CaseIILayerZero (m := m)) u

theorem dir1CaseIILayerZero_eq_zero_origin :
    dir1CaseIILayerZero (m := m) ((0 : ZMod m), (0 : ZMod m)) = 0 := by
  simp [dir1CaseIILayerZero]

theorem dir1CaseIILayerZero_eq_zero_one_zero :
    dir1CaseIILayerZero (m := m) ((1 : ZMod m), (0 : ZMod m)) = 0 := by
  simp [dir1CaseIILayerZero]

theorem dir1CaseIILayerZero_eq_zero_neg_two_zero :
    dir1CaseIILayerZero (m := m) ((-2 : ZMod m), (0 : ZMod m)) = 0 := by
  simp [dir1CaseIILayerZero]

theorem dir1CaseIILayerZero_eq_zero_neg_one_neg_one :
    dir1CaseIILayerZero (m := m) ((-1 : ZMod m), (-1 : ZMod m)) = 0 := by
  simp [dir1CaseIILayerZero]

theorem dir1CaseIILayerZero_eq_one_of_i_zero {k : ZMod m}
    (hk0 : k ≠ 0) (hkneg1 : k ≠ (-1 : ZMod m)) :
    dir1CaseIILayerZero (m := m) ((0 : ZMod m), k) = 1 := by
  simp [dir1CaseIILayerZero, hk0, hkneg1]

theorem returnMap1CaseII_origin :
    returnMap1CaseII (m := m) ((0 : ZMod m), (0 : ZMod m)) = ((2 : ZMod m), (0 : ZMod m)) := by
  simp [returnMap1CaseII, returnMapColor1, dir1CaseIILayerZero_eq_zero_origin (m := m)]

theorem returnMap1CaseII_one_zero :
    returnMap1CaseII (m := m) ((1 : ZMod m), (0 : ZMod m)) = ((3 : ZMod m), (0 : ZMod m)) := by
  ext <;> simp [returnMap1CaseII, returnMapColor1, dir1CaseIILayerZero_eq_zero_one_zero (m := m)]
  norm_num

theorem returnMap1CaseII_neg_two_zero :
    returnMap1CaseII (m := m) ((-2 : ZMod m), (0 : ZMod m)) = ((0 : ZMod m), (0 : ZMod m)) := by
  simp [returnMap1CaseII, returnMapColor1, dir1CaseIILayerZero_eq_zero_neg_two_zero (m := m)]

theorem dir1CaseIILayerZero_eq_two_of_not_special {i k : ZMod m}
    (h00 : ¬ (i = 0 ∧ k = 0))
    (hdiag : ¬ (i + k = (-1 : ZMod m) ∧
      i ≠ 0 ∧ i ≠ (1 : ZMod m) ∧ i ≠ (-2 : ZMod m) ∧ i ≠ (-1 : ZMod m)))
    (h10 : ¬ (i = (1 : ZMod m) ∧ k = 0))
    (hneg20 : ¬ (i = (-2 : ZMod m) ∧ k = 0))
    (hneg1neg1 : ¬ (i = (-1 : ZMod m) ∧ k = (-1 : ZMod m)))
    (h0line : ¬ (i = 0 ∧ k ≠ 0 ∧ k ≠ (-1 : ZMod m)))
    (h1line : ¬ (i = (1 : ZMod m) ∧ k ≠ 0))
    (h2neg2 : ¬ (i = (2 : ZMod m) ∧ k = (-2 : ZMod m)))
    (h2neg1 : ¬ (i = (2 : ZMod m) ∧ k = (-1 : ZMod m)))
    (hneg2one : ¬ (i = (-2 : ZMod m) ∧ k = (1 : ZMod m))) :
    dir1CaseIILayerZero (m := m) (i, k) = 2 := by
  simp [dir1CaseIILayerZero, h00, hdiag, h10, hneg20, hneg1neg1,
    h0line, h1line, h2neg2, h2neg1, hneg2one]

theorem returnMap1CaseII_eq_bulk_of_not_special {i k : ZMod m}
    (h00 : ¬ (i = 0 ∧ k = 0))
    (hdiag : ¬ (i + k = (-1 : ZMod m) ∧
      i ≠ 0 ∧ i ≠ (1 : ZMod m) ∧ i ≠ (-2 : ZMod m) ∧ i ≠ (-1 : ZMod m)))
    (h10 : ¬ (i = (1 : ZMod m) ∧ k = 0))
    (hneg20 : ¬ (i = (-2 : ZMod m) ∧ k = 0))
    (hneg1neg1 : ¬ (i = (-1 : ZMod m) ∧ k = (-1 : ZMod m)))
    (h0line : ¬ (i = 0 ∧ k ≠ 0 ∧ k ≠ (-1 : ZMod m)))
    (h1line : ¬ (i = (1 : ZMod m) ∧ k ≠ 0))
    (h2neg2 : ¬ (i = (2 : ZMod m) ∧ k = (-2 : ZMod m)))
    (h2neg1 : ¬ (i = (2 : ZMod m) ∧ k = (-1 : ZMod m)))
    (hneg2one : ¬ (i = (-2 : ZMod m) ∧ k = (1 : ZMod m))) :
    returnMap1CaseII (m := m) (i, k) = bulkMap1CaseI (m := m) (i, k) := by
  simp [returnMap1CaseII, returnMapColor1, bulkMap1CaseI,
    dir1CaseIILayerZero_eq_two_of_not_special (m := m)
      h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one]

theorem dir1CaseIILayerZero_eq_zero_of_diag {i k : ZMod m}
    (hdiag : i + k = (-1 : ZMod m)) (hi0 : i ≠ 0) (hi1 : i ≠ (1 : ZMod m))
    (hineg2 : i ≠ (-2 : ZMod m)) (hineg1 : i ≠ (-1 : ZMod m)) :
    dir1CaseIILayerZero (m := m) (i, k) = 0 := by
  simp [dir1CaseIILayerZero, hdiag, hi0, hi1, hineg2, hineg1]

theorem returnMap1CaseII_eq_add_two_of_diag {i k : ZMod m}
    (hdiag : i + k = (-1 : ZMod m)) (hi0 : i ≠ 0) (hi1 : i ≠ (1 : ZMod m))
    (hineg2 : i ≠ (-2 : ZMod m)) (hineg1 : i ≠ (-1 : ZMod m)) :
    returnMap1CaseII (m := m) (i, k) = (i + 2, k) := by
  simp [returnMap1CaseII, returnMapColor1,
    dir1CaseIILayerZero_eq_zero_of_diag (m := m) hdiag hi0 hi1 hineg2 hineg1]

theorem returnMap1CaseII_eq_add_one_of_i_zero {k : ZMod m}
    (hk0 : k ≠ 0) (hkneg1 : k ≠ (-1 : ZMod m)) :
    returnMap1CaseII (m := m) ((0 : ZMod m), k) = ((1 : ZMod m), k) := by
  simp [returnMap1CaseII, returnMapColor1,
    dir1CaseIILayerZero_eq_one_of_i_zero (m := m) hk0 hkneg1]

theorem dir1CaseIILayerZero_eq_one_of_i_one [Fact (5 < m)] {k : ZMod m} (hk0 : k ≠ 0) :
    dir1CaseIILayerZero (m := m) ((1 : ZMod m), k) = 1 := by
  simp [dir1CaseIILayerZero, hk0, one_ne_zero (m := m), one_ne_neg_one (m := m)]

theorem returnMap1CaseII_eq_add_one_of_i_one [Fact (5 < m)] {k : ZMod m} (hk0 : k ≠ 0) :
    returnMap1CaseII (m := m) ((1 : ZMod m), k) = ((2 : ZMod m), k) := by
  ext <;> simp [returnMap1CaseII, returnMapColor1,
    dir1CaseIILayerZero_eq_one_of_i_one (m := m) hk0]
  norm_num

theorem dir1CaseIILayerZero_eq_one_two_neg_two [Fact (5 < m)] :
    dir1CaseIILayerZero (m := m) ((2 : ZMod m), (-2 : ZMod m)) = 1 := by
  simp [dir1CaseIILayerZero, two_ne_zero (m := m), two_ne_one (m := m),
    one_ne_zero (m := m)]

theorem returnMap1CaseII_two_neg_two [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((2 : ZMod m), (-2 : ZMod m)) = ((3 : ZMod m), (-2 : ZMod m)) := by
  ext <;> simp [returnMap1CaseII, returnMapColor1,
    dir1CaseIILayerZero_eq_one_two_neg_two (m := m)]
  norm_num

theorem dir1CaseIILayerZero_eq_one_two_neg_one [Fact (5 < m)] :
    dir1CaseIILayerZero (m := m) ((2 : ZMod m), (-1 : ZMod m)) = 1 := by
  have h2neg1 : (2 : ZMod m) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := 2) (by
      have hm5 : 5 < m := Fact.out
      omega)
  simp [dir1CaseIILayerZero, two_ne_zero (m := m), two_ne_one (m := m),
    one_ne_zero (m := m), h2neg1]

theorem returnMap1CaseII_two_neg_one [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((2 : ZMod m), (-1 : ZMod m)) = ((3 : ZMod m), (-1 : ZMod m)) := by
  ext <;> simp [returnMap1CaseII, returnMapColor1,
    dir1CaseIILayerZero_eq_one_two_neg_one (m := m)]
  norm_num

theorem dir1CaseIILayerZero_eq_one_neg_two_one [Fact (5 < m)] :
    dir1CaseIILayerZero (m := m) ((-2 : ZMod m), (1 : ZMod m)) = 1 := by
  simp [dir1CaseIILayerZero, two_ne_zero (m := m), two_ne_one (m := m),
    one_ne_zero (m := m), one_ne_neg_one (m := m)]

theorem returnMap1CaseII_neg_two_one [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((-2 : ZMod m), (1 : ZMod m)) = ((-1 : ZMod m), (1 : ZMod m)) := by
  ext <;> simp [returnMap1CaseII, returnMapColor1,
    dir1CaseIILayerZero_eq_one_neg_two_one (m := m)]
  norm_num

theorem returnMap1CaseII_zero_neg_one [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((0 : ZMod m), (-1 : ZMod m)) = ((1 : ZMod m), (0 : ZMod m)) := by
  have h00 : ¬ (((0 : ZMod m) = 0) ∧ (((-1 : ZMod m)) = 0)) := by
    intro h
    exact (neg_ne_zero.mpr (one_ne_zero (m := m))) h.2
  have hdiag :
      ¬ (((0 : ZMod m) + ((-1 : ZMod m)) = (-1 : ZMod m)) ∧
          ((0 : ZMod m)) ≠ 0 ∧
          ((0 : ZMod m)) ≠ (1 : ZMod m) ∧
          ((0 : ZMod m)) ≠ (-2 : ZMod m) ∧
          ((0 : ZMod m)) ≠ (-1 : ZMod m)) := by
    intro h
    exact h.2.1 rfl
  have h10 : ¬ (((0 : ZMod m) = (1 : ZMod m)) ∧ (((-1 : ZMod m)) = 0)) := by
    intro h
    exact one_ne_zero (m := m) h.1.symm
  have hneg20 : ¬ (((0 : ZMod m) = (-2 : ZMod m)) ∧ (((-1 : ZMod m)) = 0)) := by
    intro h
    exact (neg_ne_zero.mpr (one_ne_zero (m := m))) h.2
  have hneg1neg1 : ¬ (((0 : ZMod m) = (-1 : ZMod m)) ∧ (((-1 : ZMod m)) = (-1 : ZMod m))) := by
    intro h
    exact (neg_ne_zero.mpr (one_ne_zero (m := m))) h.1.symm
  have h0line :
      ¬ (((0 : ZMod m) = 0) ∧
          (((-1 : ZMod m))) ≠ 0 ∧
          (((-1 : ZMod m))) ≠ (-1 : ZMod m)) := by
    intro h
    exact h.2.2 rfl
  have h1line : ¬ (((0 : ZMod m) = (1 : ZMod m)) ∧ (((-1 : ZMod m))) ≠ 0) := by
    intro h
    exact one_ne_zero (m := m) h.1.symm
  have h2neg2 : ¬ (((0 : ZMod m) = (2 : ZMod m)) ∧ (((-1 : ZMod m)) = (-2 : ZMod m))) := by
    intro h
    exact two_ne_zero (m := m) h.1.symm
  have h2neg1 : ¬ (((0 : ZMod m) = (2 : ZMod m)) ∧ (((-1 : ZMod m)) = (-1 : ZMod m))) := by
    intro h
    exact two_ne_zero (m := m) h.1.symm
  have hneg2one : ¬ (((0 : ZMod m) = (-2 : ZMod m)) ∧ (((-1 : ZMod m)) = (1 : ZMod m))) := by
    intro h
    exact one_ne_neg_one (m := m) h.2.symm
  calc
    returnMap1CaseII (m := m) ((0 : ZMod m), (-1 : ZMod m))
        = bulkMap1CaseI (m := m) ((0 : ZMod m), (-1 : ZMod m)) := by
            exact returnMap1CaseII_eq_bulk_of_not_special (m := m)
              (i := (0 : ZMod m)) (k := (-1 : ZMod m))
              h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((1 : ZMod m), (0 : ZMod m)) := by
          simp [bulkMap1CaseI]

theorem returnMap1CaseII_zero_two [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((0 : ZMod m), (2 : ZMod m)) = ((1 : ZMod m), (2 : ZMod m)) := by
  have h20 : (2 : ZMod m) ≠ 0 := by
    exact two_ne_zero (m := m)
  have h2neg1 : (2 : ZMod m) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := 2) (by
      have hm5 : 5 < m := Fact.out
      omega)
  simpa using
    returnMap1CaseII_eq_add_one_of_i_zero (m := m) (k := (2 : ZMod m)) h20 h2neg1

theorem returnMap1CaseII_one_two [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((1 : ZMod m), (2 : ZMod m)) = ((2 : ZMod m), (2 : ZMod m)) := by
  have h20 : (2 : ZMod m) ≠ 0 := by
    exact two_ne_zero (m := m)
  simpa using
    returnMap1CaseII_eq_add_one_of_i_one (m := m) (k := (2 : ZMod m)) h20

theorem returnMap1CaseII_one_neg_one [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((1 : ZMod m), (-1 : ZMod m)) = ((2 : ZMod m), (-1 : ZMod m)) := by
  have hk0 : (-1 : ZMod m) ≠ 0 := by
    exact neg_ne_zero.mpr (one_ne_zero (m := m))
  simpa using
    returnMap1CaseII_eq_add_one_of_i_one (m := m) (k := (-1 : ZMod m)) hk0

theorem returnMap1CaseII_neg_one_one [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((-1 : ZMod m), (1 : ZMod m)) = ((0 : ZMod m), (2 : ZMod m)) := by
  have hneg10 : (-1 : ZMod m) ≠ 0 := by
    exact neg_ne_zero.mpr (one_ne_zero (m := m))
  have hneg11 : (-1 : ZMod m) ≠ 1 := by
    intro h
    exact one_ne_neg_one (m := m) h.symm
  have hneg1neg2 : (-1 : ZMod m) ≠ (-2 : ZMod m) := by
    intro h
    have honeTwo : (1 : ZMod m) ≠ (2 : ZMod m) := by
      have hm5 : 5 < m := Fact.out
      simpa using
        natCast_ne_natCast_of_lt (m := m) (a := 1) (b := 2) (by omega) (by omega) (by omega)
    have : (1 : ZMod m) = (2 : ZMod m) := by
      simpa using congrArg Neg.neg h
    exact honeTwo this
  have h00 : ¬ (((-1 : ZMod m) = 0) ∧ ((1 : ZMod m) = 0)) := by
    intro h
    exact hneg10 h.1
  have hdiag :
      ¬ (((-1 : ZMod m) + (1 : ZMod m) = (-1 : ZMod m)) ∧
          (-1 : ZMod m) ≠ 0 ∧ (-1 : ZMod m) ≠ (1 : ZMod m) ∧
          (-1 : ZMod m) ≠ (-2 : ZMod m) ∧ (-1 : ZMod m) ≠ (-1 : ZMod m)) := by
    intro h
    exact h.2.2.2.2 rfl
  have h10 : ¬ (((-1 : ZMod m) = (1 : ZMod m)) ∧ ((1 : ZMod m) = 0)) := by
    intro h
    exact one_ne_zero (m := m) h.2
  have hneg20 : ¬ (((-1 : ZMod m) = (-2 : ZMod m)) ∧ ((1 : ZMod m) = 0)) := by
    intro h
    exact one_ne_zero (m := m) h.2
  have hneg1neg1 : ¬ (((-1 : ZMod m) = (-1 : ZMod m)) ∧ ((1 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact one_ne_neg_one (m := m) h.2
  have h0line :
      ¬ (((-1 : ZMod m) = 0) ∧ (1 : ZMod m) ≠ 0 ∧ (1 : ZMod m) ≠ (-1 : ZMod m)) := by
    intro h
    exact hneg10 h.1
  have h1line :
      ¬ (((-1 : ZMod m) = (1 : ZMod m)) ∧ (1 : ZMod m) ≠ 0) := by
    intro h
    exact hneg11 h.1
  have h2neg2 : ¬ (((-1 : ZMod m) = (2 : ZMod m)) ∧ ((1 : ZMod m) = (-2 : ZMod m))) := by
    intro h
    have h1neg2 : (1 : ZMod m) ≠ (-2 : ZMod m) := by
      simpa using natCast_ne_neg_two_of_lt (m := m) (n := 1) (by
        have hm5 : 5 < m := Fact.out
        omega)
    exact h1neg2 h.2
  have h2neg1 : ¬ (((-1 : ZMod m) = (2 : ZMod m)) ∧ ((1 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact one_ne_neg_one (m := m) h.2
  have hneg2one : ¬ (((-1 : ZMod m) = (-2 : ZMod m)) ∧ ((1 : ZMod m) = (1 : ZMod m))) := by
    intro h
    exact hneg1neg2 h.1
  calc
    returnMap1CaseII (m := m) ((-1 : ZMod m), (1 : ZMod m))
        = bulkMap1CaseI (m := m) ((-1 : ZMod m), (1 : ZMod m)) := by
            exact returnMap1CaseII_eq_bulk_of_not_special (m := m)
              (i := (-1 : ZMod m)) (k := (1 : ZMod m))
              h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((0 : ZMod m), (2 : ZMod m)) := by
          ext
          · change (-1 : ZMod m) + 1 = (0 : ZMod m)
            ring
          · change (1 : ZMod m) + 1 = (2 : ZMod m)
            norm_num

theorem returnMap1CaseII_neg_one_neg_one :
    returnMap1CaseII (m := m) ((-1 : ZMod m), (-1 : ZMod m)) = ((1 : ZMod m), (-1 : ZMod m)) := by
  ext <;> simp [returnMap1CaseII, returnMapColor1,
    dir1CaseIILayerZero_eq_zero_neg_one_neg_one (m := m)]
  ring

theorem returnMap1CaseII_three_neg_one [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((3 : ZMod m), (-1 : ZMod m)) = ((4 : ZMod m), (0 : ZMod m)) := by
  have hm5 : 5 < m := Fact.out
  have h30 : (3 : ZMod m) ≠ 0 := by
    simpa using natCast_ne_zero_of_pos_lt (m := m) (n := 3) (by omega) (by
      omega)
  have h31 : (3 : ZMod m) ≠ 1 := by
    simpa using natCast_ne_one_of_two_le_lt (m := m) (n := 3) (by omega) (by
      omega)
  have h32 : (3 : ZMod m) ≠ 2 := by
    simpa using natCast_ne_natCast_of_lt (m := m) (a := 3) (b := 2) (by
      omega) (by omega) (by omega)
  have h3neg2 : (3 : ZMod m) ≠ (-2 : ZMod m) := by
    exact natCast_ne_neg_two_of_lt (m := m) (n := 3) (by
      omega)
  have h3neg1 : (3 : ZMod m) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := 3) (by
      omega)
  have h00 : ¬ (((3 : ZMod m) = 0) ∧ ((-1 : ZMod m) = 0)) := by
    intro h
    exact h30 h.1
  have hdiag :
      ¬ (((3 : ZMod m) + (-1 : ZMod m) = (-1 : ZMod m)) ∧
          (3 : ZMod m) ≠ 0 ∧ (3 : ZMod m) ≠ (1 : ZMod m) ∧
          (3 : ZMod m) ≠ (-2 : ZMod m) ∧ (3 : ZMod m) ≠ (-1 : ZMod m)) := by
    intro h
    have hsum : (3 : ZMod m) + (-1 : ZMod m) = (2 : ZMod m) := by norm_num
    exact natCast_ne_neg_one_of_lt (m := m) (n := 2) (by
      omega) (hsum.symm.trans h.1)
  have h10 : ¬ (((3 : ZMod m) = (1 : ZMod m)) ∧ ((-1 : ZMod m) = 0)) := by
    intro h
    exact h31 h.1
  have hneg20 : ¬ (((3 : ZMod m) = (-2 : ZMod m)) ∧ ((-1 : ZMod m) = 0)) := by
    intro h
    exact neg_ne_zero.mpr (one_ne_zero (m := m)) h.2
  have hneg1neg1 : ¬ (((3 : ZMod m) = (-1 : ZMod m)) ∧ ((-1 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact h3neg1 h.1
  have h0line :
      ¬ (((3 : ZMod m) = 0) ∧ ((-1 : ZMod m)) ≠ 0 ∧ ((-1 : ZMod m)) ≠ (-1 : ZMod m)) := by
    intro h
    exact h30 h.1
  have h1line :
      ¬ (((3 : ZMod m) = (1 : ZMod m)) ∧ ((-1 : ZMod m)) ≠ 0) := by
    intro h
    exact h31 h.1
  have h2neg2 : ¬ (((3 : ZMod m) = (2 : ZMod m)) ∧ ((-1 : ZMod m) = (-2 : ZMod m))) := by
    intro h
    exact h32 h.1
  have h2neg1 : ¬ (((3 : ZMod m) = (2 : ZMod m)) ∧ ((-1 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact h32 h.1
  have hneg2one : ¬ (((3 : ZMod m) = (-2 : ZMod m)) ∧ ((-1 : ZMod m) = (1 : ZMod m))) := by
    intro h
    exact h3neg2 h.1
  calc
    returnMap1CaseII (m := m) ((3 : ZMod m), (-1 : ZMod m))
        = bulkMap1CaseI (m := m) ((3 : ZMod m), (-1 : ZMod m)) := by
            exact returnMap1CaseII_eq_bulk_of_not_special (m := m)
              (i := (3 : ZMod m)) (k := (-1 : ZMod m))
              h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((4 : ZMod m), (0 : ZMod m)) := by
          ext
          · change (3 : ZMod m) + 1 = (4 : ZMod m)
            norm_num
          · change (-1 : ZMod m) + 1 = (0 : ZMod m)
            ring

theorem returnMap1CaseII_line_zero [Fact (9 < m)] (hm : m % 6 = 4) :
    returnMap1CaseII (m := m) (linePoint1 (m := m) (0 : Fin m)) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm (0 : Fin m)) := by
  have hT : (TorusD3Even.T1CaseII (m := m) hm (0 : Fin m)).1 = 2 := by
    simpa using
      TorusD3Even.T1CaseII_eq_two_of_val_eq_zero (m := m) (hm := hm) (x := 0) rfl
  have hline :
      linePoint1 (m := m) (0 : Fin m) = ((0 : ZMod m), (0 : ZMod m)) := by
    ext <;> simp [linePoint1]
  rw [hline]
  rw [returnMap1CaseII_origin (m := m)]
  ext <;> simp [linePoint1, hT]

theorem returnMap1CaseII_line_one [Fact (9 < m)] (hm : m % 6 = 4) :
    returnMap1CaseII (m := m) (linePoint1 (m := m) (1 : Fin m)) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm (1 : Fin m)) := by
  have hT : (TorusD3Even.T1CaseII (m := m) hm (1 : Fin m)).1 = 3 := by
    have hm1 : 1 < m := by
      have hm9 : 9 < m := Fact.out
      omega
    have hx1 : ((1 : Fin m)).1 = 1 := by
      show 1 % m = 1
      exact Nat.mod_eq_of_lt hm1
    simpa using
      TorusD3Even.T1CaseII_eq_three_of_val_eq_one
        (m := m) (hm := hm) (x := (1 : Fin m)) hx1
  have hline :
      linePoint1 (m := m) (1 : Fin m) = ((1 : ZMod m), (0 : ZMod m)) := by
    ext <;> simp [linePoint1]
  rw [hline]
  rw [returnMap1CaseII_one_zero (m := m)]
  ext <;> simp [linePoint1, hT]

theorem returnMap1CaseII_line_m_sub_two [Fact (9 < m)] (hm : m % 6 = 4) :
    let x : Fin m := ⟨m - 2, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    returnMap1CaseII (m := m) (linePoint1 (m := m) x) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm x) := by
  let x : Fin m := ⟨m - 2, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  change returnMap1CaseII (m := m) (linePoint1 (m := m) x) =
    linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm x)
  have hline : linePoint1 (m := m) x = (((-2 : ZMod m)), (0 : ZMod m)) := by
    have hm2 : 2 ≤ m := by
      have hm9 : 9 < m := Fact.out
      omega
    ext <;> simp [linePoint1, x, cast_sub_two_eq_neg_two (m := m) hm2]
  have hT : (TorusD3Even.T1CaseII (m := m) hm x).1 = 0 := by
    simpa [x] using
      TorusD3Even.T1CaseII_eq_zero_of_val_eq_m_sub_two (m := m) (hm := hm) (x := x) rfl
  rw [hline, returnMap1CaseII_neg_two_zero (m := m)]
  ext <;> simp [linePoint1, hT]

theorem even_of_mod_six_eq_four (hm : m % 6 = 4) : Even m := by
  rcases TorusD3Even.eq_six_mul_add_four_of_mod_six_eq_four (m := m) hm with ⟨q, rfl⟩
  refine ⟨3 * q + 2, by omega⟩

theorem iterate_returnMap1CaseII_two_prefix [Fact (9 < m)] (hm : m % 6 = 4) {t : ℕ}
    (ht : t ≤ m - 2) :
    ((returnMap1CaseII (m := m)^[t]) (linePoint1 (m := m) (2 : Fin m))) =
      ((((2 + t : ℕ) : ZMod m)), (((t : ℕ) : ZMod m))) := by
  have hm9 : 9 < m := Fact.out
  have hm5 : 5 < m := by omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hm2 : 2 ≤ m := by omega
  have hmEven : Even m := even_of_mod_six_eq_four (m := m) hm
  calc
    ((returnMap1CaseII (m := m)^[t]) (linePoint1 (m := m) (2 : Fin m)))
        = ((bulkMap1CaseI (m := m)^[t]) (linePoint1 (m := m) (2 : Fin m))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := linePoint1 (m := m) (2 : Fin m)) t ?_
            intro s hs
            rw [iterate_bulkMap1CaseI (m := m) s (linePoint1 (m := m) (2 : Fin m))]
            have hslt : s < m - 2 := lt_of_lt_of_le hs ht
            have hi_pos : 0 < 2 + s := by omega
            have hi_lt : 2 + s < m := by omega
            have hk_lt : s < m := by omega
            have hi0 : (((2 + s : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 2 + s) hi_pos hi_lt
            have hi1 : (((2 + s : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 2 + s) (by omega) hi_lt
            have hkneg1 : (((s : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := s) (by omega)
            have hdiag_ne :
                ((((2 + s : ℕ) : ZMod m)) + (((s : ℕ) : ZMod m))) ≠ (-1 : ZMod m) := by
              have hsum_ne : (((2 + 2 * s : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_even (m := m) hmEven (n := 2 + 2 * s) ⟨s + 1, by omega⟩
              simpa [Nat.cast_add, Nat.cast_mul, two_mul, add_assoc, add_left_comm, add_comm] using hsum_ne
            have h00 : ¬ ((((2 + s : ℕ) : ZMod m)) = 0 ∧ (((s : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi0 h.1
            have hdiag :
                ¬ ((((2 + s : ℕ) : ZMod m)) + (((s : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ 0 ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hdiag_ne h.1
            have h10 : ¬ ((((2 + s : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((s : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi1 h.1
            have hneg20 : ¬ ((((2 + s : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((s : ℕ) : ZMod m)) = 0) := by
              intro h
              have hs_eq : s = m - 4 := by
                have hcast : (((2 + s : ℕ) : ZMod m)) = (((m - 2 : ℕ) : ZMod m)) := by
                  simpa [cast_sub_two_eq_neg_two (m := m) hm2] using h.1
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + s) (m - 2) m).1 hcast
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst hs_eq
              have hk_ne : (((m - 4 : ℕ) : ZMod m)) ≠ 0 := by
                exact natCast_ne_zero_of_pos_lt (m := m) (n := m - 4) (by omega) (by omega)
              exact hk_ne h.2
            have hneg1neg1 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ (((s : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hkneg1 h.2
            have h0line :
                ¬ ((((2 + s : ℕ) : ZMod m)) = 0 ∧
                    (((s : ℕ) : ZMod m)) ≠ 0 ∧
                    (((s : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi0 h.1
            have h1line :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((s : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi1 h.1
            have h2neg2 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((s : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              have hs_eq_zero : s = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + s) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst hs_eq_zero
              exact natCast_ne_neg_two_of_lt (m := m) (n := 0) (by omega) h.2
            have h2neg1 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((s : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              have hs_eq_zero : s = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + s) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst hs_eq_zero
              exact natCast_ne_neg_one_of_lt (m := m) (n := 0) (by omega) h.2
            have hneg2one :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((s : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              have hs_eq : s = m - 4 := by
                have hcast : (((2 + s : ℕ) : ZMod m)) = (((m - 2 : ℕ) : ZMod m)) := by
                  simpa [cast_sub_two_eq_neg_two (m := m) hm2] using h.1
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + s) (m - 2) m).1 hcast
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst hs_eq
              have hk_ne : (((m - 4 : ℕ) : ZMod m)) ≠ (1 : ZMod m) := by
                exact natCast_ne_one_of_two_le_lt (m := m) (n := m - 4) (by omega) (by omega)
              exact hk_ne h.2
            simpa [linePoint1] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((2 + s : ℕ) : ZMod m))) (k := (((s : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((2 + t : ℕ) : ZMod m)), (((t : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) t (linePoint1 (m := m) (2 : Fin m))]
          simp [linePoint1, Nat.cast_add, add_assoc, add_left_comm, add_comm]

theorem two_ne_neg_one_caseII [Fact (5 < m)] : (2 : ZMod m) ≠ (-1 : ZMod m) := by
  exact natCast_ne_neg_one_of_lt (m := m) (n := 2) (by
    have hm5 : 5 < m := Fact.out
    omega)

theorem neg_two_ne_neg_one [Fact (5 < m)] : (-2 : ZMod m) ≠ (-1 : ZMod m) := by
  have hm2 : 2 ≤ m := by
    have hm5 : 5 < m := Fact.out
    omega
  have hcast : (((m - 2 : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := m - 2) (by
      have hm5 : 5 < m := Fact.out
      omega)
  simpa [cast_sub_two_eq_neg_two (m := m) hm2] using hcast

theorem returnMap1CaseII_zero_neg_two [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((0 : ZMod m), (-2 : ZMod m)) = ((1 : ZMod m), (-2 : ZMod m)) := by
  have hneg20 : (-2 : ZMod m) ≠ 0 := by
    exact neg_ne_zero.mpr (two_ne_zero (m := m))
  simpa using
    returnMap1CaseII_eq_add_one_of_i_zero (m := m) (k := (-2 : ZMod m)) hneg20
      (neg_two_ne_neg_one (m := m))

theorem returnMap1CaseII_one_neg_two [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((1 : ZMod m), (-2 : ZMod m)) = ((2 : ZMod m), (-2 : ZMod m)) := by
  have hneg20 : (-2 : ZMod m) ≠ 0 := by
    exact neg_ne_zero.mpr (two_ne_zero (m := m))
  simpa using
    returnMap1CaseII_eq_add_one_of_i_one (m := m) (k := (-2 : ZMod m)) hneg20

theorem returnMap1CaseII_three_neg_two [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((3 : ZMod m), (-2 : ZMod m)) = ((4 : ZMod m), (-1 : ZMod m)) := by
  have hm5 : 5 < m := Fact.out
  have hm2 : 2 ≤ m := by omega
  have h30 : (3 : ZMod m) ≠ 0 := by
    simpa using natCast_ne_natCast_of_lt (m := m) (a := 3) (b := 0) (by omega) (by omega) (by omega)
  have h31 : (3 : ZMod m) ≠ 1 := by
    simpa using natCast_ne_natCast_of_lt (m := m) (a := 3) (b := 1) (by omega) (by omega) (by omega)
  have h32 : (3 : ZMod m) ≠ 2 := by
    simpa using natCast_ne_natCast_of_lt (m := m) (a := 3) (b := 2) (by omega) (by omega) (by omega)
  have h3neg2 : (3 : ZMod m) ≠ (-2 : ZMod m) := by
    have hne : ((3 : ℕ) : ZMod m) ≠ ((m - 2 : ℕ) : ZMod m) := by
      exact natCast_ne_natCast_of_lt (m := m) (a := 3) (b := m - 2) (by omega) (by omega) (by omega)
    simpa [cast_sub_two_eq_neg_two (m := m) hm2] using hne
  have h3neg1 : (3 : ZMod m) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := 3) (by omega)
  have hdiag :
      ¬ ((3 : ZMod m) + (-2 : ZMod m) = (-1 : ZMod m) ∧
          (3 : ZMod m) ≠ 0 ∧ (3 : ZMod m) ≠ (1 : ZMod m) ∧
          (3 : ZMod m) ≠ (-2 : ZMod m) ∧ (3 : ZMod m) ≠ (-1 : ZMod m)) := by
    intro h
    have hsum : (3 : ZMod m) + (-2 : ZMod m) = 1 := by norm_num
    have : (1 : ZMod m) = (-1 : ZMod m) := hsum.symm.trans h.1
    exact one_ne_neg_one (m := m) this
  have hneg1neg1 : ¬ ((3 : ZMod m) = (-1 : ZMod m) ∧ (-2 : ZMod m) = (-1 : ZMod m)) := by
    intro h
    exact h3neg1 h.1
  have h2neg2 : ¬ ((3 : ZMod m) = (2 : ZMod m) ∧ (-2 : ZMod m) = (-2 : ZMod m)) := by
    intro h
    exact h32 h.1
  have h2neg1 : ¬ ((3 : ZMod m) = (2 : ZMod m) ∧ (-2 : ZMod m) = (-1 : ZMod m)) := by
    intro h
    exact h32 h.1
  have hneg2one : ¬ ((3 : ZMod m) = (-2 : ZMod m) ∧ (-2 : ZMod m) = (1 : ZMod m)) := by
    intro h
    exact h3neg2 h.1
  calc
    returnMap1CaseII (m := m) ((3 : ZMod m), (-2 : ZMod m))
        = bulkMap1CaseI (m := m) ((3 : ZMod m), (-2 : ZMod m)) := by
            exact returnMap1CaseII_eq_bulk_of_not_special (m := m)
              (i := (3 : ZMod m)) (k := (-2 : ZMod m))
              (by intro h; exact h30 h.1)
              hdiag
              (by intro h; exact h31 h.1)
              (by intro h; exact h3neg2 h.1)
              hneg1neg1
              (by intro h; exact h30 h.1)
              (by intro h; exact h31 h.1)
              h2neg2
              h2neg1
              hneg2one
    _ = ((4 : ZMod m), (-1 : ZMod m)) := by
          ext
          · change (3 : ZMod m) + 1 = (4 : ZMod m)
            norm_num
          · change (-2 : ZMod m) + 1 = (-1 : ZMod m)
            ring

theorem returnMap1CaseII_four_neg_one [Fact (9 < m)] :
    returnMap1CaseII (m := m) ((4 : ZMod m), (-1 : ZMod m)) = ((5 : ZMod m), (0 : ZMod m)) := by
  have hm9 : 9 < m := Fact.out
  have hm5 : 5 < m := by omega
  have hm2 : 2 ≤ m := by omega
  have h40 : (4 : ZMod m) ≠ 0 := by
    simpa using natCast_ne_natCast_of_lt (m := m) (a := 4) (b := 0) (by omega) (by omega) (by omega)
  have h41 : (4 : ZMod m) ≠ 1 := by
    simpa using natCast_ne_natCast_of_lt (m := m) (a := 4) (b := 1) (by omega) (by omega) (by omega)
  have h42 : (4 : ZMod m) ≠ 2 := by
    simpa using natCast_ne_natCast_of_lt (m := m) (a := 4) (b := 2) (by omega) (by omega) (by omega)
  have h4neg2 : (4 : ZMod m) ≠ (-2 : ZMod m) := by
    have hne : ((4 : ℕ) : ZMod m) ≠ ((m - 2 : ℕ) : ZMod m) := by
      exact natCast_ne_natCast_of_lt (m := m) (a := 4) (b := m - 2) (by omega) (by omega) (by omega)
    simpa [cast_sub_two_eq_neg_two (m := m) hm2] using hne
  have h4neg1 : (4 : ZMod m) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := 4) (by omega)
  have hdiag :
      ¬ ((4 : ZMod m) + (-1 : ZMod m) = (-1 : ZMod m) ∧
          (4 : ZMod m) ≠ 0 ∧ (4 : ZMod m) ≠ (1 : ZMod m) ∧
          (4 : ZMod m) ≠ (-2 : ZMod m) ∧ (4 : ZMod m) ≠ (-1 : ZMod m)) := by
    intro h
    have hsum : (4 : ZMod m) + (-1 : ZMod m) = 3 := by norm_num
    have : (3 : ZMod m) = (-1 : ZMod m) := hsum.symm.trans h.1
    exact natCast_ne_neg_one_of_lt (m := m) (n := 3) (by omega) this
  have hneg1neg1 : ¬ ((4 : ZMod m) = (-1 : ZMod m) ∧ (-1 : ZMod m) = (-1 : ZMod m)) := by
    intro h
    exact h4neg1 h.1
  have h2neg2 : ¬ ((4 : ZMod m) = (2 : ZMod m) ∧ (-1 : ZMod m) = (-2 : ZMod m)) := by
    intro h
    exact h42 h.1
  have h2neg1 : ¬ ((4 : ZMod m) = (2 : ZMod m) ∧ (-1 : ZMod m) = (-1 : ZMod m)) := by
    intro h
    exact h42 h.1
  have hneg2one : ¬ ((4 : ZMod m) = (-2 : ZMod m) ∧ (-1 : ZMod m) = (1 : ZMod m)) := by
    intro h
    exact h4neg2 h.1
  calc
    returnMap1CaseII (m := m) ((4 : ZMod m), (-1 : ZMod m))
        = bulkMap1CaseI (m := m) ((4 : ZMod m), (-1 : ZMod m)) := by
            exact returnMap1CaseII_eq_bulk_of_not_special (m := m)
              (i := (4 : ZMod m)) (k := (-1 : ZMod m))
              (by intro h; exact h40 h.1)
              hdiag
              (by intro h; exact h41 h.1)
              (by intro h; exact h4neg2 h.1)
              hneg1neg1
              (by intro h; exact h40 h.1)
              (by intro h; exact h41 h.1)
              h2neg2
              h2neg1
              hneg2one
    _ = ((5 : ZMod m), (0 : ZMod m)) := by
          ext
          · change (4 : ZMod m) + 1 = (5 : ZMod m)
            norm_num
          · change (-1 : ZMod m) + 1 = (0 : ZMod m)
            ring

theorem firstReturn_line_two [Fact (9 < m)] (hm : m % 6 = 4) :
    ((returnMap1CaseII (m := m)^[m + 3]) (linePoint1 (m := m) (2 : Fin m))) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm (2 : Fin m)) := by
  have hm9 : 9 < m := Fact.out
  have hm5 : 5 < m := by omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hm2 : 2 ≤ m := by omega
  have hprefix :
      (returnMap1CaseII (m := m)^[m - 2]) (linePoint1 (m := m) (2 : Fin m)) =
        ((0 : ZMod m), (-2 : ZMod m)) := by
    have h := iterate_returnMap1CaseII_two_prefix (m := m) hm (t := m - 2) le_rfl
    simpa [Nat.cast_add, ZMod.natCast_self, zero_add, cast_sub_two_eq_neg_two (m := m) hm2] using h
  have hstep1 :
      (returnMap1CaseII (m := m)^[m - 1]) (linePoint1 (m := m) (2 : Fin m)) =
        ((1 : ZMod m), (-2 : ZMod m)) := by
    have haux :
        (returnMap1CaseII (m := m)^[1 + (m - 2)]) (linePoint1 (m := m) (2 : Fin m)) =
          ((1 : ZMod m), (-2 : ZMod m)) := by
      rw [Function.iterate_add_apply]
      rw [hprefix]
      simpa [Function.iterate_one] using returnMap1CaseII_zero_neg_two (m := m)
    have hmNat : m - 1 = 1 + (m - 2) := by omega
    have haux' := haux
    rwa [← hmNat] at haux'
  have hstep2 :
      (returnMap1CaseII (m := m)^[m]) (linePoint1 (m := m) (2 : Fin m)) =
        ((2 : ZMod m), (-2 : ZMod m)) := by
    have haux :
        (returnMap1CaseII (m := m)^[1 + (m - 1)]) (linePoint1 (m := m) (2 : Fin m)) =
          ((2 : ZMod m), (-2 : ZMod m)) := by
      rw [Function.iterate_add_apply]
      rw [hstep1]
      simpa [Function.iterate_one] using returnMap1CaseII_one_neg_two (m := m)
    have hmNat : m = 1 + (m - 1) := by omega
    have haux' := haux
    rwa [← hmNat] at haux'
  have hstep3 :
      (returnMap1CaseII (m := m)^[m + 1]) (linePoint1 (m := m) (2 : Fin m)) =
        ((3 : ZMod m), (-2 : ZMod m)) := by
    have haux :
        (returnMap1CaseII (m := m)^[1 + m]) (linePoint1 (m := m) (2 : Fin m)) =
          ((3 : ZMod m), (-2 : ZMod m)) := by
      rw [Function.iterate_add_apply]
      rw [hstep2]
      simpa [Function.iterate_one] using returnMap1CaseII_two_neg_two (m := m)
    have hmNat : m + 1 = 1 + m := by omega
    have haux' := haux
    rwa [← hmNat] at haux'
  have hstep4 :
      (returnMap1CaseII (m := m)^[m + 2]) (linePoint1 (m := m) (2 : Fin m)) =
        ((4 : ZMod m), (-1 : ZMod m)) := by
    have haux :
        (returnMap1CaseII (m := m)^[1 + (m + 1)]) (linePoint1 (m := m) (2 : Fin m)) =
          ((4 : ZMod m), (-1 : ZMod m)) := by
      rw [Function.iterate_add_apply]
      rw [hstep3]
      simpa [Function.iterate_one] using returnMap1CaseII_three_neg_two (m := m)
    have hmNat : m + 2 = 1 + (m + 1) := by omega
    have haux' := haux
    rwa [← hmNat] at haux'
  have hstep5 :
      (returnMap1CaseII (m := m)^[m + 3]) (linePoint1 (m := m) (2 : Fin m)) =
        ((5 : ZMod m), (0 : ZMod m)) := by
    have haux :
        (returnMap1CaseII (m := m)^[1 + (m + 2)]) (linePoint1 (m := m) (2 : Fin m)) =
          ((5 : ZMod m), (0 : ZMod m)) := by
      rw [Function.iterate_add_apply]
      rw [hstep4]
      simpa [Function.iterate_one] using returnMap1CaseII_four_neg_one (m := m)
    have hmNat : m + 3 = 1 + (m + 2) := by omega
    have haux' := haux
    rwa [← hmNat] at haux'
  have hT : (TorusD3Even.T1CaseII (m := m) hm (2 : Fin m)).1 = 5 := by
    have hx2 : ((2 : Fin m)).1 = 2 := by
      show 2 % m = 2
      exact Nat.mod_eq_of_lt (by omega)
    simpa using
      TorusD3Even.T1CaseII_eq_five_of_val_eq_two (m := m) (hm := hm) (x := (2 : Fin m)) hx2
  rw [hstep5]
  ext <;> simp [linePoint1, hT]

theorem iterate_returnMap1CaseII_even_prefix [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx4 : 4 ≤ x) (hxle : x ≤ m - 4) (hxeven : Even x) :
    let xFin : Fin m := ⟨x, by omega⟩
    ((returnMap1CaseII (m := m)^[m - x]) (linePoint1 (m := m) xFin)) =
      ((0 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
  let xFin : Fin m := ⟨x, by omega⟩
  have hm9 : 9 < m := Fact.out
  have hm5 : 5 < m := by omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hm2 : 2 ≤ m := by omega
  have hmEven : Even m := even_of_mod_six_eq_four (m := m) hm
  calc
    ((returnMap1CaseII (m := m)^[m - x]) (linePoint1 (m := m) xFin))
        = ((bulkMap1CaseI (m := m)^[m - x]) (linePoint1 (m := m) xFin)) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := linePoint1 (m := m) xFin) (m - x) ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t (linePoint1 (m := m) xFin)]
            have hi_pos : 0 < x + t := by omega
            have hi_lt : x + t < m := by omega
            have hk_lt : t < m := by omega
            have hk_ne_neg_one : (((t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := t) (by omega)
            have hi_ne_zero : (((x + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := x + t) hi_pos hi_lt
            have hi_ne_one : (((x + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := x + t) (by omega) hi_lt
            have hi_ne_two : (((x + t : ℕ) : ZMod m)) ≠ 2 := by
              exact natCast_ne_natCast_of_lt (m := m) (a := x + t) (b := 2) hi_lt (by omega) (by omega)
            have h00 : ¬ ((((x + t : ℕ) : ZMod m)) = 0 ∧ (((t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((x + t : ℕ) : ZMod m)) + (((t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((x + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((x + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((x + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((x + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsumEven : Even (x + 2 * t) := by
                rcases hxeven with ⟨r, hr⟩
                refine ⟨r + t, ?_⟩
                rw [hr]
                ring
              have hsum_ne : (((x + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_even (m := m) hmEven hsumEven
              apply hsum_ne
              have hsumEq :
                  ((((x + t : ℕ) : ZMod m)) + (((t : ℕ) : ZMod m))) =
                    (((x + 2 * t : ℕ) : ZMod m)) := by
                simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                  congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) (by omega : x + t + t = x + 2 * t)
              exact hsumEq.symm.trans h.1
            have h10 : ¬ ((((x + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 : ¬ ((((x + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = 0) := by
              intro h
              have ht0 : t = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' t 0 m).1 (by simpa using h.2)
                rw [Nat.mod_eq_of_lt hk_lt, Nat.zero_mod] at hmod
                exact hmod
              subst ht0
              have hx_ne_neg_two : (((x : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
                exact natCast_ne_neg_two_of_lt (m := m) (n := x) (by omega)
              exact hx_ne_neg_two h.1
            have hneg1neg1 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hk_ne_neg_one h.2
            have h0line :
                ¬ ((((x + t : ℕ) : ZMod m)) = 0 ∧
                    (((t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((x + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have h2neg1 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have hneg2one :
                ¬ ((((x + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              have ht1 : t = 1 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' t 1 m).1 (by simpa using h.2)
                rw [Nat.mod_eq_of_lt hk_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                exact hmod
              subst ht1
              have hx1_ne_neg_two : (((x + 1 : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
                exact natCast_ne_neg_two_of_lt (m := m) (n := x + 1) (by omega)
              exact hx1_ne_neg_two h.1
            simpa [linePoint1, xFin] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((x + t : ℕ) : ZMod m))) (k := (((t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((x + (m - x) : ℕ) : ZMod m)), (((m - x : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) (m - x) (linePoint1 (m := m) xFin)]
          simp [linePoint1, xFin, Nat.cast_add, add_assoc]
    _ = ((0 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
          have hsum : x + (m - x) = m := by omega
          simp [hsum]

theorem returnMap1CaseII_even_vertical_zero [Fact (9 < m)]
    {x : ℕ} (hx4 : 4 ≤ x) (hxle : x ≤ m - 4) :
    returnMap1CaseII (m := m) ((0 : ZMod m), (((m - x : ℕ) : ZMod m))) =
      ((1 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
  have hk0 : (((m - x : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := m - x) (by omega) (by omega)
  have hkneg1 : (((m - x : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := m - x) (by omega)
  simpa using
    returnMap1CaseII_eq_add_one_of_i_zero (m := m) (k := (((m - x : ℕ) : ZMod m))) hk0 hkneg1

theorem returnMap1CaseII_even_vertical_one [Fact (9 < m)]
    {x : ℕ} (hx4 : 4 ≤ x) (hxle : x ≤ m - 4) :
    returnMap1CaseII (m := m) ((1 : ZMod m), (((m - x : ℕ) : ZMod m))) =
      ((2 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
  have hm5 : 5 < m := by
    have hm9 : 9 < m := Fact.out
    omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hk0 : (((m - x : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := m - x) (by omega) (by omega)
  simpa using
    returnMap1CaseII_eq_add_one_of_i_one (m := m) (k := (((m - x : ℕ) : ZMod m))) hk0

theorem iterate_returnMap1CaseII_even_suffix [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx4 : 4 ≤ x) (hxle : x ≤ m - 4) (hxeven : Even x) :
    ((returnMap1CaseII (m := m)^[x]) ((2 : ZMod m), (((m - x : ℕ) : ZMod m)))) =
      ((((x + 2 : ℕ) : ZMod m)), (0 : ZMod m)) := by
  have hm9 : 9 < m := Fact.out
  have hm5 : 5 < m := by omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hmEven : Even m := even_of_mod_six_eq_four (m := m) hm
  calc
    ((returnMap1CaseII (m := m)^[x]) ((2 : ZMod m), (((m - x : ℕ) : ZMod m))))
        = ((bulkMap1CaseI (m := m)^[x]) ((2 : ZMod m), (((m - x : ℕ) : ZMod m)))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((2 : ZMod m), (((m - x : ℕ) : ZMod m)))) x ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t ((2 : ZMod m), (((m - x : ℕ) : ZMod m)))]
            have hi_pos : 0 < 2 + t := by omega
            have hi_lt : 2 + t < m := by omega
            have hk_pos : 0 < (m - x) + t := by omega
            have hk_lt : (m - x) + t < m := by omega
            have hi_ne_zero : (((2 + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 2 + t) hi_pos hi_lt
            have hi_ne_one : (((2 + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 2 + t) (by omega) hi_lt
            have hi_ne_neg_two : (((2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
              exact natCast_ne_neg_two_of_lt (m := m) (n := 2 + t) (by omega)
            have hi_ne_neg_one : (((2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := 2 + t) (by omega)
            have h00 : ¬ ((((2 + t : ℕ) : ZMod m)) = 0 ∧ ((((m - x) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((2 + t : ℕ) : ZMod m)) + ((((m - x) + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsumEven : Even (m - x + 2 + 2 * t) := by
                rcases hmEven with ⟨q, hq⟩
                rcases hxeven with ⟨r, hr⟩
                rw [hq, hr]
                refine ⟨q - r + 1 + t, ?_⟩
                omega
              have hsum_ne : (((m - x + 2 + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_even (m := m) hmEven hsumEven
              apply hsum_ne
              have hsumEq :
                  ((((2 + t : ℕ) : ZMod m)) + ((((m - x) + t : ℕ) : ZMod m))) =
                    (((m - x + 2 + 2 * t : ℕ) : ZMod m)) := by
                have hnat : 2 + t + ((m - x) + t) = m - x + 2 + 2 * t := by omega
                simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                  congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
              exact hsumEq.symm.trans h.1
            have h10 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ ((((m - x) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((((m - x) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact natCast_ne_zero_of_pos_lt (m := m) (n := (m - x) + t) hk_pos hk_lt h.2
            have hneg1neg1 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ ((((m - x) + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_one h.1
            have h0line :
                ¬ ((((2 + t : ℕ) : ZMod m)) = 0 ∧
                    ((((m - x) + t : ℕ) : ZMod m)) ≠ 0 ∧
                    ((((m - x) + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    ((((m - x) + t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((((m - x) + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              have ht0 : t = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + t) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst ht0
              have hk_ne : (((m - x : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
                exact natCast_ne_neg_two_of_lt (m := m) (n := m - x) (by omega)
              exact hk_ne h.2
            have h2neg1 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((((m - x) + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              have ht0 : t = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + t) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst ht0
              have hk_ne : (((m - x : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := m - x) (by omega)
              exact hk_ne h.2
            have hneg2one :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((((m - x) + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_two h.1
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((2 + t : ℕ) : ZMod m))) (k := ((((m - x) + t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((2 + x : ℕ) : ZMod m)), ((((m - x) + x : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) x ((2 : ZMod m), (((m - x : ℕ) : ZMod m)))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
    _ = ((((x + 2 : ℕ) : ZMod m)), (0 : ZMod m)) := by
          have hsum : (m - x) + x = m := by omega
          ext
          · simp [Nat.cast_add, add_comm]
          · rw [hsum, ZMod.natCast_self]

theorem firstReturn_line_even_generic_caseII [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx4 : 4 ≤ x) (hxle : x ≤ m - 4) (hxeven : Even x) :
    let xFin : Fin m := ⟨x, by omega⟩
    ((returnMap1CaseII (m := m)^[m + 2]) (linePoint1 (m := m) xFin)) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
  let xFin : Fin m := ⟨x, by omega⟩
  have hprefix := iterate_returnMap1CaseII_even_prefix (m := m) hm hx4 hxle hxeven
  have hmid0 :
      (returnMap1CaseII (m := m)^[m - x + 1]) (linePoint1 (m := m) xFin) =
        ((1 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
    have haux :
        (returnMap1CaseII (m := m)^[1 + (m - x)]) (linePoint1 (m := m) xFin) =
          ((1 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
      rw [Function.iterate_add_apply]
      rw [hprefix]
      simpa [Function.iterate_one] using returnMap1CaseII_even_vertical_zero (m := m) hx4 hxle
    have hNat : m - x + 1 = 1 + (m - x) := by omega
    have haux' := haux
    rwa [← hNat] at haux'
  have hmid1 :
      (returnMap1CaseII (m := m)^[m - x + 2]) (linePoint1 (m := m) xFin) =
        ((2 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
    have haux :
        (returnMap1CaseII (m := m)^[1 + (m - x + 1)]) (linePoint1 (m := m) xFin) =
          ((2 : ZMod m), (((m - x : ℕ) : ZMod m))) := by
      rw [Function.iterate_add_apply]
      rw [hmid0]
      simpa [Function.iterate_one] using returnMap1CaseII_even_vertical_one (m := m) hx4 hxle
    have hNat : m - x + 2 = 1 + (m - x + 1) := by omega
    have haux' := haux
    rwa [← hNat] at haux'
  have hsuffix :
      ((returnMap1CaseII (m := m)^[x]) ((2 : ZMod m), (((m - x : ℕ) : ZMod m)))) =
        ((((x + 2 : ℕ) : ZMod m)), (0 : ZMod m)) :=
    iterate_returnMap1CaseII_even_suffix (m := m) hm hx4 hxle hxeven
  have haux :
      ((returnMap1CaseII (m := m)^[x + (m - x + 2)]) (linePoint1 (m := m) xFin)) =
        ((((x + 2 : ℕ) : ZMod m)), (0 : ZMod m)) := by
    rw [Function.iterate_add_apply]
    rw [hmid1]
    exact hsuffix
  have hsum : m + 2 = x + (m - x + 2) := by omega
  have haux' := haux
  rw [← hsum] at haux'
  have hx0 : xFin.1 ≠ 0 := by
    simp [xFin]
    omega
  have hx2 : xFin.1 ≠ 2 := by
    simp [xFin]
    omega
  have hxm2 : xFin.1 ≠ m - 2 := by
    simp [xFin]
    omega
  have heven : xFin.1 % 2 = 0 := by
    rcases hxeven with ⟨r, hr⟩
    simpa [xFin, hr] using (show (r + r) % 2 = 0 by omega)
  have hT : (TorusD3Even.T1CaseII (m := m) hm xFin).1 = x + 2 := by
    simpa [xFin] using
      TorusD3Even.T1CaseII_eq_add_two_of_even_ne_special (m := m) (hm := hm)
        (x := xFin) hx0 hx2 hxm2 heven
  calc
    ((returnMap1CaseII (m := m)^[m + 2]) (linePoint1 (m := m) xFin))
        = ((((x + 2 : ℕ) : ZMod m)), (0 : ZMod m)) := haux'
    _ = linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
          ext <;> simp [linePoint1, hT]

theorem iterate_returnMap1CaseII_odd_prefix [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) (hxodd : Odd x) :
    let xFin : Fin m := ⟨x, by omega⟩
    let a : ℕ := (m - 1 - x) / 2
    ((returnMap1CaseII (m := m)^[a]) (linePoint1 (m := m) xFin)) =
      ((((x + a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))) := by
  let xFin : Fin m := ⟨x, by omega⟩
  let a : ℕ := (m - 1 - x) / 2
  have ha_lt : a < m := by
    dsimp [a]
    omega
  calc
    ((returnMap1CaseII (m := m)^[a]) (linePoint1 (m := m) xFin))
        = ((bulkMap1CaseI (m := m)^[a]) (linePoint1 (m := m) xFin)) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := linePoint1 (m := m) xFin) a ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t (linePoint1 (m := m) xFin)]
            have hi_pos : 0 < x + t := by omega
            have hi_lt : x + t < m := by
              dsimp [a] at ht
              omega
            have hi_ne_zero : (((x + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := x + t) hi_pos hi_lt
            have hi_ne_one : (((x + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := x + t) (by omega) hi_lt
            have hi_ne_two : (((x + t : ℕ) : ZMod m)) ≠ 2 := by
              exact natCast_ne_natCast_of_lt (m := m) (a := x + t) (b := 2) hi_lt (by omega) (by omega)
            have hi_ne_neg_two : (((x + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
              exact natCast_ne_neg_two_of_lt (m := m) (n := x + t) (by omega)
            have hi_ne_neg_one : (((x + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := x + t) (by omega)
            have hk_ne_neg_one : (((t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := t) (by omega)
            have h00 : ¬ ((((x + t : ℕ) : ZMod m)) = 0 ∧ (((t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((x + t : ℕ) : ZMod m)) + (((t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((x + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((x + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((x + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((x + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsum_ne : (((x + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := x + 2 * t) (by
                  dsimp [a] at ht
                  omega)
              apply hsum_ne
              simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm, two_mul] using h.1
            have h10 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_neg_two h.1
            have hneg1neg1 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_one h.1
            have h0line :
                ¬ ((((x + t : ℕ) : ZMod m)) = 0 ∧
                    (((t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((x + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    (((t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have h2neg1 :
                ¬ ((((x + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have hneg2one :
                ¬ ((((x + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_two h.1
            simpa [linePoint1, xFin] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((x + t : ℕ) : ZMod m))) (k := (((t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((x : ℕ) : ZMod m) + (((a : ℕ) : ZMod m))), (((a : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) a (linePoint1 (m := m) xFin)]
          simp [linePoint1, xFin]
    _ = ((((x + a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))) := by
          rw [Nat.cast_add]

theorem odd_caseII_half_eq [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) (hxodd : Odd x) :
    let a : ℕ := (m - 1 - x) / 2
    x + 2 * a = m - 1 := by
  dsimp
  rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
  rcases hxodd with ⟨r, hr⟩
  rw [hq, hr]
  omega

theorem returnMap1CaseII_odd_diag [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) (hxodd : Odd x) :
    let a : ℕ := (m - 1 - x) / 2
    returnMap1CaseII (m := m) ((((x + a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))) =
      ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))) := by
  let a : ℕ := (m - 1 - x) / 2
  have hxa : x + 2 * a = m - 1 := by
    simpa [a] using odd_caseII_half_eq (m := m) hm hx3 hxle hxodd
  have hdiag : (((x + a + a : ℕ) : ZMod m)) = (-1 : ZMod m) := by
    rw [show x + a + a = x + 2 * a by omega, hxa]
    simpa using cast_sub_one_eq_neg_one (m := m) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hi0 : (((x + a : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := x + a) (by omega) (by omega)
  have hi1 : (((x + a : ℕ) : ZMod m)) ≠ 1 := by
    exact natCast_ne_one_of_two_le_lt (m := m) (n := x + a) (by omega) (by omega)
  have hineg2 : (((x + a : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
    exact natCast_ne_neg_two_of_lt (m := m) (n := x + a) (by omega)
  have hineg1 : (((x + a : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := x + a) (by omega)
  have hdiag' :
      (((x + a : ℕ) : ZMod m)) + (((a : ℕ) : ZMod m)) = (-1 : ZMod m) := by
    simpa [Nat.cast_add, add_assoc] using hdiag
  have hdir :
      dir1CaseIILayerZero (m := m) ((((x + a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))) = 0 := by
    exact dir1CaseIILayerZero_eq_zero_of_diag (m := m) hdiag' hi0 hi1 hineg2 hineg1
  have hdir' :
      dir1CaseIILayerZero (m := m)
        ((((x : ℕ) : ZMod m) + (((a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))) = 0 := by
    simpa [Nat.cast_add, add_assoc] using hdir
  simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
    (show returnMap1CaseII (m := m) ((((x + a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))) =
        ((((x + a : ℕ) : ZMod m)) + 2, (((a : ℕ) : ZMod m))) by
      simp [returnMap1CaseII, returnMapColor1, hdir, hdir'])

theorem iterate_returnMap1CaseII_odd_middle [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) (hxodd : Odd x) :
    let a : ℕ := (m - 1 - x) / 2
    ((returnMap1CaseII (m := m)^[a - 1]) ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))) =
      ((0 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))) := by
  let a : ℕ := (m - 1 - x) / 2
  have hxa : x + 2 * a = m - 1 := by
    simpa [a] using odd_caseII_half_eq (m := m) hm hx3 hxle hxodd
  have ha2 : 2 ≤ a := by
    rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
    rcases hxodd with ⟨r, hrx⟩
    rw [hq] at hxle
    rw [hrx] at hxle
    dsimp [a]
    omega
  calc
    ((returnMap1CaseII (m := m)^[a - 1]) ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))))
        = ((bulkMap1CaseI (m := m)^[a - 1]) ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))) (a - 1) ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))]
            have hi_pos : 0 < x + a + 2 + t := by omega
            have hi_lt : x + a + 2 + t < m := by omega
            have hk_pos : 0 < a + t := by omega
            have hk_lt : a + t < m := by omega
            have hi_ne_zero : (((x + a + 2 + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := x + a + 2 + t) hi_pos hi_lt
            have hi_ne_one : (((x + a + 2 + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := x + a + 2 + t) (by omega) hi_lt
            have hi_ne_two : (((x + a + 2 + t : ℕ) : ZMod m)) ≠ 2 := by
              exact natCast_ne_natCast_of_lt (m := m) (a := x + a + 2 + t) (b := 2) hi_lt (by omega) (by omega)
            have hk_ne_zero : (((a + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := a + t) hk_pos hk_lt
            have hk_ne_one : (((a + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := a + t) (by omega) hk_lt
            have hk_ne_neg_one : (((a + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := a + t) (by omega)
            have h00 :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = 0 ∧ (((a + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) + (((a + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((x + a + 2 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((x + a + 2 + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((x + a + 2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((x + a + 2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsum_ne : (((1 + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := 1 + 2 * t) (by omega)
              apply hsum_ne
              have hsumEq :
                  (((x + a + 2 + t + (a + t) : ℕ) : ZMod m)) =
                    (((1 + 2 * t : ℕ) : ZMod m)) := by
                rw [show x + a + 2 + t + (a + t) = x + 2 * a + (2 * t + 2) by omega, hxa]
                have hm1 : (((m - 1 : ℕ) : ZMod m)) = (-1 : ZMod m) := by
                  exact cast_sub_one_eq_neg_one (m := m) (by
                    have hm9 : 9 < m := Fact.out
                    omega)
                rw [Nat.cast_add, Nat.cast_add, hm1]
                have hz :
                    (-1 : ZMod m) + (2 + 2 * ((t : ℕ) : ZMod m)) =
                      (1 : ZMod m) + 2 * ((t : ℕ) : ZMod m) := by
                  ring
                simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using hz
              have hsumLeft :
                  ((((x + a + 2 + t : ℕ) : ZMod m)) + (((a + t : ℕ) : ZMod m))) =
                    (((1 + 2 * t : ℕ) : ZMod m)) := by
                simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using hsumEq
              exact hsumLeft.symm.trans h.1
            have h10 :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((a + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((a + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hk_ne_zero h.2
            have hneg1neg1 :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ (((a + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hk_ne_neg_one h.2
            have h0line :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = 0 ∧
                    (((a + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((a + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    (((a + t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((a + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have h2neg1 :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((a + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have hneg2one :
                ¬ ((((x + a + 2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((a + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hk_ne_one h.2
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((x + a + 2 + t : ℕ) : ZMod m))) (k := (((a + t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((x + a + 2 + (a - 1) : ℕ) : ZMod m)), (((a + (a - 1) : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) (a - 1) ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
    _ = ((0 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))) := by
          have hfirst : x + a + 2 + (a - 1) = m := by omega
          have hsecond : a + (a - 1) = m - x - 2 := by omega
          simp [hfirst, hsecond]

theorem returnMap1CaseII_odd_vertical_zero [Fact (9 < m)]
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) :
    returnMap1CaseII (m := m) ((0 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))) =
      ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))) := by
  have hk0 : (((m - x - 2 : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := m - x - 2) (by omega) (by omega)
  have hkneg1 : (((m - x - 2 : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := m - x - 2) (by omega)
  simpa using
    returnMap1CaseII_eq_add_one_of_i_zero (m := m) (k := (((m - x - 2 : ℕ) : ZMod m))) hk0 hkneg1

theorem returnMap1CaseII_odd_vertical_one [Fact (9 < m)]
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) :
    returnMap1CaseII (m := m) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))) =
      ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))) := by
  have hk0 : (((m - x - 2 : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := m - x - 2) (by omega) (by omega)
  simpa using
    returnMap1CaseII_eq_add_one_of_i_one (m := m) (k := (((m - x - 2 : ℕ) : ZMod m))) hk0

theorem iterate_returnMap1CaseII_odd_suffix_prefix [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) (hxodd : Odd x) :
    let b : ℕ := (x - 1) / 2
    ((returnMap1CaseII (m := m)^[b]) ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) =
      ((((2 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m))) := by
  let b : ℕ := (x - 1) / 2
  calc
    ((returnMap1CaseII (m := m)^[b]) ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))
        = ((bulkMap1CaseI (m := m)^[b]) ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) b ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))]
            have hi_pos : 0 < 2 + t := by omega
            have hi_lt : 2 + t < m := by
              dsimp [b] at ht
              omega
            have hk_pos : 0 < (m - x - 2) + t := by omega
            have hk_lt : (m - x - 2) + t < m := by
              dsimp [b] at ht
              omega
            have hi_ne_zero : (((2 + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 2 + t) hi_pos hi_lt
            have hi_ne_one : (((2 + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 2 + t) (by omega) hi_lt
            have hi_ne_neg_two : (((2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
              exact natCast_ne_neg_two_of_lt (m := m) (n := 2 + t) (by omega)
            have hi_ne_neg_one : (((2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := 2 + t) (by omega)
            have h00 : ¬ ((((2 + t : ℕ) : ZMod m)) = 0 ∧ ((((m - x - 2) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((2 + t : ℕ) : ZMod m)) + ((((m - x - 2) + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsum_ne : (((m - x + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := m - x + 2 * t) (by
                  dsimp [b] at ht
                  omega)
              apply hsum_ne
              have hsumEq :
                  ((((2 + t : ℕ) : ZMod m)) + ((((m - x - 2) + t : ℕ) : ZMod m))) =
                    (((m - x + 2 * t : ℕ) : ZMod m)) := by
                have hnat : 2 + t + ((m - x - 2) + t) = m - x + 2 * t := by omega
                simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                  congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
              exact hsumEq.symm.trans h.1
            have h10 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ ((((m - x - 2) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((((m - x - 2) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_neg_two h.1
            have hneg1neg1 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ ((((m - x - 2) + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_one h.1
            have h0line :
                ¬ ((((2 + t : ℕ) : ZMod m)) = 0 ∧
                    ((((m - x - 2) + t : ℕ) : ZMod m)) ≠ 0 ∧
                    ((((m - x - 2) + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    ((((m - x - 2) + t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((((m - x - 2) + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              have ht0 : t = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + t) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst ht0
              have hk_ne : (((m - x - 2 : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
                exact natCast_ne_neg_two_of_lt (m := m) (n := m - x - 2) (by omega)
              exact hk_ne h.2
            have h2neg1 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((((m - x - 2) + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              have ht0 : t = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + t) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst ht0
              have hk_ne : (((m - x - 2 : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := m - x - 2) (by omega)
              exact hk_ne h.2
            have hneg2one :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((((m - x - 2) + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_two h.1
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((2 + t : ℕ) : ZMod m))) (k := ((((m - x - 2) + t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((2 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) b ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]

theorem returnMap1CaseII_odd_suffix_diag [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 5) (hxodd : Odd x) :
    let b : ℕ := (x - 1) / 2
    returnMap1CaseII (m := m)
      ((((2 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m))) =
      ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m))) := by
  let b : ℕ := (x - 1) / 2
  have hxb : x = 1 + 2 * b := by
    dsimp [b]
    rcases hxodd with ⟨r, hr⟩
    rw [hr]
    omega
  have hdiag :
      ((((2 + b : ℕ) : ZMod m)) + ((((m - x - 2) + b : ℕ) : ZMod m))) = (-1 : ZMod m) := by
    have hnat : 2 + b + ((m - x - 2) + b) = m - 1 := by
      rw [hxb]
      omega
    have hsum :
        ((((2 + b : ℕ) : ZMod m)) + ((((m - x - 2) + b : ℕ) : ZMod m))) =
          (((m - 1 : ℕ) : ZMod m)) := by
      simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
        congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
    exact hsum.trans <| cast_sub_one_eq_neg_one (m := m) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hi0 : (((2 + b : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := 2 + b) (by omega) (by omega)
  have hi1 : (((2 + b : ℕ) : ZMod m)) ≠ 1 := by
    exact natCast_ne_one_of_two_le_lt (m := m) (n := 2 + b) (by omega) (by omega)
  have hineg2 : (((2 + b : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
    exact natCast_ne_neg_two_of_lt (m := m) (n := 2 + b) (by omega)
  have hineg1 : (((2 + b : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := 2 + b) (by omega)
  have hstep :=
    returnMap1CaseII_eq_add_two_of_diag (m := m) hdiag hi0 hi1 hineg2 hineg1
  calc
    returnMap1CaseII (m := m)
      ((((2 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m)))
        = ((((2 + b : ℕ) : ZMod m)) + 2, ((((m - x - 2) + b : ℕ) : ZMod m))) := hstep
    _ = ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m))) := by
          ext
          · simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
            norm_num
          · rfl

theorem iterate_returnMap1CaseII_odd_suffix_tail [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 7) (hxodd : Odd x) :
    let b : ℕ := (x - 1) / 2
    let c : ℕ := b + 3
    ((returnMap1CaseII (m := m)^[c])
      ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m)))) =
      ((((x + 6 : ℕ) : ZMod m)), (0 : ZMod m)) := by
  let b : ℕ := (x - 1) / 2
  let c : ℕ := b + 3
  calc
    ((returnMap1CaseII (m := m)^[c])
      ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m))))
        = ((bulkMap1CaseI (m := m)^[c])
          ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m)))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m)))) c ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m)))]
            have hi_pos : 0 < 4 + b + t := by
              dsimp [b, c] at ht ⊢
              omega
            have hi_lt : 4 + b + t < m := by
              dsimp [b, c] at ht ⊢
              omega
            have hk_pos : 0 < (m - x - 2) + b + t := by
              dsimp [b, c] at ht ⊢
              omega
            have hk_lt : (m - x - 2) + b + t < m := by
              dsimp [b, c] at ht ⊢
              omega
            have hi_ne_zero : (((4 + b + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 4 + b + t) hi_pos hi_lt
            have hi_ne_one : (((4 + b + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 4 + b + t) (by omega) hi_lt
            have hi_ne_two : (((4 + b + t : ℕ) : ZMod m)) ≠ 2 := by
              exact natCast_ne_natCast_of_lt (m := m) (a := 4 + b + t) (b := 2) hi_lt (by omega) (by omega)
            have hi_ne_neg_one : (((4 + b + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := 4 + b + t) (by
                dsimp [b, c] at ht
                omega)
            have hk_ne_zero : ((((m - x - 2) + b + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := (m - x - 2) + b + t) hk_pos hk_lt
            have hk_ne_one : ((((m - x - 2) + b + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := (m - x - 2) + b + t) (by omega) hk_lt
            have h00 :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = 0 ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) + ((((m - x - 2) + b + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((4 + b + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((4 + b + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((4 + b + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((4 + b + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsum_ne : (((1 + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := 1 + 2 * t) (by
                  dsimp [b, c] at ht
                  omega)
              apply hsum_ne
              have hsumEq :
                  ((((4 + b + t : ℕ) : ZMod m)) + ((((m - x - 2) + b + t : ℕ) : ZMod m))) =
                    (((1 + 2 * t : ℕ) : ZMod m)) := by
                have hxb : x = 1 + 2 * b := by
                  dsimp [b]
                  rcases hxodd with ⟨r, hr⟩
                  rw [hr]
                  omega
                have hnat : 4 + b + t + ((m - x - 2) + b + t) = m + (1 + 2 * t) := by
                  rw [hxb]
                  omega
                have hcast :
                    (((4 + b + t : ℕ) : ZMod m)) + ((((m - x - 2) + b + t : ℕ) : ZMod m)) =
                      (((m + (1 + 2 * t) : ℕ) : ZMod m)) := by
                  simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                    congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
                simpa [Nat.cast_add, ZMod.natCast_self, zero_add] using hcast
              exact hsumEq.symm.trans h.1
            have h10 :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hk_ne_zero h.2
            have hneg1neg1 :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_one h.1
            have h0line :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = 0 ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) ≠ 0 ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have h2neg1 :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have hneg2one :
                ¬ ((((4 + b + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧
                    ((((m - x - 2) + b + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hk_ne_one h.2
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((4 + b + t : ℕ) : ZMod m)))
                (k := ((((m - x - 2) + b + t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((4 + b + c : ℕ) : ZMod m)), ((((m - x - 2) + b + c : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) c
            ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m)))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
    _ = ((((x + 6 : ℕ) : ZMod m)), (0 : ZMod m)) := by
          have hxb : x = 1 + 2 * b := by
            dsimp [b]
            rcases hxodd with ⟨r, hr⟩
            rw [hr]
            omega
          have hc : c = b + 3 := by rfl
          have hfirst : 4 + b + c = x + 6 := by
            rw [hc, hxb]
            omega
          have hsecond : (m - x - 2) + b + c = m := by
            rw [hc, hxb]
            omega
          have hfst :
              (((4 + b + c : ℕ) : ZMod m)) = (((x + 6 : ℕ) : ZMod m)) := by
            simpa using congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hfirst
          have hsnd :
              ((((m - x - 2) + b + c : ℕ) : ZMod m)) = (0 : ZMod m) := by
            rw [hsecond, ZMod.natCast_self]
          exact Prod.ext hfst hsnd

theorem iterate_returnMap1CaseII_odd_suffix [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 7) (hxodd : Odd x) :
    ((returnMap1CaseII (m := m)^[x + 4]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) =
      ((((x + 6 : ℕ) : ZMod m)), (0 : ZMod m)) := by
  let b : ℕ := (x - 1) / 2
  let c : ℕ := b + 3
  have hxle5 : x ≤ m - 5 := by omega
  have hxb : x = 1 + 2 * b := by
    dsimp [b]
    rcases hxodd with ⟨r, hr⟩
    rw [hr]
    omega
  have hsum : x + 4 = c + (1 + (1 + b)) := by
    calc
      x + 4 = (1 + 2 * b) + 4 := by rw [hxb]
      _ = c + (1 + (1 + b)) := by
            dsimp [c]
            omega
  have hsplit0 :
      ((returnMap1CaseII (m := m)^[x + 4]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) =
        ((returnMap1CaseII (m := m)^[c])
          (((returnMap1CaseII (m := m)^[1 + (1 + b)]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))))) := by
    simpa [hsum] using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := c)
        (n := 1 + (1 + b)) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))
  have hsplit1 :
      ((returnMap1CaseII (m := m)^[1 + (1 + b)]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) =
        returnMap1CaseII (m := m)
          (((returnMap1CaseII (m := m)^[1 + b]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))) := by
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := 1)
        (n := 1 + b) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))
  have hsplit2 :
      ((returnMap1CaseII (m := m)^[1 + b]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) =
        ((returnMap1CaseII (m := m)^[b])
          (returnMap1CaseII (m := m) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))) := by
    have hb : 1 + b = b + 1 := by omega
    rw [hb]
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := b)
        (n := 1) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))
  calc
    ((returnMap1CaseII (m := m)^[x + 4]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))
        = ((returnMap1CaseII (m := m)^[c])
            (((returnMap1CaseII (m := m)^[1 + (1 + b)]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))))) := by
              exact hsplit0
    _ = ((returnMap1CaseII (m := m)^[c])
            (returnMap1CaseII (m := m)
              (((returnMap1CaseII (m := m)^[1 + b]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))))) := by
          rw [hsplit1]
    _ = ((returnMap1CaseII (m := m)^[c])
            (returnMap1CaseII (m := m)
              (((returnMap1CaseII (m := m)^[b])
                (returnMap1CaseII (m := m) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))))))) := by
          rw [hsplit2]
    _ = ((returnMap1CaseII (m := m)^[c])
            (returnMap1CaseII (m := m)
              (((returnMap1CaseII (m := m)^[b]) ((2 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))))) := by
          simpa using
            congrArg (fun u =>
              ((returnMap1CaseII (m := m)^[c])
                (returnMap1CaseII (m := m) (((returnMap1CaseII (m := m)^[b]) u)))))
              (returnMap1CaseII_odd_vertical_one (m := m) hx3 hxle5)
    _ = ((returnMap1CaseII (m := m)^[c])
            (returnMap1CaseII (m := m)
              ((((2 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m))))) := by
          simpa [b] using
            congrArg (fun u => ((returnMap1CaseII (m := m)^[c]) (returnMap1CaseII (m := m) u)))
              (iterate_returnMap1CaseII_odd_suffix_prefix (m := m) hm hx3 hxle5 hxodd)
    _ = ((returnMap1CaseII (m := m)^[c])
            ((((4 + b : ℕ) : ZMod m)), ((((m - x - 2) + b : ℕ) : ZMod m)))) := by
          simpa [b] using
            congrArg (fun u => ((returnMap1CaseII (m := m)^[c]) u))
              (returnMap1CaseII_odd_suffix_diag (m := m) hm hx3 hxle5 hxodd)
    _ = ((((x + 6 : ℕ) : ZMod m)), (0 : ZMod m)) := by
          simpa [b, c] using
            iterate_returnMap1CaseII_odd_suffix_tail (m := m) hm hx3 hxle hxodd

theorem firstReturn_line_odd_generic_caseII [Fact (9 < m)] (hm : m % 6 = 4)
    {x : ℕ} (hx3 : 3 ≤ x) (hxle : x ≤ m - 7) (hxodd : Odd x) :
    let xFin : Fin m := ⟨x, by omega⟩
    ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin)) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
  let xFin : Fin m := ⟨x, by omega⟩
  let a : ℕ := (m - 1 - x) / 2
  have hxle5 : x ≤ m - 5 := by omega
  have hdecomp : m + 4 = (x + 4) + (1 + ((a - 1) + (1 + a))) := by
    dsimp [a]
    rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
    rcases hxodd with ⟨r, hrx⟩
    rw [hq, hrx]
    omega
  have hsplit0 :
      ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin)) =
        ((returnMap1CaseII (m := m)^[x + 4])
          (((returnMap1CaseII (m := m)^[1 + ((a - 1) + (1 + a))]) (linePoint1 (m := m) xFin)))) := by
    simpa [hdecomp] using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := x + 4)
        (n := 1 + ((a - 1) + (1 + a))) (linePoint1 (m := m) xFin))
  have hsplit1 :
      ((returnMap1CaseII (m := m)^[1 + ((a - 1) + (1 + a))]) (linePoint1 (m := m) xFin)) =
        returnMap1CaseII (m := m)
          (((returnMap1CaseII (m := m)^[(a - 1) + (1 + a)]) (linePoint1 (m := m) xFin))) := by
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := 1)
        (n := (a - 1) + (1 + a)) (linePoint1 (m := m) xFin))
  have hsplit2 :
      ((returnMap1CaseII (m := m)^[(a - 1) + (1 + a)]) (linePoint1 (m := m) xFin)) =
        ((returnMap1CaseII (m := m)^[a - 1])
          (((returnMap1CaseII (m := m)^[1 + a]) (linePoint1 (m := m) xFin)))) := by
    simpa [Nat.add_assoc] using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := a - 1)
        (n := 1 + a) (linePoint1 (m := m) xFin))
  have hsplit3 :
      ((returnMap1CaseII (m := m)^[1 + a]) (linePoint1 (m := m) xFin)) =
        returnMap1CaseII (m := m)
          (((returnMap1CaseII (m := m)^[a]) (linePoint1 (m := m) xFin))) := by
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := 1)
        (n := a) (linePoint1 (m := m) xFin))
  have haux :
      ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin)) =
        ((((x + 6 : ℕ) : ZMod m)), (0 : ZMod m)) := by
    calc
      ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin))
          = ((returnMap1CaseII (m := m)^[x + 4])
              (((returnMap1CaseII (m := m)^[1 + ((a - 1) + (1 + a))]) (linePoint1 (m := m) xFin)))) := by
                exact hsplit0
      _ = ((returnMap1CaseII (m := m)^[x + 4])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[(a - 1) + (1 + a)]) (linePoint1 (m := m) xFin))))) := by
            rw [hsplit1]
      _ = ((returnMap1CaseII (m := m)^[x + 4])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  (((returnMap1CaseII (m := m)^[1 + a]) (linePoint1 (m := m) xFin))))))) := by
            rw [hsplit2]
      _ = ((returnMap1CaseII (m := m)^[x + 4])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  (returnMap1CaseII (m := m)
                    (((returnMap1CaseII (m := m)^[a]) (linePoint1 (m := m) xFin)))))))) := by
            rw [hsplit3]
      _ = ((returnMap1CaseII (m := m)^[x + 4])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  (returnMap1CaseII (m := m) ((((x + a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))))))) := by
            simpa [xFin, a] using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[x + 4])
                (returnMap1CaseII (m := m) (((returnMap1CaseII (m := m)^[a - 1]) (returnMap1CaseII (m := m) u))))))
                (iterate_returnMap1CaseII_odd_prefix (m := m) hm hx3 hxle5 hxodd)
      _ = ((returnMap1CaseII (m := m)^[x + 4])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  ((((x + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))))))) := by
            simpa [xFin, a] using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[x + 4])
                (returnMap1CaseII (m := m) (((returnMap1CaseII (m := m)^[a - 1]) u)))))
                (returnMap1CaseII_odd_diag (m := m) hm hx3 hxle5 hxodd)
      _ = ((returnMap1CaseII (m := m)^[x + 4])
              (returnMap1CaseII (m := m)
                ((0 : ZMod m), (((m - x - 2 : ℕ) : ZMod m))))) := by
            simpa [xFin, a] using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[x + 4]) (returnMap1CaseII (m := m) u)))
                (iterate_returnMap1CaseII_odd_middle (m := m) hm hx3 hxle5 hxodd)
      _ = ((returnMap1CaseII (m := m)^[x + 4]) ((1 : ZMod m), (((m - x - 2 : ℕ) : ZMod m)))) := by
            simpa using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[x + 4]) u))
                (returnMap1CaseII_odd_vertical_zero (m := m) hx3 hxle5)
      _ = ((((x + 6 : ℕ) : ZMod m)), (0 : ZMod m)) := by
            exact iterate_returnMap1CaseII_odd_suffix (m := m) hm hx3 hxle hxodd
  have hx1 : xFin.1 ≠ 1 := by
    simp [xFin]
    omega
  have hxm5 : xFin.1 ≠ m - 5 := by
    simp [xFin]
    omega
  have hxm3 : xFin.1 ≠ m - 3 := by
    simp [xFin]
    omega
  have hxm1 : xFin.1 ≠ m - 1 := by
    simp [xFin]
    omega
  have hodd : xFin.1 % 2 = 1 := by
    rcases hxodd with ⟨r, hr⟩
    simpa [xFin, hr] using (show (r + r + 1) % 2 = 1 by omega)
  have hT : (TorusD3Even.T1CaseII (m := m) hm xFin).1 = x + 6 := by
    simpa [xFin] using
      TorusD3Even.T1CaseII_eq_add_six_of_odd_ne_special (m := m) (hm := hm)
        (x := xFin) hx1 hxm5 hxm3 hxm1 hodd
  calc
    ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin))
        = ((((x + 6 : ℕ) : ZMod m)), (0 : ZMod m)) := haux
    _ = linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
          ext <;> simp [linePoint1, hT]

theorem iterate_returnMap1CaseII_m_sub_five_suffix_tail_partial [Fact (9 < m)] (hm : m % 6 = 4) :
    ((returnMap1CaseII (m := m)^[m / 2 - 1])
      ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m)))) =
      ((0 : ZMod m), (-1 : ZMod m)) := by
  have hmEven : Even m := even_of_mod_six_eq_four (m := m) hm
  calc
    ((returnMap1CaseII (m := m)^[m / 2 - 1])
      ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m))))
        = ((bulkMap1CaseI (m := m)^[m / 2 - 1])
            ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m)))) := by
              refine iterate_eq_iterate_of_eq_on_prefix
                (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
                (z := ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m)))) (m / 2 - 1) ?_
              intro t ht
              rw [iterate_bulkMap1CaseI (m := m) t
                ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m)))]
              have hi_pos : 0 < m / 2 + 1 + t := by
                rcases hmEven with ⟨q, hq⟩
                rw [hq]
                omega
              have hi_lt : m / 2 + 1 + t < m := by
                rcases hmEven with ⟨q, hq⟩
                rw [hq] at ht ⊢
                omega
              have hk_pos : 0 < m / 2 + t := by
                rcases hmEven with ⟨q, hq⟩
                rw [hq]
                omega
              have hk_lt : m / 2 + t < m := by
                rcases hmEven with ⟨q, hq⟩
                rw [hq] at ht ⊢
                omega
              have hk_lt' : m / 2 + t + 1 < m := by
                rcases hmEven with ⟨q, hq⟩
                rw [hq] at ht ⊢
                omega
              have hi_ne_zero : (((m / 2 + 1 + t : ℕ) : ZMod m)) ≠ 0 := by
                exact natCast_ne_zero_of_pos_lt (m := m) (n := m / 2 + 1 + t) hi_pos hi_lt
              have hi_ne_one : (((m / 2 + 1 + t : ℕ) : ZMod m)) ≠ 1 := by
                exact natCast_ne_one_of_two_le_lt (m := m) (n := m / 2 + 1 + t) (by
                  rcases hmEven with ⟨q, hq⟩
                  rw [hq]
                  omega) hi_lt
              have hi_ne_two : (((m / 2 + 1 + t : ℕ) : ZMod m)) ≠ 2 := by
                exact natCast_ne_natCast_of_lt (m := m) (a := m / 2 + 1 + t) (b := 2) hi_lt (by
                  have hm9 : 9 < m := Fact.out
                  omega) (by
                    rcases hmEven with ⟨q, hq⟩
                    rw [hq]
                    omega)
              have hk_ne_zero : (((m / 2 + t : ℕ) : ZMod m)) ≠ 0 := by
                exact natCast_ne_zero_of_pos_lt (m := m) (n := m / 2 + t) hk_pos hk_lt
              have hk_ne_one : (((m / 2 + t : ℕ) : ZMod m)) ≠ 1 := by
                exact natCast_ne_one_of_two_le_lt (m := m) (n := m / 2 + t) (by
                  rcases hmEven with ⟨q, hq⟩
                  rw [hq]
                  omega) hk_lt
              have hk_ne_neg_one : (((m / 2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := m / 2 + t) hk_lt'
              have h00 :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = 0 ∧ (((m / 2 + t : ℕ) : ZMod m)) = 0) := by
                intro h
                exact hi_ne_zero h.1
              have hdiag :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) + (((m / 2 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                      (((m / 2 + 1 + t : ℕ) : ZMod m)) ≠ 0 ∧
                      (((m / 2 + 1 + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                      (((m / 2 + 1 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                      (((m / 2 + 1 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
                intro h
                have hsum_ne : (((1 + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                  exact natCast_ne_neg_one_of_lt (m := m) (n := 1 + 2 * t) (by
                    rcases hmEven with ⟨q, hq⟩
                    rw [hq] at ht ⊢
                    omega)
                apply hsum_ne
                have hnat : m / 2 + 1 + t + (m / 2 + t) = m + (1 + 2 * t) := by
                  rcases hmEven with ⟨q, hq⟩
                  rw [hq]
                  omega
                have hcast :
                    ((((m / 2 + 1 + t : ℕ) : ZMod m)) + (((m / 2 + t : ℕ) : ZMod m))) =
                      (((m + (1 + 2 * t) : ℕ) : ZMod m)) := by
                  simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                    congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
                have hsumEq :
                    ((((m / 2 + 1 + t : ℕ) : ZMod m)) + (((m / 2 + t : ℕ) : ZMod m))) =
                      (((1 + 2 * t : ℕ) : ZMod m)) := by
                  simpa [Nat.cast_add, ZMod.natCast_self, zero_add] using hcast
                exact hsumEq.symm.trans h.1
              have h10 :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((m / 2 + t : ℕ) : ZMod m)) = 0) := by
                intro h
                exact hi_ne_one h.1
              have hneg20 :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((m / 2 + t : ℕ) : ZMod m)) = 0) := by
                intro h
                exact hk_ne_zero h.2
              have hneg1neg1 :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ (((m / 2 + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
                intro h
                exact hk_ne_neg_one h.2
              have h0line :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = 0 ∧
                      (((m / 2 + t : ℕ) : ZMod m)) ≠ 0 ∧
                      (((m / 2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
                intro h
                exact hi_ne_zero h.1
              have h1line :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                      (((m / 2 + t : ℕ) : ZMod m)) ≠ 0) := by
                intro h
                exact hi_ne_one h.1
              have h2neg2 :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((m / 2 + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
                intro h
                exact hi_ne_two h.1
              have h2neg1 :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((m / 2 + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
                intro h
                exact hi_ne_two h.1
              have hneg2one :
                  ¬ ((((m / 2 + 1 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((m / 2 + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
                intro h
                exact hk_ne_one h.2
              simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                returnMap1CaseII_eq_bulk_of_not_special (m := m)
                  (i := (((m / 2 + 1 + t : ℕ) : ZMod m))) (k := (((m / 2 + t : ℕ) : ZMod m)))
                  h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((m / 2 + 1 + (m / 2 - 1) : ℕ) : ZMod m)), (((m / 2 + (m / 2 - 1) : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) (m / 2 - 1)
            ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m)))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
    _ = ((0 : ZMod m), (-1 : ZMod m)) := by
          have hm1 : m / 2 + 1 + (m / 2 - 1) = m := by
            rcases hmEven with ⟨q, hq⟩
            rw [hq]
            omega
          have hm2 : m / 2 + (m / 2 - 1) = m - 1 := by
            rcases hmEven with ⟨q, hq⟩
            rw [hq]
            omega
          rw [hm1, ZMod.natCast_self]
          rw [hm2]
          simp [cast_sub_one_eq_neg_one (m := m) (by
            have hm9 : 9 < m := Fact.out
            omega)]

theorem iterate_returnMap1CaseII_m_sub_five_suffix_tail [Fact (9 < m)] (hm : m % 6 = 4) :
    ((returnMap1CaseII (m := m)^[m / 2])
      ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m)))) =
      ((1 : ZMod m), (0 : ZMod m)) := by
  let zHalf : P0Coord m :=
    ((((m / 2 + 1 : ℕ) : ZMod m)), (((m / 2 : ℕ) : ZMod m)))
  calc
    ((returnMap1CaseII (m := m)^[m / 2]) zHalf)
        = returnMap1CaseII (m := m)
            (((returnMap1CaseII (m := m)^[m / 2 - 1]) zHalf)) := by
              rw [show m / 2 = 1 + (m / 2 - 1) by
                    rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
                    rw [hq]
                    omega]
              rw [Function.iterate_add_apply]
              simp
    _ = returnMap1CaseII (m := m) ((0 : ZMod m), (-1 : ZMod m)) := by
          rw [iterate_returnMap1CaseII_m_sub_five_suffix_tail_partial (m := m) hm]
    _ = ((1 : ZMod m), (0 : ZMod m)) := by
          have hm5 : 5 < m := by
            have hm9 : 9 < m := Fact.out
            omega
          letI : Fact (5 < m) := ⟨hm5⟩
          exact returnMap1CaseII_zero_neg_one (m := m)

theorem iterate_returnMap1CaseII_odd_suffix_m_sub_five [Fact (9 < m)] (hm : m % 6 = 4) :
    ((returnMap1CaseII (m := m)^[m - 1]) ((1 : ZMod m), (3 : ZMod m))) =
      ((1 : ZMod m), (0 : ZMod m)) := by
  have hx3 : 3 ≤ m - 5 := by
    have hm9 : 9 < m := Fact.out
    omega
  have hxle : m - 5 ≤ m - 5 := le_rfl
  let b : ℕ := ((m - 5) - 1) / 2
  have hxb : m - 5 = 1 + 2 * b := by
    dsimp [b]
    rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
    rw [hq]
    omega
  have hxodd : Odd (m - 5) := by
    refine ⟨b, ?_⟩
    omega
  have hthree : (((m - (m - 5) - 2 : ℕ) : ZMod m)) = (3 : ZMod m) := by
    have hnat : m - (m - 5) - 2 = 3 := by omega
    simpa [hnat]
  have hsum : m - 1 = m / 2 + (1 + (1 + b)) := by
    rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
    rw [hq] at hxb ⊢
    omega
  have hsplit0 :
      ((returnMap1CaseII (m := m)^[m - 1]) ((1 : ZMod m), (3 : ZMod m))) =
        ((returnMap1CaseII (m := m)^[m / 2])
          (((returnMap1CaseII (m := m)^[1 + (1 + b)]) ((1 : ZMod m), (3 : ZMod m))))) := by
    simpa [hsum] using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := m / 2)
        (n := 1 + (1 + b)) ((1 : ZMod m), (3 : ZMod m)))
  have hsplit1 :
      ((returnMap1CaseII (m := m)^[1 + (1 + b)]) ((1 : ZMod m), (3 : ZMod m))) =
        returnMap1CaseII (m := m)
          (((returnMap1CaseII (m := m)^[1 + b]) ((1 : ZMod m), (3 : ZMod m)))) := by
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := 1)
        (n := 1 + b) ((1 : ZMod m), (3 : ZMod m)))
  have hsplit2 :
      ((returnMap1CaseII (m := m)^[1 + b]) ((1 : ZMod m), (3 : ZMod m))) =
        ((returnMap1CaseII (m := m)^[b])
          (returnMap1CaseII (m := m) ((1 : ZMod m), (3 : ZMod m)))) := by
    have hb : 1 + b = b + 1 := by omega
    rw [hb]
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := b)
        (n := 1) ((1 : ZMod m), (3 : ZMod m)))
  calc
    ((returnMap1CaseII (m := m)^[m - 1]) ((1 : ZMod m), (3 : ZMod m)))
        = ((returnMap1CaseII (m := m)^[m / 2])
            (((returnMap1CaseII (m := m)^[1 + (1 + b)]) ((1 : ZMod m), (3 : ZMod m))))) := by
              exact hsplit0
    _ = ((returnMap1CaseII (m := m)^[m / 2])
            (returnMap1CaseII (m := m)
              (((returnMap1CaseII (m := m)^[1 + b]) ((1 : ZMod m), (3 : ZMod m)))))) := by
          rw [hsplit1]
    _ = ((returnMap1CaseII (m := m)^[m / 2])
            (returnMap1CaseII (m := m)
              (((returnMap1CaseII (m := m)^[b])
                (returnMap1CaseII (m := m) ((1 : ZMod m), (3 : ZMod m))))))) := by
          rw [hsplit2]
    _ = ((returnMap1CaseII (m := m)^[m / 2])
            (returnMap1CaseII (m := m)
              (((returnMap1CaseII (m := m)^[b])
                (returnMap1CaseII (m := m)
                  ((1 : ZMod m), (((m - (m - 5) - 2 : ℕ) : ZMod m)))))))) := by
          rw [hthree]
    _ = ((returnMap1CaseII (m := m)^[m / 2])
            (returnMap1CaseII (m := m)
              (((returnMap1CaseII (m := m)^[b])
                ((2 : ZMod m), (((m - (m - 5) - 2 : ℕ) : ZMod m))))))) := by
          simpa using
            congrArg (fun u =>
              ((returnMap1CaseII (m := m)^[m / 2])
                (returnMap1CaseII (m := m) (((returnMap1CaseII (m := m)^[b]) u)))))
              (returnMap1CaseII_odd_vertical_one (m := m) (x := m - 5) hx3 hxle)
    _ = ((returnMap1CaseII (m := m)^[m / 2])
            (returnMap1CaseII (m := m)
              ((((2 + b : ℕ) : ZMod m)), ((((m - (m - 5) - 2) + b : ℕ) : ZMod m))))) := by
          simpa [b] using
            congrArg (fun u => ((returnMap1CaseII (m := m)^[m / 2]) (returnMap1CaseII (m := m) u)))
              (iterate_returnMap1CaseII_odd_suffix_prefix (m := m) hm (x := m - 5) hx3 hxle hxodd)
    _ = ((returnMap1CaseII (m := m)^[m / 2])
            ((((4 + b : ℕ) : ZMod m)), ((((m - (m - 5) - 2) + b : ℕ) : ZMod m)))) := by
          simpa [b, hthree] using
            congrArg (fun u => ((returnMap1CaseII (m := m)^[m / 2]) u))
              (returnMap1CaseII_odd_suffix_diag (m := m) hm (x := m - 5) hx3 hxle hxodd)
    _ = ((1 : ZMod m), (0 : ZMod m)) := by
          have hbhalf : (4 + b : ℕ) = m / 2 + 1 := by
            dsimp [b]
            rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
            rw [hq]
            omega
          have hkhalf : (m - (m - 5) - 2) + b = m / 2 := by
            dsimp [b]
            rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
            rw [hq]
            omega
          simpa [hbhalf, hkhalf] using
            iterate_returnMap1CaseII_m_sub_five_suffix_tail (m := m) hm

theorem firstReturn_line_m_sub_five_caseII [Fact (9 < m)] (hm : m % 6 = 4) :
    let xFin : Fin m := ⟨m - 5, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin)) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
  let xFin : Fin m := ⟨m - 5, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  have hx3 : 3 ≤ m - 5 := by
    have hm9 : 9 < m := Fact.out
    omega
  have hxle : m - 5 ≤ m - 5 := le_rfl
  let b : ℕ := ((m - 5) - 1) / 2
  have hxb : m - 5 = 1 + 2 * b := by
    dsimp [b]
    rcases even_of_mod_six_eq_four (m := m) hm with ⟨q, hq⟩
    rw [hq]
    omega
  have hxodd : Odd (m - 5) := by
    refine ⟨b, ?_⟩
    omega
  let a : ℕ := (m - 1 - (m - 5)) / 2
  have ha : a = 2 := by
    dsimp [a]
    omega
  have hdecomp : m + 4 = (m - 1) + (1 + ((a - 1) + (1 + a))) := by
    rw [ha]
    omega
  have hsplit0 :
      ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin)) =
        ((returnMap1CaseII (m := m)^[m - 1])
          (((returnMap1CaseII (m := m)^[1 + ((a - 1) + (1 + a))]) (linePoint1 (m := m) xFin)))) := by
    simpa [hdecomp] using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := m - 1)
        (n := 1 + ((a - 1) + (1 + a))) (linePoint1 (m := m) xFin))
  have hsplit1 :
      ((returnMap1CaseII (m := m)^[1 + ((a - 1) + (1 + a))]) (linePoint1 (m := m) xFin)) =
        returnMap1CaseII (m := m)
          (((returnMap1CaseII (m := m)^[(a - 1) + (1 + a)]) (linePoint1 (m := m) xFin))) := by
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := 1)
        (n := (a - 1) + (1 + a)) (linePoint1 (m := m) xFin))
  have hsplit2 :
      ((returnMap1CaseII (m := m)^[(a - 1) + (1 + a)]) (linePoint1 (m := m) xFin)) =
        ((returnMap1CaseII (m := m)^[a - 1])
          (((returnMap1CaseII (m := m)^[1 + a]) (linePoint1 (m := m) xFin)))) := by
    simpa [Nat.add_assoc] using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := a - 1)
        (n := 1 + a) (linePoint1 (m := m) xFin))
  have hsplit3 :
      ((returnMap1CaseII (m := m)^[1 + a]) (linePoint1 (m := m) xFin)) =
        returnMap1CaseII (m := m)
          (((returnMap1CaseII (m := m)^[a]) (linePoint1 (m := m) xFin))) := by
    simpa using
      (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := 1)
        (n := a) (linePoint1 (m := m) xFin))
  have haux :
      ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin)) =
        ((1 : ZMod m), (0 : ZMod m)) := by
    calc
      ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin))
          = ((returnMap1CaseII (m := m)^[m - 1])
              (((returnMap1CaseII (m := m)^[1 + ((a - 1) + (1 + a))]) (linePoint1 (m := m) xFin)))) := by
                exact hsplit0
      _ = ((returnMap1CaseII (m := m)^[m - 1])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[(a - 1) + (1 + a)]) (linePoint1 (m := m) xFin))))) := by
            rw [hsplit1]
      _ = ((returnMap1CaseII (m := m)^[m - 1])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  (((returnMap1CaseII (m := m)^[1 + a]) (linePoint1 (m := m) xFin))))))) := by
            rw [hsplit2]
      _ = ((returnMap1CaseII (m := m)^[m - 1])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  (returnMap1CaseII (m := m)
                    (((returnMap1CaseII (m := m)^[a]) (linePoint1 (m := m) xFin)))))))) := by
            rw [hsplit3]
      _ = ((returnMap1CaseII (m := m)^[m - 1])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  (returnMap1CaseII (m := m) ((((m - 5 + a : ℕ) : ZMod m)), (((a : ℕ) : ZMod m)))))))) := by
            simpa [xFin, a] using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[m - 1])
                (returnMap1CaseII (m := m) (((returnMap1CaseII (m := m)^[a - 1]) (returnMap1CaseII (m := m) u))))))
                (iterate_returnMap1CaseII_odd_prefix (m := m) hm (x := m - 5) hx3 hxle hxodd)
      _ = ((returnMap1CaseII (m := m)^[m - 1])
              (returnMap1CaseII (m := m)
                (((returnMap1CaseII (m := m)^[a - 1])
                  ((((m - 5 + a + 2 : ℕ) : ZMod m)), (((a : ℕ) : ZMod m))))))) := by
            simpa [xFin, a] using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[m - 1])
                (returnMap1CaseII (m := m) (((returnMap1CaseII (m := m)^[a - 1]) u)))))
                (returnMap1CaseII_odd_diag (m := m) hm (x := m - 5) hx3 hxle hxodd)
      _ = ((returnMap1CaseII (m := m)^[m - 1])
              (returnMap1CaseII (m := m)
                ((0 : ZMod m), (((m - (m - 5) - 2 : ℕ) : ZMod m))))) := by
            simpa [xFin, a] using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[m - 1]) (returnMap1CaseII (m := m) u)))
                (iterate_returnMap1CaseII_odd_middle (m := m) hm (x := m - 5) hx3 hxle hxodd)
      _ = ((returnMap1CaseII (m := m)^[m - 1])
              ((1 : ZMod m), (((m - (m - 5) - 2 : ℕ) : ZMod m)))) := by
            simpa using
              congrArg (fun u => ((returnMap1CaseII (m := m)^[m - 1]) u))
                (returnMap1CaseII_odd_vertical_zero (m := m) (x := m - 5) hx3 hxle)
      _ = ((returnMap1CaseII (m := m)^[m - 1]) ((1 : ZMod m), (3 : ZMod m))) := by
            have hthree : (((m - (m - 5) - 2 : ℕ) : ZMod m)) = (3 : ZMod m) := by
              have hnat : m - (m - 5) - 2 = 3 := by omega
              simpa [hnat]
            rw [hthree]
      _ = ((1 : ZMod m), (0 : ZMod m)) := by
            exact iterate_returnMap1CaseII_odd_suffix_m_sub_five (m := m) hm
  have hT : (TorusD3Even.T1CaseII (m := m) hm xFin).1 = 1 := by
    have hsrc : xFin.1 = m - 5 := by
      simp [xFin]
    simpa [xFin] using
      TorusD3Even.T1CaseII_eq_one_of_val_eq_m_sub_five (m := m) (hm := hm) (x := xFin) hsrc
  calc
    ((returnMap1CaseII (m := m)^[m + 4]) (linePoint1 (m := m) xFin))
        = ((1 : ZMod m), (0 : ZMod m)) := haux
    _ = linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
          ext <;> simp [linePoint1, hT]

theorem returnMap1CaseII_m_sub_three_zero [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((((m - 3 : ℕ) : ZMod m)), (0 : ZMod m)) =
      ((((m - 2 : ℕ) : ZMod m)), (1 : ZMod m)) := by
  have hm5 : 5 < m := Fact.out
  have hi0 : (((m - 3 : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := m - 3) (by omega) (by omega)
  have hi1 : (((m - 3 : ℕ) : ZMod m)) ≠ 1 := by
    exact natCast_ne_one_of_two_le_lt (m := m) (n := m - 3) (by omega) (by omega)
  have hi2 : (((m - 3 : ℕ) : ZMod m)) ≠ 2 := by
    exact natCast_ne_natCast_of_lt (m := m) (a := m - 3) (b := 2) (by omega) (by omega) (by omega)
  have hineg2 : (((m - 3 : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
    exact natCast_ne_neg_two_of_lt (m := m) (n := m - 3) (by omega)
  have hineg1 : (((m - 3 : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := m - 3) (by omega)
  have h00 : ¬ ((((m - 3 : ℕ) : ZMod m)) = 0 ∧ ((0 : ZMod m) = 0)) := by
    intro h
    exact hi0 h.1
  have hdiag :
      ¬ ((((m - 3 : ℕ) : ZMod m)) + (0 : ZMod m) = (-1 : ZMod m) ∧
          (((m - 3 : ℕ) : ZMod m)) ≠ 0 ∧
          (((m - 3 : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
          (((m - 3 : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
          (((m - 3 : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
    intro h
    exact hineg1 (by simpa using h.1)
  have h10 : ¬ ((((m - 3 : ℕ) : ZMod m)) = (1 : ZMod m) ∧ ((0 : ZMod m) = 0)) := by
    intro h
    exact hi1 h.1
  have hneg20 : ¬ ((((m - 3 : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((0 : ZMod m) = 0)) := by
    intro h
    exact hineg2 h.1
  have hneg1neg1 :
      ¬ ((((m - 3 : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ ((0 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact neg_ne_zero.mpr (one_ne_zero (m := m)) h.2.symm
  have h0line :
      ¬ ((((m - 3 : ℕ) : ZMod m)) = 0 ∧
          ((0 : ZMod m)) ≠ 0 ∧
          ((0 : ZMod m)) ≠ (-1 : ZMod m)) := by
    intro h
    exact hi0 h.1
  have h1line :
      ¬ ((((m - 3 : ℕ) : ZMod m)) = (1 : ZMod m) ∧ ((0 : ZMod m)) ≠ 0) := by
    intro h
    exact hi1 h.1
  have h2neg2 :
      ¬ ((((m - 3 : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((0 : ZMod m) = (-2 : ZMod m))) := by
    intro h
    exact hi2 h.1
  have h2neg1 :
      ¬ ((((m - 3 : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((0 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact hi2 h.1
  have hneg2one :
      ¬ ((((m - 3 : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((0 : ZMod m) = (1 : ZMod m))) := by
    intro h
    exact hineg2 h.1
  calc
    returnMap1CaseII (m := m) ((((m - 3 : ℕ) : ZMod m)), (0 : ZMod m))
        = bulkMap1CaseI (m := m) ((((m - 3 : ℕ) : ZMod m)), (0 : ZMod m)) := by
            exact returnMap1CaseII_eq_bulk_of_not_special (m := m)
              (i := (((m - 3 : ℕ) : ZMod m))) (k := (0 : ZMod m))
              h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((m - 2 : ℕ) : ZMod m)), (1 : ZMod m)) := by
          ext
          · change (((m - 3 : ℕ) : ZMod m) + 1) = (((m - 2 : ℕ) : ZMod m))
            simpa [Nat.cast_add] using
              congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) (show m - 3 + 1 = m - 2 by omega)
          · change (0 : ZMod m) + 1 = (1 : ZMod m)
            norm_num

theorem iterate_returnMap1CaseII_two_two_prefix [Fact (9 < m)] (hm : m % 6 = 4) {t : ℕ}
    (ht : t ≤ m - 3) :
    ((returnMap1CaseII (m := m)^[t]) ((2 : ZMod m), (2 : ZMod m))) =
      ((((2 + t : ℕ) : ZMod m)), (((2 + t : ℕ) : ZMod m))) := by
  have hm5 : 5 < m := by
    have hm9 : 9 < m := Fact.out
    omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hm2 : 2 ≤ m := by
    have hm9 : 9 < m := Fact.out
    omega
  have hmEven : Even m := even_of_mod_six_eq_four (m := m) hm
  calc
    ((returnMap1CaseII (m := m)^[t]) ((2 : ZMod m), (2 : ZMod m)))
        = ((bulkMap1CaseI (m := m)^[t]) ((2 : ZMod m), (2 : ZMod m))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((2 : ZMod m), (2 : ZMod m))) t ?_
            intro s hs
            rw [iterate_bulkMap1CaseI (m := m) s ((2 : ZMod m), (2 : ZMod m))]
            have hslt : s < m - 3 := lt_of_lt_of_le hs ht
            have hi_pos : 0 < 2 + s := by omega
            have hi_lt : 2 + s < m := by omega
            have hk_pos : 0 < 2 + s := by omega
            have hk_lt : 2 + s < m := by omega
            have hi0 : (((2 + s : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 2 + s) hi_pos hi_lt
            have hi1 : (((2 + s : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 2 + s) (by omega) hi_lt
            have hk0 : (((2 + s : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 2 + s) hk_pos hk_lt
            have hk1 : (((2 + s : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 2 + s) (by omega) hk_lt
            have hkneg1 : (((2 + s : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := 2 + s) (by omega)
            have hdiag_ne :
                ((((2 + s : ℕ) : ZMod m)) + (((2 + s : ℕ) : ZMod m))) ≠ (-1 : ZMod m) := by
              have hsum_ne : (((4 + 2 * s : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_even (m := m) hmEven (n := 4 + 2 * s) ⟨s + 2, by omega⟩
              intro h
              apply hsum_ne
              have hsum_eq :
                  ((((2 + s : ℕ) : ZMod m)) + (((2 + s : ℕ) : ZMod m))) =
                    (((4 + 2 * s : ℕ) : ZMod m)) := by
                have hnat : (2 + s) + (2 + s) = 4 + 2 * s := by
                  omega
                calc
                  ((((2 + s : ℕ) : ZMod m)) + (((2 + s : ℕ) : ZMod m))) =
                      ((((2 + s) + (2 + s) : ℕ) : ZMod m)) := by
                        simp [Nat.cast_add]
                  _ = (((4 + 2 * s : ℕ) : ZMod m)) := by
                        simp [hnat]
              exact hsum_eq.symm.trans h
            have h00 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = 0 ∧ (((2 + s : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi0 h.1
            have hdiag :
                ¬ ((((2 + s : ℕ) : ZMod m)) + (((2 + s : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ 0 ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hdiag_ne h.1
            have h10 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((2 + s : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi1 h.1
            have hneg20 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((2 + s : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hk0 h.2
            have hneg1neg1 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ (((2 + s : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hkneg1 h.2
            have h0line :
                ¬ ((((2 + s : ℕ) : ZMod m)) = 0 ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ 0 ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi0 h.1
            have h1line :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    (((2 + s : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi1 h.1
            have h2neg2 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((2 + s : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              have hs0 : s = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + s) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst hs0
              exact natCast_ne_neg_two_of_lt (m := m) (n := 2) (by
                have hm9 : 9 < m := Fact.out
                omega) h.2
            have h2neg1 :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((2 + s : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              have hs0 : s = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + s) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst hs0
              exact natCast_ne_neg_one_of_lt (m := m) (n := 2) (by
                have hm9 : 9 < m := Fact.out
                omega) h.2
            have hneg2one :
                ¬ ((((2 + s : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((2 + s : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hk1 h.2
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((2 + s : ℕ) : ZMod m))) (k := (((2 + s : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((2 + t : ℕ) : ZMod m)), (((2 + t : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) t ((2 : ZMod m), (2 : ZMod m))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]

theorem iterate_returnMap1CaseII_m_sub_three_front [Fact (9 < m)] :
    let xFin : Fin m := ⟨m - 3, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    ((returnMap1CaseII (m := m)^[5]) (linePoint1 (m := m) xFin)) =
      ((2 : ZMod m), (2 : ZMod m)) := by
  let xFin : Fin m := ⟨m - 3, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  have hm5 : 5 < m := by
    have hm9 : 9 < m := Fact.out
    omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hm2 : 2 ≤ m := by
    have hm9 : 9 < m := Fact.out
    omega
  have hm2cast : (((m - 2 : ℕ) : ZMod m)) = (-2 : ZMod m) := by
    exact cast_sub_two_eq_neg_two (m := m) hm2
  have hm1cast : (((m - 1 : ℕ) : ZMod m)) = (-1 : ZMod m) := by
    exact cast_sub_one_eq_neg_one (m := m) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hline :
      linePoint1 (m := m) xFin = ((((m - 3 : ℕ) : ZMod m)), (0 : ZMod m)) := by
    ext <;> simp [linePoint1, xFin]
  have h1 :
      ((returnMap1CaseII (m := m)^[1]) (linePoint1 (m := m) xFin)) =
        ((((m - 2 : ℕ) : ZMod m)), (1 : ZMod m)) := by
    simpa [Function.iterate_one, hline] using
      returnMap1CaseII_m_sub_three_zero (m := m)
  have h2 :
      ((returnMap1CaseII (m := m)^[2]) (linePoint1 (m := m) xFin)) =
        ((-1 : ZMod m), (1 : ZMod m)) := by
    rw [show (2 : ℕ) = 1 + 1 by norm_num, Function.iterate_add_apply, h1]
    simpa [Function.iterate_one, hm2cast] using
      returnMap1CaseII_neg_two_one (m := m)
  have h3 :
      ((returnMap1CaseII (m := m)^[3]) (linePoint1 (m := m) xFin)) =
        ((0 : ZMod m), (2 : ZMod m)) := by
    rw [show (3 : ℕ) = 1 + 2 by norm_num, Function.iterate_add_apply, h2]
    simpa [Function.iterate_one, hm1cast] using
      returnMap1CaseII_neg_one_one (m := m)
  have h4 :
      ((returnMap1CaseII (m := m)^[4]) (linePoint1 (m := m) xFin)) =
        ((1 : ZMod m), (2 : ZMod m)) := by
    rw [show (4 : ℕ) = 1 + 3 by norm_num, Function.iterate_add_apply, h3]
    simpa [Function.iterate_one] using
      returnMap1CaseII_zero_two (m := m)
  have h5 :
      ((returnMap1CaseII (m := m)^[5]) (linePoint1 (m := m) xFin)) =
        ((2 : ZMod m), (2 : ZMod m)) := by
    rw [show (5 : ℕ) = 1 + 4 by norm_num, Function.iterate_add_apply, h4]
    simpa [Function.iterate_one] using
      returnMap1CaseII_one_two (m := m)
  exact h5

theorem iterate_returnMap1CaseII_m_sub_three_middle [Fact (9 < m)] (hm : m % 6 = 4) :
    ((returnMap1CaseII (m := m)^[m - 3]) ((2 : ZMod m), (2 : ZMod m))) =
      ((-1 : ZMod m), (-1 : ZMod m)) := by
  have h := iterate_returnMap1CaseII_two_two_prefix (m := m) hm (t := m - 3) le_rfl
  have hnat : 2 + (m - 3) = m - 1 := by omega
  simpa [Nat.cast_add, hnat, cast_sub_one_eq_neg_one (m := m) (by
    have hm9 : 9 < m := Fact.out
    omega)] using h

theorem iterate_returnMap1CaseII_m_sub_three_tail [Fact (9 < m)] :
    ((returnMap1CaseII (m := m)^[4]) ((-1 : ZMod m), (-1 : ZMod m))) =
      ((4 : ZMod m), (0 : ZMod m)) := by
  have hm5 : 5 < m := by
    have hm9 : 9 < m := Fact.out
    omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have h1 :
      ((returnMap1CaseII (m := m)^[1]) ((-1 : ZMod m), (-1 : ZMod m))) =
        ((1 : ZMod m), (-1 : ZMod m)) := by
    simpa [Function.iterate_one] using
      returnMap1CaseII_neg_one_neg_one (m := m)
  have h2 :
      ((returnMap1CaseII (m := m)^[2]) ((-1 : ZMod m), (-1 : ZMod m))) =
        ((2 : ZMod m), (-1 : ZMod m)) := by
    rw [show (2 : ℕ) = 1 + 1 by norm_num, Function.iterate_add_apply, h1]
    simpa [Function.iterate_one] using
      returnMap1CaseII_one_neg_one (m := m)
  have h3 :
      ((returnMap1CaseII (m := m)^[3]) ((-1 : ZMod m), (-1 : ZMod m))) =
        ((3 : ZMod m), (-1 : ZMod m)) := by
    rw [show (3 : ℕ) = 1 + 2 by norm_num, Function.iterate_add_apply, h2]
    simpa [Function.iterate_one] using
      returnMap1CaseII_two_neg_one (m := m)
  have h4 :
      ((returnMap1CaseII (m := m)^[4]) ((-1 : ZMod m), (-1 : ZMod m))) =
        ((4 : ZMod m), (0 : ZMod m)) := by
    rw [show (4 : ℕ) = 1 + 3 by norm_num, Function.iterate_add_apply, h3]
    simpa [Function.iterate_one] using
      returnMap1CaseII_three_neg_one (m := m)
  exact h4

theorem firstReturn_line_m_sub_three_caseII [Fact (9 < m)] (hm : m % 6 = 4) :
    let xFin : Fin m := ⟨m - 3, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin)) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
  let xFin : Fin m := ⟨m - 3, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  have hfront :
      ((returnMap1CaseII (m := m)^[5]) (linePoint1 (m := m) xFin)) =
        ((2 : ZMod m), (2 : ZMod m)) := by
    simpa [xFin] using iterate_returnMap1CaseII_m_sub_three_front (m := m)
  have haux :
      ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin)) =
        ((4 : ZMod m), (0 : ZMod m)) := by
    calc
      ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin))
          = ((returnMap1CaseII (m := m)^[4])
              (((returnMap1CaseII (m := m)^[(m - 3) + 5]) (linePoint1 (m := m) xFin)))) := by
                rw [show m + 6 = 4 + ((m - 3) + 5) by omega, Function.iterate_add_apply]
      _ = ((returnMap1CaseII (m := m)^[4])
              (((returnMap1CaseII (m := m)^[m - 3])
                (((returnMap1CaseII (m := m)^[5]) (linePoint1 (m := m) xFin)))))) := by
            rw [Function.iterate_add_apply]
      _ = ((returnMap1CaseII (m := m)^[4])
              (((returnMap1CaseII (m := m)^[m - 3]) ((2 : ZMod m), (2 : ZMod m))))) := by
            rw [hfront]
      _ = ((returnMap1CaseII (m := m)^[4]) ((-1 : ZMod m), (-1 : ZMod m))) := by
            rw [iterate_returnMap1CaseII_m_sub_three_middle (m := m) hm]
      _ = ((4 : ZMod m), (0 : ZMod m)) := by
            exact iterate_returnMap1CaseII_m_sub_three_tail (m := m)
  have hT : (TorusD3Even.T1CaseII (m := m) hm xFin).1 = 4 := by
    have hsrc : xFin.1 = m - 3 := by
      simp [xFin]
    simpa [xFin] using
      TorusD3Even.T1CaseII_eq_four_of_val_eq_m_sub_three (m := m) hm hsrc
  calc
    ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin))
        = ((4 : ZMod m), (0 : ZMod m)) := haux
    _ = linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
          ext <;> simp [linePoint1, hT]

theorem returnMap1CaseII_neg_one_zero [Fact (5 < m)] :
    returnMap1CaseII (m := m) ((-1 : ZMod m), (0 : ZMod m)) = ((0 : ZMod m), (1 : ZMod m)) := by
  have hneg10 : (-1 : ZMod m) ≠ 0 := by
    exact neg_ne_zero.mpr (one_ne_zero (m := m))
  have hneg11 : (-1 : ZMod m) ≠ 1 := by
    intro h
    exact one_ne_neg_one (m := m) h.symm
  have hneg1neg2 : (-1 : ZMod m) ≠ (-2 : ZMod m) := by
    intro h
    have h12 : (1 : ZMod m) = (2 : ZMod m) := by
      simpa using congrArg Neg.neg h
    have hneq : (1 : ZMod m) ≠ (2 : ZMod m) := by
      simpa using natCast_ne_natCast_of_lt (m := m) (a := 1) (b := 2) (by
        have hm5 : 5 < m := Fact.out
        omega) (by
        have hm5 : 5 < m := Fact.out
        omega) (by omega)
    exact hneq h12
  have h00 : ¬ (((-1 : ZMod m) = 0) ∧ ((0 : ZMod m) = 0)) := by
    intro h
    exact hneg10 h.1
  have hdiag :
      ¬ (((-1 : ZMod m) + (0 : ZMod m) = (-1 : ZMod m)) ∧
          (-1 : ZMod m) ≠ 0 ∧ (-1 : ZMod m) ≠ (1 : ZMod m) ∧
          (-1 : ZMod m) ≠ (-2 : ZMod m) ∧ (-1 : ZMod m) ≠ (-1 : ZMod m)) := by
    intro h
    exact h.2.2.2.2 rfl
  have h10 : ¬ (((-1 : ZMod m) = (1 : ZMod m)) ∧ ((0 : ZMod m) = 0)) := by
    intro h
    exact hneg11 h.1
  have hneg20 : ¬ (((-1 : ZMod m) = (-2 : ZMod m)) ∧ ((0 : ZMod m) = 0)) := by
    intro h
    exact hneg1neg2 h.1
  have hneg1neg1 : ¬ (((-1 : ZMod m) = (-1 : ZMod m)) ∧ ((0 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact neg_ne_zero.mpr (one_ne_zero (m := m)) h.2.symm
  have h0line :
      ¬ (((-1 : ZMod m) = 0) ∧ (0 : ZMod m) ≠ 0 ∧ (0 : ZMod m) ≠ (-1 : ZMod m)) := by
    intro h
    exact hneg10 h.1
  have h1line :
      ¬ (((-1 : ZMod m) = (1 : ZMod m)) ∧ (0 : ZMod m) ≠ 0) := by
    intro h
    exact hneg11 h.1
  have h2neg2 : ¬ (((-1 : ZMod m) = (2 : ZMod m)) ∧ ((0 : ZMod m) = (-2 : ZMod m))) := by
    intro h
    have h0neg2 : (0 : ZMod m) ≠ (-2 : ZMod m) := by
      simpa using natCast_ne_neg_two_of_lt (m := m) (n := 0) (by
        have hm5 : 5 < m := Fact.out
        omega)
    exact h0neg2 h.2
  have h2neg1 : ¬ (((-1 : ZMod m) = (2 : ZMod m)) ∧ ((0 : ZMod m) = (-1 : ZMod m))) := by
    intro h
    exact neg_ne_zero.mpr (one_ne_zero (m := m)) h.2.symm
  have hneg2one : ¬ (((-1 : ZMod m) = (-2 : ZMod m)) ∧ ((0 : ZMod m) = (1 : ZMod m))) := by
    intro h
    exact zero_ne_one h.2
  calc
    returnMap1CaseII (m := m) ((-1 : ZMod m), (0 : ZMod m))
        = bulkMap1CaseI (m := m) ((-1 : ZMod m), (0 : ZMod m)) := by
            exact returnMap1CaseII_eq_bulk_of_not_special (m := m)
              (i := (-1 : ZMod m)) (k := (0 : ZMod m))
              h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((0 : ZMod m), (1 : ZMod m)) := by
          ext
          · change (-1 : ZMod m) + 1 = (0 : ZMod m)
            ring
          · norm_num [bulkMap1CaseI]

theorem iterate_returnMap1CaseII_m_sub_one_front [Fact (9 < m)] :
    let xFin : Fin m := ⟨m - 1, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    ((returnMap1CaseII (m := m)^[3]) (linePoint1 (m := m) xFin)) =
      ((2 : ZMod m), (1 : ZMod m)) := by
  let xFin : Fin m := ⟨m - 1, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  have hm5 : 5 < m := by
    have hm9 : 9 < m := Fact.out
    omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hm1cast : (((m - 1 : ℕ) : ZMod m)) = (-1 : ZMod m) := by
    exact cast_sub_one_eq_neg_one (m := m) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hline :
      linePoint1 (m := m) xFin = ((((m - 1 : ℕ) : ZMod m)), (0 : ZMod m)) := by
    ext <;> simp [linePoint1, xFin]
  have h1 :
      ((returnMap1CaseII (m := m)^[1]) (linePoint1 (m := m) xFin)) =
        ((0 : ZMod m), (1 : ZMod m)) := by
    simpa [Function.iterate_one, hline, hm1cast] using
      returnMap1CaseII_neg_one_zero (m := m)
  have h2 :
      ((returnMap1CaseII (m := m)^[2]) (linePoint1 (m := m) xFin)) =
        ((1 : ZMod m), (1 : ZMod m)) := by
    rw [show (2 : ℕ) = 1 + 1 by norm_num, Function.iterate_add_apply, h1]
    simpa [Function.iterate_one] using
      returnMap1CaseII_eq_add_one_of_i_zero (m := m) (k := (1 : ZMod m))
        (one_ne_zero (m := m)) (one_ne_neg_one (m := m))
  have h3 :
      ((returnMap1CaseII (m := m)^[3]) (linePoint1 (m := m) xFin)) =
        ((2 : ZMod m), (1 : ZMod m)) := by
    rw [show (3 : ℕ) = 1 + 2 by norm_num, Function.iterate_add_apply, h2]
    simpa [Function.iterate_one] using
      returnMap1CaseII_eq_add_one_of_i_one (m := m) (k := (1 : ZMod m))
        (one_ne_zero (m := m))
  exact h3

theorem iterate_returnMap1CaseII_two_one_prefix [Fact (9 < m)] :
    ((returnMap1CaseII (m := m)^[m / 2 - 2]) ((2 : ZMod m), (1 : ZMod m))) =
      ((((m / 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))) := by
  calc
    ((returnMap1CaseII (m := m)^[m / 2 - 2]) ((2 : ZMod m), (1 : ZMod m)))
        = ((bulkMap1CaseI (m := m)^[m / 2 - 2]) ((2 : ZMod m), (1 : ZMod m))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((2 : ZMod m), (1 : ZMod m))) (m / 2 - 2) ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t ((2 : ZMod m), (1 : ZMod m))]
            have hi_pos : 0 < 2 + t := by
              have hm9 : 9 < m := Fact.out
              omega
            have hi_lt : 2 + t < m := by
              have hm9 : 9 < m := Fact.out
              omega
            have hk_pos : 0 < 1 + t := by
              have hm9 : 9 < m := Fact.out
              omega
            have hk_lt : 1 + t < m := by
              have hm9 : 9 < m := Fact.out
              omega
            have hi_ne_zero : (((2 + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 2 + t) hi_pos hi_lt
            have hi_ne_one : (((2 + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 2 + t) (by omega) hi_lt
            have hi_ne_neg_one : (((2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := 2 + t) (by
                have hm9 : 9 < m := Fact.out
                omega)
            have h00 : ¬ ((((2 + t : ℕ) : ZMod m)) = 0 ∧ (((1 + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((2 + t : ℕ) : ZMod m)) + (((1 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsum_ne : (((3 + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := 3 + 2 * t) (by
                  have hm9 : 9 < m := Fact.out
                  omega)
              apply hsum_ne
              have hnat : 2 + t + (1 + t) = 3 + 2 * t := by
                omega
              have hsum_eq :
                  ((((2 + t : ℕ) : ZMod m)) + (((1 + t : ℕ) : ZMod m))) =
                    (((3 + 2 * t : ℕ) : ZMod m)) := by
                calc
                  ((((2 + t : ℕ) : ZMod m)) + (((1 + t : ℕ) : ZMod m))) =
                      ((((2 + t) + (1 + t) : ℕ) : ZMod m)) := by
                        simp [Nat.cast_add]
                  _ = (((3 + 2 * t : ℕ) : ZMod m)) := by
                        simp [hnat]
              exact hsum_eq.symm.trans h.1
            have h10 : ¬ ((((2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((1 + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((1 + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 1 + t) hk_pos hk_lt h.2
            have hneg1neg1 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ (((1 + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_one h.1
            have h0line :
                ¬ ((((2 + t : ℕ) : ZMod m)) = 0 ∧
                    (((1 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((1 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ (((1 + t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((1 + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              have ht0 : t = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + t) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst ht0
              have h1neg2 : (1 : ZMod m) ≠ (-2 : ZMod m) := by
                simpa using natCast_ne_neg_two_of_lt (m := m) (n := 1) (by
                  have hm9 : 9 < m := Fact.out
                  omega)
              exact h1neg2 (by simpa using h.2)
            have h2neg1 :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ (((1 + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              have ht0 : t = 0 := by
                have hmod := (ZMod.natCast_eq_natCast_iff' (2 + t) 2 m).1 (by simpa using h.1)
                rw [Nat.mod_eq_of_lt hi_lt, Nat.mod_eq_of_lt (by omega)] at hmod
                omega
              subst ht0
              exact one_ne_neg_one (m := m) (by simpa using h.2)
            have hneg2one :
                ¬ ((((2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ (((1 + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              have h2neg2 : (((2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
                exact natCast_ne_neg_two_of_lt (m := m) (n := 2 + t) (by
                  have hm9 : 9 < m := Fact.out
                  omega)
              exact h2neg2 h.1
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((2 + t : ℕ) : ZMod m))) (k := (((1 + t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((2 + (m / 2 - 2) : ℕ) : ZMod m)), (((1 + (m / 2 - 2) : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) (m / 2 - 2) ((2 : ZMod m), (1 : ZMod m))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
    _ = ((((m / 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))) := by
          have hfirst : 2 + (m / 2 - 2) = m / 2 := by
            have hm9 : 9 < m := Fact.out
            omega
          have hsecond : 1 + (m / 2 - 2) = m / 2 - 1 := by
            have hm9 : 9 < m := Fact.out
            omega
          simp [hfirst, hsecond]

theorem returnMap1CaseII_half_diag [Fact (9 < m)] (hm : m % 6 = 4) :
    returnMap1CaseII (m := m)
      ((((m / 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))) =
      ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))) := by
  have hmEven : Even m := even_of_mod_six_eq_four (m := m) hm
  have hdiag :
      ((((m / 2 : ℕ) : ZMod m)) + (((m / 2 - 1 : ℕ) : ZMod m))) = (-1 : ZMod m) := by
    have hnat : m / 2 + (m / 2 - 1) = m - 1 := by
      rcases hmEven with ⟨q, hq⟩
      rw [hq]
      omega
    have hsum :
        ((((m / 2 : ℕ) : ZMod m)) + (((m / 2 - 1 : ℕ) : ZMod m))) =
          (((m - 1 : ℕ) : ZMod m)) := by
      simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
        congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
    exact hsum.trans <| cast_sub_one_eq_neg_one (m := m) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hi0 : (((m / 2 : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := m / 2) (by
      have hm9 : 9 < m := Fact.out
      omega) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hi1 : (((m / 2 : ℕ) : ZMod m)) ≠ 1 := by
    exact natCast_ne_one_of_two_le_lt (m := m) (n := m / 2) (by
      have hm9 : 9 < m := Fact.out
      omega) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hineg2 : (((m / 2 : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
    exact natCast_ne_neg_two_of_lt (m := m) (n := m / 2) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hineg1 : (((m / 2 : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := m / 2) (by
      have hm9 : 9 < m := Fact.out
      omega)
  calc
    returnMap1CaseII (m := m)
      ((((m / 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m)))
        = ((((m / 2 : ℕ) : ZMod m)) + 2, (((m / 2 - 1 : ℕ) : ZMod m))) := by
            exact returnMap1CaseII_eq_add_two_of_diag (m := m) hdiag hi0 hi1 hineg2 hineg1
    _ = ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))) := by
          ext
          · simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
          · rfl

theorem iterate_returnMap1CaseII_half_plus_two_prefix [Fact (9 < m)] (hm : m % 6 = 4) :
    ((returnMap1CaseII (m := m)^[m / 2 - 2])
      ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m)))) =
      ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
  have hmEven : Even m := even_of_mod_six_eq_four (m := m) hm
  calc
    ((returnMap1CaseII (m := m)^[m / 2 - 2])
      ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))))
        = ((bulkMap1CaseI (m := m)^[m / 2 - 2])
          ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m)))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m)))) (m / 2 - 2) ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t
              ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m)))]
            have hi_pos : 0 < m / 2 + 2 + t := by
              have hm9 : 9 < m := Fact.out
              omega
            have hi_lt : m / 2 + 2 + t < m := by
              have hm9 : 9 < m := Fact.out
              omega
            have hk_pos : 0 < m / 2 - 1 + t := by
              have hm9 : 9 < m := Fact.out
              omega
            have hk_lt : m / 2 - 1 + t < m := by
              have hm9 : 9 < m := Fact.out
              omega
            have hi_ne_zero : (((m / 2 + 2 + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := m / 2 + 2 + t) hi_pos hi_lt
            have hi_ne_one : (((m / 2 + 2 + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := m / 2 + 2 + t) (by
                have hm9 : 9 < m := Fact.out
                omega) hi_lt
            have hk_ne_zero : (((m / 2 - 1 + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := m / 2 - 1 + t) hk_pos hk_lt
            have hk_ne_one : (((m / 2 - 1 + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := m / 2 - 1 + t) (by
                have hm9 : 9 < m := Fact.out
                omega) hk_lt
            have hk_ne_neg_one : (((m / 2 - 1 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := m / 2 - 1 + t) (by
                have hm9 : 9 < m := Fact.out
                omega)
            have hi_ne_two : (((m / 2 + 2 + t : ℕ) : ZMod m)) ≠ (2 : ZMod m) := by
              exact natCast_ne_natCast_of_lt (m := m) (a := m / 2 + 2 + t) (b := 2) hi_lt (by
                have hm9 : 9 < m := Fact.out
                omega) (by
                have hm9 : 9 < m := Fact.out
                omega)
            have h00 :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = 0 ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) + (((m / 2 - 1 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((m / 2 + 2 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((m / 2 + 2 + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((m / 2 + 2 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((m / 2 + 2 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsum_ne : (((1 + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := 1 + 2 * t) (by
                  have hm9 : 9 < m := Fact.out
                  omega)
              apply hsum_ne
              have hnat : m / 2 + 2 + t + (m / 2 - 1 + t) = m + (1 + 2 * t) := by
                rcases hmEven with ⟨q, hq⟩
                rw [hq]
                omega
              have hsum_eq :
                  ((((m / 2 + 2 + t : ℕ) : ZMod m)) + (((m / 2 - 1 + t : ℕ) : ZMod m))) =
                    (((1 + 2 * t : ℕ) : ZMod m)) := by
                calc
                  ((((m / 2 + 2 + t : ℕ) : ZMod m)) + (((m / 2 - 1 + t : ℕ) : ZMod m)))
                      = (((m + (1 + 2 * t) : ℕ) : ZMod m)) := by
                          simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                            congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
                  _ = (((1 + 2 * t : ℕ) : ZMod m)) := by
                        simp
              exact hsum_eq.symm.trans h.1
            have h10 :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hk_ne_zero h.2
            have hneg1neg1 :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hk_ne_neg_one h.2
            have h0line :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = 0 ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have h2neg1 :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have hneg2one :
                ¬ ((((m / 2 + 2 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧
                    (((m / 2 - 1 + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hk_ne_one h.2
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((m / 2 + 2 + t : ℕ) : ZMod m))) (k := (((m / 2 - 1 + t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((((m / 2 + 2 + (m / 2 - 2) : ℕ) : ZMod m)),
          (((m / 2 - 1 + (m / 2 - 2) : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) (m / 2 - 2)
            ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m)))]
          simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
    _ = ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
          have hfirst : m / 2 + 2 + (m / 2 - 2) = m := by
            rcases hmEven with ⟨q, hq⟩
            rw [hq]
            omega
          have hsecond : m / 2 - 1 + (m / 2 - 2) = m - 3 := by
            rcases hmEven with ⟨q, hq⟩
            rw [hq]
            omega
          ext
          · simp [hfirst]
          · simp [hsecond]

theorem returnMap1CaseII_two_m_sub_three [Fact (9 < m)] :
    returnMap1CaseII (m := m) ((2 : ZMod m), (((m - 3 : ℕ) : ZMod m))) =
      ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
  have hdiag :
      ((2 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) = (-1 : ZMod m) := by
    have hnat : 2 + (m - 3) = m - 1 := by
      have hm9 : 9 < m := Fact.out
      omega
    have hsum :
        ((2 : ZMod m) + (((m - 3 : ℕ) : ZMod m))) =
          (((m - 1 : ℕ) : ZMod m)) := by
      simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
        congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
    exact hsum.trans <| cast_sub_one_eq_neg_one (m := m) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hi0 : (2 : ZMod m) ≠ 0 := by
    exact two_ne_zero (m := m)
  have hi1 : (2 : ZMod m) ≠ 1 := by
    exact two_ne_one (m := m)
  have hineg2 : (2 : ZMod m) ≠ (-2 : ZMod m) := by
    exact natCast_ne_neg_two_of_lt (m := m) (n := 2) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hineg1 : (2 : ZMod m) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := 2) (by
      have hm9 : 9 < m := Fact.out
      omega)
  calc
    returnMap1CaseII (m := m) ((2 : ZMod m), (((m - 3 : ℕ) : ZMod m)))
        = ((2 : ZMod m) + 2, (((m - 3 : ℕ) : ZMod m))) := by
            exact returnMap1CaseII_eq_add_two_of_diag (m := m) hdiag hi0 hi1 hineg2 hineg1
    _ = ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
          ext
          · norm_num
          · rfl

theorem iterate_returnMap1CaseII_four_m_sub_three_tail [Fact (9 < m)] :
    ((returnMap1CaseII (m := m)^[3]) ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) =
      ((7 : ZMod m), (0 : ZMod m)) := by
  calc
    ((returnMap1CaseII (m := m)^[3]) ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m))))
        = ((bulkMap1CaseI (m := m)^[3]) ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) := by
            refine iterate_eq_iterate_of_eq_on_prefix
              (F := returnMap1CaseII (m := m)) (G := bulkMap1CaseI (m := m))
              (z := ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) 3 ?_
            intro t ht
            rw [iterate_bulkMap1CaseI (m := m) t ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m)))]
            have hi_pos : 0 < 4 + t := by
              have hm9 : 9 < m := Fact.out
              omega
            have hi_lt : 4 + t < m := by
              have hm9 : 9 < m := Fact.out
              omega
            have hk_pos : 0 < (m - 3) + t := by
              have hm9 : 9 < m := Fact.out
              omega
            have hk_lt : (m - 3) + t < m := by
              have hm9 : 9 < m := Fact.out
              omega
            have hi_ne_zero : (((4 + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := 4 + t) hi_pos hi_lt
            have hi_ne_one : (((4 + t : ℕ) : ZMod m)) ≠ 1 := by
              exact natCast_ne_one_of_two_le_lt (m := m) (n := 4 + t) (by
                have hm9 : 9 < m := Fact.out
                omega) hi_lt
            have hi_ne_two : (((4 + t : ℕ) : ZMod m)) ≠ (2 : ZMod m) := by
              exact natCast_ne_natCast_of_lt (m := m) (a := 4 + t) (b := 2) hi_lt (by
                have hm9 : 9 < m := Fact.out
                omega) (by omega)
            have hi_ne_neg_one : (((4 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
              exact natCast_ne_neg_one_of_lt (m := m) (n := 4 + t) (by
                have hm9 : 9 < m := Fact.out
                omega)
            have hi_ne_neg_two : (((4 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) := by
              exact natCast_ne_neg_two_of_lt (m := m) (n := 4 + t) (by
                have hm9 : 9 < m := Fact.out
                omega)
            have hk_ne_zero : ((((m - 3) + t : ℕ) : ZMod m)) ≠ 0 := by
              exact natCast_ne_zero_of_pos_lt (m := m) (n := (m - 3) + t) hk_pos hk_lt
            have h00 :
                ¬ ((((4 + t : ℕ) : ZMod m)) = 0 ∧ ((((m - 3) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_zero h.1
            have hdiag :
                ¬ ((((4 + t : ℕ) : ZMod m)) + ((((m - 3) + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧
                    (((4 + t : ℕ) : ZMod m)) ≠ 0 ∧
                    (((4 + t : ℕ) : ZMod m)) ≠ (1 : ZMod m) ∧
                    (((4 + t : ℕ) : ZMod m)) ≠ (-2 : ZMod m) ∧
                    (((4 + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              have hsum_ne : (((1 + 2 * t : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
                exact natCast_ne_neg_one_of_lt (m := m) (n := 1 + 2 * t) (by
                  have hm9 : 9 < m := Fact.out
                  omega)
              apply hsum_ne
              have hnat : 4 + t + ((m - 3) + t) = m + (1 + 2 * t) := by
                omega
              have hsum_eq :
                  ((((4 + t : ℕ) : ZMod m)) + ((((m - 3) + t : ℕ) : ZMod m))) =
                    (((1 + 2 * t : ℕ) : ZMod m)) := by
                calc
                  ((((4 + t : ℕ) : ZMod m)) + ((((m - 3) + t : ℕ) : ZMod m)))
                      = (((m + (1 + 2 * t) : ℕ) : ZMod m)) := by
                          simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
                            congrArg (fun n : ℕ => ((n : ℕ) : ZMod m)) hnat
                  _ = (((1 + 2 * t : ℕ) : ZMod m)) := by
                        simp
              exact hsum_eq.symm.trans h.1
            have h10 :
                ¬ ((((4 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧ ((((m - 3) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hi_ne_one h.1
            have hneg20 :
                ¬ ((((4 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((((m - 3) + t : ℕ) : ZMod m)) = 0) := by
              intro h
              exact hk_ne_zero h.2
            have hneg1neg1 :
                ¬ ((((4 + t : ℕ) : ZMod m)) = (-1 : ZMod m) ∧ ((((m - 3) + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_one h.1
            have h0line :
                ¬ ((((4 + t : ℕ) : ZMod m)) = 0 ∧
                    ((((m - 3) + t : ℕ) : ZMod m)) ≠ 0 ∧
                    ((((m - 3) + t : ℕ) : ZMod m)) ≠ (-1 : ZMod m)) := by
              intro h
              exact hi_ne_zero h.1
            have h1line :
                ¬ ((((4 + t : ℕ) : ZMod m)) = (1 : ZMod m) ∧
                    ((((m - 3) + t : ℕ) : ZMod m)) ≠ 0) := by
              intro h
              exact hi_ne_one h.1
            have h2neg2 :
                ¬ ((((4 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((((m - 3) + t : ℕ) : ZMod m)) = (-2 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have h2neg1 :
                ¬ ((((4 + t : ℕ) : ZMod m)) = (2 : ZMod m) ∧ ((((m - 3) + t : ℕ) : ZMod m)) = (-1 : ZMod m)) := by
              intro h
              exact hi_ne_two h.1
            have hneg2one :
                ¬ ((((4 + t : ℕ) : ZMod m)) = (-2 : ZMod m) ∧ ((((m - 3) + t : ℕ) : ZMod m)) = (1 : ZMod m)) := by
              intro h
              exact hi_ne_neg_two h.1
            simpa [Nat.cast_add, add_assoc, add_left_comm, add_comm] using
              returnMap1CaseII_eq_bulk_of_not_special (m := m)
                (i := (((4 + t : ℕ) : ZMod m))) (k := ((((m - 3) + t : ℕ) : ZMod m)))
                h00 hdiag h10 hneg20 hneg1neg1 h0line h1line h2neg2 h2neg1 hneg2one
    _ = ((7 : ZMod m), ((((m - 3) + 3 : ℕ) : ZMod m))) := by
          rw [iterate_bulkMap1CaseI (m := m) 3 ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m)))]
          ext
          · norm_num
          · simp [Nat.cast_add, add_assoc, add_left_comm, add_comm]
    _ = ((7 : ZMod m), (0 : ZMod m)) := by
          have hm3 : 3 ≤ m := by
            have hm9 : 9 < m := Fact.out
            omega
          have hsum : (m - 3) + 3 = m := Nat.sub_add_cancel hm3
          simp [hsum]

theorem iterate_returnMap1CaseII_zero_m_sub_three_tail [Fact (9 < m)] :
    ((returnMap1CaseII (m := m)^[6]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) =
      ((7 : ZMod m), (0 : ZMod m)) := by
  have hm5 : 5 < m := by
    have hm9 : 9 < m := Fact.out
    omega
  letI : Fact (5 < m) := ⟨hm5⟩
  have hk0 : (((m - 3 : ℕ) : ZMod m)) ≠ 0 := by
    exact natCast_ne_zero_of_pos_lt (m := m) (n := m - 3) (by
      have hm9 : 9 < m := Fact.out
      omega) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have hkneg1 : (((m - 3 : ℕ) : ZMod m)) ≠ (-1 : ZMod m) := by
    exact natCast_ne_neg_one_of_lt (m := m) (n := m - 3) (by
      have hm9 : 9 < m := Fact.out
      omega)
  have h1 :
      ((returnMap1CaseII (m := m)^[1]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) =
        ((1 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
    simpa [Function.iterate_one] using
      returnMap1CaseII_eq_add_one_of_i_zero (m := m) (k := (((m - 3 : ℕ) : ZMod m))) hk0 hkneg1
  have h2 :
      ((returnMap1CaseII (m := m)^[2]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) =
        ((2 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
    rw [show (2 : ℕ) = 1 + 1 by norm_num, Function.iterate_add_apply, h1]
    simpa [Function.iterate_one] using
      returnMap1CaseII_eq_add_one_of_i_one (m := m) (k := (((m - 3 : ℕ) : ZMod m))) hk0
  have h3 :
      ((returnMap1CaseII (m := m)^[3]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) =
        ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
    calc
      ((returnMap1CaseII (m := m)^[3]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))))
          = ((returnMap1CaseII (m := m)^[1])
              (((returnMap1CaseII (m := m)^[2]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m)))))) := by
                simpa using
                  (Function.iterate_add_apply (f := returnMap1CaseII (m := m)) (m := 1) (n := 2)
                    ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))))
      _ = returnMap1CaseII (m := m) ((2 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
            simp [Function.iterate_one, h2]
      _ = ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
            exact returnMap1CaseII_two_m_sub_three (m := m)
  calc
    ((returnMap1CaseII (m := m)^[6]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))))
        = ((returnMap1CaseII (m := m)^[3])
            (((returnMap1CaseII (m := m)^[3]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m)))))) := by
              rw [show (6 : ℕ) = 3 + 3 by norm_num, Function.iterate_add_apply]
    _ = ((returnMap1CaseII (m := m)^[3]) ((4 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) := by
          rw [h3]
    _ = ((7 : ZMod m), (0 : ZMod m)) := by
          exact iterate_returnMap1CaseII_four_m_sub_three_tail (m := m)

theorem iterate_returnMap1CaseII_m_sub_one_middle_aux [Fact (9 < m)] (hm : m % 6 = 4) :
    let xFin : Fin m := ⟨m - 1, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    ((returnMap1CaseII (m := m)^[(m / 2 - 2) + (1 + ((m / 2 - 2) + 3))]) (linePoint1 (m := m) xFin)) =
      ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
  let xFin : Fin m := ⟨m - 1, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  have hfront :
      ((returnMap1CaseII (m := m)^[3]) (linePoint1 (m := m) xFin)) =
        ((2 : ZMod m), (1 : ZMod m)) := by
    simpa [xFin] using iterate_returnMap1CaseII_m_sub_one_front (m := m)
  have hprefix :
      ((returnMap1CaseII (m := m)^[(m / 2 - 2) + 3]) (linePoint1 (m := m) xFin)) =
        ((((m / 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))) := by
    rw [Function.iterate_add_apply, hfront]
    exact iterate_returnMap1CaseII_two_one_prefix (m := m)
  have hdiag :
      ((returnMap1CaseII (m := m)^[1 + ((m / 2 - 2) + 3)]) (linePoint1 (m := m) xFin)) =
        ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m))) := by
    rw [show 1 + ((m / 2 - 2) + 3) = 1 + ((m / 2 - 2) + 3) by rfl, Function.iterate_add_apply, hprefix]
    simpa [Function.iterate_one] using returnMap1CaseII_half_diag (m := m) hm
  calc
    ((returnMap1CaseII (m := m)^[(m / 2 - 2) + (1 + ((m / 2 - 2) + 3))]) (linePoint1 (m := m) xFin))
        = ((returnMap1CaseII (m := m)^[m / 2 - 2])
            (((returnMap1CaseII (m := m)^[1 + ((m / 2 - 2) + 3)]) (linePoint1 (m := m) xFin)))) := by
              rw [Function.iterate_add_apply]
    _ = ((returnMap1CaseII (m := m)^[m / 2 - 2])
          ((((m / 2 + 2 : ℕ) : ZMod m)), (((m / 2 - 1 : ℕ) : ZMod m)))) := by
            rw [hdiag]
    _ = ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
          exact iterate_returnMap1CaseII_half_plus_two_prefix (m := m) hm

theorem iterate_returnMap1CaseII_m_sub_one_middle [Fact (9 < m)] (hm : m % 6 = 4) :
    let xFin : Fin m := ⟨m - 1, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    ((returnMap1CaseII (m := m)^[m]) (linePoint1 (m := m) xFin)) =
      ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
  let xFin : Fin m := ⟨m - 1, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  let n : ℕ := (m / 2 - 2) + (1 + ((m / 2 - 2) + 3))
  have hdecomp : m = (m / 2 - 2) + (1 + ((m / 2 - 2) + 3)) := by
    have hm9 : 9 < m := Fact.out
    omega
  have hexp :
      ((returnMap1CaseII (m := m)^[m]) (linePoint1 (m := m) xFin)) =
        ((returnMap1CaseII (m := m)^[n]) (linePoint1 (m := m) xFin)) := by
    dsimp [n]
    exact congrArg (fun j : ℕ => ((returnMap1CaseII (m := m)^[j]) (linePoint1 (m := m) xFin))) hdecomp
  have haux :
      ((returnMap1CaseII (m := m)^[n]) (linePoint1 (m := m) xFin)) =
        ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
    simpa [xFin, n] using iterate_returnMap1CaseII_m_sub_one_middle_aux (m := m) hm
  exact hexp.trans haux

theorem firstReturn_line_m_sub_one_caseII [Fact (9 < m)] (hm : m % 6 = 4) :
    let xFin : Fin m := ⟨m - 1, by
      have hm9 : 9 < m := Fact.out
      omega⟩
    ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin)) =
      linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
  let xFin : Fin m := ⟨m - 1, by
    have hm9 : 9 < m := Fact.out
    omega⟩
  have hmid :
      ((returnMap1CaseII (m := m)^[m]) (linePoint1 (m := m) xFin)) =
        ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m))) := by
    simpa [xFin] using iterate_returnMap1CaseII_m_sub_one_middle (m := m) hm
  have haux :
      ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin)) =
        ((7 : ZMod m), (0 : ZMod m)) := by
    calc
      ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin))
          = ((returnMap1CaseII (m := m)^[6])
              (((returnMap1CaseII (m := m)^[m]) (linePoint1 (m := m) xFin)))) := by
                rw [show m + 6 = 6 + m by omega, Function.iterate_add_apply]
      _ = ((returnMap1CaseII (m := m)^[6]) ((0 : ZMod m), (((m - 3 : ℕ) : ZMod m)))) := by
            rw [hmid]
      _ = ((7 : ZMod m), (0 : ZMod m)) := by
            exact iterate_returnMap1CaseII_zero_m_sub_three_tail (m := m)
  have hT : (TorusD3Even.T1CaseII (m := m) hm xFin).1 = 7 := by
    have hsrc : xFin.1 = m - 1 := by
      simp [xFin]
    simpa [xFin] using
      TorusD3Even.T1CaseII_eq_seven_of_val_eq_m_sub_one (m := m) hm hsrc
  calc
    ((returnMap1CaseII (m := m)^[m + 6]) (linePoint1 (m := m) xFin))
        = ((7 : ZMod m), (0 : ZMod m)) := haux
    _ = linePoint1 (m := m) (TorusD3Even.T1CaseII (m := m) hm xFin) := by
          ext <;> simp [linePoint1, hT]

def rho1CaseII [Fact (9 < m)] (x : Fin m) : ℕ :=
  if hx0 : x.1 = 0 then
    1
  else if hx1 : x.1 = 1 then
    1
  else if hx2 : x.1 = 2 then
    m + 3
  else if hxm5 : x.1 = m - 5 then
    m + 4
  else if hxm3 : x.1 = m - 3 then
    m + 6
  else if hxm2 : x.1 = m - 2 then
    1
  else if hxm1 : x.1 = m - 1 then
    m + 6
  else if hodd : x.1 % 2 = 1 then
    m + 4
  else
    m + 2

end TorusD3Odometer
