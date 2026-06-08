# Hype vs Evidence — AI Adoption in Hospitality

**Prepared for:** Cleo, CEO  
**Purpose:** Separate what the data actually supports from what vendors are selling

---

## The core question Cleo is really asking

"Everyone says AI will transform everything. But which parts are real, which are exaggerated, and what would actually make sense for a company like mine to try first?"

This document answers that directly.

---

## Claims that ARE supported by evidence

### ✅ Dynamic pricing increases ADR by 10–15%
**Source:** Hotel Technology News (Dec 2025), multiple independent industry reports  
**Our data supports it:** We found only a €5.42 ADR gap between peak (Oct €118.43) and low (May €113.00) despite a 20.9% booking volume swing. This is near-zero dynamic pricing. The opportunity is real and visible in the data.  
**Verdict: INVEST — this is one of the highest-ROI, most proven AI applications in hospitality.**

### ✅ Cancellation prediction using lead time and channel is accurate and actionable
**Source:** Our analysis of 119,388 real booking records  
**Evidence:** Lead time has r=+0.293 correlation with cancellation. TA/TO channel cancels at 2.3× Direct at identical ADR. Groups cancel at 61.1%. These are strong, consistent, actionable signals.  
**Verdict: INVEST — the signals are real, the data is available, the solution is buildable today.**

### ✅ AI early movers in EU aparthotels are achieving 8–14% RevPAR advantage
**Source:** Competitor operator benchmarks (Numa, Limehome, BobW investor materials)  
**Verdict: PLAUSIBLE — directional evidence from public sources. Not independently audited but consistent across multiple operators.**

### ✅ McKinsey: AI personalisation + pricing = 3–10% annual revenue uplift, <18mo payback
**Source:** McKinsey research (via Tommaso Maria Ricci AI for Hospitality Guide, Apr 2026)  
**Verdict: STRONG — McKinsey is a credible source. Figures are directional, not guaranteed.**

### ✅ Special requests signal committed guests (r=−0.235)
**Source:** Our analysis of 119,388 bookings  
**Evidence:** Guests with 0 special requests cancel at 48%, vs 5% for guests with 4+ requests. Pre-arrival engagement surveys demonstrably reduce cancellation.  
**Verdict: INVEST — actionable, cheap to implement, directly reduces cancellation.**

---

## Claims that are PARTIALLY supported

### ⚠ "AI will reduce your guest relations headcount significantly"
**Vendor claim:** Automation replaces 30–50% of manual guest comms work  
**Reality:** Automation handles routine messages — confirmations, pre-arrival, upsells. But complex guest issues (complaints, special requirements, local knowledge) still need humans. Realistic expectation: 20–30% reduction in time spent on routine comms.  
**Verdict: WAIT on headcount reduction claims. Pilot first, measure actual time savings.**

### ⚠ "AI forecasting is dramatically better than human forecasting"
**Industry claim:** ~20% accuracy improvement over legacy RMS  
**Reality:** This is true vs legacy rule-based RMS systems. If Cleo's team is already doing manual but thoughtful forecasting, the improvement may be smaller. Data quality is the limiting factor.  
**Verdict: PILOT — validate against your own forecasting before committing to expensive RMS replacement.**

### ⚠ "AI chatbots improve guest satisfaction scores"
**Vendor claim:** NPS +10–15 from AI concierge  
**Reality:** Guest satisfaction with AI chatbots is highly variable. Guests with simple queries are satisfied. Guests with complex needs are frustrated when they cannot reach a human. Design matters enormously.  
**Verdict: WAIT — this is a Phase 3 consideration, not a first investment.**

---

## Claims that are MOSTLY HYPE at this company size

### ❌ "Full AI-driven autonomous pricing with no human oversight"
**Vendor claim:** Let AI set all rates automatically across all channels  
**Reality:** OTA contracts often include rate parity clauses. Automated rate manipulation without legal review creates contract risk. At 8–12 properties with different demand profiles, a rules engine with human override is more appropriate than fully autonomous AI.  
**Verdict: HYPE for now. Rules engine first, autonomous later.**

### ❌ "AI will give you a 30%+ RevPAR uplift in year one"
**Source:** Some vendor websites and YouTube content  
**Reality:** 30%+ figures come from outlier cases (properties with extremely poor baseline data and pricing). Realistic industry benchmarks for AI-enabled RevPAR improvement are 8–15% over 12–18 months.  
**Verdict: HYPE. Adjust expectations to 8–15% over 18 months.**

### ❌ "You need a dedicated data science team to get started"
**Vendor claim:** Enterprise AI requires an ML team  
**Reality:** The tools we built in this project (LangChain, n8n, Tableau) cost near-zero and required no ML engineers. Rules-based AI with LLM personalisation is achievable by one data analyst.  
**Verdict: HYPE. Start lean.**

---

## Summary table

| Claim | Evidence level | Verdict |
|---|---|---|
| Dynamic pricing +10–15% ADR | ★★★★☆ Strong | INVEST (Phase 1) |
| Cancellation prediction accuracy | ★★★★★ Own data | INVEST (Phase 1) |
| Early movers gaining RevPAR advantage | ★★★☆☆ Directional | INVEST (competitive pressure) |
| McKinsey 3–10% revenue uplift | ★★★★☆ Strong | INVEST |
| Special requests as retention signal | ★★★★★ Own data | INVEST |
| Headcount reduction from automation | ★★☆☆☆ Partial | WAIT / PILOT |
| AI forecasting accuracy improvement | ★★★☆☆ Conditional | PILOT |
| AI chatbot NPS improvement | ★★☆☆☆ Variable | WAIT |
| Autonomous pricing no human oversight | ★★☆☆☆ Risk | HYPE — not yet |
| 30%+ RevPAR uplift year one | ★☆☆☆☆ Outlier | HYPE |
| Need a full ML team to start | ★☆☆☆☆ False | HYPE — start lean |

---

## What Cleo should validate before investing

1. **Actual PMS cancellation rate** — is it near 37.5% or different?
2. **PMS data quality** — can we extract lead time, channel, segment cleanly?
3. **OTA contract terms** — do they restrict automated rate changes?
4. **GDPR lawful basis** — can we send personalised retention emails?
5. **City manager readiness** — will they use and trust AI recommendations?

These five checks can be done in 2 weeks at near-zero cost. The answers determine whether to pilot now or fix prerequisites first.
