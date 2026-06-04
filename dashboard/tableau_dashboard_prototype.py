"""
tableau_dashboard_prototype.py
──────────────────────────────
3-page dashboard prototype covering all 3 use cases.

Page 1 — UC1: Dynamic Pricing & Revenue
Page 2 — UC2: Cancellation Prediction (existing)
Page 3 — UC3: Guest Communication & Upsell

Run:
    python tableau_dashboard_prototype.py

Output:
    dashboard_uc1_pricing.png
    dashboard_uc2_cancellation.png
    dashboard_uc3_upsell.png
"""

import os, warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ── Colours ───────────────────────────────────────────────────────────────────
C_BG     = "#0F1117"
C_CARD   = "#1A1D27"
C_BORDER = "#2A2D3E"
C_TEXT   = "#E8EAF0"
C_MUTED  = "#8B8FA8"
C_RED    = "#E05252"
C_GREEN  = "#4CAF82"
C_BLUE   = "#5B9CF6"
C_AMBER  = "#F5A623"
C_PURPLE = "#9B6CF6"
C_TEAL   = "#3DD6C4"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Load data ─────────────────────────────────────────────────────────────────
def load_data():
    candidates = [
        "/home/claude/data/processed/bookings_clean.csv",
        os.path.join(os.path.dirname(__file__), "data", "processed", "bookings_clean.csv"),
        os.path.join(os.path.dirname(__file__), "..", "data", "processed", "bookings_clean.csv"),
    ]
    for p in candidates:
        if os.path.exists(p):
            df = pd.read_csv(p)
            print(f"Loaded {len(df):,} rows from {p}")
            return df
    raise FileNotFoundError("bookings_clean.csv not found. Run: python tools.py --preprocess")

df = load_data()
df = df[df["adr"] > 0].copy()
df["total_nights"] = df.get("stays_in_weekend_nights", 0) + df.get("stays_in_week_nights", 0)

# ── Helpers ───────────────────────────────────────────────────────────────────
def new_fig(title, subtitle):
    fig = plt.figure(figsize=(22, 14), facecolor=C_BG)
    fig.text(0.03, 0.965, title, color=C_TEXT, fontsize=20, fontweight="bold", va="top")
    fig.text(0.03, 0.945, subtitle, color=C_MUTED, fontsize=11, va="top")
    fig.add_artist(plt.Line2D([0.03,0.97],[0.935,0.935],
                   transform=fig.transFigure, color=C_BORDER, linewidth=1))
    return fig

def kpi(fig, x, y, w, h, val, label, sub="", color=C_BLUE):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(C_CARD)
    for s in ax.spines.values():
        s.set_edgecolor(C_BORDER); s.set_linewidth(1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.5, 0.62, val, transform=ax.transAxes,
            color=color, fontsize=26, fontweight="bold", ha="center", va="center")
    ax.text(0.5, 0.28, label, transform=ax.transAxes,
            color=C_TEXT, fontsize=11, ha="center", va="center")
    if sub:
        ax.text(0.5, 0.10, sub, transform=ax.transAxes,
                color=C_MUTED, fontsize=9, ha="center", va="center")

def style(ax, title):
    ax.set_facecolor(C_CARD)
    for s in ax.spines.values():
        s.set_edgecolor(C_BORDER); s.set_linewidth(0.8)
    ax.tick_params(colors=C_MUTED, labelsize=9)
    ax.set_title(title, color=C_TEXT, fontsize=11, fontweight="bold", pad=10, loc="left")
    ax.title.set_position([0.02, 1.0])
    ax.xaxis.label.set_color(C_MUTED)
    ax.yaxis.label.set_color(C_MUTED)

def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=C_BG, edgecolor="none")
    print(f"Saved: {path}")
    plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — UC1: Dynamic Pricing
# ══════════════════════════════════════════════════════════════════════════════
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
monthly = df.groupby("arrival_date_month").agg(
    bookings=("adr","count"), mean_adr=("adr","mean"), cancel_rate=("is_canceled","mean")
).reindex([m for m in month_order if m in df["arrival_date_month"].unique()])

