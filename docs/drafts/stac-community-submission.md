# STAC Community Submission — `iso-to-stac`

This is the submission package for proposing the
[`iso-to-stac`](../../extensions/iso-to-stac/) extension to the
[`stac-extensions/` GitHub organisation](https://github.com/stac-extensions)
for inclusion in the [STAC Extension Index](https://stac-extensions.github.io/).

The companion [`fao`](../../extensions/fao/) extension is intentionally
**not** part of this submission. It is FAO-platform-specific (workspace,
product identifiers, FAO product-type classifier) and remains a
permanent custom extension served directly from this repository's git
tree at the release tag. See the umbrella `README.md` for the
rationale.

---

## Header

| Field | Value |
| --- | --- |
| Title | ISO 19115-2 to STAC Mapping |
| Identifier (interim) | `https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/iso-to-stac/json-schema/schema.json` |
| Identifier (target on acceptance) | `https://stac-extensions.github.io/iso-to-stac/v0.2.0/schema.json` |
| Field name prefix | `iso` |
| Scope | Item, Collection |
| Maturity | Proposal |
| Owner | @un-fao |
| License | Apache-2.0 |
| Reference implementation | [`reference-implementation/`](../../reference-implementation/) (Python) |
| Pilot deployment | FAO Agro-Informatics Platform — `data.review.fao.org/geospatial/` (review), `data.apps.fao.org/geospatial/` (production) |

## Why this extension

There is no existing STAC extension that maps the ISO 19115 metadata
model onto STAC. Every organisation merging an ISO 19115-based catalog
(ISO TC 211 / OGC API - Records / GeoNetwork / pygeometa producers, FAO
CKAN, NASA CMR, ESA EOPF, …) into STAC ends up either:

1. inventing its own ad-hoc field set, or
2. losing ISO concepts that have no STAC home (lineage statement,
   maintenance frequency, codelist values, presentation form, character
   set, …), or
3. pushing them into free-text `description`, breaking the round-trip.

`iso-to-stac` fills that gap with three layers, each shippable on its
own:

1. **A normative crosswalk** — `mapping/iso19115-2-to-stac.md` —
   mapping every ISO 19115-1 field used by a representative producer
   profile to its STAC location, **preferring an existing community
   extension wherever possible**. Eight community extensions are
   referenced (`scientific`, `themes`, `language`, `processing`,
   `timestamps`, `datacube`, `raster`, `classification`, `render`,
   `alternate-assets`, `version`, `contacts`) before this extension
   contributes anything new.
2. **A small set of `iso:*` fields** — exactly 12, only where step 1
   found no existing extension. The full table is reproduced below.
3. **An optional FAO ISO 19115-1 profile** — published as a separate
   conformance tier in the README; not normative on the schema, so the
   extension is reusable by any ISO 19115 producer regardless of
   profile.

The combination lets a STAC client read the full ISO 19115-1 metadata
of a dataset without leaving STAC.

## Field set (`iso:*`)

All fields are optional at the schema level; profile-required fields
are documented in the README. The schema co-exists with other
extensions on the same Item / Collection (the `^(?!iso:)` pattern
allows non-`iso:`-prefixed siblings).

| Field | Type | ISO 19115-1 source | Justification — why no existing STAC home |
| --- | --- | --- | --- |
| `iso:lineage_statement` | string | `MD_DataIdentification.resourceLineage.LI_Lineage.statement` | New producers SHOULD prefer `processing:lineage` (which cites NASA's ISO lineage information as its source). Retained as a fallback for FAO-style profiles that need a Collection-top-level field with an `iso:` prefix. **Open question:** drop before v1.0? See "Open questions" below. |
| `iso:maintenance_and_update_frequency` | string | `MD_MaintenanceInformation.maintenanceAndUpdateFrequency` | `MD_MaintenanceFrequencyCode` codelist (continual/daily/…/notPlanned). No STAC equivalent. |
| `iso:presentation_form` | string | `CI_Citation.presentationForm` | `CI_PresentationFormCode` codelist (mapDigital/imageDigital/…). No STAC equivalent. |
| `iso:character_set_code` | string | `MD_DataIdentification.characterSet` | `MD_CharacterSetCode` codelist (utf8/ucs2/…). No STAC equivalent. |
| `iso:spatial_representation_type` | string | `MD_DataIdentification.spatialRepresentationType` | `MD_SpatialRepresentationTypeCode` codelist (vector/grid/textTable/tin/stereoModel/video). No STAC equivalent. |
| `iso:purpose` | string | `MD_DataIdentification.purpose` | Free-text purpose statement. STAC core `description` is used for the resource description; ISO `purpose` is a distinct concept. |
| `iso:status` | string | `MD_DataIdentification.status` | `MD_ProgressCode` codelist (completed/onGoing/…/withdrawn). No STAC equivalent. |
| `iso:access_constraints` | string | `MD_LegalConstraints.accessConstraints` | `MD_RestrictionCode` codelist value. STAC core `license` only carries the SPDX-style identifier. |
| `iso:use_constraints` | string | `MD_LegalConstraints.useConstraints` | Same codelist; distinct ISO concept (use vs access). |
| `iso:use_limitation` | string | `MD_LegalConstraints.useLimitation` | Free-text limitation. No STAC equivalent. |
| `iso:other_constraints` | string | `MD_LegalConstraints.otherConstraints` | Free-text. No STAC equivalent. |
| `iso:supplemental_information` | string | `MD_DataIdentification.supplementalInformation` | Distinct from STAC `description`; carrying it as a typed field preserves the ISO/STAC round-trip. |

The full crosswalk (every ISO 19115-1 field used by FAO, including the
ones that map to existing extensions) lives at
[`mapping/iso19115-2-to-stac.md`](../../extensions/iso-to-stac/mapping/iso19115-2-to-stac.md).

## What this extension does **not** do

- It does not redefine ISO concepts that already map to community
  extensions. The crosswalk explicitly uses `processing:lineage`,
  `language` / `languages[]`, `themes`, `contacts`, `sci:citation`,
  `sci:doi`, `version`, raster band metadata from `raster`, etc.
- It does not enforce profile-required-ness in JSON Schema. The FAO
  profile's MANDATORY / Needed / Optional tiers are documented; profile
  validation is the validator's job, not the schema's. This keeps the
  extension reusable by any ISO 19115 producer, not just FAO.
- It does not introduce new `rel` types. ISO link concepts map onto
  STAC core (`describedby`, `license`, `via`, `style`, `legend`, `sld`,
  …).
- It does not propose a Records-of-records pattern (a single STAC
  document **describing** an external ISO record) — that's OGC API -
  Records' job. This extension carries the ISO content **inside** the
  STAC document.

## Implementations & pilot evidence

- **Reference implementation** —
  [`reference-implementation/`](../../reference-implementation/) is a
  pip-installable Python package (`fao-stac-extensions`) that exposes
  `SCHEMA_URI`, `PREFIX`, and is wired into `pytest` so every example
  validates against the schema and the modality-mutex counter-example
  fails as expected. CI status is in the umbrella README badge.
- **Live deployment** — the FAO Agro-Informatics Platform serves
  Collections / Items declaring this extension URL on
  `data.review.fao.org/geospatial/search/stac/`. Worked examples in
  this repository (`extensions/iso-to-stac/examples/{item,collection}.json`)
  are drawn from a real product (Agricultural Stress Index — Dekadal —
  Global 1km, `ASI-D`).
- **Crosswalk** — `mapping/iso19115-2-to-stac.md` covers every ISO
  field the FAO profile carries (≈ 110 rows organised by ISO 19115-1
  section), each with an explicit profile tier and a hyperlink to the
  contributing extension's repo where applicable.

## Open questions for community review

1. **`iso:lineage_statement` vs `processing:lineage`.** The Processing
   extension explicitly cites NASA's ISO lineage information as its
   source, so it is the de-facto STAC home for ISO lineage. The schema
   description for `iso:lineage_statement` already advises new
   producers to prefer `processing:lineage`. **Should we drop
   `iso:lineage_statement` before v1.0 of this extension and recommend
   `processing:lineage` exclusively?** FAO is willing to migrate.
2. **Codelist values.** The `iso:*` fields that wrap ISO codelists
   (`MD_MaintenanceFrequencyCode`, `MD_RestrictionCode`,
   `MD_ProgressCode`, `CI_PresentationFormCode`,
   `MD_CharacterSetCode`, `MD_SpatialRepresentationTypeCode`) are
   schema-typed as `string` rather than enum, on the assumption that
   ISO TC 211 may extend the codelists. **Should the schema enumerate
   the current values for stronger validation, accepting that
   updates require a schema bump?**
3. **Field naming.** `iso:lineage_statement` is the longest name;
   shorter alternatives (`iso:lineage`) collide with `processing:lineage`
   semantics. **Comments welcome on naming for clarity.**
4. **Profile separation.** The FAO ISO 19115-1 profile is documented in
   the extension's README but not normative on the schema. **Is the
   community comfortable with this separation, or should profiles live
   in a separate document outside the extension repo?**

## Migration path for adopters

Producers already shipping ISO 19115 alongside STAC adopt the extension
by:

1. Adding the schema URL to `stac_extensions[]`.
2. Translating their ISO record using the crosswalk in
   `mapping/iso19115-2-to-stac.md`. Most fields land on existing
   community extensions; only the 12 fields above need the `iso:`
   prefix.
3. Optionally declaring conformance with the FAO ISO 19115-1 profile
   (or their own profile) to commit to the MANDATORY / Needed tiers.

## Repository

- Umbrella: <https://github.com/un-fao/fao-stac-extensions>
- This extension: <https://github.com/un-fao/fao-stac-extensions/tree/main/extensions/iso-to-stac>
- Schema: <https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/iso-to-stac/json-schema/schema.json>
- Crosswalk: <https://github.com/un-fao/fao-stac-extensions/blob/main/extensions/iso-to-stac/mapping/iso19115-2-to-stac.md>

## How to take this submission forward

The proposal is being shared with the STAC community in two parallel
channels:

1. **GitHub discussion** — a short version of this document is
   posted at <https://github.com/radiantearth/stac-spec/discussions>
   (Extensions category) for community feedback before any PR. Draft
   discussion body in [Appendix A](#appendix-a--github-discussion-body).
2. **OGC Metadata SWG / ISO TC 211 liaison** — coordination note in
   [`ogc-metadata-coordination.md`](ogc-metadata-coordination.md), shared
   with the Metadata SWG so the crosswalk benefits from upstream
   review.

After community feedback settles, FAO will open a PR to the
[`stac-extensions/.github`](https://github.com/stac-extensions/.github)
proposal-tracking repository (Candidate phase per the umbrella README's
standardization pathway).

---

## Appendix A — GitHub discussion body

Title: **Proposal: `iso-to-stac` extension — ISO 19115-2 ↔ STAC mapping**

```markdown
Hi all,

FAO is proposing a new STAC extension that maps the ISO 19115 metadata
model onto STAC, so a STAC client can read the full ISO 19115-1 metadata
of a dataset without leaving STAC.

There is no existing STAC ↔ ISO 19115 mapping extension; producers with
ISO catalogs end up inventing ad-hoc fields or losing ISO concepts in
free-text descriptions. We've drafted a normative crosswalk covering
every ISO 19115-1 field used by a representative producer profile,
preferring existing community extensions wherever they cover the
concept (`processing`, `scientific`, `themes`, `language`, `contacts`,
`raster`, `version`, `timestamps`, …) and contributing 12 new `iso:*`
fields only where no existing extension covers the ISO concept.

- **Repo:** https://github.com/un-fao/fao-stac-extensions
- **Extension:** https://github.com/un-fao/fao-stac-extensions/tree/main/extensions/iso-to-stac
- **Schema (interim URL):** https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/iso-to-stac/json-schema/schema.json
- **Crosswalk:** https://github.com/un-fao/fao-stac-extensions/blob/main/extensions/iso-to-stac/mapping/iso19115-2-to-stac.md
- **Reference implementation:** https://github.com/un-fao/fao-stac-extensions/tree/main/reference-implementation
- **Pilot deployment:** https://data.review.fao.org/geospatial/search/stac/

Open questions we'd like community input on (full list in
docs/drafts/stac-community-submission.md):

1. Drop `iso:lineage_statement` and recommend `processing:lineage`
   exclusively before v1.0?
2. Schema-enumerate ISO codelist values, or keep them as `string` to
   tolerate ISO TC 211 extensions?
3. Profile separation — are MANDATORY / Needed / Optional tiers
   acceptable as documented-but-not-normative?

Coordination with the OGC Metadata SWG (ISO TC 211 liaison) is running
in parallel; coordination note in
docs/drafts/ogc-metadata-coordination.md.

Happy to iterate on naming, scope, and field set before we open a PR
to the stac-extensions/ org.

Thanks,
FAO Agro-Informatics Platform team
```

**This document is the submission package; the discussion body above
is what gets posted manually by a maintainer to the STAC discussion
forum.**
