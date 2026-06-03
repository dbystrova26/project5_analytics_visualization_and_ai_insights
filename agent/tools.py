"""
tools.py — Data analysis tools for the aparthotel AI agent.

Each tool is a plain Python function decorated with @tool so LangChain
can call it. Tools are intentionally simple — they load the processed
dataset, run a calculation, and return a human-readable string.

Run directly to preprocess raw datasets:
    python tools.py --preprocess
"""

import os
import argparse
import pandas as pd
import numpy as np
from langchain.tools import tool


# ── Paths — works whether script is run from project root or agent/ subfolder ─
_HERE = os.path.dirname(os.path.abspath(__file__))
_root_data = os.path.join(_HERE, "data", "raw")
_sub_data  = os.path.join(_HERE, "..", "data", "raw")
DATA_RAW       = os.path.normpath(_root_data if os.path.exists(_root_data) else _sub_data)
DATA_PROCESSED = os.path.normpath(DATA_RAW.replace("raw", "processed"))
BOOKINGS_FILE  = os.path.join(DATA_PROCESSED, "bookings_clean.csv")


def _load_bookings() -> pd.DataFrame:
    """Load the cleaned bookings dataset. Raises FileNotFoundError with helpful message."""
    if not os.path.exists(BOOKINGS_FILE):
        raise FileNotFoundError(
            f"Processed dataset not found at {BOOKINGS_FILE}. "
            "Run: python tools.py --preprocess"
        )
    return pd.read_csv(BOOKINGS_FILE)


# ─────────────────────────────────────────────
# TOOL 1: Cancellation rate by segment
# ─────────────────────────────────────────────
@tool
def cancellation_rate_by_segment(column: str = "market_segment") -> str:
    """
    Calculate cancellation rate broken down by a categorical column.
    Useful columns: 'market_segment', 'distribution_channel', 'hotel'.
    Returns a formatted table with cancellation % per group.
    """
    df = _load_bookings()

    if column not in df.columns:
        available = [c for c in df.columns if df[c].dtype == object]
        return f"Column '{column}' not found. Available categorical columns: {available}"

    result = (
        df.groupby(column)["is_canceled"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "cancellation_rate", "count": "total_bookings"})
        .sort_values("cancellation_rate", ascending=False)
    )
    result["cancellation_rate"] = (result["cancellation_rate"] * 100).round(1)

    lines = [f"Cancellation rate by {column}:", ""]
    for segment, row in result.iterrows():
        lines.append(
            f"  {segment:<30} {row['cancellation_rate']:>5.1f}%  "
            f"(n={int(row['total_bookings']):,})"
        )
    return "\n".join(lines)


# ─────────────────────────────────────────────
# TOOL 2: ADR statistics
# ─────────────────────────────────────────────
@tool
def adr_statistics(group_by: str = "none") -> str:
    """
    Return Average Daily Rate (ADR) summary statistics.
    Optionally group by a column (e.g. 'market_segment', 'hotel', 'arrival_date_month').
    Pass group_by='none' for overall statistics.
    """
    df = _load_bookings()
    df = df[df["adr"] > 0]

    if group_by == "none":
        stats = df["adr"].describe()
        return (
            f"ADR statistics (overall):\n"
            f"  Mean:   €{stats['mean']:.2f}\n"
            f"  Median: €{stats['50%']:.2f}\n"
            f"  Min:    €{stats['min']:.2f}\n"
            f"  Max:    €{stats['max']:.2f}\n"
            f"  Std:    €{stats['std']:.2f}\n"
            f"  Count:  {int(stats['count']):,} bookings"
        )

    if group_by not in df.columns:
        return f"Column '{group_by}' not found."

    result = df.groupby(group_by)["adr"].agg(["mean", "median", "count"]).round(2)
    lines = [f"ADR statistics by {group_by}:", ""]
    for group, row in result.iterrows():
        lines.append(
            f"  {str(group):<30} mean €{row['mean']:>6.2f}  "
            f"median €{row['median']:>6.2f}  n={int(row['count']):,}"
        )
    return "\n".join(lines)


