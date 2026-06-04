# Use case proposals — Pan-European aparthotel AI strategy

> **Data note:** All numbers below are from real analysis of 119,388 booking records
> (Hotel Booking Reservation 2024, Kaggle) run through the LangChain agent.
> Full scores and methodology in `evaluation/insight_review.md`.

---

## Use case 1 — Dynamic pricing / revenue optimisation engine

### Business problem
Chleo's revenue managers set nightly rates using seasonal rules and gut feeling. The data shows almost zero dynamic pricing in practice.

### Evidence from real data

| Finding | Real number | Source tool |
|---|---|---|
| Peak vs low month ADR gap | Only **€5.42** (Oct €118.43 vs May €113.00) | `seasonal_pricing_analysis` |
| Volume swing peak vs low | **20.9%** more bookings in peak months | `seasonal_pricing_analysis` |
| Weekend vs weekday ADR | Weekend: **€115.50** vs Weekday: **€115.85** — no premium | `weekend_vs_weekday_adr` |
| Long stay ADR | 8–14 nights: **€112.41** — lower than 1-night (€116.23) | `stay_length_adr_analysis` |
| Highest ADR segment | Offline TA/TO **€117.85** | `adr_statistics(group_by='market_segment')` |
| Lowest ADR segment | Corporate **€114.36** — despite lowest cancel rate | `adr_statistics(group_by='market_segment')` |

**Key insight:** A €5.42 ADR gap across the full year despite 20.9% volume swings = the chain is barely adjusting rates to demand. A dynamic pricing model capturing even half the opportunity at peak periods would generate significant additional revenue.

### Proposed solution
A gradient boosting model predicts optimal nightly rate per property per date using lead time, month, day of week, local event flags, competitor rates, and market segment. Every recommendation includes a plain-language explanation: *"Recommended €135 because: October weekend, 2-day lead time (8.1% cancel = committed), competitor median €142."*

### Expected value
8–15% RevPAR uplift is industry-standard. At this chain's scale, even 5% uplift on €5M revenue base = **€250K additional annual revenue**.

### Dashboard metrics
ADR by month (seasonality chart), volume vs ADR scatter (pricing efficiency), ADR by segment, weekend vs weekday comparison.

---

## Use case 2 — Cancellation & no-show predictor

### Business problem
37.5% of all bookings cancel (44,010 of 117,429). Each empty apartment is 100% lost revenue with fixed costs still running.

### Evidence from real data

| Finding | Real number | Source tool |
|---|---|---|
| Overall cancellation rate | **37.5%** (44,010 bookings) | `cancellation_rate_by_segment` |
| Groups segment | **61.1%** cancel (n=19,810) | `cancellation_rate_by_segment(column='market_segment')` |
| Direct channel | **17.5%** cancel | `cancellation_rate_by_segment(column='distribution_channel')` |
| TA/TO channel | **41.0%** cancel — 2.3× higher than Direct | `cancellation_rate_by_segment(column='distribution_channel')` |
| OTA vs Direct ADR | €117.96 vs €117.69 — **<1% difference** | `adr_statistics(group_by='market_segment')` |
| 365d+ lead time | **68.0%** cancel | `lead_time_analysis` |
| 0–2d lead time | **8.1%** cancel (most committed) | `lead_time_analysis` |
| Lead time correlation | **r=+0.293** — strongest numeric predictor | `correlation_with_cancellation` |
| Special requests | **r=–0.235** — protective signal | `correlation_with_cancellation` |
| City Hotel cancel rate | **40.6–43.2%** | `cancellation_rate_by_segment(column='hotel')` |
| Resort Hotel cancel rate | **26.3–29.9%** — 13–16pp lower | `cancellation_rate_by_segment(column='hotel')` |
| No Deposit bookings | Highest cancel rate in deposit analysis | `deposit_type_cancellation` |

**Key insight:** Three levers explain most cancellations — channel (OTA 2.3× riskier), timing (365d+ bookings cancel at 68%), and segment (Groups 61.1%). A classification model combining these signals gives the n8n retention workflow its trigger.

### Proposed solution
Binary classification model scores each booking's cancellation probability. Bookings above a risk threshold trigger the n8n retention workflow: personalised email/SMS offer → sent 72h before arrival → logged to Google Sheets.

### Expected value
100 cancellations/week × 10% recovery rate × €150 ADR = **~€78,000/year recovered** from a model costing almost nothing to run.

### Dashboard metrics
Cancellation rate by channel, lead time risk curve, monthly trend, special requests chart, city vs resort comparison, segment risk table.

---

## Use case 3 — Automated guest communication & upsell agent

### Business problem
Guest relations is the most headcount-intensive function. Pre-arrival, mid-stay, and post-stay communications across 10+ cities cannot scale manually at this company size.

### Evidence from real data

| Finding | Real number | Source tool |
|---|---|---|
| Guests without parking booked | **93.8%** | `upsell_opportunity_analysis` |
| BB/SC (basic) meal plan guests | **86.2%** | `upsell_opportunity_analysis` |
| 1-night stays | **17.4%** | `upsell_opportunity_analysis` |
| Repeat guest rate | **2.8%** | `repeat_guest_analysis` |
| Repeat guest cancel rate | **16.2%** vs 38.1% first-time | `repeat_guest_analysis` |
| Repeat guest ADR | **€75** vs €104 first-time — 28% less | `repeat_guest_analysis` |
| Portugal (top origin) | **30.7%** of bookings, 68% cancel | `guest_origin_analysis` |
| Transient customers | **75%+** of all bookings | `guest_origin_analysis` |
| Special requests signal | **r=–0.235** — engaged guests cancel 2× less | `correlation_with_cancellation` |

**Key insight:** 93.8% no-parking + 86.2% basic meal plans + 17.4% one-night stays = three automated upsell triggers for every booking. The guest comms agent addresses all three in a single pre-arrival message, with zero manual effort.

**Loyalty finding:** Repeat guests cancel at half the rate (16.2% vs 38.1%) but pay 28% less (€75 vs €104). This is the clearest ROI case for a loyalty programme — these guests are already committed, they just need to be incentivised to pay direct rates.

### Proposed solution
LangChain agent handles full guest communication sequence triggered by PMS webhooks via n8n. All factual fields (address, times, prices) come from PMS — LLM writes personalisation only. Every message logged to Google Sheets for audit.

### Expected value
If automation handles 70% of guest comms for 2 FTE per city at €35K/year fully loaded = **€490K/year** redeployable across 10 cities.

### Dashboard metrics
Meal plan distribution, repeat vs first-time behaviour, top origin countries, stay length segmentation, special requests distribution, customer type breakdown.

---

## Dataset justification

| Dataset | Use cases | Key columns | Real findings |
|---|---|---|---|
| Hotel Booking Reservation 2024 | UC1, UC2, UC3 | lead_time, adr, is_canceled, market_segment, distribution_channel, meal, deposit_type, customer_type, country, total_of_special_requests | 119,388 rows, 10 insights |
| Hotel Prices in Europe 2024 | UC1 | price, date, city | Event-driven ADR benchmarks |
| Tourism & Hospitality Industry Analysis | Context | revpar, occupancy_rate | Sector KPI context |
