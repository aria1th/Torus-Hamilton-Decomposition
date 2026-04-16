# D5 Unified Proof Archive Design

Date: 2026-04-03

## 1. Goal

Build one new `d=5` proof-support tarball that a fresh researcher can unpack
and use without chasing older tarballs by hand.

The bundle should do two things at once:

1. preserve the **current canonical RoundY reading** of the D5 proof program;
2. retain the **historical evidence and replay scripts** already packaged in
   the older `tmp/tarfiles/*.tar` bundles.

So this is not a raw tar-of-tars.
It is a curated extracted archive with provenance.

## 2. Design constraints

The archive should satisfy the following rules.

- no nested tarballs as primary content
- current canonical reading comes first
- historical material stays available but visibly secondary
- provenance of every imported packet remains explicit
- file collisions are avoided by source-scoped directories
- small duplicated summaries are acceptable when they preserve bundle context
- large redundant tar copies are excluded

## 3. Current source inventory

The source inputs are:

### A. Canonical current repo material

- `RoundY/README.md`
- `RoundY/current-frontier-and-approach.md`
- `RoundY/instruction_for_codex.md`
- the current `284/285/286` packet
- the current `290–305` theorem/status packet
- the accepted background references explicitly named by the current
  instructions
- `RouteY-Existence/` as the curated parallel existence layer

### B. Current April extracted bundles

- `tmp/unpacked_tarfiles/d5_current_proof_bundle_curated_2026-04-03/`
- `tmp/unpacked_tarfiles/d5_15r9_full_proof_archive_2026-04-01/`

These are the closest extracted packets to the present `15r+9` and current
proof-support state.

### C. March extracted support bundles

- `tmp/unpacked_tarfiles/d5_consolidated_standalone_package_2026-03-28_master_c_refresh/`
- `tmp/unpacked_tarfiles/d5_consolidated_support_archive_2026-03-28_v3/`
- `tmp/unpacked_tarfiles/roundy_d5_endpoint_return_model_bundle_20260321_update_197/`
- `tmp/unpacked_tarfiles/d5_requested_four_files_2026-03-30/`

These are historical support layers and should be presented that way.

## 4. Inclusion policy

### 4.1 Must include

- current RoundY frontier docs and manuscript-order docs
- current RoundY residual compute/spec docs directly referenced by the current
  frontier
- current `RouteY-Existence` curated tree
- all extracted April proof notes and replay/check scripts
- the March endpoint / return-model bundle because it carries low-level replay
  code and artifact summaries
- the March standalone/support extracts because they preserve earlier evidence
  packets and cross-bundle reading guides

### 4.2 Include but label as secondary

- handoff-style summaries that are superseded by fuller archives
- Korean guide files inside older bundles
- exploratory or superseded notes that already sit inside a historical bundle
- the March 21 endpoint/model extraction, but only as archive provenance

### 4.3 Exclude

- the raw `.tar` files themselves from the new tarball
- temporary extraction scratch outside the curated staging tree
- unrelated non-D5 repo material
- duplicated files copied only for path convenience when a source-scoped copy
  is already present

## 5. Archive layout

The new staging tree should look like this.

```text
d5_unified_proof_archive_2026-04-03/
  00_guides/
    START_HERE.md
    MANIFEST.md
    SOURCE_CROSSWALK.md
    DESIGN.md
  10_canonical_roundy/
    RoundY/...
  20_parallel_routey_existence/
    RouteY-Existence/...
    supplements/
      d5_requested_four_files_2026-03-30/...
  30_current_support_packets/
    d5_current_proof_bundle_2026-04-03/...
    d5_15r9_full_proof_archive_2026-04-01/...
  40_historical_bundle_extracts/
    final_d5_consolidated_package_2026-03-27/...
    d5_consolidated_support_archive_2026-03-28_v3/...
  90_archive_provenance/
    roundy_d5_endpoint_return_model_bundle_20260321_update_197/...
```

This keeps the canonical read first while still preserving every imported
bundle as an inspectable extracted subtree.

## 6. Why this layout

### A. Current proof state must not be buried

The user asked for a bundle about the D5 proof, not merely a historical dump.
So `00_guides/`, `10_canonical_roundy/`, and `20_parallel_routey_existence/`
must come before the imported tar extracts.

### B. Provenance must stay recoverable

Flattening all imported files into one directory would destroy bundle context
and create many collisions (`README.md`, `MANIFEST.txt`, `summary.log`,
`analysis_summary.json`, and several repeated theorem/check filenames).
So imported content must remain source-scoped.

### C. Historical completeness still matters

The March and April tarballs contain real evidence, scripts, and guide layers
that are not all promoted into the repo tree.
So the new unified tar should preserve them as extracted subtrees rather than
silently dropping them.

## 7. Bundle guide files to generate

The new unified tar should include four fresh top-level guide files.

### `START_HERE.md`

Purpose:

- give the shortest reading order for a fresh researcher
- separate current canonical docs from historical evidence packets

### `MANIFEST.md`

Purpose:

- list the staged top-level directories
- record file counts by source block

### `SOURCE_CROSSWALK.md`

Purpose:

- map each imported older tarball to its role
- state whether it is canonical, current support, or historical support
- record the main reason it was retained
- record which source bundles were intentionally omitted or absorbed

### `DESIGN.md`

Purpose:

- carry this design note into the bundle itself

## 8. Recommended reading order inside the new archive

1. `00_guides/START_HERE.md`
2. `10_canonical_roundy/RoundY/README.md`
3. `10_canonical_roundy/RoundY/current-frontier-and-approach.md`
4. `10_canonical_roundy/RoundY/instruction_for_codex.md`
5. `20_parallel_routey_existence/RouteY-Existence/README.md`
6. only then the extracted April and March packets as needed

## 9. Assembly plan

1. create a clean staging directory under `tmp/`
2. copy current canonical repo material into `10_canonical_roundy/`
3. copy the curated `RouteY-Existence/` tree into
   `20_parallel_routey_existence/`
4. copy the March 29/30 four-file supplement into
   `20_parallel_routey_existence/supplements/`
5. copy the current April support bundles into `30_current_support_packets/`,
   omitting the standalone April 1 handoff because the full archive absorbs it
6. copy the March historical bundles into `40_historical_bundle_extracts/`
7. copy the March 21 endpoint/model bundle into `90_archive_provenance/`
8. generate top-level guide markdown files
9. generate a file manifest for the staged tree
10. create the final `.tar` in `tmp/tarfiles/`

## 10. Validation plan

At minimum validate:

- every declared source subtree exists
- the top-level guide files exist
- the tar can be listed with `tar -tf`
- the manifest count is consistent with the staged file count

Optional but useful:

- run `python -m py_compile` on any new assembly helper script
- compare the final tar top-level tree with the design layout

## 11. Naming

Recommended output names:

- staging directory:
  `tmp/d5_unified_proof_archive_2026-04-03/`
- final tar:
  `tmp/tarfiles/d5_unified_proof_archive_2026-04-03.tar`

## 12. Bottom line

The right unified D5 archive is:

- current canonical RoundY first,
- curated RouteY-Existence second,
- extracted April current-support packets next,
- and March historical/support bundles after that,

all inside one source-scoped extracted tar with fresh top-level guides and no
nested raw tarballs.
