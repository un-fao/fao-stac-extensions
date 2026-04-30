# ISO 19115-1 ↔ STAC Mapping (FAO Profile)

Normative mapping table for the FAO ISO 19115-1 profile.

This table is the per-field crosswalk that lets an FAO ISO 19115-1
metadata record be merged into a STAC Collection / Item without
information loss: every ISO field used by the FAO profile resolves
either to a STAC core field, to a field contributed by an existing
community extension, or to an `iso:*` field defined by this extension
(only when no upstream extension covers the ISO concept).

## Reading the table

| Column | Meaning |
| --- | --- |
| **Profile** | Required-ness in the FAO ISO 19115-1 profile. **MANDATORY** = mandatory in both ISO and the profile (must be present). **Needed** = required by the FAO profile, not by ISO. **Optional** = optional in both. **One of** = pick one of the rows that follow. |
| **ISO 19115-1 Field** | The ISO field name. |
| **STAC Field** | Target STAC location. `iso:*` fields are defined by this extension; `fao:*` fields are defined by the [`fao`](../../fao/) extension; everything else is STAC core or contributed by the named extension. |
| **Level** | Where the field lives: `Catalog`, `Collection`, `Item`, `Asset`, `Link`. |
| **Extension** | Upstream STAC extension contributing the field, if any. |

## Mapping