overall_adr = df["adr"].mean()
max_adr_month = monthly["mean_adr"].idxmax()
min_adr_month = monthly["mean_adr"].idxmin()
adr_gap = monthly["mean_adr"].max() - monthly["mean_adr"].min()

bins_st   = [0,1,3,7,14,999]
labs_st   = ["1 night","2-3 nights","4-7 nights","8-14 nights","15+ nights"]
df["stay_bucket"] = pd.cut(df["total_nights"], bins=bins_st, labels=labs_st)
stay_adr = df.groupby("stay_bucket", observed=True)["adr"].mean()

seg_adr = df.groupby("market_segment")["adr"].mean().sort_values(ascending=True)

fig1 = new_fig("Dynamic Pricing & Revenue Intelligence",
               "UC1 — Revenue Optimisation · Pan-European Aparthotel Chain")

cw, cy, ch, gap = 0.175, 0.80, 0.10, 0.013
kpi(fig1, 0.03,              cy, cw, ch, f"€{overall_adr:.0f}", "Overall Mean ADR", "all non-cancelled bookings", C_BLUE)
kpi(fig1, 0.03+cw+gap,       cy, cw, ch, f"€{monthly['mean_adr'].max():.0f}", f"Peak ADR ({max_adr_month[:3]})", "highest monthly average", C_GREEN)
kpi(fig1, 0.03+2*(cw+gap),   cy, cw, ch, f"€{monthly['mean_adr'].min():.0f}", f"Low ADR ({min_adr_month[:3]})", "lowest monthly average", C_AMBER)
kpi(fig1, 0.03+3*(cw+gap),   cy, cw, ch, f"€{adr_gap:.0f}", "Peak-to-Low ADR Gap", "pricing opportunity window", C_RED)
kpi(fig1, 0.03+4*(cw+gap),   cy, cw, ch,
    f"{(monthly['bookings'].max()-monthly['bookings'].min())/monthly['bookings'].min():.0%}",
    "Volume Swing Peak vs Low", "demand variation across year", C_PURPLE)

r1y, r1h = 0.44, 0.30
r2y, r2h = 0.07, 0.30
cx = [0.03, 0.365, 0.695]
cw2 = 0.30

# Chart 1 — ADR by month (bar)
ax = fig1.add_axes([cx[0], r1y, cw2, r1h])
style(ax, "Mean ADR by Month — Seasonality")
colors = [C_GREEN if v > overall_adr*1.05 else C_AMBER if v < overall_adr*0.95 else C_BLUE
          for v in monthly["mean_adr"]]
ax.bar(range(len(monthly)), monthly["mean_adr"], color=colors, width=0.65, zorder=3)
ax.axhline(overall_adr, color=C_MUTED, linestyle="--", linewidth=1, alpha=0.7, zorder=2)
ax.set_xticks(range(len(monthly)))
ax.set_xticklabels([m[:3] for m in monthly.index], fontsize=8)
ax.set_ylabel("Mean ADR (€)")
ax.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
ax.text(len(monthly)-1, overall_adr+1, f"avg €{overall_adr:.0f}",
        color=C_MUTED, fontsize=8, ha="right")

# Chart 2 — Volume vs ADR scatter
ax2 = fig1.add_axes([cx[1], r1y, cw2, r1h])
style(ax2, "Booking Volume vs ADR — Pricing Efficiency")
ax2.scatter(monthly["bookings"], monthly["mean_adr"],
            color=C_BLUE, s=80, zorder=3, alpha=0.8)
for m, row in monthly.iterrows():
    ax2.annotate(m[:3], (row["bookings"], row["mean_adr"]),
                 textcoords="offset points", xytext=(5,3),
                 color=C_MUTED, fontsize=7)
