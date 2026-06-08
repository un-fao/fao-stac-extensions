# Changelog

All notable changes to this extension are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this extension adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.3.0] — Field typing (geometry_type enum) + Collection-branch fix

This release tightens the schema so the field typing it documents is
actually enforced (issue #3), alongside the example/README refinements
staged after v0.2.0.

### Added

- `fao:geometry_type` is now a closed enum of the GeoJSON (RFC 7946)
  geometry types — `Point`, `MultiPoint`, `LineString`,
  `MultiLineString`, `Polygon`, `MultiPolygon`, `GeometryCollection`
  (#3 D2). Previously any string; values outside the set now fail
  validation.
- Three additional worked examples covering the rest of the
  `fao:product_type` enum: `examples/collection-mosaic.json`
  (`L3-QUAL-NDVI-LT.LCE`), `examples/collection-mosaicset.json`
  (`L3-RSM-D.KOG`), and `examples/item-mosaicset.json` (a dekadal Item
  from the same MOSAICSET). The MOSAIC and MOSAICSET examples include
  top-level `proj:epsg` carrying the tile's native UTM zone, per the
  FAO STAC change report.
- `examples/README.md` indexing every worked example.
- `fao:product_type` enum tightened to `mapset` / `mosaic` /
  `mosaicset` / `map`. `dataset` removed (catch-all not used by the
  FAO platform); `map` added as the typical Item-level value (an Item
  inside a `mapset` Collection is itself a single map). The schema
  already allowed `fao:product_type` at Item level; this closes the
  enum.

### Changed

- **BREAKING — Collection branch restructured to `allOf` so top-level
  typing and the raster/vector mutex are enforced.** The v0.2.0
  Collection schema combined the top-level / `assets` / `item_assets` /
  `summaries` locations under `anyOf`; a Collection carrying `assets`
  or `summaries` satisfied another branch and its top-level `fao:*`
  fields were never validated. The locations are now combined under
  `allOf`, so `fao:geometry_type`'s enum (and the existing
  `modality_mutex`) apply to every Collection.
- Schema `$id` and `stac_extensions[]` URL bumped to
  `https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.3.0/extensions/fao/json-schema/schema.json`
  (was the `v0.2.0` path under the same host). The `fao` extension is
  org-specific and will not be submitted to the `stac-extensions/`
  org, so this raw-tree URL is the **permanent** identifier, served
  directly from the git tree at the release tag — no separate publish
  workflow. The `v0.2.0` URL remains resolvable at its tag.
- All Item examples now carry `fao:product_type: "map"` to demonstrate
  the convention.
- Worked examples now emit the legacy `gismgr_item_id` (Item) and
  `gismgr_layer_id` (Collection) alongside the new `fao:*` fields, to
  demonstrate the deprecation pattern. The schema does not define
  these legacy fields; they pass validation through the existing
  `^(?!fao:)` pattern as untyped extras. README gains a "Migration &
  deprecated legacy fields" section documenting which legacy fields
  each new `fao:*` field replaces.
- Removed redundant `fao:workspace` / `fao:product_id` / `proj:epsg`
  entries from `summaries` blocks in Collection examples — these
  values are invariant within a Collection, so top-level placement is
  sufficient and matches the live FAO wire (which keeps `summaries`
  empty for invariant fields).

### Deprecated

### Removed

### Fixed

- Schema now enforces raster-vs-vector mutual exclusivity. The
  README documented the discipline since v0.2.0 but the schema
  permitted documents carrying both `fao:product_type` (raster) and
  `fao:geometry_type` / `fao:feature_count` (vector). A new
  `#/definitions/modality_mutex` is referenced from `Item.properties`
  and from the Collection branch's outer `allOf` so the mutex is
  enforced regardless of which other anyOf branch matches. The
  Python test suite gains
  `test_fao_raster_vector_mutex_enforced` and
  `test_fao_vector_only_document_validates` to lock the behaviour in.

## [v0.2.0] — Initial field set

### Added

- Typed identifier fragments replacing the legacy opaque platform id:
  `fao:workspace`, `fao:product_id`, `fao:item_code`, `fao:layer_id`.
- Raster product-type classifier `fao:product_type` with enum
  `mapset` / `mosaic` / `mosaicset` / `dataset`.
- Vector-only fields `fao:geometry_type` and `fao:feature_count`.
- Custom asset role `dimension-labels` documented in the README (no
  schema entry — it appears in `assets[<key>].roles[]`).
- Worked Item + Collection examples drawn from a real FAO raster
  product (`ASI-D`), declaring the full profile extension stack
  (`scientific`, `themes`, `language`, `processing`, `timestamps`,
  `datacube`, `raster`, `classification`, `render`, `alternate-assets`,
  `projection`, `file`, `iso-to-stac`, `fao`).

### Notes

- The schema does not enforce raster-vs-vector exclusivity; producers
  follow the `RASTER ONLY` / `VECTOR ONLY` discipline documented in
  the README. A future minor release may tighten this with a
  `dependentSchemas` clause once the field set is stable.
- The schema URL is `https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/fao/json-schema/schema.json`
  (served directly from the git tree at the release tag — the `fao`
  extension is permanently org-specific).

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
