# OGC Metadata SWG Coordination Note — `iso-to-stac`

This is the parallel coordination note shared with the OGC Metadata
Standards Working Group (ISO TC 211 liaison) for the
[`iso-to-stac`](../../extensions/iso-to-stac/) extension. The companion
GitHub-side submission text lives in
[`stac-community-submission.md`](stac-community-submission.md); this note
is focused on the points where a STAC ↔ ISO mapping benefits from
upstream OGC / ISO review.

## Context

FAO maintains its dataset metadata in ISO 19115-1 form (CKAN-backed
catalog, `data.apps.fao.org/catalog`) and its geospatial content in
STAC form (FAO geospatial STAC catalog,
`data.apps.fao.org/geospatial/`). A single dataset is described by
both, with different vocabularies, and historically users had to
consult both. The `iso-to-stac` extension merges the two so a STAC
client can read the full ISO 19115-1 metadata of a dataset without
leaving STAC.

There is no existing STAC ↔ ISO 19115 mapping extension. The proposal
fills that gap with a normative crosswalk plus a small set of `iso:*`
fields covering only the ISO concepts that have no equivalent in any
existing community extension.

## Why coordination with the Metadata SWG matters

1. The crosswalk is **normative** for downstream STAC adopters but
   **derivative** of ISO 19115-1. Upstream review reduces the chance of
   diverging interpretations between ISO and STAC tooling (pygeometa,
   GeoNetwork, OGC API - Records implementations).
2. The extension explicitly references several **ISO codelists**
   (`MD_MaintenanceFrequencyCode`, `MD_RestrictionCode`,
   `MD_ProgressCode`, `CI_PresentationFormCode`, `MD_CharacterSetCode`,
   `MD_SpatialRepresentationTypeCode`). Today these are typed as
   `string` in the schema; the SWG can advise on whether to
   schema-enumerate them and how to handle codelist evolution.
3. The crosswalk overlaps with **OGC API - Records** core record
   properties (e.g. `themes`, `language`, `keywords`, `created`,
   `updated`). Aligning vocabulary before broader adoption avoids the
   STAC and Records communities defining incompatible mappings of the
   same ISO concept.

## Specific points to surface

### 1. Lineage — overlap with the STAC Processing extension

ISO `LI_Lineage.statement` maps to **`processing:lineage`** (Processing
extension), which explicitly cites NASA's ISO lineage information as
its source. The crosswalk recommends `processing:lineage` for new
producers and retains `iso:lineage_statement` only as a fallback for
profile-locked Collection-top-level placement. **Open question:** drop
`iso:lineage_statement` before v1.0 of the extension and recommend
`processing:lineage` exclusively?

### 2. Codelist values

The 12 `iso:*` fields that wrap ISO codelists are schema-typed as
`string` rather than `enum`, on the assumption that ISO TC 211 may
extend the codelists. **Open question:** should the schema enumerate
the current values for stronger validation, accepting that codelist
updates trigger a schema bump? Or should we publish the codelists as a
separate, versioned JSON document the schema references?

### 3. Contacts and responsible-party roles

The crosswalk uses **two** contact-shaped mappings side by side:

- **Lossy:** ISO `CI_Responsibility.party.organisationName` →
  STAC core `providers[].name` (with role mapped to STAC's four
  enum values).
- **Lossless:** ISO `CI_Responsibility` →
  [Contacts extension](https://github.com/stac-extensions/contacts)
  `contacts[]` (free-form `roles[]`, full `phone`/`address` blocks).

Producers with ISO contacts richer than STAC core's four-role
enumeration should adopt the Contacts extension; the crosswalk
documents both paths. **Open question:** does the SWG want to coordinate
the role vocabulary between Records, Contacts, and ISO?

### 4. Spatial representation type

`iso:spatial_representation_type` is a `MD_SpatialRepresentationTypeCode`
codelist value (vector / grid / textTable / tin / stereoModel / video).
STAC has no native concept of spatial-representation type — implicit in
which extensions are declared (`raster`, `vector`, `pointcloud`, …).
**Open question:** is there value in a normative table mapping ISO
spatial-representation-type values to recommended STAC extension stacks?

### 5. Citation, DOI, edition

ISO `CI_Citation.identifier` (when carrying a DOI) maps to **`sci:doi`**
(Scientific Citation extension) and `CI_Citation.edition` maps to
**`version`** (Versioning Indicators extension). Cross-reference
welcome: are there other Records / Metadata SWG mappings that should
align?

### 6. Mandatory profile-tier separation

The FAO ISO 19115-1 profile's MANDATORY / Needed / Optional tiers are
documented in the extension README and crosswalk but **not enforced by
the JSON Schema**. This keeps the extension reusable by any ISO
producer, not just FAO. **Open question:** does the SWG see value in
publishing profile manifests as a separate schema family?

## What we are asking of the Metadata SWG

1. Review the crosswalk at
   [`mapping/iso19115-2-to-stac.md`](../../extensions/iso-to-stac/mapping/iso19115-2-to-stac.md)
   for fidelity to ISO 19115-1 / 19115-2 / 19139, and for alignment
   with the OGC API - Records record-properties vocabulary.
2. Comment on the open questions in §1–§6 above, especially:
   - the `processing:lineage` deprecation question
   - the codelist enumeration question
3. Optionally co-author or co-review a short OGC engineering report
   summarising the mapping for OGC implementers.

## Pointers

- Extension repo: <https://github.com/un-fao/fao-stac-extensions>
- Crosswalk: <https://github.com/un-fao/fao-stac-extensions/blob/main/extensions/iso-to-stac/mapping/iso19115-2-to-stac.md>
- STAC community submission package:
  [`stac-community-submission.md`](stac-community-submission.md)
- OGC API - Records: <https://ogcapi.ogc.org/records/>
- STAC ↔ Records sibling work in this repo: see the
  [`ogc-dimensions`](https://github.com/ccancellieri/ogc-dimensions) FAO
  proposal, which proposes a paginated dimensions surface for STAC
  / OGC API and walks the same Proposal → Pilot → Candidate → Stable
  pathway.

## Suggested handover

This note is intended to be shared on the OGC Metadata SWG mailing
list / pipermail thread, with a short cover email pointing to the GitHub
discussion and to the crosswalk. The discussion lives on the GitHub
side; the SWG channel is for asynchronous standards review only.