ax2.axhline(overall_adr, color=C_AMBER, linestyle="--", linewidth=1, alpha=0.6)
ax2.set_xlabel("Booking Volume")
ax2.set_ylabel("Mean ADR (€)")
ax2.grid(color=C_BORDER, linewidth=0.5, zorder=1)
ax2.text(0.05, 0.92, "Points top-right = high demand + high ADR (ideal)\n"
         "Points bottom-right = high demand + low ADR (underpriced ⚠)",
         transform=ax2.transAxes, color=C_MUTED, fontsize=8,
         bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG, edgecolor=C_BORDER))

# Chart 3 — ADR by market segment
ax3 = fig1.add_axes([cx[2], r1y, cw2, r1h])
style(ax3, "Mean ADR by Market Segment")
bars = ax3.barh(seg_adr.index, seg_adr.values,
                color=[C_GREEN if v > overall_adr else C_AMBER for v in seg_adr.values],
                height=0.6, zorder=3)
ax3.axvline(overall_adr, color=C_MUTED, linestyle="--", linewidth=1, alpha=0.6)
for bar, val in zip(bars, seg_adr.values):
    ax3.text(val+0.5, bar.get_y()+bar.get_height()/2,
             f"€{val:.0f}", va="center", color=C_TEXT, fontsize=9, fontweight="bold")
ax3.set_xlabel("Mean ADR (€)")
ax3.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=1)

# Chart 4 — ADR by stay length
ax4 = fig1.add_axes([cx[0], r2y, cw2, r1h])
style(ax4, "ADR by Length of Stay")
ax4.bar(stay_adr.index.astype(str), stay_adr.values,
        color=C_BLUE, width=0.6, zorder=3)
for i, v in enumerate(stay_adr.values):
    ax4.text(i, v+0.5, f"€{v:.0f}", ha="center",
             color=C_TEXT, fontsize=9, fontweight="bold")
ax4.set_ylabel("Mean ADR (€)")
ax4.set_xlabel("Stay Length")
ax4.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
ax4.tick_params(axis='x', labelsize=8)

# Chart 5 — Weekend vs weekday
ax5 = fig1.add_axes([cx[1], r2y, cw2, r1h])
style(ax5, "Weekend vs Weekday Stay ADR")
df["weekend_flag"] = df["stays_in_weekend_nights"] > df["stays_in_week_nights"]
wk_adr = df.groupby("weekend_flag")["adr"].mean()
labels_wk = {True: "Weekend-heavy", False: "Weekday-heavy"}
cols_wk   = [C_PURPLE, C_BLUE]
ax5.bar([labels_wk[k] for k in wk_adr.index], wk_adr.values,
        color=cols_wk, width=0.45, zorder=3)
for i, v in enumerate(wk_adr.values):
    ax5.text(i, v+0.5, f"€{v:.0f}", ha="center",
             color=C_TEXT, fontsize=14, fontweight="bold")
ax5.set_ylabel("Mean ADR (€)")
ax5.set_ylim(0, wk_adr.max()*1.2)
ax5.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)

# Chart 6 — Monthly booking volume
ax6 = fig1.add_axes([cx[2], r2y, cw2, r1h])
style(ax6, "Monthly Booking Volume — Demand Pattern")
ax6.fill_between(range(len(monthly)), monthly["bookings"], alpha=0.2, color=C_TEAL)
ax6.plot(range(len(monthly)), monthly["bookings"],
         color=C_TEAL, linewidth=2.5, marker="o", markersize=5, zorder=3)
ax6.set_xticks(range(len(monthly)))
ax6.set_xticklabels([m[:3] for m in monthly.index], fontsize=8)
ax6.set_ylabel("Bookings")
ax6.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)

fig1.text(0.03, 0.025,
          "Data: Hotel Booking Reservation 2024 (Kaggle) · 119,388 rows · "
          "UC1: Dynamic Pricing — identify underpriced periods and segments",
          color=C_MUTED, fontsize=8)
save(fig1, "dashboard_uc1_pricing.png")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — UC2: Cancellation Prediction (same as before, preserved)
# ══════════════════════════════════════════════════════════════════════════════
cancel_rate  = df["is_canceled"].mean()
total_cancel = df["is_canceled"].sum()
avg_adr      = df["adr"].mean()
avg_lead     = df["lead_time"].mean()

