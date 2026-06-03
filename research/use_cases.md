# Use case proposals — Pan-European aparthotel AI strategy

> **Data evidence note:** All insights below are drawn from real analysis of 119,388 booking records
> (Hotel Booking Reservation 2024, Kaggle) run through the LangChain agent in this project.
> Full scores and methodology in `evaluation/insight_review.md`.

---

## Use case 1 — Dynamic pricing / revenue optimisation engine

### Business problem
Chleo's revenue managers set nightly rates using seasonal rules and gut feeling. They miss event-driven demand spikes (festivals, conferences, public holidays) and underprice peak periods while overpricing slow ones.

### Evidence from data (Insight 2 + Insight 3)

**Insight 2 — Lead time reveals pricing windows:**
Our analysis found that bookings made 0–2 days before arrival have only an 8.1% cancellation rate — the most committed, price-insensitive customers book last minute. Yet these guests are likely receiving the same or lower rates than long-lead guests who cancel at 68%. A dynamic pricing model would charge a premium in the final 48–72h window when conversion probability is highest.

**Insight 3 — OTA vs direct ADR parity is a missed opportunity:**
OTA channel guests cancel at 41.0% vs direct at 17.5%, yet both pay nearly identical ADR (€117.96 vs €117.69). A pricing model that accounts for channel-level cancellation risk would price OTA bookings higher to offset the expected revenue loss from cancellations — recovering margin that is currently being left on the table.

**Supporting numbers:**
- 0–2 day lead time cancellation rate: **8.1%** (highest commitment)
- 365+ day lead time cancellation rate: **68.0%** (lowest commitment)
- OTA ADR: €117.96 vs Direct ADR: €117.69 — **<1% difference** despite 2.3x cancellation risk gap

### Proposed solution
A gradient boosting model (XGBoost or LightGBM) trained on historical booking data predicts the optimal nightly rate for each property and date. The model uses lead time, day of week, month, local event calendar flags, competitor rate benchmarks, and market segment mix.

The model outputs a human-readable explanation alongside every recommendation:
*"Recommended €195 because: 2-day lead time (8.1% cancel rate window), Primavera Festival this weekend in Barcelona, competitor median is €210."*

### Why relevant for this company size
At 500 employees across 10+ cities, pricing is decentralised and inconsistent. A centralised engine creates a single source of truth while allowing city managers to override.

### Expected value
8–15% RevPAR uplift is industry-standard for dynamic pricing adoption — likely €500K–€2M additional annual revenue at this chain's scale.

### Dashboard metric
RevPAR vs forecast gap, ADR by city, ADR by lead time bucket, event-driven pricing heat map.

---

## Use case 2 — Cancellation & no-show predictor

### Business problem
High cancellation rates leave apartments empty with no time to rebook. Each empty night is 100% lost revenue with fixed costs still running.

### Evidence from data (Insights 1, 2, 3, 5)

**Insight 1 — Group bookings are the highest-risk segment:**
Groups cancel at **61.1%** (n=19,810) — nearly 4x the Direct channel rate of 15.3%. This single segment represents a disproportionate share of cancellation-driven revenue loss and is the highest-priority target for a cancellation model.

**Insight 2 — Lead time is the single strongest predictor:**
Cancellation rate increases monotonically with lead time. Pearson correlation: r=+0.293 — the strongest numeric predictor in the dataset. The pattern is clear: 0–2 days = 8.1%, 7–13 days = 18.4%, 30–59 days = 36.3%, 90–364 days = 49.4%, 365+ days = 68.0%. This gives the model a reliable, explainable signal.

**Insight 3 — Distribution channel doubles the risk:**
TA/TO channel: **41.0%** cancellation vs Direct: **17.5%**. Online TA specifically: **36.7%**. Channel is a strong categorical feature for the classification model.

