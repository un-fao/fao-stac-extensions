#    Copyright 2025 FAO
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Author: Carlo Cancellieri (ccancellieri@gmail.com)
#    Company: FAO, Viale delle Terme di Caracalla, 00100 Rome, Italy
#    Contact: copyright@fao.org - http://fao.org/contact-us/terms/en/

"""End-to-end pystac validation of every committed example.

Loads each example with pystac (``Item.from_dict`` /
``Collection.from_dict``) and runs ``obj.validate()`` against STAC core +
the two FAO-owned extensions (``fao`` and ``iso-to-stac``). Demonstrates
that the URL-pinned schemas this repository ships with are loadable and
validate cleanly through a real STAC client.

The example documents declare a wider extension stack
(``processing``, ``raster``, ``timestamps``, ``datacube``, …) so users
can see the FAO ISO 19115-1 profile end-to-end. Some of those upstream
schemas have known gaps at Collection level (e.g. ``processing``
v1.2.0 only defines an Item branch); those are pre-existing community
issues, not ours, and visible in ``stac-node-validator`` output too.
The pystac test below filters ``stac_extensions[]`` down to just
``fao`` and ``iso-to-stac`` so it asserts the property in scope: our
schemas validate cleanly via pystac. The full Node-side
``stac-node-validator`` run still validates against every declared
extension.

Until the v0.3.0 git tag is pushed to GitHub, the
``raw.githubusercontent.com/.../v0.3.0/...`` URLs return 404, so we
override pystac's schema fetcher to read the two FAO schemas from
disk. Once the tag is published, the override has no effect.

The example documents carry placeholder ``rel=root`` / ``rel=parent``
links pointing at ``https://example.org/``; those are stripped before
loading so pystac does not try to walk them — schema validation only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen

import pytest

pystac = pytest.importorskip("pystac")
from pystac.validation import JsonSchemaSTACValidator, RegisteredValidator
from pystac.validation.schema_uri_map import DefaultSchemaUriMap

from fao_stac_extensions import fao, iso_to_stac

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXTENSIONS = REPO_ROOT / "extensions"

LOCAL_SCHEMAS = {
    fao.SCHEMA_URI: EXTENSIONS / "fao" / "json-schema" / "schema.json",
    iso_to_stac.SCHEMA_URI: EXTENSIONS / "iso-to-stac" / "json-schema" / "schema.json",
}

WALKED_RELS = {"root", "parent", "self", "items", "child"}


class _LocalAwareValidator(JsonSchemaSTACValidator):
    """Maps the two FAO schema URIs to local files; everything else hits the network."""

    def _get_schema(self, schema_uri: str) -> dict[str, Any]:  # type: ignore[override]
        if schema_uri in LOCAL_SCHEMAS:
            return json.loads(LOCAL_SCHEMAS[schema_uri].read_text())
        return json.loads(urlopen(schema_uri).read())


@pytest.fixture(autouse=True)
def _install_local_aware_validator():
    previous = RegisteredValidator.get_validator()
    RegisteredValidator.set_validator(_LocalAwareValidator(DefaultSchemaUriMap()))
    try:
        yield
    finally:
        RegisteredValidator.set_validator(previous)


_LOADERS = {"Feature": pystac.Item.from_dict, "Collection": pystac.Collection.from_dict}


def _example_paths() -> list[Path]:
    return sorted(EXTENSIONS.glob("*/examples/*.json"))


FAO_OWNED_SCHEMA_URIS = frozenset(LOCAL_SCHEMAS)


@pytest.mark.parametrize("example_path", _example_paths(), ids=lambda p: p.name)
def test_pystac_loads_and_validates(example_path: Path) -> None:
    payload = json.loads(example_path.read_text())
    loader = _LOADERS.get(payload.get("type"))
    if loader is None:
        pytest.skip(f"Unsupported STAC type for pystac: {payload.get('type')!r}")

    payload["stac_extensions"] = [
        uri for uri in payload.get("stac_extensions", [])
        if uri in FAO_OWNED_SCHEMA_URIS
    ]
    payload["links"] = [
        link for link in payload.get("links", [])
        if link.get("rel") not in WALKED_RELS
    ]

    obj = loader(payload)
    obj.validate()
