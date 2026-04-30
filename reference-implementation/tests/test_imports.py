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

"""Smoke tests: each subpackage imports and exposes its schema URI + prefix."""


def test_root_import():
    import fao_stac_extensions

    assert fao_stac_extensions.__version__


def test_fao_subpackage():
    from fao_stac_extensions import fao

    assert fao.SCHEMA_URI == "https://stac-extensions.github.io/fao/v0.2.0/schema.json"
    assert fao.PREFIX == "fao"


def test_iso_to_stac_subpackage():
    from fao_stac_extensions import iso_to_stac

    assert (
        iso_to_stac.SCHEMA_URI
        == "https://stac-extensions.github.io/iso-to-stac/v0.2.0/schema.json"
    )
    assert iso_to_stac.PREFIX == "iso"
