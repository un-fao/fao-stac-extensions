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
| Proposal (skeleton) | now |
| Authoring (fields + examples) | next iteration, after the field allocation tables are agreed |
| Pilot | TBD — after the FAO Agro-Informatics Platform emits the extension URLs |
| Candidate | After PR to the `stac-extensions/` org index |
| Stable | After at least one external implementer adopts |

[Unreleased]: <https://github.com/un-fao/fao-stac-extensions/compare/v0.1.0...HEAD>
[v0.1.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.1.0>
