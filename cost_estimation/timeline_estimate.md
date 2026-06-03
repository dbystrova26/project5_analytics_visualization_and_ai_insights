# Implementation timeline — Pan-European aparthotel AI strategy

**Approach:** Phased rollout — start with highest-ROI use case, prove value, then expand  
**Recommended start:** UC2 (cancellation prediction) + UC3 (guest comms) first — fastest to build and directly visible to Chleo  
**Then:** UC1 (dynamic pricing) — higher complexity, higher ROI, needs UC2 data pipeline as foundation

---

## Phase 1 — Foundation & quick wins (Weeks 1–6)

**Goal:** Prove AI works, build team confidence, create audit infrastructure

| Week | Activities |
|---|---|
| 1–2 | Data audit: assess PMS data quality, map available fields, identify gaps |
| 2–3 | Build data pipeline: PMS → cleaned CSV → processed features (UC1 & UC2 foundation) |
| 3–4 | Build cancellation prediction model (UC2) — rule-based v1 first, then ML v2 |
| 4–5 | Build n8n retention workflow (UC2 + UC3) — test with 1 property in shadow mode |
| 5–6 | Build guest comms agent (UC3) — 10 message templates, test with real bookings |
| 6 | Go-live: UC2 + UC3 on 2 pilot properties. Begin logging all AI actions to Google Sheets |

**Milestone:** 2 properties running live AI retention workflow and automated guest comms.

---

## Phase 2 — Scale & validate (Weeks 7–10)

**Goal:** Roll out UC2 + UC3 to all properties, build dashboard, start pricing research

| Week | Activities |
|---|---|
| 7 | Roll out UC2 + UC3 to all 8–12 properties after pilot validation |
| 7–8 | Build PowerBI dashboard (Phase 1 metrics: cancellation rate, message delivery rate) |
| 8–9 | Begin dynamic pricing data collection — gather competitor rate data, event calendars |
| 9–10 | Train pricing model v1 on historical booking data (advisory mode only — no auto-publish) |
| 10 | Internal review: show Chleo Phase 1 results. Present cancellation reduction and comms metrics |

**Milestone:** Full chain on UC2 + UC3. First pricing model trained and ready for shadow testing.

---

## Phase 3 — Dynamic pricing (Weeks 11–14)

**Goal:** Deploy pricing engine in advisory mode, validate accuracy, plan auto-publish

| Week | Activities |
|---|---|
| 11–12 | Pricing model shadow mode: model suggests rates, revenue managers decide. Log acceptance rate |
| 12–13 | Refine model based on city manager feedback. Add event calendar integration |
| 13–14 | Legal review of OTA contracts for rate automation compliance |
| 14 | Pricing model v1 go-live in advisory mode across all cities |

**Milestone:** Pricing recommendations visible in dashboard. Revenue managers using AI suggestions.

---

## Phase 4 — Automation & monitoring (Weeks 15+)

**Goal:** Move pricing to semi-automated, build monitoring, plan ongoing improvement

| Week | Activities |
|---|---|
| 15–16 | Set up model monitoring (Evidently AI or custom) — track drift and accuracy |
| 16–18 | Optionally enable auto-publish pricing for low-variance periods (e.g. weekdays with >60 days lead time) |
| Ongoing | Quarterly model retraining. Monthly insight quality review. Annual strategy review with Chleo |

---

## Summary timeline

```
Weeks 1–6:   Build foundation + UC2 cancellation + UC3 guest comms (2 pilot properties)
Weeks 7–10:  Roll out to all cities + dashboard + start pricing research
Weeks 11–14: Dynamic pricing in shadow mode + legal review
Weeks 15+:   Monitoring, automation, continuous improvement
```

**Total time to first visible AI value:** 6 weeks  
**Total time to full UC1+UC2+UC3 deployment:** 14–16 weeks  
**Ongoing:** Quarterly retraining and review cycle

---

## Key dependencies

- PMS must support webhook notifications (most modern PMS systems do — confirm before Week 1)
- SendGrid or Twilio account setup (1 day)
- Google Workspace account for audit Sheets (likely already exists)
- At least 12 months of historical booking data in PMS for pricing model training
- Legal sign-off on OTA contracts before pricing automation goes live
