"""
tools.py — Data analysis tools for the aparthotel AI agent.

Covers all 3 use cases:
  UC1 — Dynamic pricing / revenue optimisation
  UC2 — Cancellation & no-show prediction
  UC3 — Guest communication & upsell

Run to preprocess raw data:
    python tools.py --preprocess
"""

import os
import argparse
import pandas as pd
import numpy as np
from langchain.tools import tool

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_root_data = os.path.join(_HERE, "data", "raw")
_sub_data  = os.path.join(_HERE, "..", "data", "raw")
DATA_RAW       = os.path.normpath(_root_data if os.path.exists(_root_data) else _sub_data)
DATA_PROCESSED = os.path.normpath(DATA_RAW.replace("raw", "processed"))
BOOKINGS_FILE  = os.path.join(DATA_PROCESSED, "bookings_clean.csv")


def _load() -> pd.DataFrame:
    if not os.path.exists(BOOKINGS_FILE):
        raise FileNotFoundError(
            f"Processed dataset not found at {BOOKINGS_FILE}. "
            "Run: python tools.py --preprocess"
        )
    return pd.read_csv(BOOKINGS_FILE)


# ══════════════════════════════════════════════════════════════════════════════
# UC1 — DYNAMIC PRICING TOOLS
# ══════════════════════════════════════════════════════════════════════════════

@tool
def adr_statistics(group_by: str = "none") -> str:
    """
    UC1 — Dynamic Pricing.
    Return Average Daily Rate (ADR) statistics overall or grouped by a column.
    Useful group_by values: 'arrival_date_month', 'market_segment',
    'hotel', 'distribution_channel', 'deposit_type'.
    Pass group_by='none' for overall stats.
    """
    df = _load()
    df = df[df["adr"] > 0]

    if group_by == "none":
        s = df["adr"].describe()
        return (
            f"ADR statistics (overall):\n"
            f"  Mean:   €{s['mean']:.2f}\n"
            f"  Median: €{s['50%']:.2f}\n"
            f"  Min:    €{s['min']:.2f}\n"
            f"  Max:    €{s['max']:.2f}\n"
            f"  Std:    €{s['std']:.2f}\n"
            f"  Count:  {int(s['count']):,} bookings"
        )

    if group_by not in df.columns:
        return f"Column '{group_by}' not found."

    result = df.groupby(group_by)["adr"].agg(["mean", "median", "count"]).round(2)
    lines = [f"ADR by {group_by}:", ""]
    for grp, row in result.iterrows():
        lines.append(
            f"  {str(grp):<30} mean €{row['mean']:>7.2f}  "
            f"median €{row['median']:>7.2f}  n={int(row['count']):,}"
        )
    return "\n".join(lines)


@tool
def seasonal_pricing_analysis() -> str:
    """
    UC1 — Dynamic Pricing.
    Compare ADR and booking volume by month to identify underpriced peak periods.
    Reveals months where high demand is not matched by higher rates.
    """
    df = _load()
    df = df[df["adr"] > 0]

    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]

    result = df.groupby("arrival_date_month").agg(
        bookings=("is_canceled", "count"),
        cancel_rate=("is_canceled", "mean"),
        mean_adr=("adr", "mean"),
        median_adr=("adr", "median"),
    ).reindex([m for m in month_order if m in df["arrival_date_month"].unique()])
    result["mean_adr"] = result["mean_adr"].round(2)
    result["cancel_rate"] = (result["cancel_rate"] * 100).round(1)

    lines = ["Seasonal analysis — bookings, ADR, cancellation rate by month:", "",
             f"  {'Month':<12} {'Bookings':>9} {'Cancel%':>8} {'Mean ADR':>10} {'Median ADR':>11}",
             "  " + "-"*54]
    for month, row in result.iterrows():
        lines.append(
            f"  {month:<12} {int(row['bookings']):>9,} {row['cancel_rate']:>7.1f}%"
            f" €{row['mean_adr']:>8.2f}  €{row['median_adr']:>8.2f}"
        )
    return "\n".join(lines)