ch_col = "distribution_channel" if "distribution_channel" in df.columns else "market_segment"
df_ch = df[df[ch_col] != "Undefined"]
cancel_by_ch = (df_ch.groupby(ch_col)["is_canceled"]
                .agg(["mean","count"])
                .rename(columns={"mean":"rate","count":"n"})
                .sort_values("rate", ascending=True))
cancel_by_ch["rate_pct"] = cancel_by_ch["rate"] * 100

bins_lt = [0,3,7,14,30,60,90,180,365,9999]
labs_lt = ["0-2d","3-6d","7-13d","14-29d","30-59d","60-89d","90-179d","180-364d","365d+"]
df["lead_bucket"] = pd.cut(df["lead_time"], bins=bins_lt, labels=labs_lt, right=False)
lead_c = (df.groupby("lead_bucket", observed=True)["is_canceled"]
          .agg(["mean","count"])
          .rename(columns={"mean":"rate","count":"n"}))
lead_c["rate_pct"] = lead_c["rate"] * 100

monthly_c = (df.groupby("arrival_date_month")["is_canceled"]
             .agg(["mean","count"])
             .rename(columns={"mean":"rate","count":"n"})
             .reindex([m for m in month_order if m in df["arrival_date_month"].unique()]))
monthly_c["rate_pct"] = monthly_c["rate"] * 100

sr_cancel = None
if "total_of_special_requests" in df.columns:
    sr_cancel = df.groupby("total_of_special_requests")["is_canceled"].mean() * 100
    sr_cancel = sr_cancel[sr_cancel.index <= 4]

hotel_c = df.groupby("hotel")["is_canceled"].mean() * 100 if "hotel" in df.columns else None

seg_col = "market_segment" if "market_segment" in df.columns else ch_col
risk_tbl = (df[df[seg_col] != "Undefined"].groupby(seg_col)["is_canceled"]
            .agg(["mean","count"])
            .rename(columns={"mean":"rate","count":"bookings"})
            .sort_values("rate", ascending=False)
            .head(6))
risk_tbl["rate_pct"] = (risk_tbl["rate"]*100).round(1)

fig2 = new_fig("Cancellation & No-Show Risk Dashboard",
               "UC2 — Cancellation Prediction · Pan-European Aparthotel Chain")

cw, cy, ch2, gap = 0.175, 0.80, 0.10, 0.013
kpi(fig2, 0.03,            cy, cw, ch2, f"{cancel_rate:.1%}", "Overall Cancel Rate",
    f"{int(total_cancel):,} of {len(df):,} bookings", C_RED)
kpi(fig2, 0.03+cw+gap,     cy, cw, ch2, f"€{avg_adr:.0f}", "Mean ADR", "", C_BLUE)
kpi(fig2, 0.03+2*(cw+gap), cy, cw, ch2, f"{avg_lead:.0f}d", "Avg Lead Time", "", C_AMBER)
kpi(fig2, 0.03+3*(cw+gap), cy, cw, ch2, "61.1%", "Group Cancel Rate",
    "highest risk segment", C_RED)
kpi(fig2, 0.03+4*(cw+gap), cy, cw, ch2, "2.3×", "OTA vs Direct Risk",
    "41.0% OTA vs 17.5% Direct", C_AMBER)

r1y,r2y,rh,cw3 = 0.44,0.07,0.30,0.30

ax = fig2.add_axes([cx[0], r1y, cw3, rh])
style(ax, "Cancellation Rate by Booking Channel")
bc = [C_GREEN if r<25 else C_AMBER if r<40 else C_RED for r in cancel_by_ch["rate_pct"]]
bars = ax.barh(cancel_by_ch.index, cancel_by_ch["rate_pct"], color=bc, height=0.6, zorder=3)
ax.axvline(cancel_rate*100, color=C_MUTED, linestyle="--", linewidth=1, alpha=0.6)
for bar, val in zip(bars, cancel_by_ch["rate_pct"]):
    ax.text(val+0.5, bar.get_y()+bar.get_height()/2,
            f"{val:.1f}%", va="center", color=C_TEXT, fontsize=9, fontweight="bold")
