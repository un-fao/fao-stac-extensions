# ISO 19115-1 ↔ STAC Mapping (FAO Profile)

Normative mapping table for the FAO ISO 19115-1 profile.

This document is the per-field crosswalk that lets an FAO ISO 19115-1
metadata record be merged into a STAC Collection / Item without
information loss: every ISO field used by the FAO profile resolves
either to a STAC core field, to a field contributed by an existing
community extension, or to an `iso:*` field defined by this extension
(only when no upstream extension covers the ISO concept).

The tables are grouped by ISO 19115-1 section for readability. A short
[References](#references) section at the end links to the upstream
standards and to other community efforts in the same space.

## Profile tiers

| Tier | Meaning |
| --- | --- |
| **MANDATORY** | Mandatory in both ISO and the FAO profile. Producers MUST supply the value. |
| **Needed** | Required by the FAO profile, not by ISO. Producers SHOULD supply the value. |
| Optional | Optional in both ISO and the FAO profile. Producers MAY supply the value. |
| Not needed | Defined by ISO but not used by the FAO profile. |
| _one of below_ | The next group of rows offers alternatives; pick exactly one. |

## STAC field reference key

| Notation | Meaning |
| --- | --- |
| `field` | A STAC core field. |
| `prefix:field` | A field contributed by the named extension (e.g. `sci:citation` from the Scientific Citation extension). |
| `iso:field` | A new field defined by this extension. The full list is in the [New `iso:*` fields](#new-iso-fields-defined-by-this-extension) section. |
| `Asset` / `Link` (no field name) | The ISO concept becomes an entry in the `assets` block or the `links` array; the body of the entry is detailed in the rows that follow. |

---

## 1. Identification & Citation

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Title | `title` | Collection | core |
| **Needed** | Citation | `sci:citation` | Collection | [Scientific Citation](https://github.com/stac-extensions/scientific) |
| **MANDATORY** | Citation Identifier (when DOI) | `sci:doi` | Collection | [Scientific Citation](https://github.com/stac-extensions/scientific) |
| Optional | Citation Edition | `version` | Collection | [Versioning Indicators](https://github.com/stac-extensions/version) |
| **MANDATORY** | Description | `description` | Collection | core |
| **Needed** | Theme Keywords | `keywords` | Collection | core |
| **Needed** | Temporal Keywords | `keywords` | Collection | core |
| **Needed** | Place Keywords | `keywords` | Collection | core |
| **MANDATORY** | Topic Category | `themes` (with `scheme` set to ISO topic category codelist URI) | Collection | [Themes](https://github.com/stac-extensions/themes) |
| **MANDATORY** | Language (resource — primary) | `language` | Collection | [Language](https://github.com/stac-extensions/language) |
| Optional | Language (resource — additional) | `languages[]` | Collection | [Language](https://github.com/stac-extensions/language) |
| Optional | Presentation Form | `iso:presentation_form` | Collection | this |
| Optional | Character Set Code | `iso:character_set_code` | Collection | this |
| Optional | Spatial Representation Type | `iso:spatial_representation_type` | Collection | this |
| Optional | Purpose | `iso:purpose` | Collection | this |
| Optional | Supplemental Information | `iso:supplemental_information` | Collection | this |

> **Note on `language` vs `languages[]`** — ISO `MD_DataIdentification.language[]`
> is an *array* of resource languages; the STAC Language extension splits this
> into `language` (the primary) and `languages` (other available). OGC API -
> Records introduces a separate `resourceLanguages` field for this use case;
> STAC has not adopted that field. Producers SHOULD set `language` to the
> primary resource language and emit `languages[]` for any others.

## 2. Date (referring to data)

The ISO `CI_Date` block holds the data's creation, publication, and
revision dates at Asset level via the Timestamps extension. Pick the
date types that apply.

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | _Date (referring to data)_ | _(see one-of below)_ | Asset | [Timestamps](https://github.com/stac-extensions/timestamps) |
| _one of below_ | Date — Creation | `created` | Asset | Timestamps |
|  | Date — Publication | `published` | Asset | Timestamps |
|  | Date — Revision | `updated` | Asset | Timestamps |

## 3. Maintenance, Status & Purpose

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Maintenance and Update Frequency | `iso:maintenance_and_update_frequency` | Collection | this |
| Optional | Status | `iso:status` | Collection | this |

(Purpose is in section 1.)

## 4. Constraints & Rights

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | License | `license` | Collection | core (use [SPDX](https://spdx.org/licenses/) identifier) |
| Optional | Access Constraints | `iso:access_constraints` | Collection | this |
| Optional | Use Constraints | `iso:use_constraints` | Collection | this |
| Optional | Use Limitation | `iso:use_limitation` | Collection | this |
| Optional | Other Constraints | `iso:other_constraints` | Collection | this |

## 5. Spatial & Temporal Extent

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **Needed** | Geographical Extent — Bounding Box | `extent.spatial.bbox` | Collection / Item | core |
| **Needed** | Temporal Extent — Begin / End date | `extent.temporal.interval` | Collection | core |
| Optional | Vertical Extent — Min / Max | `cube:dimensions.z.extent` | Collection | [Datacube](https://github.com/stac-extensions/datacube) |
| **Needed** | Spatial Resolution — Distance and Unit | `raster:bands[].spatial_resolution` (or `gsd` from EO) | Item | [Raster](https://github.com/stac-extensions/raster) / [EO](https://github.com/stac-extensions/eo) |
| Optional | Spatial Resolution — Scale denominator | `raster:bands[].spatial_resolution` (or `gsd` from EO) | Item | Raster / EO |

## 6. Distribution & Resources

ISO `MD_DigitalTransferOptions.onLine.CI_OnlineResource` blocks become
entries in the STAC `assets` block (when they point at the data
itself) or in `links` (when they point at related resources). The
sub-rows describe the body of each entry.

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **Needed** | Distribution format | _(Asset)_ | Asset | core (`assets[].type`) |
| Optional | Distribution format — Name | _(Asset)_ | Asset | core (`assets[].title`) |

### 6.1. Data for download

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Linkage URL | `assets[].href` (primary) or `links[].href` | Asset / Link | core |
| **MANDATORY** | Name | `assets[].title` (primary) or `links[].title` | Asset / Link | core |
| Optional | Description | `assets[].description` or `links[].description` | Asset / Link | core |
|  | Date — Creation | `created` | Asset | [Timestamps](https://github.com/stac-extensions/timestamps) |
|  | Date — Publication | `published` | Asset | Timestamps |
|  | Date — Revision | `updated` | Asset | Timestamps |

### 6.2. WMTS

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Linkage URL | `links[].href` (`rel=tiles` or service-specific) | Link | core |
| **MANDATORY** | Name | `links[].title` | Link | core |
| Optional | Description | `links[].description` | Link | core |

### 6.3. Licence link

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Linkage URL | `links[].href` (`rel=license`) | Link | core |
| **MANDATORY** | Name | `links[].title` | Link | core |
| Optional | Description | `links[].description` | Link | core |

### 6.4. CKAN metadata link

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Linkage URL | `links[].href` (`rel=describedby`, `type=application/xml`) | Link | core |
| **MANDATORY** | Name | `links[].title` | Link | core |
| Optional | Description | `links[].description` | Link | core |

> **Asset alternative — the `iso-19115` role.** STAC core
> [best practices](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md)
> define `iso-19115` as a standard *asset* role for an ISO 19115 metadata
> file. If a producer prefers to expose the ISO metadata as an Asset
> rather than a Link (e.g. when checksum / file-size information from the
> [File Info extension](https://github.com/stac-extensions/file) is
> useful), set `assets[<key>].roles` to `["metadata", "iso-19115"]` and
> `assets[<key>].type` to `"application/xml"`. The FAO profile uses the
> link form for back-compatibility with existing CKAN catalogues.

## 7. Quality & Lineage

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **Needed** | Data Quality — Lineage — Statement Description | `processing:lineage` (preferred); `iso:lineage_statement` (fallback) | Collection or Provider | [Processing](https://github.com/stac-extensions/processing) |

> **Important — `processing:lineage` is the canonical home for ISO lineage
> statements.** The STAC Processing extension explicitly cites
> [NASA's ISO lineage information](https://wiki.earthdata.nasa.gov/display/NASAISO/Lineage+Information)
> as the source of the `processing:lineage` definition, so an ISO
> `LI_Lineage.statement` SHOULD be carried as `processing:lineage`. The
> Processing extension allows the field at Collection top-level, Item
> properties, and per-`providers[]` entry — pick the scope that matches
> the lineage statement's scope in the source ISO record (typically
> Collection-level for a dataset-wide statement; per-provider when
> different parties contributed different processing steps).
>
> `iso:lineage_statement` is retained as a fallback for FAO producers
> that need a strictly Collection-top-level field with an `iso:` prefix
> for ISO-round-trip clarity. **New producers SHOULD prefer
> `processing:lineage`.** The `iso:lineage_statement` field is a
> candidate for deprecation in a future release of this extension.

Related Processing extension fields that may apply: `processing:level`
(processing-level short name), `processing:facility`, `processing:datetime`,
`processing:version`, `processing:software`, plus the `derived_from`,
`processing-execution`, `processing-software`, and `processing-validation`
link relation types.

## 8. Metadata Block

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Metadata Creation Date | `created` | Collection | [Timestamps](https://github.com/stac-extensions/timestamps) |
| **MANDATORY** | Metadata Update Date | `updated` | Collection | Timestamps |
| Not needed | Metadata Language | (use `language` extension if needed) | Collection | [Language](https://github.com/stac-extensions/language) |

## 9. Contacts

The FAO profile carries metadata contacts and resource points of
contact in STAC core `providers[]`. The community-maintained STAC
[Contacts extension](https://github.com/stac-extensions/contacts)
(inspired by ISO 19115 + OGC API - Records) provides a richer
alternative with `addresses`, `phones`, `emails`, and other fields as
first-class properties — see [References](#references). Producers MAY
emit `contacts[]` in addition to `providers[]` for the same parties.

The same mapping applies to both the metadata contact and the
resource point of contact.

| Profile | ISO 19115-1 Field | STAC Field (current FAO profile) | STAC Field (Contacts ext, recommended for new producers) | Level |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Metadata Contact / Point of Contact | `providers[]` | `contacts[]` | Collection |
| **MANDATORY** | Organization name | `providers[].name` | `contacts[].organization` | Collection |
| **Needed** | Individual name | `providers[].name` | `contacts[].name` | Collection |
| **MANDATORY** | Role | `providers[].roles[]` | `contacts[].roles[]` | Collection |
| **Needed** | Electronic mail address | `providers[].description` (FAO workaround) | `contacts[].emails[].value` | Collection |
| Not needed | Address | _no STAC core equivalent — drop_ | `contacts[].addresses[]` | Collection |
| Not needed | URL | `providers[].url` | `contacts[].links[]` (`rel=about`) | Collection |

### 9.1. Role mapping (`CI_RoleCode` → STAC role)

ISO `CI_RoleCode` values map to STAC role values *differently* depending
on whether the producer uses STAC core `providers[]` or the STAC
[Contacts extension](https://github.com/stac-extensions/contacts):

- **`providers[].roles[]`** is constrained by STAC core to four values
  (`licensor` / `producer` / `processor` / `host`). The mapping below is
  therefore **lossy** — multiple ISO codes collapse into the same STAC
  role.
- **`contacts[].roles[]`** is `array of free-form strings` per the
  Contacts extension schema. Producers SHOULD carry the ISO
  `CI_RoleCode` value verbatim there for a **lossless** round-trip.

The mapping is the same whether the role applies to the metadata
contact or to the resource point of contact.

| ISO `CI_RoleCode` | `providers[].roles[]` (lossy) | `contacts[].roles[]` (lossless) |
| --- | --- | --- |
| author | producer | author |
| custodian | host | custodian |
| distributor | host | distributor |
| originator | producer | originator |
| owner | licensor | owner |
| pointOfContact | host | pointOfContact |
| principalInvestigator | producer | principalInvestigator |
| processor | processor | processor |
| publisher | host | publisher |
| resourceProvider | producer | resourceProvider |
| user | _no STAC equivalent — drop_ | user |

---

## New `iso:*` fields defined by this extension

Where the tables above map an ISO field to `iso:*`, this extension
defines the field because no existing STAC extension covers the ISO
concept. The full description, JSON Schema entry, and codelist hints
for each are in [`../README.md`](../README.md) and
[`../json-schema/schema.json`](../json-schema/schema.json).

| Field | Type | Profile | ISO 19115-1 source |
| --- | --- | --- | --- |
| `iso:lineage_statement` | string | **MANDATORY** | `MD_DataIdentification.resourceLineage.LI_Lineage.statement` |
| `iso:maintenance_and_update_frequency` | string (codelist) | **Needed** | `MD_MaintenanceInformation.maintenanceAndUpdateFrequency` (`MD_MaintenanceFrequencyCode`) |
| `iso:presentation_form` | string (codelist) | Optional | `CI_Citation.presentationForm` (`CI_PresentationFormCode`) |
| `iso:character_set_code` | string (codelist) | Optional | `MD_DataIdentification.characterSet` (`MD_CharacterSetCode`) |
| `iso:spatial_representation_type` | string (codelist) | Optional | `MD_DataIdentification.spatialRepresentationType` (`MD_SpatialRepresentationTypeCode`) |
| `iso:purpose` | string | Optional | `MD_DataIdentification.purpose` |
| `iso:status` | string (codelist) | Optional | `MD_DataIdentification.status` (`MD_ProgressCode`) |
| `iso:access_constraints` | string (codelist) | Optional | `MD_LegalConstraints.accessConstraints` (`MD_RestrictionCode`) |
| `iso:use_constraints` | string (codelist) | Optional | `MD_LegalConstraints.useConstraints` (`MD_RestrictionCode`) |
| `iso:use_limitation` | string | Optional | `MD_LegalConstraints.useLimitation` |
| `iso:other_constraints` | string | Optional | `MD_LegalConstraints.otherConstraints` |
| `iso:supplemental_information` | string | Optional | `MD_DataIdentification.supplementalInformation` |

---

## References

### Upstream standards

- [ISO 19115-1:2014 — Geographic information — Metadata — Part 1: Fundamentals](https://www.iso.org/standard/53798.html)
- [ISO 19115-2:2019 — Geographic information — Metadata — Part 2: Extensions for acquisition and processing](https://www.iso.org/standard/67039.html)
- [ISO 19139:2007 — Geographic MetaData XML schema implementation](https://www.iso.org/standard/32557.html)
- [ISO standards codelist registry (`gmxCodelists.xml`)](https://standards.iso.org/iso/19115/resources/Codelists/gml/) — the source of every `*Code` value referenced above (`MD_MaintenanceFrequencyCode`, `MD_RestrictionCode`, `MD_ProgressCode`, `MD_SpatialRepresentationTypeCode`, `CI_PresentationFormCode`, `CI_RoleCode`, …)

### STAC ecosystem

- [STAC core specification](https://github.com/radiantearth/stac-spec) — the spec this extension extends.
- [STAC best practices: `iso-19115` link role](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md) — STAC core defines `iso-19115` as a standard asset/link role for references to ISO XML metadata files. The FAO profile uses `links[rel=describedby] type=application/xml` for the same purpose.
- [STAC Contacts extension](https://github.com/stac-extensions/contacts) — explicitly inspired by ISO 19115 + OGC API - Records; covers the contact / address / email mapping more completely than STAC core's `providers[]`. New FAO-profile producers SHOULD consider emitting `contacts[]` alongside `providers[]`.
- [STAC Scientific Citation extension](https://github.com/stac-extensions/scientific) — used here for `sci:citation` (and optionally `sci:doi`).
- [STAC Themes extension](https://github.com/stac-extensions/themes) — used here for `themes` (ISO topic category and other knowledge-organisation systems).
- [STAC Language extension](https://github.com/stac-extensions/language) — used here for `language`.
- [STAC Processing extension](https://github.com/stac-extensions/processing) — defines `processing:lineage` per provider; complementary to `iso:lineage_statement`.
- [STAC Timestamps extension](https://github.com/stac-extensions/timestamps) — used here for `created` / `updated` / `published` on Assets and on the Collection metadata block.
- [STAC Datacube extension](https://github.com/stac-extensions/datacube) — used here for vertical extent (`cube:dimensions.z`) and any further dimensions.
- [STAC Raster extension](https://github.com/stac-extensions/raster) — used here for spatial resolution (`raster:bands[].spatial_resolution`).
- [STAC EO extension](https://github.com/stac-extensions/eo) — alternative source for spatial resolution (`gsd`) when the data is electro-optical.

### Adjacent communities

- [OGC API - Records](https://ogcapi.ogc.org/records/) — the OGC API for catalogue records; ISO-inspired and shares the same contact/address shape that the STAC Contacts extension adopts. The FAO profile aligns with OGC API - Records where possible.
- [pygeometa](https://github.com/geopython/pygeometa) — Python library for generating ISO 19115 / 19139 / DCAT / OGC API - Records metadata documents from a single source. Reference implementation for ISO 19139 generation; useful when round-tripping STAC ↔ ISO XML.
- [GeoNetwork](https://geonetwork-opensource.org/) — open-source catalogue platform that natively serves ISO 19115 / 19139 metadata; implements its own ISO ↔ DCAT mappings that informed parts of this crosswalk.
- [pystac](https://github.com/stac-utils/pystac) — Python library for working with STAC objects; the natural integration point for any ISO ↔ STAC mapper.
