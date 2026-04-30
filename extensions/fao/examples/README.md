# Examples

Worked examples drawn from real FAO STAC collections, with synthetic
`example.org` URLs replacing live production hostnames and storage-bucket
paths. The collection ids and product codes are public STAC metadata and
are kept verbatim.

| File | Collection | `fao:product_type` | What it demonstrates |
| --- | --- | --- | --- |
| [`item.json`](item.json) + [`collection.json`](collection.json) | `ASI-D` | `mapset` | Single-grid global product. Categorical datacube dimensions (`SEASON`, `LCT`), `classification:classes` on the band, `dimension-labels` asset role. The Collection populates every `iso:*` field except `iso:other_constraints`. |
| [`collection-mosaic.json`](collection-mosaic.json) | `L3-QUAL-NDVI-LT.LCE` | `mosaic` | Per-tile slice of a parent MOSAIC. `fao:product_id` carries the `<MAPSTORE>.<TILE>` form (`L3-QUAL-NDVI-LT.LCE`); `fao:layer_id` keeps the parent reference (`WAPOR-3.L3-QUAL-NDVI-LT`). Top-level `proj:epsg` carries the tile's native UTM zone. |
| [`collection-mosaicset.json`](collection-mosaicset.json) | `L3-RSM-D.KOG` | `mosaicset` | Per-tile slice of a MOSAICSET (multi-tile composite organised by tile). Dekadal time dimension; UTM-zone `proj:epsg` at the top level. |
| [`item-mosaicset.json`](item-mosaicset.json) | `L3-RSM-D.KOG` | (item) | A single dekadal Item from the MOSAICSET above. Demonstrates per-tile `proj:code` (`EPSG:32637`) on the Item alongside WGS84 `cube:dimensions` on the parent Collection. |

Per the change report that guided v2 of the FAO STAC payloads, MOSAIC
and MOSAICSET parents are no longer published — only the per-tile child
Collections are. The `mosaic` / `mosaicset` examples above are tile-level
Collections by design.
