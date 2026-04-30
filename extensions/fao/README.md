# FAO Extension Specification

- **Title:** FAO
- **Identifier:** <https://stac-extensions.github.io/fao/v0.2.0/schema.json>
- **Field Name Prefix:** fao
- **Scope:** Item, Collection, Asset
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: @un-fao

This extension carries FAO platform-specific fields applicable to both
raster and vector products published by the FAO Agro-Informatics
Platform.

The field set is intentionally **service-agnostic**: it does not expose
internal service identifiers (e.g. the name of the raster-serving
backend), storage-bucket paths, or other implementation details. The
opaque platform identifier that earlier wire formats carried as a single
string is fragmented here into typed fields (`fao:workspace`,
`fao:product_id`, `fao:item_code`).

- Examples:
  - [Item example](examples/item.json): Raster Item drawn from an `ASI-D`-style payload, declaring `fao:*` alongside the standard extensions used by the FAO profile.
  - [Collection example](examples/collection.json): Companion Collection.
- [JSON Schema](json-schema/schema.json)
- [Changelog](./CHANGELOG.md)

## Fields

The fields below can appear in:

- [ ] Catalogs
- [x] Collections
- [x] Item Properties (incl. Summaries in Collections)
- [x] Assets (asset role only — no typed asset fields)
- [ ] Links

| Field Name | Type | Applies to | Description |
| --- | --- | --- | --- |
| fao:workspace | string | shared | FAO workspace (e.g. `"ASIS"`, `"WAPOR-3"`). |
| fao:product_id | string | shared | FAO product identifier within the workspace. Typically equals the Collection id. |
| fao:item_code | string | Item only | Per-item leaf code. Typically equals the Item id. |
| fao:layer_id | string | Collection only | Service-agnostic FAO layer reference for provenance tracking. |
| fao:product_type | string (enum) | RASTER ONLY | `mapset` \| `mosaic` \| `mosaicset` \| `dataset`. |
| fao:geometry_type | string | VECTOR ONLY | OGR/GeoJSON geometry type (`Point`, `Polygon`, `MultiPolygon`, …). |
| fao:feature_count | integer ≥ 0 | VECTOR ONLY | Number of features in the layer (Collection) or item (Item). |

### Raster vs vector

The schema does not enforce raster-vs-vector exclusivity — a single
field set covers both modalities. Producers SHOULD honour the
`RASTER ONLY` / `VECTOR ONLY` discipline above:

- A raster Collection emits `fao:workspace`, `fao:product_id`,
  `fao:product_type`, and (per Item) `fao:item_code`. It does not emit
  `fao:geometry_type` or `fao:feature_count`.
- A vector Collection emits `fao:workspace`, `fao:product_id`,
  `fao:geometry_type`, `fao:feature_count`, and (per Item)
  `fao:item_code` and `fao:feature_count`. It does not emit
  `fao:product_type`.

### Asset roles

The FAO profile uses one custom asset role:

| Role | Asset shape | Description |
| --- | --- | --- |
| `dimension-labels` | `application/json` link to a per-collection labels file | Carries human-readable labels for the `cube:dimensions` categorical members declared by the [datacube extension](https://github.com/stac-extensions/datacube). Applies to Collections that declare any non-spatial categorical dimension. |

This is registered as a STAC asset role string (it appears in
`assets[<key>].roles[]`); it is not a typed field on any object, so the
JSON Schema does not validate it.

## Relation types

This extension defines no new `rel` types. The link relations used by
the FAO profile are STAC core (`describedby`, `license`, `via`, `style`,
`legend`, `sld`, `self`, `parent`, `root`, `items`, `item`).

## Contributing

All contributions are subject to the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md).
For contributions, please follow the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md).
Instructions for running tests are at the umbrella-repo root README.