@tool
def weekend_vs_weekday_adr() -> str:
    """
    UC1 — Dynamic Pricing.
    Compare ADR for weekend stays vs weekday stays.
    Identifies if weekend pricing premium exists or is being left on the table.
    """
    df = _load()
    df = df[df["adr"] > 0]
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df = df[df["total_nights"] > 0]
    df["is_weekend_heavy"] = df["stays_in_weekend_nights"] > df["stays_in_week_nights"]

    result = df.groupby("is_weekend_heavy").agg(
        mean_adr=("adr", "mean"),
        median_adr=("adr", "median"),
        bookings=("adr", "count"),
        cancel_rate=("is_canceled", "mean"),
    ).round(2)

    lines = ["Weekend-heavy vs weekday-heavy stays:", ""]
    labels = {True: "Weekend-heavy stays", False: "Weekday-heavy stays"}
    for key, row in result.iterrows():
        lines.append(f"  {labels[key]}:")
        lines.append(f"    Mean ADR:      €{row['mean_adr']:.2f}")
        lines.append(f"    Median ADR:    €{row['median_adr']:.2f}")
        lines.append(f"    Bookings:      {int(row['bookings']):,}")
        lines.append(f"    Cancel rate:   {row['cancel_rate']*100:.1f}%")
        lines.append("")
    return "\n".join(lines)


@tool
def stay_length_adr_analysis() -> str:
    """
    UC1 — Dynamic Pricing.
    Analyse how ADR varies by length of stay (1 night, 2-3 nights, 4-7 nights, 7+).
    Identifies whether longer stays are priced with appropriate discounts or premiums.
    """
    df = _load()
    df = df[df["adr"] > 0]
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df = df[df["total_nights"] > 0]

    bins   = [0, 1, 3, 7, 14, 999]
    labels = ["1 night", "2-3 nights", "4-7 nights", "8-14 nights", "15+ nights"]
    df["stay_bucket"] = pd.cut(df["total_nights"], bins=bins, labels=labels)

    result = df.groupby("stay_bucket", observed=True).agg(
        mean_adr=("adr", "mean"),
        bookings=("adr", "count"),
        cancel_rate=("is_canceled", "mean"),
    ).round(2)

    lines = ["ADR by length of stay:", "",
             f"  {'Stay length':<14} {'Mean ADR':>10} {'Bookings':>10} {'Cancel%':>8}",
             "  " + "-"*46]
    for bucket, row in result.iterrows():
        lines.append(
            f"  {str(bucket):<14} €{row['mean_adr']:>8.2f}"
            f" {int(row['bookings']):>10,} {row['cancel_rate']*100:>7.1f}%"
        )
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# UC2 — CANCELLATION PREDICTION TOOLS
# ══════════════════════════════════════════════════════════════════════════════

@tool
def cancellation_rate_by_segment(column: str = "market_segment") -> str:
    """
    UC2 — Cancellation Prediction.
    Cancellation rate grouped by a categorical column.
    Useful columns: 'market_segment', 'distribution_channel', 'hotel',
    'deposit_type', 'customer_type', 'meal'.
    """
    df = _load()

    if column not in df.columns:
        available = [c for c in df.columns if df[c].dtype == object]
        return f"Column '{column}' not found. Available: {available}"

    result = (
        df.groupby(column)["is_canceled"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "rate", "count": "n"})
        .sort_values("rate", ascending=False)
    )
    result["rate_pct"] = (result["rate"] * 100).round(1)

    lines = [f"Cancellation rate by {column}:", ""]
    for seg, row in result.iterrows():
        lines.append(
            f"  {str(seg):<35} {row['rate_pct']:>5.1f}%  (n={int(row['n']):,})"
        )
    return "\n".join(lines)


@tool
def lead_time_analysis() -> str:
    """
    UC2 — Cancellation Prediction.
    Cancellation rate per lead time bucket (0-2d through 365d+).
    Lead time is the single strongest numeric predictor of cancellation.
    """
    df = _load()

    bins   = [0, 3, 7, 14, 30, 60, 90, 365, 9999]
    labels = ["0-2d","3-6d","7-13d","14-29d","30-59d","60-89d","90-364d","365d+"]
    df["lead_bucket"] = pd.cut(df["lead_time"], bins=bins, labels=labels, right=False)

    result = (
        df.groupby("lead_bucket", observed=True)["is_canceled"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "rate", "count": "n"})
    )
    result["rate_pct"] = (result["rate"] * 100).round(1)

    lines = ["Lead time vs cancellation rate:", "",
             f"  {'Bucket':<12} {'Cancel%':>9} {'Bookings':>10}",
             "  " + "-"*35]
    for bucket, row in result.iterrows():
        lines.append(
            f"  {str(bucket):<12} {row['rate_pct']:>8.1f}%  {int(row['n']):>9,}"
        )
    return "\n".join(lines)


