# Contributing

Thanks for considering a contribution to the FAO STAC Extensions
repository.

## Code of Conduct

All interactions in this repository are governed by the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md),
which this project adopts in full. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## How to contribute

1. **Open an issue first** for any non-trivial change so the design can
   be discussed before code is written. Use the templates under
   `.github/ISSUE_TEMPLATE/`.
2. **Fork the repository**, create a feature branch off `main`, make
   your changes there.
3. **Run the local test suites** before opening a PR (see below).
4. **Open a pull request** using the template at
   `.github/pull_request_template.md`.
5. CI will run the same tests on your PR. Address any failures.

## Local test suites

Two test suites run in CI; run both locally before opening a PR.

### Schema + Markdown linting (Node)

Validates JSON Schemas, validates every example against its schema via
`stac-node-validator`, and lints Markdown formatting.

```bash
npm install
npm test
```

### Reference implementation (Python)

Validates schemas via `jsonschema`, validates every example against its
schema in Python, and asserts the schema's mutual-exclusivity rule
catches synthetic counter-examples.

```bash
cd reference-implementation
pip install -e '.[dev]'
pytest
```

## What goes where

- `extensions/<name>/json-schema/schema.json` — normative schema. Do
  not weaken validation rules without an issue + discussion.
- `extensions/<name>/README.md` — field tables and prose.
- `extensions/<name>/examples/*.json` — worked examples; every example
  MUST validate against the extension's schema.
- `extensions/iso-to-stac/mapping/iso19115-2-to-stac.md` — normative
  ISO ↔ STAC crosswalk.
- `reference-implementation/` — Python reference implementation.
- `docs/` — additional documentation (drafts, design notes,
  community-submission packages).

## Releases

Each extension keeps its own versioned `CHANGELOG.md`. The umbrella
repository also has a top-level `CHANGELOG.md` summarising
cross-extension changes. Schema URLs follow the pattern
`https://stac-extensions.github.io/<name>/v<version>/schema.json` after
acceptance into the
[`stac-extensions` GitHub organisation](https://github.com/stac-extensions);
prior to acceptance, schemas are served from the un-fao GitHub Pages
deployment created by `.github/workflows/publish.yaml`.

## Avoiding personal data

Per FAO policy, public commits and PR bodies MUST NOT contain
personally identifiable information beyond the FAO contact line in
the file copyright header. Use FAO group mailboxes (e.g.
`copyright@fao.org`) rather than personal addresses where possible.
