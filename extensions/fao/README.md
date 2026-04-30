# FAO Extension Specification

- **Title:** FAO
- **Identifier:** <https://stac-extensions.github.io/fao/v1.0.0/schema.json>
- **Field Name Prefix:** fao
- **Scope:** Item, Collection
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: @un-fao

This document describes the FAO Extension to the
[SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec)
(STAC) specification. It carries FAO platform-specific fields that apply
to both raster and vector products published by the FAO Agro-Informatics
Platform.

The field set is intentionally platform-agnostic: it does not expose
internal service identifiers, storage-bucket paths, or other
implementation details.

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
- [x] Assets (for both Collections and Items, incl. Item Asset Definitions in Collections)
- [ ] Links

| Field Name        | Type   | Description                                            |
| ----------------- | ------ | ------------------------------------------------------ |
| fao:placeholder   | string | Placeholder field. The real field set lands in v0.2.0. |

The field table is a placeholder for the v0.1.0 skeleton. The full set of
`fao:*` fields will be added in v0.2.0 once the field allocation has been
finalised.

## Contributing

All contributions are subject to the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md).
For contributions, please follow the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md).
Instructions for running tests are copied here for convenience.

### Running tests

The same checks that run as checks on PR's are part of the repository and
can be run locally to verify that changes are valid. To run tests locally,
you'll need `npm`, which is a standard part of any
[node.js installation](https://nodejs.org/en/download/).

First you'll need to install everything with npm once. Just navigate to
the root of this extension and on your command line run:

```bash
npm install
```

Then to check markdown formatting and test the examples against the JSON
schema, you can run:

```bash
npm test
```

This will spit out the same texts that you see online, and you can then go
and fix your markdown or examples.

If the tests reveal formatting problems with the examples, you can fix
them with:

```bash
npm run format-examples
```