# ─────────────────────────────────────────────
# TOOL 3: Lead time distribution
# ─────────────────────────────────────────────
@tool
def lead_time_analysis(buckets: str = "default") -> str:
    """
    Analyse booking lead time (days between booking and arrival).
    Shows cancellation rate per lead time bucket.
    """
    df = _load_bookings()

    bin_edges  = [0, 3, 7, 14, 30, 60, 90, 365, 9999]
    bin_labels = ["0–2d", "3–6d", "7–13d", "14–29d", "30–59d", "60–89d", "90–364d", "365d+"]

    df["lead_bucket"] = pd.cut(
        df["lead_time"], bins=bin_edges, labels=bin_labels, right=False
    )

    result = (
        df.groupby("lead_bucket", observed=True)["is_canceled"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "cancel_rate", "count": "bookings"})
    )
    result["cancel_rate"] = (result["cancel_rate"] * 100).round(1)

    lines = ["Lead time vs cancellation rate:", "", f"  {'Bucket':<12} {'Cancel %':>9} {'Bookings':>10}"]
    lines.append("  " + "-" * 35)
    for bucket, row in result.iterrows():
        lines.append(
            f"  {str(bucket):<12} {row['cancel_rate']:>8.1f}%  {int(row['bookings']):>9,}"
        )
    return "\n".join(lines)


# ─────────────────────────────────────────────
# TOOL 4: Booking volume trend
# ─────────────────────────────────────────────
@tool
def booking_volume_trend(period: str = "month") -> str:
    """
    Show booking volume over time to identify seasonal patterns.
    period: 'month' or 'week'
    """
    df = _load_bookings()

    if "arrival_date_month" not in df.columns:
        return "Date columns not found. Check preprocessing output."

    group = df.groupby(["arrival_date_year", "arrival_date_month"]).size().reset_index(name="bookings")
    lines = ["Monthly booking volume:", ""]
    for _, row in group.iterrows():
        lines.append(f"  {int(row['arrival_date_year'])} {row['arrival_date_month']:<12}: {int(row['bookings']):,} bookings")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# TOOL 5: Correlation with cancellation
# ─────────────────────────────────────────────
@tool
def correlation_with_cancellation(top_n: int = 5) -> str:
    """
    Calculate correlation of numeric features with the is_canceled flag.
    Returns the top N most correlated features.
    """
    df = _load_bookings()

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != "is_canceled"]

    correlations = df[numeric_cols + ["is_canceled"]].corr()["is_canceled"].drop("is_canceled")
    top = correlations.abs().sort_values(ascending=False).head(top_n)

    lines = [f"Top {top_n} numeric features correlated with cancellation:", ""]
    for feature, _ in top.items():
        direction = "positive" if correlations[feature] > 0 else "negative"
        lines.append(f"  {feature:<35} r={correlations[feature]:>+.3f}  ({direction})")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# PREPROCESSING
# ─────────────────────────────────────────────
def preprocess_datasets():
    """Clean raw datasets and save to data/processed/."""
    os.makedirs(DATA_PROCESSED, exist_ok=True)

    raw_candidates = [
        "hotel_bookings.csv",
        "hotel-booking-reservation.csv",
        "hotel_booking_reservation.csv",
        "H1.csv",
    ]

    df = None
    for fname in raw_candidates:
        path = os.path.join(DATA_RAW, fname)
        if os.path.exists(path):
            print(f"Loading {fname}...")
            df = pd.read_csv(path)
            break

    if df is None:
        print(
            f"No raw booking CSV found in {DATA_RAW}.\n"
            "Please download from: https://www.kaggle.com/datasets/kundanbedmutha/hotel-booking-reservation\n"
            "and save as data/raw/hotel_bookings.csv"
        )
        return

    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns")

    # Drop columns with >40% missing
    df = df.loc[:, df.isnull().mean() < 0.4]

    # Fill common nulls
    for col, fill in [("children", 0), ("country", "Unknown"), ("agent", 0), ("company", 0)]:
        if col in df.columns:
            df[col] = df[col].fillna(fill)

    # Remove impossible ADR values
    if "adr" in df.columns:
        before = len(df)
        df = df[(df["adr"] >= 0) & (df["adr"] < 5000)]
        print(f"Removed {before - len(df)} rows with invalid ADR")

    if "is_canceled" in df.columns:
        df["is_canceled"] = df["is_canceled"].astype(int)

    out_path = os.path.join(DATA_PROCESSED, "bookings_clean.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path} ({len(df):,} rows)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preprocess", action="store_true")
    args = parser.parse_args()
    if args.preprocess:
        preprocess_datasets()
    else:
        print("Usage: python tools.py --preprocess")
