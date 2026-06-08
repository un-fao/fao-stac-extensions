# Changelog

All notable changes to this extension are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this extension adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.3.0] — Codelist & date-time typing; deprecations

This release tightens the schema so the field typing it documents is
actually enforced (issue #3), alongside the mapping- and community-file
refinements staged after v0.2.0.

### Added

- **Codelist `$defs`** in `json-schema/schema.json`:
  `MD_RestrictionCode`, `MD_ProgressCode`,
  `MD_SpatialRepresentationTypeCode`, `MD_MaintenanceFrequencyCode`,
  `CI_PresentationFormCode`, `MD_CharacterSetCode` — the canonical ISO
  19115 codelist members, referenced from the matching `iso:*` fields.
  `iso:access_constraints` and `iso:use_constraints` share one
  `MD_RestrictionCode` enum by reference (closes #4).
- `tests/test_examples.py` now enforces `format` (RFC 3339 `date-time`,
  via `rfc3339-validator` added to the `[dev]` extra) and adds
  `test_iso_codelist_and_date_typing_enforced` — a synthetic
  counter-example proving the enum and date constraints are rejected at
  Collection top level even when the document also carries
  `assets`/`summaries`.
- `iso:supplemental_information` field (Optional in the FAO profile)
  for `MD_DataIdentification.supplementalInformation`. The source
  spreadsheet recommended appending it to STAC `description`, which
  loses the ISO/STAC round-trip; carrying it as a typed `iso:*` field
  preserves both reads. The Collection example demonstrates a
  realistic value (sentinel-value notes for ASI-D's pixel encoding).
- Mapping doc gains a `References` section linking to the ISO
  upstream standards (19115-1, 19115-2, 19139, the codelist registry),
  to relevant STAC extensions (Contacts, Scientific, Themes,
  Language, Processing, Timestamps, Datacube, Raster, EO) including
  the [Contacts extension](https://github.com/stac-extensions/contacts)
  as the recommended path for new producers, to OGC API - Records,
  pygeometa, GeoNetwork, and pystac.

#### Standards-review-driven mapping improvements

After reading the schemas of adjacent STAC extensions and STAC core's
[best practices](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md):

- **Lineage**: `processing:lineage` is now recommended over
  `iso:lineage_statement` for ISO `LI_Lineage.statement`. The
  Processing extension explicitly cites NASA's ISO lineage
  information as its source, so it is the de-facto STAC home for ISO
  lineage. `iso:lineage_statement` is retained as a fallback for FAO
  producers needing a strictly Collection-top-level field with an
  `iso:` prefix; the schema description flags it as a candidate for
  deprecation in a future release.
- **DOI**: new mapping row for ISO `CI_Citation.identifier` (when
  carrying a DOI) → `sci:doi` (Scientific Citation extension).
- **Edition**: new mapping row for ISO `CI_Citation.edition` →
  `version` (Versioning Indicators extension).
- **Languages**: explicit `language` vs `languages[]` distinction with
  a callout explaining the ISO multiplicity vs STAC's primary/other
  split, and a pointer to OGC API - Records `resourceLanguages`.
- **`iso-19115` asset role**: section 6.4 (CKAN metadata link) now
  documents the STAC core asset alternative
  (`assets[].roles = ["metadata", "iso-19115"]`) for producers that
  prefer the asset form over `describedby` links.
- **Contacts role mapping**: section 9.1 now distinguishes the lossy
  `providers[].roles[]` mapping (constrained to STAC core's four role
  values) from the lossless `contacts[].roles[]` mapping (the
  Contacts extension permits free-form role strings).

### Changed

- **BREAKING — date fields require RFC 3339 `date-time` (#3 D1).**
  `iso:data_creation_date`, `iso:data_revision_date` and
  `iso:data_publication_date` previously accepted any string; they now
  require a full RFC 3339 `date-time` (e.g. `2014-01-01T00:00:00Z`),
  aligning with STAC `datetime` and giving indexers a stable `date`
  mapping. *Migration:* pad partial dates
  (`2014` → `2014-01-01T00:00:00Z`); omit the field when the date is
  unknown — do not send the string `"null"`.
- **BREAKING — codelist fields are closed enums (#3 D2, closes #4).**
  `iso:status`, `iso:spatial_representation_type`,
  `iso:maintenance_and_update_frequency`, `iso:character_set_code`,
  `iso:presentation_form`, `iso:access_constraints` and
  `iso:use_constraints` now validate against their ISO 19115 codelist
  members instead of accepting free text, so typos fail validation.
  *Migration:* the canonical US-ASCII member is `usAscii`, not `ascii`.
- **BREAKING — Collection branch restructured to `allOf` so top-level
  typing is enforced.** The v0.2.0 Collection schema combined the
  top-level / `assets` / `item_assets` / `summaries` locations under
  `anyOf`; a Collection carrying `assets` or `summaries` satisfied
  another branch and its top-level `iso:*` fields were never validated,
  leaving the typing cosmetic. The locations are now combined under
  `allOf`, so the new date/enum constraints apply to every Collection.
- Schema `$id` and `stac_extensions[]` URL bumped to
  `https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.3.0/extensions/iso-to-stac/json-schema/schema.json`
  (was the `v0.2.0` path under the same host). This **interim** URL is
  served directly from the umbrella repository's git tree at the
  release tag while the extension is at the Proposal / Pilot phase;
  once accepted into the `stac-extensions/` org the `$id` moves to
  `https://stac-extensions.github.io/iso-to-stac/...` in a subsequent
  release. The `v0.2.0` URL remains resolvable at its tag for existing
  consumers.
- **Mapping doc reshaped.** `mapping/iso19115-2-to-stac.md` is now
  organised by ISO 19115-1 section (Identification & Citation; Date;
  Maintenance / Status / Purpose; Constraints & Rights; Spatial &
  Temporal Extent; Distribution & Resources; Quality & Lineage;
  Metadata Block; Contacts) with one self-contained table per section
  rather than a single monolithic 110-row table. Each row carries an
  explicit Profile tier (no more empty cells inherited from the row
  above) and a hyperlink to the contributing extension's repo. The
  Contacts section now shows both the current FAO mapping
  (`providers[]`) and the recommended STAC Contacts extension shape
  (`contacts[]`) side-by-side.
- Mapping doc: header rewritten to describe its purpose as a per-field
  ISO ↔ STAC crosswalk, no longer references the (uncommitted) source
  working document by filename.
- README rewritten to lead with the motivation (merging the FAO ISO
  metadata catalog with the FAO STAC catalog).

### Removed

- Mapping doc: dropped the "Spatial Representation Info from GISMGR"
  section and the `gismgr_layer_id` row. GISMGR is the FAO
  raster-serving service and is not part of any standard; the rows
  the spreadsheet placed under that header documented STAC fields
  (bands, `cube:dimensions`, `cube:variables`, `renders`) sourced
  from GISMGR — those are not ISO ↔ STAC mappings, so they don't
  belong in this crosswalk. The platform identifier `gismgr_layer_id`
  is replaced by the typed `fao:layer_id` field documented in the
  [`fao` extension](../fao/), with the dual-emit deprecation pattern
  shown in that extension's examples.

### Deprecated

- **`iso:lineage_statement` (#3 D5).** Now flagged `deprecated: true`
  with a `$comment` pointing to `processing:lineage` from the STAC
  Processing extension (which cites NASA's ISO lineage information as
  its source). Retained as a fallback for one release; scheduled for
  removal in a future version. New producers SHOULD use
  `processing:lineage`.

### Removed

### Fixed

- LINKS to RESOURCES section: the asset `created` / `published` /
  `updated` rows are now correctly attributed to the **Timestamps**
  extension (was previously misattributed to Alternate Assets).

## [v0.2.0] — Initial field set + mapping spec

### Added

- 11 new `iso:*` fields covering ISO 19115-1 concepts with no equivalent
  in any existing STAC extension:
  - `iso:lineage_statement` (**MANDATORY** in the FAO profile)
  - `iso:maintenance_and_update_frequency` (**Needed** in the FAO profile)
  - `iso:presentation_form`, `iso:character_set_code`,
    `iso:spatial_representation_type`, `iso:purpose`, `iso:status`,
    `iso:access_constraints`, `iso:use_constraints`,
    `iso:use_limitation`, `iso:other_constraints` (Optional in the FAO
    profile)
- Normative ISO 19115-1 ↔ STAC mapping table at
  [`mapping/iso19115-2-to-stac.md`](mapping/iso19115-2-to-stac.md), with
  per-row Profile column (MANDATORY / Needed / Optional / Not needed),
  and the `CI_RoleCode` → `providers[].roles[]` mapping section.
- Worked Item + Collection examples demonstrating the profile end-to-end
  with the full extension stack (`scientific`, `themes`, `language`,
  `processing`, `timestamps`, `datacube`, `raster`, `classification`,
  `render`, `alternate-assets`, `projection`, `file`, `fao`,
  `iso-to-stac`).

### Notes

- The schema does NOT enforce profile-level required-ness. The Profile
  tiers (MANDATORY / Needed / Optional) are documented in the README
  and in the mapping doc; a separate validator MUST enforce them.
- The schema URL is `https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/iso-to-stac/json-schema/schema.json`
  (interim — moves to `stac-extensions.github.io/iso-to-stac/...` on
  community acceptance).

## [v0.1.0] — Skeleton

### Added

- Repository skeleton derived from the official
  [STAC extension template](https://github.com/stac-extensions/template).
- Placeholder JSON Schema, README field table, and example Item /
  Collection.

[Unreleased]: <https://github.com/un-fao/fao-stac-extensions/compare/v0.3.0...HEAD>
[v0.3.0]: <https://github.com/un-fao/fao-stac-extensions/compare/v0.2.0...v0.3.0>
[v0.2.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.2.0>
[v0.1.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.1.0>