ax.set_xlabel("Cancellation Rate (%)")
ax.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=1)

ax2 = fig2.add_axes([cx[1], r1y, cw3, rh])
style(ax2, "Cancellation Rate by Lead Time")
xv = range(len(lead_c))
ax2.fill_between(xv, lead_c["rate_pct"].values, alpha=0.15, color=C_RED)
ax2.plot(xv, lead_c["rate_pct"].values, color=C_RED, linewidth=2.5,
         marker="o", markersize=6, zorder=3)
ax2.set_xticks(xv)
ax2.set_xticklabels(lead_c.index, rotation=35, ha="right", fontsize=8)
ax2.set_ylabel("Cancellation Rate (%)")
ax2.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)

ax3 = fig2.add_axes([cx[2], r1y, cw3, rh])
style(ax3, "Monthly Cancellation Trend")
if monthly_c is not None and len(monthly_c) > 0:
    bc2 = [C_RED if v>cancel_rate*100*1.05 else C_BLUE for v in monthly_c["rate_pct"]]
    ax3.bar(range(len(monthly_c)), monthly_c["rate_pct"], color=bc2, width=0.65, zorder=3)
    ax3.set_xticks(range(len(monthly_c)))
    ax3.set_xticklabels([m[:3] for m in monthly_c.index], fontsize=8)
    ax3.axhline(cancel_rate*100, color=C_AMBER, linestyle="--", linewidth=1.2, alpha=0.8)
    ax3.set_ylabel("Cancellation Rate (%)")
    ax3.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)

ax4 = fig2.add_axes([cx[0], r2y, cw3, rh])
style(ax4, "Special Requests → Lower Cancellation")
if sr_cancel is not None:
    bc3 = [C_RED if i==0 else C_AMBER if i==1 else C_GREEN for i in range(len(sr_cancel))]
    ax4.bar(sr_cancel.index.astype(str), sr_cancel.values, color=bc3, width=0.6, zorder=3)
    for i,(x,v) in enumerate(zip(sr_cancel.index, sr_cancel.values)):
        ax4.text(i, v+0.5, f"{v:.1f}%", ha="center", color=C_TEXT, fontsize=9, fontweight="bold")
    ax4.text(0.97, 0.95, "r = −0.235", transform=ax4.transAxes, color=C_TEAL,
             fontsize=10, ha="right", va="top",
             bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG, edgecolor=C_TEAL))
    ax4.set_xlabel("Number of Special Requests")
    ax4.set_ylabel("Cancellation Rate (%)")
    ax4.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)

ax5 = fig2.add_axes([cx[1], r2y, cw3, rh])
style(ax5, "City vs Resort Hotel Cancellation")
if hotel_c is not None and len(hotel_c) >= 2:
    bc4 = [C_RED if v>35 else C_GREEN for v in hotel_c.values]
    bars5 = ax5.bar(hotel_c.index, hotel_c.values, color=bc4, width=0.45, zorder=3)
    for bar, val in zip(bars5, hotel_c.values):
        ax5.text(bar.get_x()+bar.get_width()/2, val+0.5, f"{val:.1f}%",
                 ha="center", color=C_TEXT, fontsize=13, fontweight="bold")
    ax5.set_ylabel("Cancellation Rate (%)")
    ax5.set_ylim(0, hotel_c.max()*1.25)
    ax5.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)

ax6 = fig2.add_axes([cx[2], r2y, cw3, rh])
style(ax6, "Cancellation Risk by Market Segment")
ax6.set_xlim(0,1); ax6.set_ylim(0,1)
ax6.set_xticks([]); ax6.set_yticks([])
headers = ["Segment","Cancel%","Bookings","Risk"]
hxs     = [0.01, 0.42, 0.65, 0.84]
ax6.text(0.5, 0.94, "", transform=ax6.transAxes)
for hx,h in zip(hxs,headers):
    ax6.text(hx, 0.91, h, color=C_MUTED, fontsize=9, fontweight="bold", transform=ax6.transAxes)
