"""Prepare the product catalog for photo search."""
import kagglehub
import pandas as pd
from pathlib import Path

# Download dataset
path = Path(kagglehub.dataset_download(
    "paramaggarwal/fashion-product-images-dataset"
))

print("Dataset location:", path)

# Find the CSV containing product information
csv_files = list(path.rglob("styles.csv"))

if not csv_files:
    raise FileNotFoundError("styles.csv not found")

# Load product metadata
df = pd.read_csv(
    csv_files[0],
    on_bad_lines="skip"
)

print("Number of products:", len(df))
print(df.columns.tolist())
print(df.head())
