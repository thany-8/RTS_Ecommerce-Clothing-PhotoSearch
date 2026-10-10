"""Prepare the product catalog for photo search."""
import kagglehub
import pandas as pd
from pathlib import Path
import shutil

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


################################################################
#                                                              #
#      Check how many clothing products are available          #
#                                                              #     
################################################################


# Keep only apparel products
clothing = df[df["masterCategory"] == "Apparel"].copy()

print("\nTotal apparel products:", len(clothing))

# Check gender distribution
print("\nProducts by gender:")
print(clothing["gender"].value_counts())

# Check clothing types
print("\nClothing types:")
print(clothing["articleType"].value_counts())


################################################################
#                                                              #
#            Let's select 900 RTS products                     #
#                                                              #
#       Women = 350.     Men = 350.    Kid = 200               #
#                                                              #     
################################################################


# Clothing categories RTS will sell
allowed_types = [
    "Tshirts", "Shirts", "Tops", "Jeans",
    "Shorts", "Trousers", "Dresses",
    "Jackets", "Sweatshirts", "Sweaters",
    "Skirts", "Leggings", "Track Pants",
    "Kurtas", "Kurtis", "Tunics"
]

# Filter to selected clothing types
clothing = df[
    (df["masterCategory"] == "Apparel") &
    (df["articleType"].isin(allowed_types))
].copy()

# Find actual image files in the downloaded dataset
image_paths = {
    int(p.stem): p
    for p in Path(path).rglob("*.jpg")
    if p.stem.isdigit()
}

# Keep only products with an image
clothing = clothing[
    clothing["id"].isin(image_paths)
].copy()

# Select products for each section
women = clothing[clothing["gender"] == "Women"].sample(
    n=350, random_state=42
)

men = clothing[clothing["gender"] == "Men"].sample(
    n=350, random_state=42
)

kids = clothing[
    clothing["gender"].isin(["Boys", "Girls"])
].sample(
    n=200, random_state=42
)

# Combine into one catalog
catalog = pd.concat([women, men, kids])

# Add RTS store categories
catalog["storeCategory"] = catalog["gender"].replace({
    "Boys": "Kids",
    "Girls": "Kids"
})

################################################################
#                                                              #
#      The output from  PRODUCTS.CSV                           #
#                                                              #     
################################################################

# Get the root of the RTS project
project_root = Path(__file__).resolve().parent.parent

# Point to the data folder
output_dir = project_root / "data"
output_dir.mkdir(parents=True, exist_ok=True)

# Save the catalog
output_file = output_dir / "products.csv"

catalog.to_csv(output_file, index=False)

print("RTS catalog saved to:", output_file)
print("Total products:", len(catalog))
print(catalog.head())

print("\nProducts by category:")
print(catalog["storeCategory"].value_counts())




# Folder for RTS product images
images_dir = project_root / "data" / "images"
images_dir.mkdir(parents=True, exist_ok=True)

# Copy only the selected catalog images
for product_id in catalog["id"]:
    source = image_paths[int(product_id)] # Get the source image path for the current product ID
    destination = images_dir / f"{product_id}.jpg"

    shutil.copy2(source, destination)  # Copy the image to the destination folder

# Add an image URL for each product
catalog["image_url"] = catalog["id"].apply(
    lambda product_id: f"/images/{product_id}.jpg"
)

# Save the updated catalog
catalog.to_csv(output_file, index=False)

print("Total products:", len(catalog))
print("Images copied:", len(list(images_dir.glob("*.jpg"))))
print(catalog[["id", "productDisplayName", "image_url"]].head())

