# Changelog

All notable changes to this extension are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this extension adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `iso:supplemental_information` field (Optional in the FAO profile)
  for `MD_DataIdentification.supplementalInformation`. The source
  spreadsheet recommended appending it to STAC `description`, which
  loses the ISO/STAC round-trip; carrying it as a typed `iso:*` field
  preserves both reads. The Collection example demonstrates a
  realistic value (sentinel-value notes for ASI-D's pixel encoding).

### Changed

- Mapping spec at `mapping/iso19115-2-to-stac.md`: header rewritten to
  describe its purpose as a per-field ISO ↔ STAC crosswalk, no longer
  references the (uncommitted) source working document by filename.
- README rewritten to lead with the motivation (merging the FAO ISO
  metadata catalog with the FAO STAC catalog).

### Deprecated

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
- The schema URL is `https://stac-extensions.github.io/iso-to-stac/v0.2.0/schema.json`.

## [v0.1.0] — Skeleton

### Added

- Repository skeleton derived from the official
  [STAC extension template](https://github.com/stac-extensions/template).
- Placeholder JSON Schema, README field table, and example Item /
  Collection.

[Unreleased]: <https://github.com/un-fao/fao-stac-extensions/compare/v0.2.0...HEAD>
[v0.2.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.2.0>
[v0.1.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.1.0>
