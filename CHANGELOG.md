# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This repository follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the umbrella level; each extension under `extensions/` keeps its own
versioned CHANGELOG.

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

## [v0.2.0] — Initial field sets for both extensions

### Added

- `extensions/fao/` — initial field set (`fao:workspace`,
  `fao:product_id`, `fao:item_code`, `fao:layer_id`,
  `fao:product_type`, `fao:geometry_type`, `fao:feature_count`),
  raster + vector worked examples, README field table. See the
  per-extension [CHANGELOG](extensions/fao/CHANGELOG.md).
- `extensions/iso-to-stac/` — 11 new `iso:*` fields, normative
  mapping table at
  [`mapping/iso19115-2-to-stac.md`](extensions/iso-to-stac/mapping/iso19115-2-to-stac.md),
  worked examples demonstrating the full FAO profile (12+ extensions
  declared on the same Collection / Item). See the per-extension
  [CHANGELOG](extensions/iso-to-stac/CHANGELOG.md).
- Reference-implementation package version bumped to `0.2.0`. Models
  and the ISO XML mapper still land in a later release.

### Changed

- Schema URLs bumped from `v1.0.0` (skeleton placeholder) to `v0.2.0`
  across both extensions and all references (examples, package.json,
  reference-implementation, tests).
- Top-level README extension table updated to remove the "skeleton"
  status; both extensions are now at "Proposal — initial field set".

## [v0.1.0] — Skeleton

### Added

- Umbrella repository scaffolding derived from the official
  [STAC extension template](https://github.com/stac-extensions/template).
- Two extension skeletons:
  - `extensions/fao/` — placeholder fields, JSON Schema, examples,
    CHANGELOG.
  - `extensions/iso-to-stac/` — placeholder fields, JSON Schema,
    examples, CHANGELOG, mapping placeholder directory.
- Python reference-implementation skeleton with empty
  `fao_stac_extensions.fao` and `fao_stac_extensions.iso_to_stac`
  packages and a passing import test per package.
- Apache-2.0 license, .gitignore, top-level README.

### Roadmap

| Phase | Target |
| --- | --- |
| Proposal (skeleton) | v0.1.0 (DONE) |
| Authoring (fields + examples + mapping) | v0.2.0 (DONE) |
| Pilot | TBD — after the FAO Agro-Informatics Platform emits the v0.2.0 URLs |
| Candidate | After PR to the `stac-extensions/` org index |
| Stable | After at least one external implementer adopts |

[Unreleased]: <https://github.com/un-fao/fao-stac-extensions/compare/v0.2.0...HEAD>
[v0.2.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.2.0>
[v0.1.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.1.0>
