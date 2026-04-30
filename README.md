# FAO STAC Extensions

Umbrella repository for STAC extensions authored and maintained by the
Food and Agriculture Organization of the United Nations (FAO).

## Why this exists

FAO publishes geospatial data through two parallel catalogs:

- **`data.apps.fao.org/catalog`** — a CKAN-backed catalog that exposes
  rich ISO 19115-1 metadata for every dataset (lineage, constraints,
  maintenance frequency, contacts, citation, ISO topic categories…).
- **the FAO geospatial STAC catalog** (in review at
  `data.review.fao.org/geospatial/search/stac/`, prod at
  `data.apps.fao.org/geospatial/search/stac/`) — an OGC API / STAC
  catalog that exposes the same datasets as Collections and Items
  with raster / vector / datacube content.

The two catalogs describe the same datasets but use different metadata
shapes, and historically users had to consult both. The work in this
repository merges the ISO catalog content into the STAC catalog
without information loss, so a single STAC API call returns the full
ISO 19115-1 metadata alongside the geospatial content. Doing the merge
via two community-shareable STAC extensions (rather than ad-hoc
private fields) means other catalogs facing the same merge problem can
adopt the same vocabulary.

Each extension lives under [`extensions/`](extensions/) and follows the
official [STAC extension template](https://github.com/stac-extensions/template)
(README, JSON Schema, examples, CHANGELOG). The umbrella repo also hosts
a Python reference implementation under
[`reference-implementation/`](reference-implementation/) covering all
extensions.

## Extensions

| Extension | Field prefix | Status | Description |
| --- | --- | --- | --- |
| [`fao`](extensions/fao/) | `fao` | Proposal — initial field set (v0.2.0) | FAO platform-specific fields applicable to both raster and vector products published by the FAO Agro-Informatics Platform. |
| [`iso-to-stac`](extensions/iso-to-stac/) | `iso` | Proposal — initial field set (v0.2.0) | Canonical mapping between ISO 19115-2 and STAC, plus the FAO ISO 19115-1 profile. Adds `iso:*` fields only where no existing extension covers the ISO concept. |

## Repository Layout

```
fao-stac-extensions/
├── extensions/
│   ├── fao/                    # The fao extension (template-shaped)
│   └── iso-to-stac/            # The iso-to-stac extension (template-shaped)
├── reference-implementation/   # Pip-installable Python package
├── docs/drafts/                # Submission drafts (community + OGC)
├── README.md
├── CHANGELOG.md
└── LICENSE                     # Apache-2.0
```

## Standardization Pathway

Each extension follows the same lifecycle, mirroring the sibling
[`ogc-dimensions`](https://github.com/ccancellieri/ogc-dimensions) FAO
proposal:

| Phase | Artifact |
| --- | --- |
| Proposal | Schema + README + examples land in this repo |
| Pilot | Live deployment on the FAO Agro-Informatics Platform emits the extension URL |
| Candidate | PR to the `stac-extensions/` org index |
| Stable | After at least one external implementer adopts |

For `iso-to-stac` specifically, coordination with the OGC Metadata SWG
(ISO TC 211 liaison) runs in parallel — there is no existing STAC ↔ ISO
19115 mapping extension, which is the gap this fills.

## Running Tests

The same checks that run in CI can be run locally. You'll need
[Node.js](https://nodejs.org/en/download/) (for the JSON Schema and
Markdown linters) and Python 3.11+ (for the reference implementation).

```bash
# Schema + Markdown linting (both extensions)
npm install
npm test

# Reference implementation
cd reference-implementation
pip install -e .
pytest
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Copyright FAO, Viale delle Terme di Caracalla, 00100 Rome, Italy.
Contact: copyright@fao.org — <http://fao.org/contact-us/terms/en/>.