| Profile | ISO 19115-1 Field | STAC Field | Level | Extension |
| --- | --- | --- | --- | --- |
| **MANDATORY** | Title | `title` | Collection |  |
| **MANDATORY** | Citation | `sci:citation` | Collection | Scientific Citation (Extention Stable) |
| **MANDATORY** | Date (referring to data) |  | Asset | Timestamp |
| _one of below_ | Data - Creation | `created` | Asset |  |
|  | Date - Publication | `published` | Asset |  |
|  | Date - Revision | `updated` | Asset |  |
| Optional | Presentation Form | `iso:presentation_form` |  |  |
| Optional | Data Character Set Code | `iso:character_set_code` |  |  |
| Optional | Spatial Representation Type | `iso:spatial_representation_type` |  |  |
| **MANDATORY** | Description | `description` | Collection |  |
| Optional | Purpose | `iso:purpose` |  |  |
| Optional | Status | `iso:status` |  |  |
| **MANDATORY** | Maintenance and Update Frequency | `iso:maintenance_and_update_frequency` |  |  |
| **MANDATORY** | Theme Keywords | `keywords` | Collection |  |
| **MANDATORY** | Temporal Keywords | `keywords` | Collection |  |
| **MANDATORY** | Place Keywords | `keywords` | Collection |  |
| **MANDATORY** | License | `license` | Collection | License |
| Optional | Access Constraints | `iso:access_constraints` |  |  |
| Optional | Use Constraints | `iso:use_constraints` |  |  |
| Optional | Use Limitation | `iso:use_limitation` |  |  |
| Optional | Other Constraints | `iso:other_constraints` |  |  |
| **MANDATORY** | Language | `language` |  |  |
| **MANDATORY** | Spatial Resolution - Distance and Unit | raster:bands[].spatial_resolution or gsd (EO ext) | Item |  |
| Optional | Spatial Resolution - Scale denominator | raster:bands[].spatial_resolution or gsd (EO ext) | Item |  |
| **MANDATORY** | * Topic Category | `themes` | Collection | Themes |
| **MANDATORY** | Temporal Extent - Begin date, End date | `extent`: {temporal`: { `interval`: [] | Collection |  |
| **MANDATORY** | Geographical Extent - Bounding Box | `extent`: {spatial`: { `bbox`: [] | Collection/Item |  |
| Optional | Vertical Extent - Minimun value, Maximum value | cube:dimensions.z.extent (datacube ext) | Collection | Datacube |
| Optional | Supplemental Information | `description` (append) | Collection |  |
| **MANDATORY** | Distribution format |  | Asset |  |
| Optional | Distribution format - Name |  | Asset |  |
| **MANDATORY** | Data Quality - Lineage - Statement Description | `iso:lineage_statement` | Collection | Processing |
| | | **— LINKS to RESOURCES —** | | |
| | | **— Data for download —** | | |
| **MANDATORY** | Linkage URL | links[].href | Collection/Item |  |
| **MANDATORY** | Name | links[].title | Collection/Item |  |
| Optional | Description | links[].description | Collection/Item |  |
|  | _(continued)_ | `created` | To specify the creation date of the data | Timestamp |
|  | _(continued)_ | `published` | To specify the publication date of the data | Timestamp |
|  | _(continued)_ | `updated` | To specify the updated date of the data | Timestamp |
| | | **— WMTS —** | | |
| **MANDATORY** | Linkage URL | links[].href | Collection/Item |  |
| **MANDATORY** | Name | links[].title | Collection/Item |  |
| Optional | Description | links[].description | Collection/Item |  |
| | | **— Licence —** | | |
| **MANDATORY** | Linkage URL | links[].href | Collection |  |
| **MANDATORY** | Name | links[].title | Collection |  |
| Optional | Description | links[].description | Collection |  |
| | | **— CKAN Metadata —** | | |
| **MANDATORY** | Linkage URL | links[].href | Collection |  |
| **MANDATORY** | Name | links[].title | Collection |  |
| Optional | Description | links[].description | Collection |  |
| | | **— Spatial Representation Info from GISMNG —** | | |
| **MANDATORY** | _(continued)_ | `bands` | root |  |
|  | _(continued)_ | `description` |  |  |
|  | _(continued)_ | `nodata` |  |  |
|  | _(continued)_ | `unit` |  |  |
|  | _(continued)_ | `raster:scale` |  | Raster |
|  | _(continued)_ | `raster:offset` |  | Raster |
|  | _(continued)_ | `data_type` |  |  |
|  | _(continued)_ | `classification:classes` |  | Classification |
| **MANDATORY** | _(continued)_ | `cube:dimensions` | root | Datacube |
|  | _(continued)_ | x, y extent |  |  |
|  | _(continued)_ | time extent |  |  |
|  | _(continued)_ | any further dimensions |  |  |
|  | _(continued)_ | `reference_system` | Item properties / Collection summaries | Datacube extension |
| Needed (open) | _(continued)_ | `cube:variables` | root |  |
|  | _(continued)_ | type |  |  |
|  | _(continued)_ | dimension |  |  |
|  | _(continued)_ | description |  |  |
|  | _(continued)_ | unit |  |  |
|  | _(continued)_ | data_type |  |  |
|  | _(continued)_ | nodata |  |  |
| **MANDATORY** | _(continued)_ | `renders`: data | root | Renders |
|  | _(continued)_ | title |  |  |
|  | _(continued)_ | assets |  |  |
|  | _(continued)_ | resampling |  |  |
|  | _(continued)_ | colormap-name |  |  |
| **MANDATORY** | gismgr_layer_id | `fao:layer_id` *(see [fao extension](../../fao/))* | root |  |
| | | **— Metadata information —** | | |
| **MANDATORY** | Metadata Creation Date | `created` |  |  |
| **MANDATORY** | Metadata Update Date | `updated` |  |  |
| Not needed | Metadata Language | English |  |  |
| | | **— Contacts information —** | | |
| **MANDATORY** | Metadata Contact | `providers` |  |  |
| **MANDATORY** | Organization name | `name` |  |  |
| **MANDATORY** | Individual name | `name` |  |  |
| **MANDATORY** | *Role | `roles` |  |  |
| _one of below_ | author | `producer` |  |  |
|  | custodian | `host` |  |  |
|  | distributor | `host` |  |  |
|  | originator | `producer` |  |  |
|  | owner | `licensor` |  |  |
|  | point of contact | `host` |  |  |
|  | principle investigator | `producer` |  |  |
|  | processor | `processor` |  |  |
|  | publisher | `host` |  |  |
|  | resource provider | `producer` |  |  |
|  | user | No STAC equivalent |  |  |
| **MANDATORY** | Electronic mail Address | `description` | Collection |  |
| Not needed | Address | No STAC equivalent | Collection |  |
| Not needed | URL | `url` | Collection |  |
| **MANDATORY** | Point of Contact (for data) | `providers` | Collection |  |
| **MANDATORY** | Organization Name | `name` | Collection |  |
| **MANDATORY** | Individual name | `name` | Collection |  |
| **MANDATORY** | Role | `roles` | Collection |  |
| _one of below_ | author | `producer` | Collection |  |
|  | custodian | `host` | Collection |  |
|  | distributor | `host` | Collection |  |
|  | originator | `producer` | Collection |  |
|  | owner | `licensor` | Collection |  |
|  | point of contact | `host` | Collection |  |
|  | principle investigator | `producer` | Collection |  |
|  | processor | `processor` | Collection |  |
|  | publisher | `host` | Collection |  |
|  | resource provider | `producer` | Collection |  |
|  | user | No STAC equivalent | Collection |  |
| **MANDATORY** | Electronic mail Address | `description` | Collection |  |
| Not needed | Address | No STAC equivalent | Collection |  |
| Not needed | URL | `url` | Collection |  |

## New `iso:*` fields defined by this extension

Where the table above maps an ISO field to `iso:*`, this extension
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

## Role mapping (CI_RoleCode → STAC provider role)

The ISO `CI_RoleCode` codelist values map to STAC `providers[].roles[]`
values as follows. The mapping is the same whether the role applies to
the metadata contact or to the resource point of contact.

| ISO `CI_RoleCode` | STAC `providers[].roles[]` |
| --- | --- |
| author | producer |
| custodian | host |
| distributor | host |
| originator | producer |
| owner | licensor |
| pointOfContact | host |
| principalInvestigator | producer |
| processor | processor |
| publisher | host |
| resourceProvider | producer |
| user | _no STAC equivalent — drop_ |
