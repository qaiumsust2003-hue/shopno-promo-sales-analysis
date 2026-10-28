"""Build the store-week promotion/sales table from the Complete Journey sample data.

Source (full tables): https://github.com/bradleyboehmke/completejourney (CC0), derived from the
84.51 Complete Journey 2.0 files. Run from the repo root:

    pip install pandas pyreadr
    python data/prepare_data.py
"""
import urllib.request
from pathlib import Path

import pandas as pd
import pyreadr

BASE = "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/data/"
RAW = Path("data/raw")
OUT = Path("data/processed/weekly_store_sales.csv")


def fetch(name: str) -> pd.DataFrame:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.rds"
    if not path.exists():
        urllib.request.urlretrieve(BASE + f"{name}.rds", path)
    return next(iter(pyreadr.read_r(str(path)).values()))


tx = fetch("transactions")      # 1.47M line items, 2017
promo = fetch("promotions")     # product x store x week display/mailer placement

# Flag each transaction line with the promotion active for that product/store/week.
promo["on_display"] = (promo["display_location"] != "0").astype("int8")
promo["in_mailer"] = (promo["mailer_location"] != "0").astype("int8")
promo = promo[(promo["on_display"] + promo["in_mailer"]) > 0]  # keep promoted rows only
flags = promo.groupby(["product_id", "store_id", "week"], as_index=False)[["on_display", "in_mailer"]].max()
df = tx.merge(flags, on=["product_id", "store_id", "week"], how="left").fillna({"on_display": 0, "in_mailer": 0})

# Discount columns are positive amounts taken off the list price.
df["disc"] = df["retail_disc"].abs() + df["coupon_disc"].abs() + df["coupon_match_disc"].abs()
df["coupon"] = df["coupon_disc"].abs() + df["coupon_match_disc"].abs()
df["list_value"] = df["sales_value"] + df["disc"]

g = df.groupby(["store_id", "week"])
out = pd.DataFrame({
    "sales_value": g["sales_value"].sum(),
    "n_lines": g.size(),
    "share_on_display": g["on_display"].mean(),
    "share_in_mailer": g["in_mailer"].mean(),
    "discount_rate": g["disc"].sum() / g["list_value"].sum(),
    "coupon_rate": g["coupon"].sum() / g["list_value"].sum(),
}).reset_index()

OUT.parent.mkdir(parents=True, exist_ok=True)
out.to_csv(OUT, index=False)
print(out.shape)
print(out.describe().T.to_string())