@tool
def correlation_with_cancellation(top_n: int = 8) -> str:
    """
    UC2 — Cancellation Prediction.
    Pearson correlation of all numeric features with is_canceled.
    Returns top N features — shows what drives cancellation risk.
    """
    df = _load()

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != "is_canceled"]

    corr = df[numeric_cols + ["is_canceled"]].corr()["is_canceled"].drop("is_canceled")
    top  = corr.abs().sort_values(ascending=False).head(top_n)

    lines = [f"Top {top_n} features correlated with cancellation:", ""]
    for feat in top.index:
        direction = "positive ↑" if corr[feat] > 0 else "negative ↓"
        lines.append(
            f"  {feat:<40} r={corr[feat]:>+.3f}  ({direction})"
        )
    return "\n".join(lines)


@tool
def deposit_type_cancellation() -> str:
    """
    UC2 — Cancellation Prediction.
    Cancellation rate by deposit type (No Deposit, Non Refund, Refundable).
    Deposit type is a strong signal — non-refundable deposits dramatically
    reduce cancellation risk.
    """
    df = _load()

    result = (
        df.groupby("deposit_type")["is_canceled"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "rate", "count": "n"})
        .sort_values("rate", ascending=False)
    )

    lines = ["Cancellation rate by deposit type:", ""]
    for dep, row in result.iterrows():
        lines.append(
            f"  {str(dep):<20} {row['rate']*100:>5.1f}%  (n={int(row['n']):,})"
        )
    lines.append("")
    lines.append("Insight: Non-refundable deposits almost eliminate cancellations.")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# UC3 — GUEST COMMUNICATION & UPSELL TOOLS
# ══════════════════════════════════════════════════════════════════════════════

@tool
def upsell_opportunity_analysis() -> str:
    """
    UC3 — Guest Communication & Upsell.
    Identifies upsell opportunities:
    - Room upgrade gap (reserved vs assigned room type mismatch)
    - Meal plan upgrade potential (guests on no-meal or B&B plans)
    - Parking upsell (guests with 0 parking spaces requested)
    - Extended stay potential (1-night stays that could be extended)
    """
    df = _load()

    lines = ["Upsell opportunity analysis:", ""]

    # Room upgrade gap
    if "reserved_room_type" in df.columns and "assigned_room_type" in df.columns:
        df["room_upgrade"] = df["reserved_room_type"] != df["assigned_room_type"]
        upgrade_rate = df["room_upgrade"].mean()
        lines.append(f"  Room type changed at check-in: {upgrade_rate:.1%} of bookings")
        lines.append(f"  → Proactive upgrade offer opportunity before arrival")
        lines.append("")

    # Meal plan distribution
    if "meal" in df.columns:
        meal_dist = df["meal"].value_counts(normalize=True) * 100
        lines.append("  Meal plan distribution:")
        for meal, pct in meal_dist.items():
            upsell = " ← upsell to HB/FB" if meal in ["SC", "BB"] else ""
            lines.append(f"    {str(meal):<6} {pct:>5.1f}%{upsell}")
        lines.append("")

    # Parking upsell
    if "required_car_parking_spaces" in df.columns:
        no_parking = (df["required_car_parking_spaces"] == 0).mean()
        lines.append(f"  Guests with no parking booked: {no_parking:.1%}")
        lines.append(f"  → Pre-arrival parking upsell potential")
        lines.append("")

    # Extended stay potential
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    one_night = (df["total_nights"] == 1).mean()
    lines.append(f"  1-night stays: {one_night:.1%} of all bookings")
    lines.append(f"  → Extend-your-stay offer opportunity at check-in")

    return "\n".join(lines)


