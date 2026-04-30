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

"""Schema-validation tests for committed examples.

Mirrors the Node-side `stac-node-validator` check in CI but runs in
Python via `jsonschema`. Catches drift between examples and schemas
that would otherwise only be caught by the Node CI job (or worse,
missed entirely until a downstream consumer hits the bad data).

Also asserts that the schema's raster/vector mutual exclusivity rule
is actually enforced on a synthetic counter-example.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXTENSIONS = REPO_ROOT / "extensions"


def _load(path: Path) -> dict:
    with path.open() as fh:
        return json.load(fh)


def _schema_path(extension: str) -> Path:
    return EXTENSIONS / extension / "json-schema" / "schema.json"


def _example_paths(extension: str) -> list[Path]:
    return sorted((EXTENSIONS / extension / "examples").glob("*.json"))


@pytest.mark.parametrize("extension", ["fao", "iso-to-stac"])
def test_schema_is_valid_draft07(extension: str) -> None:
    schema = _load(_schema_path(extension))
    Draft7Validator.check_schema(schema)


@pytest.mark.parametrize(
    "extension,example_path",
    [
        (ext, ex)
        for ext in ("fao", "iso-to-stac")
        for ex in _example_paths(ext)
    ],
    ids=lambda v: v.name if isinstance(v, Path) else v,
)
def test_example_validates_against_schema(extension: str, example_path: Path) -> None:
    schema = _load(_schema_path(extension))
    example = _load(example_path)
    Draft7Validator(schema).validate(example)


def test_fao_raster_vector_mutex_enforced() -> None:
    """A document carrying both raster-only and vector-only fields must fail."""
    schema = _load(_schema_path("fao"))
    base = _load(EXTENSIONS / "fao" / "examples" / "collection.json")

    bad = copy.deepcopy(base)
    # base already has fao:product_type=mapset (raster); inject vector-only fields.
    bad["fao:geometry_type"] = "Polygon"
    bad["fao:feature_count"] = 42

    with pytest.raises(ValidationError):
        Draft7Validator(schema).validate(bad)


def test_fao_vector_only_document_validates() -> None:
    """A document with only vector-only fields (no fao:product_type) must validate."""
    schema = _load(_schema_path("fao"))
    base = _load(EXTENSIONS / "fao" / "examples" / "collection.json")

    vector = copy.deepcopy(base)
    vector.pop("fao:product_type", None)
    vector.pop("gismgr_layer_id", None)
    vector["fao:geometry_type"] = "MultiPolygon"
    vector["fao:feature_count"] = 1234

    Draft7Validator(schema).validate(vector)
