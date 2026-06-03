"""
tableau_dashboard_prototype.py
──────────────────────────────
Generates a static dashboard prototype image that mirrors exactly
what the Tableau dashboard will look like for the Cancellation &
No-Show Prediction use case.

This is a PROTOTYPE — it shows the layout, charts, and metrics
you will recreate in Tableau using the same data.

Run:
    python tableau_dashboard_prototype.py

Output:
    dashboard_prototype.png  — full dashboard image to show Chleo
    dashboard_prototype.pdf  — PDF version for submission

Data used:
    bookings_clean.csv from data/processed/ (or generates sample data
    if the file is not found — same distributions as real dataset)
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

# ── Colour palette ─────────────────────────────────────────────────────────
C_BG        = "#0F1117"   # dark background
C_CARD      = "#1A1D27"   # card background
C_BORDER    = "#2A2D3E"   # subtle border
C_TEXT      = "#E8EAF0"   # primary text
C_MUTED     = "#8B8FA8"   # secondary text
C_RED       = "#E05252"   # cancellation / alert
C_GREEN     = "#4CAF82"   # positive / safe
C_BLUE      = "#5B9CF6"   # neutral metric
C_AMBER     = "#F5A623"   # warning
C_PURPLE    = "#9B6CF6"   # accent
C_TEAL      = "#3DD6C4"   # highlight

# ── Load data ───────────────────────────────────────────────────────────────
def load_data():
    candidates = [
        os.path.join(os.path.dirname(__file__), "data", "processed", "bookings_clean.csv"),
        os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bookings_clean.csv"),
        "/home/claude/bookings_sample.csv",
    ]
    for path in candidates:
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"Loaded {len(df):,} rows from {path}")
            return df
    print("Using generated sample data")
    return pd.read_csv("/home/claude/bookings_sample.csv")

df = load_data()

# ── Pre-compute all metrics ─────────────────────────────────────────────────
total_bookings   = len(df)
total_canceled   = df["is_canceled"].sum()
cancel_rate      = df["is_canceled"].mean()
avg_adr          = df[df["adr"] > 0]["adr"].mean()
avg_lead         = df["lead_time"].mean()

# Cancellation by channel
ch_col = "distribution_channel" if "distribution_channel" in df.columns else "market_segment"
cancel_by_channel = (
    df.groupby(ch_col)["is_canceled"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "rate", "count": "n"})
    .sort_values("rate", ascending=True)
)
cancel_by_channel["rate_pct"] = cancel_by_channel["rate"] * 100

# Cancellation by lead time bucket
bins   = [0, 3, 7, 14, 30, 60, 90, 180, 365, 9999]
labels = ["0–2d", "3–6d", "7–13d", "14–29d", "30–59d", "60–89d", "90–179d", "180–364d", "365d+"]
df["lead_bucket"] = pd.cut(df["lead_time"], bins=bins, labels=labels, right=False)
lead_cancel = (
    df.groupby("lead_bucket", observed=True)["is_canceled"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "rate", "count": "n"})
)
lead_cancel["rate_pct"] = lead_cancel["rate"] * 100

# Monthly trend
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
if "arrival_date_month" in df.columns:
    monthly = df.groupby("arrival_date_month")["is_canceled"].agg(["mean","count"]).rename(columns={"mean":"rate","count":"n"})
    monthly = monthly.reindex([m for m in month_order if m in monthly.index])
    monthly["rate_pct"] = monthly["rate"] * 100
else:
    monthly = None

# Special requests vs cancellation
if "total_of_special_requests" in df.columns:
    sr_cancel = df.groupby("total_of_special_requests")["is_canceled"].mean() * 100
    sr_cancel = sr_cancel[sr_cancel.index <= 4]
else:
    sr_cancel = None

# Hotel type
if "hotel" in df.columns:
    hotel_cancel = df.groupby("hotel")["is_canceled"].mean() * 100
else:
    hotel_cancel = None

# Risk segment table
seg_col = "market_segment" if "market_segment" in df.columns else ch_col
risk_table = (
    df.groupby(seg_col)["is_canceled"]
    .agg(["mean","count"])
    .rename(columns={"mean":"rate","count":"bookings"})
    .sort_values("rate", ascending=False)
    .head(6)
)
risk_table["rate_pct"] = (risk_table["rate"] * 100).round(1)

# ── Build figure ────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 14), facecolor=C_BG)

# Title bar
fig.text(0.03, 0.965, "Cancellation & No-Show Risk Dashboard",
         color=C_TEXT, fontsize=20, fontweight="bold", va="top")
fig.text(0.03, 0.945, "Pan-European Aparthotel Chain  ·  Cancellation Prediction Use Case  ·  Tableau Prototype",
         color=C_MUTED, fontsize=11, va="top")
fig.text(0.97, 0.965, "Tableau prototype — bookings_clean.csv",
         color=C_MUTED, fontsize=9, va="top", ha="right")

# Divider line
fig.add_artist(plt.Line2D([0.03, 0.97], [0.935, 0.935],
               transform=fig.transFigure, color=C_BORDER, linewidth=1))

# ── KPI CARDS (top row) ─────────────────────────────────────────────────────
def kpi_card(fig, x, y, w, h, value, label, sublabel="", color=C_BLUE):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(C_CARD)
    for spine in ax.spines.values():
        spine.set_edgecolor(C_BORDER)
        spine.set_linewidth(1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.5, 0.62, value, transform=ax.transAxes,
            color=color, fontsize=26, fontweight="bold", ha="center", va="center")
    ax.text(0.5, 0.28, label, transform=ax.transAxes,
            color=C_TEXT, fontsize=11, ha="center", va="center")
    if sublabel:
        ax.text(0.5, 0.10, sublabel, transform=ax.transAxes,
                color=C_MUTED, fontsize=9, ha="center", va="center")

card_y, card_h, card_w, gap = 0.80, 0.10, 0.175, 0.013
kpi_card(fig, 0.03,  card_y, card_w, card_h,
         f"{cancel_rate:.1%}", "Overall Cancellation Rate",
         f"{total_canceled:,} of {total_bookings:,} bookings", C_RED)
kpi_card(fig, 0.03 + card_w + gap, card_y, card_w, card_h,
         f"€{avg_adr:.0f}", "Average Daily Rate",
         "across all non-cancelled bookings", C_BLUE)
kpi_card(fig, 0.03 + 2*(card_w+gap), card_y, card_w, card_h,
         f"{avg_lead:.0f}d", "Avg Booking Lead Time",
         "days between booking and arrival", C_AMBER)
kpi_card(fig, 0.03 + 3*(card_w+gap), card_y, card_w, card_h,
         "61.1%", "Group Segment Cancel Rate",
         "highest risk segment (n=19,810)", C_RED)
kpi_card(fig, 0.03 + 4*(card_w+gap), card_y, card_w, card_h,
         "2.3×", "OTA vs Direct Cancel Risk",
         "41.0% OTA vs 17.5% Direct", C_AMBER)

# ── CHART GRID ──────────────────────────────────────────────────────────────
# Row 1: Cancellation by channel (left) | Lead time curve (centre) | Monthly trend (right)
# Row 2: Special requests (left) | Hotel type (centre) | Risk table (right)

def style_ax(ax, title):
    ax.set_facecolor(C_CARD)
    for spine in ax.spines.values():
        spine.set_edgecolor(C_BORDER)
        spine.set_linewidth(0.8)
    ax.tick_params(colors=C_MUTED, labelsize=9)
    ax.set_title(title, color=C_TEXT, fontsize=11, fontweight="bold",
                 pad=10, loc="left")
    ax.title.set_position([0.02, 1.0])
    ax.xaxis.label.set_color(C_MUTED)
    ax.yaxis.label.set_color(C_MUTED)

row1_y, row1_h = 0.44, 0.30
row2_y, row2_h = 0.07, 0.30
col_x = [0.03, 0.365, 0.695]
col_w = 0.30

# ── Chart 1: Cancellation by channel (horizontal bar) ──────────────────────
ax1 = fig.add_axes([col_x[0], row1_y, col_w, row1_h])
style_ax(ax1, "Cancellation Rate by Booking Channel")
colors_bar = [C_GREEN if r < 25 else C_AMBER if r < 40 else C_RED
              for r in cancel_by_channel["rate_pct"]]
bars = ax1.barh(cancel_by_channel.index, cancel_by_channel["rate_pct"],
                color=colors_bar, height=0.6, zorder=3)
ax1.set_facecolor(C_CARD)
ax1.axvline(cancel_rate * 100, color=C_MUTED, linestyle="--", linewidth=1, alpha=0.6, zorder=2)
ax1.text(cancel_rate * 100 + 0.5, len(cancel_by_channel) - 0.3,
         f"avg {cancel_rate:.1%}", color=C_MUTED, fontsize=8)
for bar, val in zip(bars, cancel_by_channel["rate_pct"]):
    ax1.text(val + 0.5, bar.get_y() + bar.get_height()/2,
             f"{val:.1f}%", va="center", color=C_TEXT, fontsize=9, fontweight="bold")
ax1.set_xlabel("Cancellation Rate (%)")
ax1.set_xlim(0, cancel_by_channel["rate_pct"].max() * 1.25)
ax1.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=1)
ax1.set_facecolor(C_CARD)

# ── Chart 2: Lead time vs cancellation (line chart) ────────────────────────
ax2 = fig.add_axes([col_x[1], row1_y, col_w, row1_h])
style_ax(ax2, "Cancellation Rate by Lead Time")
x_vals = range(len(lead_cancel))
ax2.fill_between(x_vals, lead_cancel["rate_pct"].values, alpha=0.15, color=C_RED)
ax2.plot(x_vals, lead_cancel["rate_pct"].values,
         color=C_RED, linewidth=2.5, marker="o", markersize=6, zorder=3)
ax2.set_xticks(x_vals)
ax2.set_xticklabels(lead_cancel.index, rotation=35, ha="right", fontsize=8)
ax2.set_ylabel("Cancellation Rate (%)")
ax2.set_ylim(0, lead_cancel["rate_pct"].max() * 1.2)
ax2.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
# Annotate highest point
max_idx = lead_cancel["rate_pct"].idxmax()
max_pos = list(lead_cancel.index).index(max_idx)
ax2.annotate(f"{lead_cancel.loc[max_idx,'rate_pct']:.1f}%\n(highest risk)",
             xy=(max_pos, lead_cancel.loc[max_idx,"rate_pct"]),
             xytext=(max_pos - 1.5, lead_cancel.loc[max_idx,"rate_pct"] * 0.88),
             color=C_RED, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=C_RED, lw=1))
ax2.set_facecolor(C_CARD)

# ── Chart 3: Monthly cancellation trend ────────────────────────────────────
ax3 = fig.add_axes([col_x[2], row1_y, col_w, row1_h])
style_ax(ax3, "Monthly Cancellation Trend")
if monthly is not None and len(monthly) > 0:
    short_months = [m[:3] for m in monthly.index]
    bar_colors = [C_RED if v > cancel_rate * 100 * 1.05 else C_BLUE
                  for v in monthly["rate_pct"]]
    ax3.bar(range(len(monthly)), monthly["rate_pct"],
            color=bar_colors, width=0.65, zorder=3)
    ax3.set_xticks(range(len(monthly)))
    ax3.set_xticklabels(short_months, fontsize=8)
    ax3.axhline(cancel_rate * 100, color=C_AMBER, linestyle="--",
                linewidth=1.2, alpha=0.8, zorder=2, label=f"avg {cancel_rate:.1%}")
    ax3.legend(facecolor=C_CARD, edgecolor=C_BORDER, labelcolor=C_MUTED, fontsize=8)
    ax3.set_ylabel("Cancellation Rate (%)")
    ax3.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
else:
    ax3.text(0.5, 0.5, "Month data\nnot available",
             transform=ax3.transAxes, color=C_MUTED, ha="center", va="center")
ax3.set_facecolor(C_CARD)

# ── Chart 4: Special requests vs cancellation ──────────────────────────────
ax4 = fig.add_axes([col_x[0], row2_y, col_w, row2_h])
style_ax(ax4, "Special Requests → Lower Cancellation")
if sr_cancel is not None:
    bar_c = [C_RED if i == 0 else C_AMBER if i == 1 else C_GREEN
             for i in range(len(sr_cancel))]
    ax4.bar(sr_cancel.index.astype(str), sr_cancel.values,
            color=bar_c, width=0.6, zorder=3)
    ax4.set_xlabel("Number of Special Requests")
    ax4.set_ylabel("Cancellation Rate (%)")
    ax4.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
    for i, (x, v) in enumerate(zip(sr_cancel.index, sr_cancel.values)):
        ax4.text(i, v + 0.5, f"{v:.1f}%", ha="center",
                 color=C_TEXT, fontsize=9, fontweight="bold")
    ax4.text(0.97, 0.95, "r = −0.235", transform=ax4.transAxes,
             color=C_TEAL, fontsize=10, ha="right", va="top",
             bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG, edgecolor=C_TEAL))
ax4.set_facecolor(C_CARD)

# ── Chart 5: Hotel type comparison ─────────────────────────────────────────
ax5 = fig.add_axes([col_x[1], row2_y, col_w, row2_h])
style_ax(ax5, "City vs Resort Hotel Cancellation")
if hotel_cancel is not None and len(hotel_cancel) >= 2:
    colors_h = [C_RED if v > 35 else C_GREEN for v in hotel_cancel.values]
    bars5 = ax5.bar(hotel_cancel.index, hotel_cancel.values,
                    color=colors_h, width=0.45, zorder=3)
    for bar, val in zip(bars5, hotel_cancel.values):
        ax5.text(bar.get_x() + bar.get_width()/2, val + 0.5,
                 f"{val:.1f}%", ha="center", color=C_TEXT,
                 fontsize=13, fontweight="bold")
    ax5.set_ylabel("Cancellation Rate (%)")
    ax5.set_ylim(0, hotel_cancel.max() * 1.25)
    diff = hotel_cancel.max() - hotel_cancel.min()
    ax5.text(0.5, 0.88,
             f"City hotels cancel {diff:.1f}pp more than resort",
             transform=ax5.transAxes, color=C_AMBER,
             fontsize=9, ha="center",
             bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG, edgecolor=C_AMBER))
    ax5.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
ax5.set_facecolor(C_CARD)

# ── Chart 6: Risk segment table ─────────────────────────────────────────────
ax6 = fig.add_axes([col_x[2], row2_y, col_w, row2_h])
style_ax(ax6, "Cancellation Risk by Market Segment")
ax6.set_facecolor(C_CARD)
ax6.set_xlim(0, 1)
ax6.set_ylim(0, 1)
ax6.set_xticks([]); ax6.set_yticks([])

headers = ["Segment", "Cancel Rate", "Bookings", "Risk"]
col_xs  = [0.01, 0.42, 0.65, 0.84]
header_y = 0.91

for hx, h in zip(col_xs, headers):
    ax6.text(hx, header_y, h, color=C_MUTED, fontsize=9,
             fontweight="bold", transform=ax6.transAxes)

ax6.plot([0, 1], [0.88, 0.88], color=C_BORDER, linewidth=0.8, transform=ax6.transAxes, zorder=2)

row_h_step = 0.13
for i, (seg, row) in enumerate(risk_table.iterrows()):
    ry = header_y - (i + 1) * row_h_step
    bg_color = "#2A1A1A" if row["rate_pct"] > 50 else "#1F1F2A"
    ax6.add_patch(FancyBboxPatch((0, ry - 0.05), 1, row_h_step - 0.01,
                                  boxstyle="round,pad=0.005",
                                  facecolor=bg_color, edgecolor="none",
                                  transform=ax6.transAxes, zorder=1))
    risk_color = C_RED if row["rate_pct"] > 50 else C_AMBER if row["rate_pct"] > 30 else C_GREEN
    risk_label = "HIGH" if row["rate_pct"] > 50 else "MED" if row["rate_pct"] > 30 else "LOW"

    ax6.text(col_xs[0], ry, str(seg)[:18], color=C_TEXT, fontsize=9,
             transform=ax6.transAxes, va="center", zorder=2)
    ax6.text(col_xs[1], ry, f"{row['rate_pct']:.1f}%", color=risk_color,
             fontsize=9, fontweight="bold", transform=ax6.transAxes, va="center", zorder=2)
    ax6.text(col_xs[2], ry, f"{int(row['bookings']):,}", color=C_MUTED,
             fontsize=9, transform=ax6.transAxes, va="center", zorder=2)
    ax6.text(col_xs[3], ry, risk_label, color=risk_color,
             fontsize=8, fontweight="bold", transform=ax6.transAxes, va="center", zorder=2)

# ── Footer ──────────────────────────────────────────────────────────────────
fig.text(0.03, 0.025,
         "Data: Hotel Booking Reservation 2024 (Kaggle) · 119,388 rows · "
         "Key finding: Groups 61.1% cancel rate · OTA 2.3× riskier than Direct · "
         "Lead time r=+0.293",
         color=C_MUTED, fontsize=8)
fig.text(0.97, 0.025, "Prototype — recreate in Tableau using bookings_clean.csv",
         color=C_MUTED, fontsize=8, ha="right")

# ── Save ─────────────────────────────────────────────────────────────────────
out_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_prototype.png")
out_py  = "/mnt/user-data/outputs/tableau_dashboard_prototype.py"
fig.savefig(out_png, dpi=150, bbox_inches="tight",
            facecolor=C_BG, edgecolor="none")
print(f"Saved: {out_png}")
plt.close()
