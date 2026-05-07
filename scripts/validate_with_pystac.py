"""Validate every committed example with pystac and emit a per-example report.

Two passes are run:

1. **Scoped pass.** Validates each example against STAC core + the two
   FAO-owned extensions (``fao``, ``iso-to-stac``) only. This is the
   property the FAO release commits to: our schemas are correct and
   every example loads cleanly through pystac. Failures here exit 1.

2. **Full-stack pass.** Validates each example against the full
   ``stac_extensions[]`` stack as committed (including upstream
   community extensions such as ``processing``, ``raster``,
   ``timestamps``, …). Reports per-example OK / FAIL with the
   underlying jsonschema error so reviewers can see which combinations
   work end-to-end and which trip on upstream gaps. Never exits
   non-zero — these are not FAO regressions.

When ``$GITHUB_STEP_SUMMARY`` is set (i.e. running inside GitHub
Actions), a markdown summary table is also appended there so the
per-example status renders directly on the workflow run page instead
of being buried in the job log.

Until the v0.2.0 git tag is pushed to GitHub the
``raw.githubusercontent.com/.../v0.2.0/...`` URLs return 404, so we
override pystac's schema fetcher to read the two FAO schemas from
disk. Once the tag is published, the override has no effect.

Run::

    pip install pystac jsonschema
    python scripts/validate_with_pystac.py
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any
from urllib.request import urlopen

import pystac
from pystac.validation import JsonSchemaSTACValidator, RegisteredValidator
from pystac.validation.schema_uri_map import DefaultSchemaUriMap

logging.getLogger("pystac").setLevel(logging.CRITICAL)

REPO = Path(__file__).resolve().parent.parent
GITHUB_STEP_SUMMARY = os.environ.get("GITHUB_STEP_SUMMARY")

LOCAL_SCHEMAS = {
    "https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/fao/json-schema/schema.json":
        REPO / "extensions/fao/json-schema/schema.json",
    "https://raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/extensions/iso-to-stac/json-schema/schema.json":
        REPO / "extensions/iso-to-stac/json-schema/schema.json",
}
FAO_OWNED_SCHEMA_URIS = frozenset(LOCAL_SCHEMAS)
WALKED_RELS = {"root", "parent", "self", "items", "child"}


class _LocalAwareValidator(JsonSchemaSTACValidator):
    """Map the two FAO schema URIs to local files; everything else hits the network."""

    def _get_schema(self, schema_uri: str) -> dict[str, Any]:  # type: ignore[override]
        if schema_uri in LOCAL_SCHEMAS:
            return json.loads(LOCAL_SCHEMAS[schema_uri].read_text())
        return json.loads(urlopen(schema_uri).read())


RegisteredValidator.set_validator(_LocalAwareValidator(DefaultSchemaUriMap()))

LOADERS = {"Feature": pystac.Item.from_dict, "Collection": pystac.Collection.from_dict}


def _strip_walked_links(payload: dict[str, Any]) -> dict[str, Any]:
    payload["links"] = [
        link for link in payload.get("links", [])
        if link.get("rel") not in WALKED_RELS
    ]
    return payload


def _validate(payload: dict[str, Any]) -> None:
    loader = LOADERS[payload["type"]]
    obj = loader(payload)
    obj.validate()


Result = tuple[Path, bool, str]  # (path, ok, message)


def _run_pass(name: str, scope: str) -> list[Result]:
    print(f"\n=== {name} ===")
    results: list[Result] = []
    for path in sorted(REPO.glob("extensions/*/examples/*.json")):
        payload = json.loads(path.read_text())
        if payload.get("type") not in LOADERS:
            continue
        if scope == "scoped":
            payload["stac_extensions"] = [
                uri for uri in payload.get("stac_extensions", [])
                if uri in FAO_OWNED_SCHEMA_URIS
            ]
        _strip_walked_links(payload)
        rel = path.relative_to(REPO)
        try:
            _validate(payload)
            print(f"OK   {rel}")
            results.append((path, True, ""))
        except Exception as exc:
            first_line = str(exc).splitlines()[0] if str(exc) else exc.__class__.__name__
            print(f"FAIL {rel}: {first_line}")
            results.append((path, False, first_line))
    return results


def _markdown_table(title: str, gating: bool, results: list[Result]) -> str:
    lines = [f"### {title}", ""]
    if gating:
        lines.append("_Gates the build — failures here block CI._")
    else:
        lines.append("_Informational — upstream community-extension gaps surface here, not blocking._")
    lines.extend(["", "| Example | Status | Detail |", "| --- | --- | --- |"])
    for path, ok, msg in results:
        rel = path.relative_to(REPO)
        status = "✅ OK" if ok else "❌ FAIL"
        detail = msg.replace("|", "\\|") if msg else "—"
        lines.append(f"| `{rel}` | {status} | {detail} |")
    n_fail = sum(1 for _, ok, _ in results if not ok)
    n_pass = sum(1 for _, ok, _ in results if ok)
    lines.extend(["", f"**{n_pass} passed, {n_fail} failed.**", ""])
    return "\n".join(lines)


scoped = _run_pass(
    "Scoped pass — STAC core + fao + iso-to-stac only (gates the build)",
    scope="scoped",
)
full = _run_pass(
    "Full-stack pass — every declared extension (informational)",
    scope="full",
)

scoped_fail = sum(1 for _, ok, _ in scoped if not ok)
full_fail = sum(1 for _, ok, _ in full if not ok)

print("\n=== Summary ===")
print(f"Scoped pass:     {scoped_fail} failure(s)")
print(f"Full-stack pass: {full_fail} failure(s) "
      f"(upstream community-extension gaps; not blocking)")

if full_fail:
    print("\nFull-stack failure detail:")
    for path, ok, msg in full:
        if not ok:
            print(f"\n  {path.relative_to(REPO)}:\n    {msg}")

if GITHUB_STEP_SUMMARY:
    summary = "\n".join([
        "## pystac validation report",
        "",
        f"Repo at `{REPO.name}`. Schema URLs pinned to the release tag at "
        "`raw.githubusercontent.com/un-fao/fao-stac-extensions/v0.2.0/...`.",
        "",
        _markdown_table("Scoped pass — FAO-owned schemas", True, scoped),
        _markdown_table("Full-stack pass — every declared extension", False, full),
    ])
    with open(GITHUB_STEP_SUMMARY, "a", encoding="utf-8") as fh:
        fh.write(summary)
        fh.write("\n")

sys.exit(1 if scoped_fail else 0)
