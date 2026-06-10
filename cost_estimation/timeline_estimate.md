# Recommendation: Invest / Wait / Pilot?

**Recommendation: PILOT**

Run a 6–8 week pilot on 2 properties (Phase 1 of this plan) before committing full budget.
Pilot cost: €5–10K. Decision point: Week 6 with real cancellation and comms data.

**Why not invest fully now:**
- PMS data quality needs validation before committing to ML model build
- GDPR review required before sending automated guest emails at scale
- OTA contracts need legal check before pricing automation goes live
- City managers need to trust AI recommendations before chain-wide rollout

**Why not wait:**
- Direct competitors (Numa, Limehome, BobW) are already using AI in operations
- 71% of hospitality professionals say AI is having significant impact right now (Canary Technologies 2026)
- OTA commission draining 15–25% per booking continues every week without action
- EU serviced apartment sector is consolidating around tech-forward operators (HVS 2025)
- The cost of inaction compounds — each week of flat ADR pricing is recoverable revenue lost

**What would change this recommendation:**

| Condition | Changes to |
|---|---|
| Pilot shows ≥3pp cancellation reduction | Invest — proceed to Phase 2 scale |
| PMS data quality is very poor | Wait — fix data infrastructure first |
| OTA contracts block pricing automation | Pivot — scale comms only, skip UC1 |
| City managers refuse AI recommendations | Wait — invest in change management first |

---

## Why cancellation prediction first (not dynamic pricing)

Dynamic pricing (UC1) has the highest ROI but requires:
- Historical competitor rate data (not yet collected)
- OTA contract legal review before rate automation
- 12+ months of booking data for model training
- Higher build complexity (€9,500–€19,000 vs €5,000–€10,000)

Cancellation prediction (UC2) + guest comms (UC3) can go live in 6 weeks because:
- All required data (lead time, channel, segment) already exists in the PMS
- n8n workflow is already built and tested end-to-end
- ROI is immediate and measurable (cancellation rate week-on-week)
- Proves AI transparency to Chleo — every action logged, every decision explained

Dynamic pricing follows in Phase 3 once the data pipeline is established.

---

## Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| PMS data quality poor | Medium | High | Data audit in Week 1 before any build commitment |
| OTA contracts restrict rate automation | Medium | Medium | Legal review in Phase 3 before pricing goes live |
| City managers don't trust AI | Medium | High | Human override on every action; shadow mode first |
| GDPR compliance issue | Low | High | DPO review before Week 6 go-live |
| LLM generates incorrect guest info | Medium | High | All factual fields from PMS — LLM writes personalisation only |
| Model drift over time | Low | Medium | Quarterly retraining; monthly spot-checks |
| Pricing model causes rate conflicts | Low | High | Advisory mode only until acceptance rate >80% |

---

## Team roles and owners

| Role | Phase | Time | Responsibility |
|---|---|---|---|
| Data analyst | All phases | 1 FTE build, 0.25 FTE ongoing | Build, test, monitor, maintain |
| Revenue manager | All phases | 0.2 FTE | Champion, calibrate thresholds, approve pricing suggestions |
| City GM (pilot properties) | Phase 1 | 0.1 FTE | Context, feedback, adoption |
| IT / PMS admin | Phase 1 | 2 days | PMS webhook access |
| DPO (Data Protection Officer) | Phase 1 | 1 day | GDPR review sign-off |
| Legal (OTA contracts) | Phase 3 | 2 days | Contract review before pricing automation |
| CEO (Chleo) | Phase 1, 2, 3 | 3 hours total | Decision approvals at each Go/No-Go gate |
