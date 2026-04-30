# ISO 19115-2 ↔ STAC Mapping Extension Specification

- **Title:** ISO 19115-2 to STAC Mapping
- **Identifier:** <https://stac-extensions.github.io/iso-to-stac/v0.2.0/schema.json>
- **Field Name Prefix:** iso
- **Scope:** Item, Collection
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: @un-fao

## Why this exists

FAO maintains its dataset metadata in ISO 19115-1 form (served through
`data.apps.fao.org/catalog`, CKAN-backed) and its geospatial content in
STAC form (served through the FAO geospatial STAC catalog). A single
dataset is described by both, with different vocabularies. This
extension merges the two so a STAC client can read the full ISO 19115-1
metadata of a FAO dataset without leaving STAC.

It does this in three layers:

1. **A mapping** — a normative table that maps every ISO 19115-1 field
   used by the FAO ISO profile to its STAC location, preferring an
   existing community extension wherever possible. The full table lives
   at [`mapping/iso19115-2-to-stac.md`](mapping/iso19115-2-to-stac.md).
2. **A profile** — a statement of which mapped fields are mandatory,
   needed, or optional in the FAO ISO 19115-1 profile (see "Profile
   requirements" below).
3. **A STAC extension** — a small set of `iso:*` fields covering the ISO
   concepts that have no equivalent in any existing STAC extension.

The two example documents in [`examples/`](examples/) demonstrate the
profile end-to-end: each declares the full set of upstream extensions
the FAO profile expects (`scientific`, `themes`, `language`,
`processing`, `timestamps`, `datacube`, `raster`, `classification`,
`render`, `alternate-assets`, plus the FAO `fao` extension and this
`iso-to-stac` extension), so a reader can see exactly how an ISO
19115-1 record maps into a STAC Collection / Item under the FAO profile.

- Examples:
  - [Item example](examples/item.json): Profile in action on an Item
  - [Collection example](examples/collection.json): Profile in action on a Collection
- [JSON Schema](json-schema/schema.json)
- [Mapping](mapping/iso19115-2-to-stac.md)
- [Changelog](./CHANGELOG.md)

## Fields

The `iso:*` fields defined by this extension. They can be used in:

- [ ] Catalogs
- [x] Collections
- [x] Item Properties
- [ ] Assets
- [ ] Links

| Field Name | Type | Description |
| --- | --- | --- |
| iso:lineage_statement | string | `MD_DataIdentification.resourceLineage.LI_Lineage.statement` — human-readable lineage statement. |
| iso:maintenance_and_update_frequency | string | `MD_MaintenanceInformation.maintenanceAndUpdateFrequency` — `MD_MaintenanceFrequencyCode` value. |
| iso:presentation_form | string | `CI_Citation.presentationForm` — `CI_PresentationFormCode` value. |
| iso:character_set_code | string | `MD_DataIdentification.characterSet` — `MD_CharacterSetCode` value. |
| iso:spatial_representation_type | string | `MD_DataIdentification.spatialRepresentationType` — `MD_SpatialRepresentationTypeCode` value. |
| iso:purpose | string | `MD_DataIdentification.purpose` — free text. |
| iso:status | string | `MD_DataIdentification.status` — `MD_ProgressCode` value. |
| iso:access_constraints | string | `MD_LegalConstraints.accessConstraints` — `MD_RestrictionCode` value. |
| iso:use_constraints | string | `MD_LegalConstraints.useConstraints` — `MD_RestrictionCode` value. |
| iso:use_limitation | string | `MD_LegalConstraints.useLimitation` — free text. |
| iso:other_constraints | string | `MD_LegalConstraints.otherConstraints` — free text. |

All fields are optional at the schema level. The FAO ISO 19115-1 profile
imposes the additional requirements below.

## Profile requirements (FAO ISO 19115-1)

Three tiers:

- **MANDATORY** — fields the FAO ISO profile marks in red. Producers
  MUST supply them; absence is a profile-conformance failure.
- **Needed** — fields the profile requires in practice but ISO does not
  mark mandatory. Producers SHOULD supply them.
- **Optional** — neither ISO nor the profile requires them; producers
  MAY supply them.

The mapping document at [`mapping/iso19115-2-to-stac.md`](mapping/iso19115-2-to-stac.md)
carries the full profile column for every row. The summary for `iso:*`
fields specifically:

| Field | Profile tier |
| --- | --- |
| `iso:lineage_statement` | **MANDATORY** |
| `iso:maintenance_and_update_frequency` | **Needed** |
| `iso:presentation_form` | Optional |
| `iso:character_set_code` | Optional |
| `iso:spatial_representation_type` | Optional |
| `iso:purpose` | Optional |
| `iso:status` | Optional |
| `iso:access_constraints` | Optional |
| `iso:use_constraints` | Optional |
| `iso:use_limitation` | Optional |
| `iso:other_constraints` | Optional |

The schema does NOT enforce these requirements: profile checking is the
responsibility of the validator, not the extension. Schema-level
`required: []` would prevent producers who comply with ISO but not the
FAO profile from using the extension.

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
