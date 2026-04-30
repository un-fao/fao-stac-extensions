# ISO 19115-2 ↔ STAC Mapping Extension Specification

- **Title:** ISO 19115-2 to STAC Mapping
- **Identifier:** <https://stac-extensions.github.io/iso-to-stac/v1.0.0/schema.json>
- **Field Name Prefix:** iso
- **Scope:** Item, Collection
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: @un-fao

This document describes the ISO 19115-2 ↔ STAC Mapping Extension to the
[SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec)
(STAC) specification.

The extension has two purposes:

1. Define the canonical mapping between [ISO 19115-2](https://www.iso.org/standard/67039.html)
   metadata elements and STAC fields, preferring existing community
   extensions wherever a one-to-one (or one-to-many) mapping exists.
2. Add a small set of `iso:*` fields ONLY where an ISO 19115-2 element
   has no acceptable home in STAC core or in an existing extension.

A reference Python implementation that consumes ISO 19115-2 XML and
emits a STAC-shaped dictionary ships alongside the spec under
[`reference-implementation/`](../../reference-implementation/) at the
umbrella-repo root.

- Examples:
  - [Item example](examples/item.json): Shows the basic usage of the extension in a STAC Item
  - [Collection example](examples/collection.json): Shows the basic usage of the extension in a STAC Collection
- [JSON Schema](json-schema/schema.json)
- [Changelog](./CHANGELOG.md)

## Fields

The fields in the table below can be used in these parts of STAC documents:

- [ ] Catalogs
- [x] Collections
- [x] Item Properties (incl. Summaries in Collections)
- [ ] Assets
- [ ] Links

| Field Name      | Type   | Description                                            |
| --------------- | ------ | ------------------------------------------------------ |
| iso:placeholder | string | Placeholder field. The real field set lands in v0.2.0. |

The field table is a placeholder for the v0.1.0 skeleton. The full
mapping table and the `iso:*` field set will be added in v0.2.0.

## Mapping Spec

The normative ISO 19115-2 ↔ STAC mapping table will live at
[`mapping/iso19115-2-to-stac.md`](mapping/iso19115-2-to-stac.md) in
v0.2.0. Until then, the directory is a placeholder.

## Contributing

All contributions are subject to the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md).
For contributions, please follow the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md).
Instructions for running tests are at the umbrella-repo root README.
