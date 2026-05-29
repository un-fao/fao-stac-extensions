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
from jsonschema import Draft7Validator, FormatChecker, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXTENSIONS = REPO_ROOT / "extensions"

# Enforce `format` assertions (e.g. the RFC 3339 `date-time` on iso:* date
# fields). jsonschema only checks date-time when an RFC 3339 backend is
# installed; `rfc3339-validator` is pulled in via the [dev] extra. Without a
# format checker, format keywords are silently ignored.
_FORMAT_CHECKER = FormatChecker()


def _validator(schema: dict) -> Draft7Validator:
    return Draft7Validator(schema, format_checker=_FORMAT_CHECKER)


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
    _validator(schema).validate(example)


def test_fao_raster_vector_mutex_enforced() -> None:
    """A document carrying both raster-only and vector-only fields must fail."""
    schema = _load(_schema_path("fao"))
    base = _load(EXTENSIONS / "fao" / "examples" / "collection.json")

    bad = copy.deepcopy(base)
    # base already has fao:product_type=mapset (raster); inject vector-only fields.
    bad["fao:geometry_type"] = "Polygon"
    bad["fao:feature_count"] = 42

    with pytest.raises(ValidationError):
        _validator(schema).validate(bad)


def test_fao_vector_only_document_validates() -> None:
    """A document with only vector-only fields (no fao:product_type) must validate."""
    schema = _load(_schema_path("fao"))
    base = _load(EXTENSIONS / "fao" / "examples" / "collection.json")

    vector = copy.deepcopy(base)
    vector.pop("fao:product_type", None)
    vector.pop("gismgr_layer_id", None)
    vector["fao:geometry_type"] = "MultiPolygon"
    vector["fao:feature_count"] = 1234

    _validator(schema).validate(vector)


def test_iso_codelist_and_date_typing_enforced() -> None:
    """v0.3.0 tightening (D1/D2): codelist enums and RFC 3339 date-time are
    enforced at Collection top level even when the document also carries
    assets/summaries. Under the v0.2.0 anyOf structure those siblings could
    satisfy a branch on their own, leaving the top-level iso:* fields unchecked
    — so this also guards the allOf restructuring that closed that bypass."""
    schema = _load(_schema_path("iso-to-stac"))
    url = schema["$id"].rstrip("#")

    def collection(**fields: object) -> dict:
        return {
            "type": "Collection",
            "stac_extensions": [url],
            "assets": {},
            "summaries": {},
            **fields,
        }

    validator = _validator(schema)

    # valid codelist value + RFC 3339 date-time pass
    validator.validate(
        collection(
            **{
                "iso:status": "completed",
                "iso:data_creation_date": "2014-01-01T00:00:00Z",
            }
        )
    )

    # bad codelist value is rejected (D2)
    with pytest.raises(ValidationError):
        validator.validate(collection(**{"iso:status": "not-a-progress-code"}))

    # partial / non-RFC-3339 date is rejected (D1)
    with pytest.raises(ValidationError):
        validator.validate(collection(**{"iso:data_creation_date": "2014"}))
