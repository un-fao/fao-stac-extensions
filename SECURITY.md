# Security Policy

## Scope

This repository contains JSON Schemas, Markdown documentation, and a
small Python reference-implementation skeleton — no production runtime,
no network listeners, no credential handling, no database connections.
The realistic security surface is therefore limited to:

- Malformed or malicious JSON Schemas that could cause downstream
  validators to misbehave.
- Supply-chain risk in the `npm` (`stac-node-validator`, `remark-cli`
  and friends) and `pip` (`jsonschema`, `pytest`) dev-dependencies
  used in CI.
- GitHub Actions workflow vulnerabilities (e.g. command injection via
  untrusted event inputs).

## Reporting a vulnerability

Please report suspected vulnerabilities to **`copyright@fao.org`**
rather than opening a public issue. Include:

- A description of the vulnerability and its impact.
- Reproduction steps or a proof-of-concept where applicable.
- Your assessment of severity.

You can expect an acknowledgement within 5 working days. Coordinated
disclosure is preferred; we will agree a disclosure timeline with the
reporter.

## Scope of supported versions

Only the latest released version of each extension is supported with
security fixes. Older versions remain available at their archived
schema URLs but will not receive patches.
