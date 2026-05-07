# STAC Community Submission — `iso-to-stac`

This is the submission package for proposing
[`iso-to-stac`](../../extensions/iso-to-stac/) to the
[`stac-extensions/` GitHub organisation](https://github.com/stac-extensions)
for inclusion in the [STAC Extension Index](https://stac-extensions.github.io/).

`iso-to-stac` ships **two artifacts in one repo** — both delivered
together because either alone is incomplete:

1. **A STAC extension** (`extensions/iso-to-stac/json-schema/schema.json`)
   — 12 typed `iso:*` fields, contributed only where no existing STAC
   community extension covers the ISO concept (lineage statement,
   `MD_MaintenanceFrequencyCode`, `MD_RestrictionCode`,
   presentation form, character set, etc.).
2. **A mapping document** (`extensions/iso-to-stac/mapping/iso19115-2-to-stac.md`)
   — the normative ISO 19115 ↔ STAC crosswalk that maps every
   ISO 19115-1 field used by a representative producer to its STAC
   location, **preferring an existing community extension wherever it
   covers the concept**. The mapping references the upstream sources
   (ISO 19115-1, ISO 19115-2, ISO 19139, the codelist registry, OGC
   API - Records, pygeometa, GeoNetwork) and to the community
   extensions it relies on (`processing`, `scientific`, `themes`,
   `language`, `timestamps`, `datacube`, `raster`, `classification`,
   `render`, `alternate-assets`, `version`, `contacts`).

The extension on its own would only carry the 12 leftover fields and
miss the point. The mapping document on its own would document a
crosswalk no producer can implement losslessly. Together, a STAC
client can read the full ISO 19115-1 metadata of a dataset without
leaving STAC.

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

`iso-to-stac` fills that gap by pairing the **mapping document** with a
small **extension** — every ISO field has a destination, and the
extension carries only the residue:

1. **The mapping document** — `mapping/iso19115-2-to-stac.md` — maps
   every ISO 19115-1 field used by a representative producer to its
   STAC location, **preferring an existing community extension wherever
   it covers the concept**. The crosswalk references twelve community
   extensions (`scientific`, `themes`, `language`, `processing`,
   `timestamps`, `datacube`, `raster`, `classification`, `render`,
   `alternate-assets`, `version`, `contacts`) and the upstream
   standards (ISO 19115-1 / 19115-2 / 19139, the codelist registry,
   OGC API - Records, pygeometa, GeoNetwork) before any new field is
   contributed.
2. **The extension** — exactly 12 `iso:*` fields contributed only
   where step 1 found no existing extension. The full field table is
   reproduced below.
3. **An optional FAO ISO 19115-1 profile** — documented in the
   extension README as a separate conformance tier (MANDATORY / Needed
   / Optional); not normative on the schema, so the extension stays
   reusable by any ISO 19115 producer.

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

1. **Mapping doc co-location.** The crosswalk lives inside the
   extension repo at `extensions/iso-to-stac/mapping/iso19115-2-to-stac.md`,
   so a single git pull gives implementers both the schema and the
   normative mapping. **Is that the right shape, or should the mapping
   doc be split out to a separate `iso19115-to-stac` repo / spec that
   the extension references?** FAO has no strong preference; the
   community may.
2. **`iso:lineage_statement` vs `processing:lineage`.** The Processing
   extension explicitly cites NASA's ISO lineage information as its
   source, so it is the de-facto STAC home for ISO lineage. The schema
   description for `iso:lineage_statement` already advises new
   producers to prefer `processing:lineage`. **Should we drop
   `iso:lineage_statement` before v1.0 of this extension and recommend
   `processing:lineage` exclusively?** FAO is willing to migrate.
3. **Codelist values.** The `iso:*` fields that wrap ISO codelists
   (`MD_MaintenanceFrequencyCode`, `MD_RestrictionCode`,
   `MD_ProgressCode`, `CI_PresentationFormCode`,
   `MD_CharacterSetCode`, `MD_SpatialRepresentationTypeCode`) are
   schema-typed as `string` rather than enum, on the assumption that
   ISO TC 211 may extend the codelists. **Should the schema enumerate
   the current values for stronger validation, accepting that
   updates require a schema bump?**
4. **Field naming.** `iso:lineage_statement` is the longest name;
   shorter alternatives (`iso:lineage`) collide with `processing:lineage`
   semantics. **Comments welcome on naming for clarity.**
5. **Profile separation.** The FAO ISO 19115-1 profile is documented in
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

Title: **Proposal: `iso-to-stac` — STAC extension + ISO 19115 ↔ STAC mapping document**

> **Important — GitHub Flavored Markdown rendering note**
>
> Do not hard-wrap paragraphs or list items below. GitHub renders
> every single newline inside a paragraph or list item as a `<br>`,
> which turns wrapped prose into a broken staircase. Each paragraph
> and list item must be one physical line; the reader's viewport
> handles word-wrap. Blank lines between blocks are still required.

```markdown
Hi all,

FAO is proposing `iso-to-stac` — a pair of artifacts that together let a STAC client read the full ISO 19115-1 metadata of a dataset without leaving STAC:

1. **A STAC extension** (12 `iso:*` fields) — contributed only where no existing community extension covers the ISO concept (lineage statement, `MD_MaintenanceFrequencyCode`, `MD_RestrictionCode`, character-set / spatial-representation / presentation-form codelists, etc.).
2. **A mapping document** — a normative ISO 19115 ↔ STAC crosswalk that maps every ISO 19115-1 field used by a representative producer to its STAC location, preferring an existing community extension wherever it covers the concept. The mapping references the upstream sources (ISO 19115-1 / 19115-2 / 19139, the codelist registry, OGC API - Records, pygeometa, GeoNetwork) and the community extensions it relies on (`processing`, `scientific`, `themes`, `language`, `timestamps`, `datacube`, `raster`, `classification`, `render`, `alternate-assets`, `version`, `contacts`).

**Why both are needed:** a small extension on its own would describe only the leftover fields; a mapping document on its own would document a crosswalk no producer can implement losslessly. Together they cover the whole ISO 19115-1 surface FAO uses in production today.

**Note on the sibling `fao` extension** in the same repo: alongside `iso-to-stac`, we ship an `fao` extension with FAO-specific identifiers (`fao:workspace`, `fao:product_id`, `fao:product_type`, `fao:layer_id`, `fao:item_code`, …). It is intentionally org-scoped and stays a **permanent custom extension — not part of this proposal**. We flag it only because every example in the repo carries both `fao:*` and `iso:*` fields together, so reviewers reading the examples will see them side by side. The pairing also serves as the real-world test bed for `iso-to-stac`: a production org-specific extension consuming the generic ISO mapping. The `iso-to-stac` proposal here is independent of `fao` and works for any ISO 19115 producer.

### Links

- **Repo:** https://github.com/un-fao/fao-stac-extensions
- **Extension:** https://github.com/un-fao/fao-stac-extensions/tree/main/extensions/iso-to-stac
- **Schema (interim URL):** https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/iso-to-stac/json-schema/schema.json
- **Mapping document:** https://github.com/un-fao/fao-stac-extensions/blob/main/extensions/iso-to-stac/mapping/iso19115-2-to-stac.md
- **Reference implementation:** https://github.com/un-fao/fao-stac-extensions/tree/main/reference-implementation
- **Pilot deployment:** https://data.review.fao.org/geospatial/search/stac/
- **Sibling `fao` extension** (not part of this proposal): https://github.com/un-fao/fao-stac-extensions/tree/main/extensions/fao

### Open questions for the community

(Full list in the submission doc in the repo.)

1. Should the mapping document live inside the extension repo (as it does today), or should it be split out as a separate `iso19115-to-stac` mapping spec that the extension references?
2. Drop `iso:lineage_statement` and recommend `processing:lineage` exclusively before v1.0? (The Processing extension explicitly cites NASA's ISO lineage info as its source.)
3. Schema-enumerate the ISO codelist values, or keep them as `string` so ISO TC 211 codelist extensions don't trigger a schema bump?
4. Profile separation — the FAO ISO 19115-1 profile (MANDATORY / Needed / Optional tiers) is documented but not enforced by the schema; is that the right shape, or should profile manifests live in a separate schema family?

Coordination with the OGC Metadata SWG (ISO TC 211 liaison) is running in parallel; coordination note at <https://github.com/un-fao/fao-stac-extensions/blob/main/docs/drafts/ogc-metadata-coordination.md>.

Happy to iterate on naming, scope, and field set before we open a PR to the `stac-extensions/` org.

Thanks,
FAO Agro-Informatics Platform team
```

**Posted as:** <https://github.com/radiantearth/stac-spec/discussions/1384>
(Ideas category). This document is the submission package and is kept
in sync with the live discussion body — update both together.
