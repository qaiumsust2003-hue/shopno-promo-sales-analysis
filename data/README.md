# Data

## Source
**Complete Journey** retail shopping data from 84.51° (originally from the Complete Journey 2.0 source files), packaged as the R package `completejourney` by Brad Boehmke and Steven Mortimer.

- Repository: https://github.com/bradleyboehmke/completejourney
- Original source files: https://www.8451.com/area51
- License: CC0 (stated in the package `DESCRIPTION`)
- Coverage: 2,469 households, one year (2017), 1.47M transaction lines, plus product-store-week promotion placements (display and mailer).

## Why not Shopno data?
Shopno (Shwapno) Superstore does not publish store-level sales or promotion data. This dataset has the same structure a Shopno analysis would need (store, week, sales, promotion exposure, discounts) and is used as a public stand-in. Findings describe this dataset, not Shopno.

## Files
| File | Description |
|------|-------------|
| `prepare_data.py` | Downloads the raw `.rds` tables (gitignored in `data/raw/`) and builds the store-week table |
| `processed/weekly_store_sales.csv` | 7,341 store-week rows used for modelling |

## Columns in `weekly_store_sales.csv`
| Column | Meaning |
|--------|---------|
| `store_id`, `week` | Store and week of 2017 (1 to 53) |
| `sales_value` | Total sales amount in the store-week (target) |
| `n_lines` | Number of transaction lines (a proxy for traffic and store size) |
| `share_on_display` | Share of lines sold for products on an in-store display that week |
| `share_in_mailer` | Share of lines sold for products featured in a mailer that week |
| `discount_rate` | Total discounts divided by list value (sales plus discounts) |
| `coupon_rate` | Coupon discounts divided by list value |

## Reproduce
```bash
pip install pandas pyreadr
python data/prepare_data.py
```