**Insight 5 — Special requests signal commitment:**
Bookings with at least one special request correlate negatively with cancellation (r=–0.235). Zero-request bookings combined with long lead time and OTA channel = highest risk profile. This three-feature combination gives the model a practical, auditable scoring rule Chleo can explain to her team.

**Supporting numbers:**
- Groups: **61.1%** cancellation (n=19,810)
- TA/TO channel: **41.0%** vs Direct: **17.5%**
- Lead time r=+0.293 — strongest single predictor
- Special requests r=–0.235 — strongest protective signal

### Proposed solution
A binary classification model (logistic regression or random forest) scores each booking's cancellation probability at the time of booking and again 72h before arrival. High-risk bookings trigger an automated retention workflow via n8n:
- Personalised email/SMS with a non-refundable upgrade offer
- Or early check-in incentive to confirm commitment
- All actions logged to Google Sheets for full audit trail

### Why relevant for this company size
Manual monitoring across 500+ apartments in 10+ cities is not feasible. At this scale, even a 5% improvement in net cancellation rate has material margin impact.

### Expected value
If the chain has ~100 cancellations/week and retention offers recover 10% at average ADR €150 → **~€78,000/year recovered** from a model costing almost nothing to run.

### Dashboard metric
Cancellation rate by channel (OTA vs direct), cancellation rate by lead time bucket, weekly cancellation trend, retention offer conversion rate.

---

## Use case 3 — Automated guest communication & upsell agent

### Business problem
Guest relations is the most headcount-intensive function in an aparthotel. Pre-arrival, mid-stay, and post-stay communications across 10 cities and hundreds of daily guests cannot scale manually.

### Evidence from data (Insight 5)

**Insight 5 — Engaged guests cancel less and spend more:**
Guests who make special requests cancel significantly less (r=–0.235 with cancellation). This means proactive pre-arrival outreach — asking guests for preferences, parking needs, and special requests — does double duty: it both reduces cancellation risk and creates upsell opportunities (parking, late check-out, room upgrades).

Guests who request parking (r=–0.195 with cancellation) are demonstrably more committed and more likely to respond positively to upsell offers. Targeting this segment with personalised upgrade offers before arrival is a low-cost, high-conversion opportunity.

**Supporting numbers:**
- Special requests: r=–0.235 with cancellation (protective signal)
- Parking requests: r=–0.195 with cancellation
- These signals identify the ~30–40% of guests most likely to engage with upsell offers

### Proposed solution
An LLM-powered agent (built with LangChain) handles the full guest communication sequence, triggered by PMS events via n8n webhooks:
- Pulls guest name, property, and check-in details from PMS
- Generates a personalised pre-arrival message asking for preferences
- Selects upsell offer by stay length (short stay → late check-out; long stay → extension discount)
- Sends via WhatsApp Business API or email (SendGrid)
- Logs every message with timestamp and content to Google Sheets for audit

All factual fields (address, times, prices) come from PMS data — not LLM generation — to prevent hallucination.

### Why relevant for this company size
500 employees across 10 cities cannot maintain a large guest comms team. Automation improves margin without degrading experience, if done with guardrails.

### Expected value
If automation handles 70% of guest comms currently done by staff, and each city has 2 FTE at €35K/year fully loaded → **€490K/year in redeployable staff cost** across the chain.

### Dashboard metric
Upsell conversion rate, review score trend, message response rate, average response time, special request rate per booking.

---

## Dataset justification summary

| Dataset | Use cases served | Key columns used | Real findings |
|---|---|---|---|
| Hotel Booking Reservation 2024 | UC1, UC2, UC3 | lead_time, adr, is_canceled, market_segment, distribution_channel, total_special_requests | 119,388 rows, all 5 insights |
| Hotel Prices in Europe 2024 | UC1 | price, date, city | Event-driven ADR benchmarks |
| Tourism & Hospitality Industry Analysis | Context / benchmarking | revpar, occupancy_rate, adr by segment | Sector KPI context |

All datasets are from Kaggle, publicly available, and free to download with a free account.
