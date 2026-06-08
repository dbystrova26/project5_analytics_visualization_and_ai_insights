"""
ai_adoption_dashboard.py
━━━━━━━━━━━━━━━━━━━━━━━━
AI Adoption Evidence Dashboard — Hospitality Sector
Answers Cleo's core question: "Is AI investment worth it for a company like mine?"

DATA SOURCES (all hardcoded — no API calls needed):
  Chart 1: Canary Technologies 2026 hospitality survey (via Hotel News Resource, Apr 2026)
  Chart 2: The Business Research Company — AI in Hospitality Market Report (Apr 2026)
           CAGR 57.7%, market reaches $11.1B by 2030
  Chart 3: Hotel Technology News — "How AI Will Rewrite Hotel Revenue Management" (Dec 2025)
           Hotels using AI-driven RMS report ~17% revenue increase vs non-adopters
  Chart 4: Directional estimates based on public operator reports, investor materials,
           and press coverage for Numa, Limehome, BobW, Accor Adagio, Staycity
           NOTE: % values are estimated AI integration maturity, not official figures
  Chart 5: McKinsey research (via AI for Hospitality Guide, Apr 2026) — <18 months payback
           Other comparisons are industry benchmark estimates
  Chart 6: Composite of Hotel Technology News (Dec 2025), McKinsey, HVS (Jul 2025)
           NOTE: ROI % values are directional benchmarks, not guaranteed outcomes

Run:
    pip install plotly
    python ai_adoption_dashboard.py

Output:
    dashboard/ai_adoption_dashboard.html  (open in any browser)
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Colour palette ────────────────────────────────────────────────────────────
C_BG    = "#0A0E1A"
C_CARD  = "#111827"
C_TEXT  = "#F1F5F9"
C_MUTED = "#94A3B8"
C_BORDER= "#1F2937"
C_AMBER = "#F59E0B"
C_GREEN = "#10B981"
C_BLUE  = "#3B82F6"
C_RED   = "#F43F5E"

# ── Data (hardcoded from published sources — see docstring) ───────────────────

# Chart 1 — Canary Technologies 2026 survey
adoption_labels = ["Already using AI\nsignificantly", "Planned adoption\nby 2024", "Not yet / unsure"]
adoption_values = [71, 50, 29]
adoption_colors = [C_GREEN, C_AMBER, C_MUTED]

# Chart 2 — The Business Research Company market forecast
market_years  = [2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
market_values = [0.40, 0.63, 0.99, 1.57, 2.47, 3.90, 6.15, 9.69, 11.10]

# Chart 3 — Hotel Technology News Dec 2025
uplift_labels = ["AI adopters", "Non-adopters\n(baseline)"]
uplift_values = [17, 0]
uplift_text   = ["+17% revenue\nvs non-adopters", "0% (baseline)"]
uplift_colors = [C_GREEN, C_MUTED]

# Chart 4 — Estimated AI integration maturity (directional, not official)
operators = ["BobW", "Limehome", "Numa", "Accor Adagio", "Staycity", "Cleo's chain\n(current est.)"]
op_status = [95, 90, 90, 70, 55, 10]
op_colors = [C_GREEN if s >= 75 else C_AMBER if s >= 50 else C_RED for s in op_status]

# Chart 5 — McKinsey + industry benchmark estimates
invest_labels = ["AI pricing &\npersonalisation", "Traditional\nRMS upgrade", "New PMS\nimplementation", "Staff hiring\n(guest relations)"]
invest_months = [18, 36, 48, 24]
invest_colors = [C_GREEN, C_AMBER, C_RED, C_MUTED]

# Chart 6 — Composite industry benchmark (directional)
uc_labels = ["Dynamic\npricing", "Cancellation\nprediction", "Guest comms\nautomation", "Demand\nforecasting", "AI chatbot /\nconcierge"]
uc_roi    = [15, 12, 8, 6, 3]
uc_colors = [C_GREEN if r >= 10 else C_AMBER if r >= 5 else C_MUTED for r in uc_roi]

# ── Build figure ──────────────────────────────────────────────────────────────
fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=[
        "1. Hospitality professionals already using AI (%)",
        "2. AI hospitality market size forecast ($B)",
        "3. Revenue uplift — AI adopters vs non-adopters",
        "4. EU aparthotel operators — AI integration maturity*",
        "5. Investment payback period (months)",
        "6. Top AI use cases — estimated RevPAR uplift*",
    ],
    vertical_spacing=0.20,
    horizontal_spacing=0.09,
)

# Chart 1
fig.add_trace(go.Bar(
    x=adoption_labels, y=adoption_values,
    marker_color=adoption_colors,
    text=[f"{v}%" for v in adoption_values],
    textposition="outside",
    textfont=dict(color=C_TEXT, size=12, family="monospace"),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>%{y}%<extra>Canary Technologies 2026</extra>",
), row=1, col=1)

# Chart 2
fig.add_trace(go.Scatter(
    x=market_years, y=market_values,
    mode="lines+markers",
    line=dict(color=C_AMBER, width=3),
    marker=dict(size=7, color=C_AMBER, line=dict(color=C_BG, width=2)),
    fill="tozeroy",
    fillcolor="rgba(245,158,11,0.1)",
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>$%{y:.2f}B<extra>Business Research Company</extra>",
), row=1, col=2)

# Chart 3
fig.add_trace(go.Bar(
    x=uplift_labels, y=uplift_values,
    marker_color=uplift_colors,
    text=uplift_text,
    textposition="outside",
    textfont=dict(color=C_TEXT, size=10),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>+%{y}% revenue<extra>Hotel Technology News Dec 2025</extra>",
), row=1, col=3)

# Chart 4
fig.add_trace(go.Bar(
    x=op_status, y=operators,
    orientation="h",
    marker_color=op_colors,
    text=[f"{s}%" for s in op_status],
    textposition="outside",
    textfont=dict(color=C_TEXT, size=10),
    showlegend=False,
    hovertemplate="<b>%{y}</b><br>~%{x}% AI integration<extra>*Estimated from public sources</extra>",
), row=2, col=1)

# Chart 5
fig.add_trace(go.Bar(
    x=invest_labels, y=invest_months,
    marker_color=invest_colors,
    text=[f"{m} months" for m in invest_months],
    textposition="outside",
    textfont=dict(color=C_TEXT, size=10),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>~%{y} months payback<extra>McKinsey / industry estimates</extra>",
), row=2, col=2)

# Chart 6
fig.add_trace(go.Bar(
    x=uc_labels, y=uc_roi,
    marker_color=uc_colors,
    text=[f"+{r}% RevPAR" for r in uc_roi],
    textposition="outside",
    textfont=dict(color=C_TEXT, size=10),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>~+%{y}% RevPAR<extra>*Directional benchmark</extra>",
), row=2, col=3)

# ── Layout ────────────────────────────────────────────────────────────────────
fig.update_layout(
    title=dict(
        text=(
            "<b>AI Adoption Evidence Dashboard — Hospitality Sector</b><br>"
            "<span style='font-size:12px'>Is AI investment worth it for Cleo's pan-European aparthotel chain?</span>"
        ),
        font=dict(size=17, color=C_TEXT),
        x=0.01, y=0.99,
    ),
    paper_bgcolor=C_BG,
    plot_bgcolor=C_CARD,
    font=dict(color=C_MUTED, family="'DM Sans', sans-serif"),
    height=900,
    margin=dict(t=80, b=80, l=70, r=40),
)

for ann in fig.layout.annotations:
    ann.font = dict(color=C_TEXT, size=11)

for i in range(1, 7):
    xa = f"xaxis{i if i > 1 else ''}"
    ya = f"yaxis{i if i > 1 else ''}"
    for ax in [xa, ya]:
        if ax in fig.layout:
            fig.layout[ax].update(
                gridcolor=C_BORDER, gridwidth=1,
                zeroline=False, linecolor=C_BORDER,
                tickfont=dict(color=C_MUTED, size=9),
            )

# Y-axis range for charts with text above bars
fig.update_yaxes(range=[0, 85], row=1, col=1)
fig.update_yaxes(range=[0, 25], row=1, col=3)
fig.update_xaxes(range=[0, 115], row=2, col=1)
fig.update_yaxes(range=[0, 60], row=2, col=2)
fig.update_yaxes(range=[0, 20], row=2, col=3)

# KPI strip removed — numbers are clear from the charts themselves

# Source footnote
fig.add_annotation(
    text=(
        "* Charts 4 and 6 show directional estimates from composite sources — not single independently-audited figures. "
        "Full source list: sources.md<br>"
        "Sources: Canary Technologies (2026) · The Business Research Company (Apr 2026) · "
        "Hotel Technology News (Dec 2025) · McKinsey/Tommaso Maria Ricci (Apr 2026) · "
        "HVS European Serviced Apartments (Jul 2025) · Competitor public investor materials"
    ),
    xref="paper", yref="paper",
    x=0.0, y=-0.09,
    showarrow=False,
    font=dict(color=C_MUTED, size=8),
    align="left",
)

# ── Save ──────────────────────────────────────────────────────────────────────
import os, sys

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "ai_adoption_dashboard.html")

fig.write_html(
    out_path,
    include_plotlyjs="cdn",
    full_html=True,
    config={"displaylogo": False, "displayModeBar": True,
            "modeBarButtonsToRemove": ["lasso2d","select2d"],
            "toImageButtonOptions": {"format":"png","width":1600,"height":900}}
)
print(f"Saved: {out_path}")
print("Open dashboard/ai_adoption_dashboard.html in your browser")
