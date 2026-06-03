# Dashboard documentation — Aparthotel Revenue & Cancellation Intelligence

**Tool:** PowerBI Desktop (.pbix)  
**Audience:** Chleo (CEO) and city general managers  
**Purpose:** Single source of truth for revenue performance, cancellation patterns, and pricing opportunities across the chain

---

## Use case description

Chleo currently has no central view of how her 8–12 city properties are performing relative to each other or relative to market benchmarks. Revenue decisions are made by city managers independently, with no consistent KPI framework.

This dashboard provides the "communication layer" — the top-level view a CEO needs to ask the right questions before drilling into analysis. It is designed to be the first screen Chleo opens every Monday morning.

---

## Dashboard pages

### Page 1 — Executive overview
**Stakeholder question answered:** "How is the business performing this month?"

**Visuals:**
- KPI cards: RevPAR, Occupancy %, ADR, Cancellation rate (current month vs prior month)
- City performance bar chart: RevPAR by city, sorted descending, with target line
- Monthly trend line: RevPAR over last 12 months with rolling average

**Design rationale:** KPI cards at the top follow the "communication layer" principle — the most important numbers are visible without scrolling. The city bar chart immediately shows which city needs attention. The trend line gives historical context.

---

### Page 2 — Cancellation analysis
**Stakeholder question answered:** "Where are we losing revenue to cancellations?"

**Visuals:**
- Cancellation rate by booking channel (OTA vs direct vs corporate) — stacked bar
- Cancellation rate by lead time bucket (0–2d, 3–6d, 7–13d, 14–29d, 30d+) — line chart
- Monthly cancellation trend — area chart
- Table: top 10 highest-cancellation properties this month

**Design rationale:** The channel breakdown directly supports the "reduce OTA dependency" strategic narrative. The lead time chart visualises the insight that last-minute bookings are highest-risk. These two visuals together tell Chleo where to focus the n8n retention workflow.

---

### Page 3 — Pricing intelligence
**Stakeholder question answered:** "Are we pricing correctly?"

**Visuals:**
- ADR by month — column chart showing seasonal pattern
- ADR vs occupancy scatter — each dot is one month; clusters above/below the trend line show pricing opportunities
- Booking volume vs ADR by city — bubble chart

**Design rationale:** The ADR-by-month chart directly demonstrates Insight 4 (summer underpricing). The scatter plot is the most powerful visual — it shows the relationship between how full properties are and how much they're charging, revealing if properties are filling up cheaply (underpriced) or staying empty at high rates (overpriced).

---

## Key metrics explanation

| Metric | Definition | Why it matters |
|---|---|---|
| RevPAR | Revenue Per Available Room = Occupancy % × ADR | Primary health metric for any hotel business |
| ADR | Average Daily Rate = total room revenue / rooms sold | Measures pricing strength |
| Occupancy % | Rooms sold / rooms available | Measures demand capture |
| Cancellation rate | Cancelled bookings / total bookings | Directly impacts predictability and revenue |
| Direct booking rate | Direct bookings / total bookings | OTA dependency proxy — lower OTA means lower commissions |
| Average lead time | Days between booking date and arrival | Longer lead times = more stable revenue |

---

## Data source

Primary: `data/processed/bookings_clean.csv` (cleaned from Hotel Booking Reservation 2024, Kaggle)  
Supplement: `data/processed/eu_prices.csv` (cleaned from Hotel Prices in Europe 2024, Kaggle)

Both CSVs are loaded directly into PowerBI via "Get Data → Text/CSV".

---

## How to use the dashboard

**Filters (top of each page):**
- Date range slicer — filter to any month or year range
- City slicer — isolate a single property or compare a subset
- Booking channel slicer — compare OTA vs direct performance

**Interactions:**
- Clicking any bar in the city chart cross-filters all other visuals on the page
- Clicking a month in the trend chart highlights that month's KPI cards
- Hover on any data point to see the full tooltip with underlying numbers

**Navigation:**
- Use the page tabs at the bottom: Executive / Cancellations / Pricing
- Or use the arrow buttons in the navigation panel on the left

---

## Design rationale summary

This dashboard follows the **communication layer** principle from the Module 5 PowerBI lecture:

- **No analysis layer content on the main pages** — no pivot tables, no raw data, no statistical output. Those live in the agent outputs.
- **Stakeholder-focused metrics** — every metric answers a question a CEO actually asks. "What is r²?" is not on this dashboard.
- **Single source of truth** — one dataset, one set of numbers. City managers cannot bring their own spreadsheets to contradict the dashboard.
- **Progressive disclosure** — overview first, details on demand via drill-through.

---

## Screenshots

*(Add screenshots of each dashboard page here after building in PowerBI)*

- `screenshots/page1_overview.png`
- `screenshots/page2_cancellations.png`
- `screenshots/page3_pricing.png`