@tool
def repeat_guest_analysis() -> str:
    """
    UC3 — Guest Communication & Upsell.
    Analyses repeat guest behaviour vs first-time guests.
    Repeat guests cancel less and are better targets for loyalty offers.
    """
    df = _load()

    if "is_repeated_guest" not in df.columns:
        return "is_repeated_guest column not found."

    result = df.groupby("is_repeated_guest").agg(
        bookings=("is_canceled", "count"),
        cancel_rate=("is_canceled", "mean"),
        mean_adr=("adr", "mean"),
        mean_special_requests=("total_of_special_requests", "mean"),
    ).round(3)

    lines = ["Repeat vs first-time guest analysis:", ""]
    labels = {0: "First-time guests", 1: "Repeat guests"}
    for key, row in result.iterrows():
        lines.append(f"  {labels.get(key, key)}:")
        lines.append(f"    Bookings:         {int(row['bookings']):,}")
        lines.append(f"    Cancel rate:      {row['cancel_rate']*100:.1f}%")
        lines.append(f"    Mean ADR:         €{row['mean_adr']:.2f}")
        lines.append(f"    Avg special reqs: {row['mean_special_requests']:.2f}")
        lines.append("")
    return "\n".join(lines)


@tool
def guest_origin_analysis(top_n: int = 10) -> str:
    """
    UC3 — Guest Communication & Upsell.
    Top guest origin countries by booking volume and cancellation rate.
    Informs language personalisation and targeted marketing for the
    guest communication agent.
    """
    df = _load()

    if "country" not in df.columns:
        return "country column not found."

    result = (
        df.groupby("country").agg(
            bookings=("is_canceled", "count"),
            cancel_rate=("is_canceled", "mean"),
            mean_adr=("adr", "mean"),
        )
        .sort_values("bookings", ascending=False)
        .head(top_n)
    )
    result["cancel_rate"] = (result["cancel_rate"] * 100).round(1)
    result["mean_adr"] = result["mean_adr"].round(2)

    lines = [f"Top {top_n} guest origin countries:", "",
             f"  {'Country':<8} {'Bookings':>10} {'Cancel%':>8} {'Mean ADR':>10}",
             "  " + "-"*40]
    for country, row in result.iterrows():
        lines.append(
            f"  {str(country):<8} {int(row['bookings']):>10,}"
            f" {row['cancel_rate']:>7.1f}%  €{row['mean_adr']:>7.2f}"
        )
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# PREPROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def preprocess_datasets():
    """Clean raw datasets and save to data/processed/."""
    os.makedirs(DATA_PROCESSED, exist_ok=True)

    candidates = [
        "hotel_bookings.csv",
        "hotel-booking-reservation.csv",
        "hotel_booking_reservation.csv",
    ]

    df = None
    for fname in candidates:
        path = os.path.join(DATA_RAW, fname)
        if os.path.exists(path):
            print(f"Loading {fname}...")
            df = pd.read_csv(path)
            break

    if df is None:
        print(f"No raw booking CSV found in {DATA_RAW}.")
        return

    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns")

    # Drop high-missing columns
    df = df.loc[:, df.isnull().mean() < 0.4]

    # Fill nulls
    for col, fill in [("children", 0), ("country", "Unknown"),
                       ("agent", 0), ("company", 0)]:
        if col in df.columns:
            df[col] = df[col].fillna(fill)

    # Remove invalid ADR
    if "adr" in df.columns:
        before = len(df)
        df = df[(df["adr"] >= 0) & (df["adr"] < 5000)]
        print(f"Removed {before - len(df)} rows with invalid ADR")

    # Add derived columns useful for all 3 use cases
    if "stays_in_weekend_nights" in df.columns and "stays_in_week_nights" in df.columns:
        df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]

    if "is_canceled" in df.columns:
        df["is_canceled"] = df["is_canceled"].astype(int)

    out = os.path.join(DATA_PROCESSED, "bookings_clean.csv")
    df.to_csv(out, index=False)
    print(f"Saved: {out} ({len(df):,} rows)")
    print(f"Columns: {df.columns.tolist()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preprocess", action="store_true")
    args = parser.parse_args()
    if args.preprocess:
        preprocess_datasets()
    else:
        print("Usage: python tools.py --preprocess")
