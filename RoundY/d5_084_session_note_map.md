# D5 084 Session Note Map

This note organizes older RoundY session/work files that are still present in
the tree but are **not** part of the canonical theorem chain or the canonical
compute-evidence chain.

Its purpose is:

1. to explain what these session notes are;
2. to separate historical work logs from actual theorem/evidence references;
3. to give a clear status to specific files such as `codex_work_s22.md`.

## 1. What session notes are

Files such as:

- `codex_work_s*.md`
- `note_s*.md`
- `doc_s20.md`, `docs_s21.md`
- `feedback_s63.md`

are mostly:

- session logs,
- task specs,
- temporary work summaries,
- or short progress memos.

They are useful for provenance and archaeology, but they are **not** canonical
theorem notes unless their content was later promoted into `RoundY/theorem/`.

## 2. Rule for using them

When reading RoundY now:

- use `RoundY/theorem/` for theorem content,
- use `RoundY/checks/` for stable compute-evidence files,
- use session notes only if a stable theorem/check note explicitly points back
  to them for provenance.

So the default policy is:

> do not cite a `codex_work_*` note as a theorem reference unless its content
> has no stable promoted replacement.

## 3. `codex_work_s22.md`

### What it is

`codex_work_s22.md` is an early strict-palette context-search task spec:

- it asks whether a `5`-context active layer-`2/3` grammar depending only on
  `phase_align, b1, b2` can produce nontrivial section dynamics;
- it belongs to the earlier search / palette / Latin-rigidity stage;
- it predates the later return-map / bridge / globalization compression.

### What it is not

It is **not**:

- a theorem note,
- a stable compute-evidence object,
- or part of the current `076–083` bridge/globalization theorem chain.

### Current status

Treat `codex_work_s22.md` as:

- historical task provenance for an early search branch,
- not part of the active D5 theorem package,
- not something that needs promotion into `RoundY/theorem/`.

If one wants the modern canonical reading for the current branch instead, use:

- `theorem/d5_082_frontier_and_theorem_map.md`
- `theorem/d5_083_gluing_flow_and_final_theorem.md`

## 4. `note_s20.md` and the `note_s*.md` series

### What they are

Files such as:

- `note_s20.md`
- `note_s21.md`
- `note_s22.md`
- and the rest of the `note_s*.md` series

are short historical session notes from earlier stages of the D5 branch.

They typically record:

- what was being tried that session,
- what failed,
- which search/spec branch was being opened,
- or what intermediate direction looked promising at that time.

### What they are not

They are generally **not**:

- stable theorem notes,
- stable compute-evidence files,
- or part of the canonical `076–083` theorem chain.

### Current status

Treat the `note_s*.md` series exactly like the `codex_work_s*.md` series:

- useful for historical provenance,
- useful when reconstructing earlier search branches,
- not to be cited as theorem inputs unless a stable note explicitly depends on
  them.

## 5. `works_063_a/b/c`

These are different from `codex_work_s22.md`.

They are theorem-side route-organization notes, not session logs.
They are already mapped in:

- `theorem/d5_084_theorem_name_map.md`

and already largely promoted into:

- `theorem/d5_063_route_organization.md`

So no extra promotion is needed there beyond the existing theorem-name map.

## 6. Practical categories

The useful split is now:

### Canonical theorem notes

- files in `RoundY/theorem/` that are part of the active chain
- especially the promoted `076–083` notes

### Canonical compute evidence

- files in `RoundY/checks/`
- especially the promoted `077` and `081` support files

### Historical theorem-route notes

- older theorem notes now mapped by `theorem/d5_084_theorem_name_map.md`
- for example `works_063_a/b/c`, `d5_070.md`, `d5_072_r2.md`, `d5_073_r1.md`

### Historical session/work notes

- `codex_work_s*.md`
- `note_s*.md`
- other session logs in RoundY root

These are useful only as provenance unless promoted later.

## 7. Bottom line

- `works_063_a/b/c` are already theorem-mapped and effectively handled.
- `codex_work_s22.md` is a historical search-task note, not a missing theorem.
- `note_s20.md` and the other `note_s*.md` files are also historical session
  notes, not missing theorem inputs.
- the small subset of session notes that still contain useful extractable
  mathematical content is recorded in:
  `theorem/d5_084_session_extractions.md`
- the current active branch should be read through the promoted `076–083`
  theorem notes, not through old session logs.
