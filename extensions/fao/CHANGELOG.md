# Changelog

All notable changes to this extension are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this extension adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
- The schema URL is `https://stac-extensions.github.io/fao/v0.2.0/schema.json`.

## [v0.1.0] — Skeleton

### Added

- Repository skeleton derived from the official
  [STAC extension template](https://github.com/stac-extensions/template).
- Placeholder JSON Schema, README field table, and example Item /
  Collection.

[Unreleased]: <https://github.com/un-fao/fao-stac-extensions/compare/v0.2.0...HEAD>
[v0.2.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.2.0>
[v0.1.0]: <https://github.com/un-fao/fao-stac-extensions/releases/tag/v0.1.0>