ax6.plot([0,1],[0.88,0.88], color=C_BORDER, linewidth=0.8, transform=ax6.transAxes)
step = 0.13
for i,(seg,row) in enumerate(risk_tbl.iterrows()):
    ry = 0.91-(i+1)*step
    rc = C_RED if row["rate_pct"]>50 else C_AMBER if row["rate_pct"]>30 else C_GREEN
    rl = "HIGH" if row["rate_pct"]>50 else "MED" if row["rate_pct"]>30 else "LOW"
    ax6.text(hxs[0], ry, str(seg)[:18], color=C_TEXT, fontsize=9, transform=ax6.transAxes, va="center")
    ax6.text(hxs[1], ry, f"{row['rate_pct']:.1f}%", color=rc, fontsize=9, fontweight="bold", transform=ax6.transAxes, va="center")
    ax6.text(hxs[2], ry, f"{int(row['bookings']):,}", color=C_MUTED, fontsize=9, transform=ax6.transAxes, va="center")
    ax6.text(hxs[3], ry, rl, color=rc, fontsize=8, fontweight="bold", transform=ax6.transAxes, va="center")

fig2.text(0.03, 0.025,
          "Data: Hotel Booking Reservation 2024 (Kaggle) · 119,388 rows · "
          "UC2: Cancellation Prediction — Groups 61.1% · OTA 2.3× riskier · Lead time r=+0.293",
          color=C_MUTED, fontsize=8)
save(fig2, "dashboard_uc2_cancellation.png")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — UC3: Guest Communication & Upsell
# ══════════════════════════════════════════════════════════════════════════════
meal_dist = df["meal"].value_counts(normalize=True)*100 if "meal" in df.columns else None
meal_labels = {"BB":"Bed & Breakfast","FB":"Full Board","HB":"Half Board",
               "SC":"Self Catering","Undefined":"No Meal"}

repeat_stats = None
if "is_repeated_guest" in df.columns:
    repeat_stats = df.groupby("is_repeated_guest").agg(
        cancel_rate=("is_canceled","mean"), mean_adr=("adr","mean"), count=("adr","count")
    )

top_countries = None
if "country" in df.columns:
    top_countries = (df.groupby("country").agg(
        bookings=("adr","count"), cancel_rate=("is_canceled","mean"), mean_adr=("adr","mean")
    ).sort_values("bookings", ascending=False).head(8))
    top_countries["cancel_rate"] = (top_countries["cancel_rate"]*100).round(1)

no_parking  = (df["required_car_parking_spaces"]==0).mean() if "required_car_parking_spaces" in df.columns else 0
one_night   = (df["total_nights"]==1).mean()
repeat_pct  = df["is_repeated_guest"].mean() if "is_repeated_guest" in df.columns else 0
upsell_meal = (meal_dist[["SC","BB"]].sum() if meal_dist is not None and all(k in meal_dist.index for k in ["SC","BB"]) else
               meal_dist[[k for k in ["SC","BB"] if k in meal_dist.index]].sum() if meal_dist is not None else 50)

fig3 = new_fig("Guest Communication & Upsell Intelligence",
               "UC3 — Guest Engagement · Pan-European Aparthotel Chain")

cw, cy, ch3, gap = 0.175, 0.80, 0.10, 0.013
kpi(fig3, 0.03,            cy, cw, ch3, f"{repeat_pct:.1%}", "Repeat Guest Rate",
    "loyalty programme opportunity", C_TEAL)
kpi(fig3, 0.03+cw+gap,     cy, cw, ch3, f"{no_parking:.1%}", "Guests w/o Parking",
    "pre-arrival parking upsell pool", C_AMBER)
