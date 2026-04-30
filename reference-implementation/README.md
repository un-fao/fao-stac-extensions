# fao-stac-extensions (reference implementation)

Python reference implementation for the FAO STAC extensions defined at
the umbrella-repo root. See the [top-level README](https://github.com/un-fao/fao-stac-extensions#readme)
for the full spec layout, standardization pathway, and extension list.

This skeleton package exposes one module per extension with the schema
URI and field-name prefix. Field models, the ISO 19115-2 XML mapper, and
the mapping table land in v0.2.0.

## Install

```bash
pip install -e .[dev]
```

## Run tests

```bash
pytest
```

## License

Apache-2.0.
