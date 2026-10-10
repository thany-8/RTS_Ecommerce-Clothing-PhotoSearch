# RTS Photo Search

RTS is a clothing e-commerce project with a photo search feature. Users will be able to upload a picture of clothing and find similar products available in our catalog.

## Project Structure

```text
RTS-photo-search/
├── backend/
│   └── prepare_catalog.py
├── data/
│   ├── products.csv
│   └── images/
└── README.md
```

## Getting Started

**1. Clone the repository**

```bash
git clone <repository-url>
cd RTS-photo-search
```

If you already cloned the repository, get the latest changes:

```bash
git pull origin main
```

**2. Check the product catalog**

The repository includes:

- `data/products.csv` — 900 selected clothing products for Women, Men, and Kids.
- `data/images/` — 900 corresponding product images.

Each image is named using its product ID. For example, product `57982` corresponds to `57982.jpg`.

**3. Verify the dataset**

Run these commands from the project root:

```bash
wc -l data/products.csv
find data/images -name "*.jpg" | wc -l
```

Expected results:

- 901 CSV lines (900 products + header)
- 900 images

## Important Notes

- **You do not need to download the original 23 GB Kaggle dataset.** The selected catalog and images are already included in GitHub.
- `backend/prepare_catalog.py` was used to generate the catalog. You do not need to run it for normal setup.
- The product catalog currently contains metadata and images. Prices, stock, and sizes will be added later.
- Photo Search using a pretrained ResNet50 model is the next development step.

## Dataset Source

[Kaggle — Fashion Product Images](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)

Dataset images are used for development and testing. Review the dataset license before redistributing or deploying them publicly.

## Team Workflow

Create a separate Git branch for your work, commit your changes, and open a pull request before merging into `main`.