kpi(fig3, 0.03+2*(cw+gap), cy, cw, ch3, f"{one_night:.1%}", "1-Night Stays",
    "extend-your-stay offer target", C_BLUE)
kpi(fig3, 0.03+3*(cw+gap), cy, cw, ch3, f"{upsell_meal:.1f}%", "SC/BB Meal Plans",
    "meal upgrade upsell opportunity", C_PURPLE)
kpi(fig3, 0.03+4*(cw+gap), cy, cw, ch3, "r=−0.235", "Special Requests Signal",
    "engaged guests cancel 2× less", C_GREEN)

r1y,r2y,rh,cw3 = 0.44,0.07,0.30,0.30

# Chart 1 — Meal plan distribution
ax = fig3.add_axes([cx[0], r1y, cw3, rh])
style(ax, "Meal Plan Distribution — Upsell Opportunity")
if meal_dist is not None:
    mlabels = [meal_labels.get(m, m) for m in meal_dist.index]
    mcolors = [C_AMBER if m in ["SC","Undefined"] else C_BLUE if m=="BB" else C_GREEN
               for m in meal_dist.index]
    ax.barh(mlabels, meal_dist.values, color=mcolors, height=0.6, zorder=3)
    for i, v in enumerate(meal_dist.values):
        ax.text(v+0.3, i, f"{v:.1f}%", va="center", color=C_TEXT, fontsize=9, fontweight="bold")
    ax.set_xlabel("Share of Bookings (%)")
    ax.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=1)
    ax.text(0.97, 0.05, "← Upsell target", transform=ax.transAxes,
            color=C_AMBER, fontsize=9, ha="right",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG, edgecolor=C_AMBER))

# Chart 2 — Repeat vs first-time guests
ax2 = fig3.add_axes([cx[1], r1y, cw3, rh])
style(ax2, "Repeat vs First-Time Guest Behaviour")
if repeat_stats is not None:
    labels_r = {0:"First-time", 1:"Repeat"}
    x_pos = [0, 1]
    cancel_vals = repeat_stats["cancel_rate"].values * 100
    adr_vals    = repeat_stats["mean_adr"].values

    ax2b = ax2.twinx()
    ax2.bar(x_pos, cancel_vals, color=[C_RED, C_GREEN], width=0.35, zorder=3, label="Cancel %")
    ax2b.plot(x_pos, adr_vals, color=C_AMBER, marker="D", markersize=10,
              linewidth=2, zorder=4, label="Mean ADR")
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([labels_r[k] for k in repeat_stats.index], fontsize=10)
    ax2.set_ylabel("Cancellation Rate (%)", color=C_MUTED)
    ax2b.set_ylabel("Mean ADR (€)", color=C_AMBER)
    ax2b.tick_params(colors=C_AMBER)
    ax2.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
    for i, (cv, av) in enumerate(zip(cancel_vals, adr_vals)):
        ax2.text(x_pos[i]-0.08, cv+0.5, f"{cv:.1f}%", color=C_TEXT, fontsize=10, fontweight="bold")
        ax2b.text(x_pos[i]+0.05, av+0.5, f"€{av:.0f}", color=C_AMBER, fontsize=9, fontweight="bold")

# Chart 3 — Top countries
ax3 = fig3.add_axes([cx[2], r1y, cw3, rh])
style(ax3, "Top Guest Origin Countries")
if top_countries is not None:
    tc = top_countries.head(7)
    bc = [C_RED if cr>40 else C_AMBER if cr>25 else C_GREEN for cr in tc["cancel_rate"]]
    bars3 = ax3.barh(tc.index, tc["bookings"], color=bc, height=0.6, zorder=3)
    ax3.set_xlabel("Number of Bookings")
    ax3.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=1)
    for bar, (country, row) in zip(bars3, tc.iterrows()):
        ax3.text(row["bookings"]+10, bar.get_y()+bar.get_height()/2,
                 f"{row['cancel_rate']:.0f}% cancel", va="center",
                 color=C_MUTED, fontsize=8)

