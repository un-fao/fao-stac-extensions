# Critical Review — v0.2.0 → next

A self-review of the v0.2.0 release covering schema correctness, test
coverage, mapping quality against upstream standards, and repository
hygiene. Each finding either ships a fix in this branch or is recorded
as a deferred follow-up.

## Findings & resolutions

### 1. Schema bug — raster/vector mutex was not enforced

**Finding.** The `fao` extension documented a "RASTER ONLY" /
"VECTOR ONLY" discipline in the README but the schema permitted
documents carrying both `fao:product_type` (raster) and
`fao:geometry_type` / `fao:feature_count` (vector). A first attempt to
enforce the mutex via an `allOf` clause inside the `fields` definition
silently failed because the Collection branch's outer `anyOf` could be
satisfied by the `summaries`-required branch alone, bypassing
`fields` entirely.

**Resolution.** Lifted the mutex to a separate `#/definitions/modality_mutex`
definition and reference it from:

- the `Item.properties` schema (so co-existence on Item properties is
  caught), and
- the Collection branch's `allOf` (so co-existence at Collection
  top-level is caught regardless of which `anyOf` branch matches).

Added `test_fao_raster_vector_mutex_enforced` and
`test_fao_vector_only_document_validates` to lock the behaviour in.

### 2. Test coverage gap — examples could drift from schemas

**Finding.** The Python test suite was three import asserts. Example
drift was only caught by the Node-side `stac-node-validator` job in
CI; if that job were skipped or broken the drift would land silently.

**Resolution.** Added `tests/test_examples.py` that:

- meta-validates each schema against JSON Schema Draft-07,
- discovers every `.json` file under `extensions/<ext>/examples/` and
  validates it against the extension's schema (parametrised so each
  example produces a distinct test result),
- asserts the modality-mutex rule on a synthetic counter-example.

Added `jsonschema>=4` to the `[dev]` extra in `pyproject.toml`. CI
already runs both the npm and Python suites, so example drift is now
caught twice independently.

### 3. Mapping quality — `processing:lineage` is the canonical home

**Finding.** The `iso-to-stac` mapping doc routed ISO
`LI_Lineage.statement` to the new `iso:lineage_statement` field. The
[STAC Processing extension](https://github.com/stac-extensions/processing)
explicitly cites
[NASA's ISO lineage information](https://wiki.earthdata.nasa.gov/display/NASAISO/Lineage+Information)
as the source of `processing:lineage` — making it the de-facto STAC
home for ISO lineage statements.

**Resolution.** The mapping doc now lists `processing:lineage` as the
preferred target (with `iso:lineage_statement` retained as a fallback
for FAO producers needing a strictly Collection-top-level field with
an `iso:` prefix). The `iso:lineage_statement` schema description was
updated to flag the field as a candidate for deprecation in a future
release, pointing producers at `processing:lineage` instead.

### 4. Mapping quality — DOI and edition were missing

**Finding.** The mapping doc covered `sci:citation` for the citation
free-text but did not address the structured pieces of
`CI_Citation`: the identifier (which is often a DOI) or the edition.

**Resolution.** Added two rows to the Identification & Citation
section:

- ISO `CI_Citation.identifier` (when DOI) → `sci:doi` (Scientific
  Citation extension).
- ISO `CI_Citation.edition` → `version` (Versioning Indicators
  extension).

### 5. Mapping quality — language vs. languages

**Finding.** ISO `MD_DataIdentification.language` is an *array*; the
mapping doc routed it to a single `language` field, losing the
multiplicity. STAC's
[Language extension](https://github.com/stac-extensions/language)
splits this into `language` (the primary) and `languages[]` (others),
and OGC API - Records introduces a separate `resourceLanguages` field
for the same purpose (not adopted by STAC).

**Resolution.** Mapping doc now distinguishes the two cases and
includes a callout explaining the shape mismatch and the OGC API -
Records alternative.

### 6. Mapping quality — `iso-19115` asset role is a STAC core convention

**Finding.** The mapping doc's CKAN-metadata-link section described
linking the ISO XML via `links[rel=describedby] type=application/xml`
but did not mention that
[STAC core best practices](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md)
define `iso-19115` as a standard *asset role* for the same purpose.
Producers preferring the asset form (e.g. for File-Info checksums)
were not pointed at the standard.

**Resolution.** Added a callout to section 6.4 documenting the asset
alternative with `roles: ["metadata", "iso-19115"]`.

### 7. Mapping quality — contacts roles vocabulary is lossless

**Finding.** The role mapping table at section 9.1 mapped every
`CI_RoleCode` value to one of STAC core's four
`providers[].roles[]` values, which is necessarily lossy (multiple
ISO codes collapse into the same STAC role). The
[STAC Contacts extension](https://github.com/stac-extensions/contacts)
schema permits free-form `roles[]` strings, which means producers
using `contacts[]` instead of `providers[]` can carry the ISO code
verbatim for a lossless round-trip.

**Resolution.** Section 9.1 now shows two columns — the lossy
`providers[]` mapping and the lossless `contacts[]` mapping — with a
prose explanation. Producers using the Contacts extension SHOULD
preserve the ISO code verbatim.

### 8. Repository hygiene — community files

**Finding.** The repo lacked the standard community files that
`stac-extensions` org acceptance reviewers (and most contributors)
expect: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue
templates, PR template.

**Resolution.** Added:

- `CONTRIBUTING.md` documenting branch / PR workflow and both test
  suites.
- `CODE_OF_CONDUCT.md` adopting the STAC spec Code of Conduct.
- `SECURITY.md` describing the realistic security surface and the
  `copyright@fao.org` reporting channel.
- `.github/ISSUE_TEMPLATE/{bug_report,feature_request}.md`.
- `.github/pull_request_template.md` with a checklist matching the
  invariants this repo cares about (no AI references, no prod URLs,
  schemas tests passing, etc.).

### 9. Repository hygiene — README badges

**Finding.** The umbrella README had no visible CI status or licence
indicator.

**Resolution.** Added two badges (Actions CI status, Apache-2.0
licence) at the top of the README.

## Findings deferred (not in this PR)

- **JSON Schema `$id` URLs point at `stac-extensions.github.io/...`**
  which only resolves after the extensions are accepted into the
  `stac-extensions/` GitHub organisation. The proper interim URL is
  the un-fao GitHub Pages deployment produced by `publish.yaml`. This
  was previously raised by the project lead and explicitly deferred;
  flagging it here for visibility.
- **`.editorconfig`** — single-contributor repo, no immediate need.
- **`py.typed`** — the reference-implementation package is essentially
  empty; no public API to type-check yet.
- **Bumping `peaceiris/actions-gh-pages` from v3.9.3** — not security-
  critical; will be picked up the next time the publish workflow needs
  changes.

## Verification

Before opening the PR:

- `npm test` (Node CI mirror): passes.
- `cd reference-implementation && pytest`: 14/14 tests pass — the
  new schema-validation tests catch every example, and the
  modality-mutex test catches the synthetic counter-example.
- `grep -i 'gismgr|claude|anthropic|gemini'` across all committable
  files: clean.
