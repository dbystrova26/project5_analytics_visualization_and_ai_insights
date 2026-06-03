"""
download_data.py — Download all project datasets from Kaggle.

Downloads three datasets into data/raw/:
  1. Hotel Booking Reservation 2024
  2. Hotel Prices in Europe 2024
  3. Tourism & Hospitality Industry Analysis 2025

Requirements:
  - kaggle package: pip install kaggle
  - Kaggle credentials in .env (KAGGLE_USERNAME + KAGGLE_KEY)
    OR kaggle.json placed at ~/.kaggle/kaggle.json

Run:
  python download_data.py
"""

import os
import zipfile
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Set up Kaggle credentials from .env before importing kaggle ───────────────
kaggle_user = os.getenv("KAGGLE_USERNAME")
kaggle_key = os.getenv("KAGGLE_KEY")

if kaggle_user and kaggle_key:
    os.environ["KAGGLE_USERNAME"] = kaggle_user
    os.environ["KAGGLE_KEY"] = kaggle_key
    print("Kaggle credentials loaded from .env")
else:
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if kaggle_json.exists():
        print(f"Using Kaggle credentials from {kaggle_json}")
    else:
        print(
            "\nNo Kaggle credentials found.\n"
            "Option 1: Add KAGGLE_USERNAME and KAGGLE_KEY to your .env file\n"
            "Option 2: Download kaggle.json from kaggle.com/settings/account\n"
            "          and place it at ~/.kaggle/kaggle.json\n"
        )
        exit(1)

try:
    import kaggle
except ImportError:
    print("kaggle package not installed. Run: pip install kaggle")
    exit(1)

# ── Directories ───────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ── Datasets to download ──────────────────────────────────────────────────────
DATASETS = [
    {
        "id": "kundanbedmutha/hotel-booking-reservation",
        "description": "Hotel Booking Reservation 2024",
        "expected_file": "hotel_bookings.csv",
    },
    {
        "id": "maelysboudier/hotel-prices-in-europe",
        "description": "Hotel Prices in Europe 2024",
        "expected_file": None,  # will rename whatever CSV comes out
    },
    {
        "id": "smithmurphy/tourism-and-hospitality-industry-analysis-dataset",
        "description": "Tourism & Hospitality Industry Analysis 2025",
        "expected_file": None,
    },
]


def download_dataset(dataset_id: str, description: str, expected_file: str | None):
    """Download a Kaggle dataset, unzip it, and place CSVs in data/raw/."""
    print(f"\nDownloading: {description}")
    print(f"  Source: kaggle.com/datasets/{dataset_id}")

    # Download zip into a temp subfolder
    tmp_dir = RAW_DIR / "_tmp_download"
    tmp_dir.mkdir(exist_ok=True)

    try:
        kaggle.api.dataset_download_files(
            dataset_id,
            path=str(tmp_dir),
            unzip=True,
            quiet=False,
        )
    except Exception as e:
        print(f"  ERROR downloading {dataset_id}: {e}")
        return

    # Move all CSVs from tmp to raw/
    csv_files = list(tmp_dir.rglob("*.csv"))
    if not csv_files:
        print(f"  WARNING: No CSV files found after download of {dataset_id}")
        shutil.rmtree(tmp_dir)
        return

    for csv_path in csv_files:
        # Use expected_file name if provided, otherwise keep original name
        if expected_file and len(csv_files) == 1:
            dest = RAW_DIR / expected_file
        else:
            dest = RAW_DIR / csv_path.name

        # Avoid overwriting if already exists
        if dest.exists():
            print(f"  Already exists, skipping: {dest.name}")
        else:
            shutil.move(str(csv_path), str(dest))
            size_mb = dest.stat().st_size / 1_000_000
            print(f"  Saved: {dest.name} ({size_mb:.1f} MB)")

    # Clean up temp dir
    shutil.rmtree(tmp_dir)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("Aparthotel Project — Kaggle Dataset Downloader")
    print("=" * 55)
    print(f"Saving to: {RAW_DIR}\n")

    for ds in DATASETS:
        download_dataset(ds["id"], ds["description"], ds["expected_file"])

    # Summary
    print("\n" + "=" * 55)
    csv_files = list(RAW_DIR.glob("*.csv"))
    if csv_files:
        print(f"Done. {len(csv_files)} CSV file(s) in data/raw/:")
        for f in csv_files:
            size_mb = f.stat().st_size / 1_000_000
            print(f"  {f.name} ({size_mb:.1f} MB)")
        print("\nNext step: python tools.py --preprocess")
    else:
        print("No files downloaded. Check errors above.")