# Chart 4 — Stay length for upsell targeting
ax4 = fig3.add_axes([cx[0], r2y, cw3, rh])
style(ax4, "Stay Length Distribution — Upsell Segments")
stay_dist = df.groupby("stay_bucket", observed=True).size() / len(df) * 100
sc = [C_AMBER if "1 night" in str(b) else C_BLUE if "2-3" in str(b) else C_GREEN for b in stay_dist.index]
ax4.bar(stay_dist.index.astype(str), stay_dist.values, color=sc, width=0.65, zorder=3)
for i, v in enumerate(stay_dist.values):
    ax4.text(i, v+0.3, f"{v:.1f}%", ha="center", color=C_TEXT, fontsize=9, fontweight="bold")
ax4.set_ylabel("Share of Bookings (%)")
ax4.set_xlabel("Stay Length")
ax4.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)
ax4.tick_params(axis='x', labelsize=8)
ax4.text(0.02, 0.92, "← Extend-stay offer", transform=ax4.transAxes,
         color=C_AMBER, fontsize=8,
         bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG, edgecolor=C_AMBER))

# Chart 5 — Special requests distribution
ax5 = fig3.add_axes([cx[1], r2y, cw3, rh])
style(ax5, "Special Requests Distribution")
if "total_of_special_requests" in df.columns:
    sr_dist = df.groupby("total_of_special_requests").agg(
        count=("adr","count"), cancel_rate=("is_canceled","mean")
    ).head(6)
    sr_dist["cancel_pct"] = sr_dist["cancel_rate"]*100
    bc5 = [C_RED if v>cancel_rate*100 else C_GREEN for v in sr_dist["cancel_pct"]]
    ax5.bar(sr_dist.index.astype(str), sr_dist["count"], color=bc5, width=0.6, zorder=3)
    ax5b = ax5.twinx()
    ax5b.plot(range(len(sr_dist)), sr_dist["cancel_pct"].values,
              color=C_AMBER, marker="o", linewidth=2, markersize=6, zorder=4)
    ax5b.set_ylabel("Cancel Rate (%)", color=C_AMBER)
    ax5b.tick_params(colors=C_AMBER)
    ax5.set_xlabel("Number of Special Requests")
    ax5.set_ylabel("Booking Count")
    ax5.grid(axis="y", color=C_BORDER, linewidth=0.5, zorder=1)

# Chart 6 — Customer type breakdown
ax6 = fig3.add_axes([cx[2], r2y, cw3, rh])
style(ax6, "Customer Type — Personalisation Segments")
if "customer_type" in df.columns:
    ct = df.groupby("customer_type").agg(
        count=("adr","count"), cancel_rate=("is_canceled","mean"), mean_adr=("adr","mean")
    ).sort_values("count", ascending=True)
    bc6 = [C_GREEN if cr<0.25 else C_AMBER if cr<0.40 else C_RED for cr in ct["cancel_rate"]]
    bars6 = ax6.barh(ct.index, ct["count"], color=bc6, height=0.6, zorder=3)
    for bar, (ctype, row) in zip(bars6, ct.iterrows()):
        ax6.text(row["count"]+10, bar.get_y()+bar.get_height()/2,
                 f"{row['cancel_rate']*100:.0f}% cancel · €{row['mean_adr']:.0f} ADR",
                 va="center", color=C_MUTED, fontsize=8)
    ax6.set_xlabel("Number of Bookings")
    ax6.grid(axis="x", color=C_BORDER, linewidth=0.5, zorder=1)

fig3.text(0.03, 0.025,
          "Data: Hotel Booking Reservation 2024 (Kaggle) · 119,388 rows · "
          "UC3: Guest Upsell — meal upgrades, parking, stay extensions, loyalty targeting",
          color=C_MUTED, fontsize=8)
save(fig3, "dashboard_uc3_upsell.png")

print("\nAll 3 dashboard pages saved:")
print("  dashboard_uc1_pricing.png")
print("  dashboard_uc2_cancellation.png")
print("  dashboard_uc3_upsell.png")
