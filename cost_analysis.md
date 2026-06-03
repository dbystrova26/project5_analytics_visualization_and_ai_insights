# Cost estimation — AI implementation for pan-European aparthotel chain

**Prepared for:** Chleo (CEO)  
**Company size:** ~500 employees, 8–12 European cities  
**Scope:** All three use cases — dynamic pricing, cancellation prediction, guest comms automation

---

## Methodology

Costs are estimated based on:
- Comparable AI implementation projects in mid-market hospitality (50–500 unit operators)
- Free-tier vs paid API pricing for LLM usage at this scale (~500 bookings/week)
- Freelance vs boutique agency day rates in Western Europe (€600–€1,200/day)
- Open-source tooling (LangChain, n8n self-hosted) to minimise vendor costs

All figures are upfront (build) costs. Running costs are shown separately per month.

---

## Use case 1 — Dynamic pricing engine

| Item | Cost estimate |
|---|---|
| Data pipeline (PMS → cleaned dataset) | €2,000 – €4,000 |
| ML model development (XGBoost/LightGBM) | €4,000 – €8,000 |
| Rate recommendation API (deployment) | €1,500 – €3,000 |
| Channel manager integration | €1,000 – €2,000 |
| Testing & QA (2 weeks shadow mode) | €1,000 – €2,000 |
| **Subtotal UC1** | **€9,500 – €19,000** |

**Running costs (monthly):**
- Cloud hosting (AWS/GCP, small instance): €80–€150/month
- Model retraining (quarterly): €500/quarter
- Monitoring tool (optional, e.g. Evidently AI): €0 (open source) or €200/month

---

## Use case 2 — Cancellation prediction model

| Item | Cost estimate |
|---|---|
| Feature engineering on booking data | €1,500 – €3,000 |
| Classification model (logistic regression / RF) | €2,000 – €4,000 |
| Risk score API endpoint | €1,000 – €2,000 |
| n8n workflow integration | €500 – €1,000 |
| **Subtotal UC2** | **€5,000 – €10,000** |

**Note:** UC2 can reuse the data pipeline built for UC1 — this reduces cost if both are implemented together.

**Running costs (monthly):**
- Included in UC1 infrastructure: +€0 if co-deployed
- LLM API for retention messages: ~€50–€100/month (at 500 bookings/week, ~30% high-risk, ~1,500 messages/month × €0.03/message)

---

## Use case 3 — Guest communication automation

| Item | Cost estimate |
|---|---|
| LangChain agent development | €2,000 – €4,000 |
| n8n workflow build & testing | €1,000 – €2,000 |
| PMS webhook integration | €500 – €1,500 |
| SendGrid / Twilio setup | €300 – €500 |
| Google Sheets audit log | €200 – €300 |
| Content template development (10 message types) | €800 – €1,500 |
| **Subtotal UC3** | **€4,800 – €9,800** |

**Running costs (monthly):**
- LLM API (Anthropic/OpenAI): €100–€300/month
- SendGrid email: €20–€50/month (free tier covers first 100 emails/day)
- Twilio SMS: ~€0.05/SMS × 1,500 messages = €75/month
- n8n cloud: €0 (self-hosted) to €50/month (cloud)

---

## Total cost summary

| Scope | Build cost | Monthly running |
|---|---|---|
| UC1 only (dynamic pricing) | €9,500 – €19,000 | €180 – €350 |
| UC2 only (cancellation) | €5,000 – €10,000 | €50 – €200 |
| UC3 only (guest comms) | €4,800 – €9,800 | €195 – €400 |
| **All 3 (with shared infrastructure)** | **€15,000 – €30,000** | **€350 – €750** |

---

## ROI estimate (Year 1)

| Use case | Conservative ROI | Optimistic ROI |
|---|---|---|
| Dynamic pricing (8% RevPAR uplift on €5M revenue base) | €400,000 | €750,000 |
| Cancellation reduction (10% of 1,500 cancellations/month × €140 ADR) | €25,200 | €50,400 |
| Guest comms automation (replaces 2 FTE at €35K fully loaded) | €70,000 | €70,000 |
| **Total Year 1 benefit** | **€495,200** | **€870,400** |
| **Net ROI (after €30K build cost)** | **€465,200** | **€840,400** |
| **Payback period** | **< 1 month** | **< 2 weeks** |

---

## Assumptions & caveats

1. Revenue base of €5M assumes a 500-unit chain at ~65% occupancy and €50 average ADR — adjust if Chleo's actual figures differ.
2. Dynamic pricing ROI assumes the model is in production advisory mode for 3 months, then full automation. Real uplift will depend on how willing city managers are to follow AI recommendations.
3. FTE replacement cost assumes guest comms automation replaces 2 FTE across the chain. If current team is larger, savings are higher.
4. All LLM API costs assume current (2024–2025) pricing — prices have historically fallen year over year.
5. Build costs assume a freelance data engineer + ML engineer based in Western Europe. Eastern Europe or offshore teams would reduce build costs by 30–50%.
6. These estimates do not include GDPR compliance legal costs (DPIA, DPO consultation) — budget an additional €2,000–€5,000 for this.
