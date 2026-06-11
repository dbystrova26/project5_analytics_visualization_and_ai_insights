# Sources

**Project 5 — AI Investment Case for Cleo**
Daria Bystrova · Ironhack · June 2026

All numbers, statistics, and claims in this project are traceable to one of the sources below.
Sources marked **[MARKET]** support the AI adoption and market context slides.
Sources marked **[DATA]** are the primary dataset used for all UC2 analysis.
Sources marked **[TOOL]** are the AI/automation tools used in the built solution.
Directional estimates (competitor AI maturity, RevPAR uplift by use case) are noted explicitly — they are composite benchmarks, not single independently-audited figures.

---

## Primary Dataset

**[DATA-1] Kaggle Hotel Booking Demand Dataset (2024 version)**
- Used for: all UC2 cancellation analysis — 119,388 booking records, 33 columns
- Key figures derived: 37.5% overall cancellation rate, 44,010 cancellations, 61.1% group cancel rate (n=19,810), 41% OTA vs 17.5% Direct cancel rate, 68% cancel rate for 365d+ advance bookings, r=+.293 lead time correlation, r=−.235 special requests correlation, €118 average ADR, €5.42 ADR gap vs 20.9% demand swing
- URL: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
- Note: Dataset reflects a hotel booking system; applied to Cleo's context as a directional proxy. Limitations documented in agent output (raw_insights.json).

---

## Market & Industry Sources

**[MARKET-1] Canary Technologies — 2026 Hospitality Technology Trends Report**
- Used for: "71% of hospitality professionals say AI has significant operational impact"
- Also: "50% planned adoption by 2024", "29% not yet / unsure"
- URL: https://www.canarytechnologies.com/post/hospitality-technology-trends

**[MARKET-2] The Business Research Company — AI in Hospitality Market Report, April 2026**
- Used for: "$2.28B AI hospitality market size by 2030 (CAGR 57.7%)"
- Market size trajectory: $0.23B (2025) → $2.28B (2030)
- URL: https://www.thebusinessresearchcompany.com/report/artificial-intelligence-in-hospitality-global-market-report

**[MARKET-3] Hotel Technology News — December 2025**
- Used for: "+17% total revenue uplift for AI-enabled revenue management vs non-adopters"
- URL: https://hoteltechnologynews.com

**[MARKET-4] McKinsey & Company / Tommaso Maria Ricci — April 2026**
- Used for: "<18 months payback on AI pricing & personalisation investment"
- URL: https://www.mckinsey.com/industries/travel-logistics-and-infrastructure/our-insights

**[MARKET-5] HVS — European Serviced Apartments Report, July 2025**
- Used for: EU aparthotel market context; competitive landscape reference
- URL: https://www.hvs.com/article/european-serviced-apartments

**[MARKET-6] Competitor public investor and press materials, 2024–2025**
- Used for: "8–14% RevPAR advantage for EU tech-forward operators vs peers"
- Used for: EU aparthotel AI maturity estimates — BobW (~95%), Limehome (~90%), Numa (~90%), Accor Adagio (~70%), Staycity (~55%)
- ⚠ Directional estimates from composite sources — not single independently-audited figures
- Sources: BobW investor materials; Limehome press releases; Numa funding announcements; Accor group reports

---

## Tools & Platforms Used

**[TOOL-1] LangChain**
- Used for: agent framework — bind_tools loop, tool dispatching, LLM orchestration
- URL: https://www.langchain.com

**[TOOL-2] Anthropic Claude (claude-haiku) / OpenAI GPT-3.5 & GPT-4**
- Used for: LLM core in the agent (model-agnostic via .env); GPT-3.5 used in the tested n8n retention email workflow
- Anthropic: https://www.anthropic.com
- OpenAI: https://www.openai.com

**[TOOL-3] pandas (Python)**
- Used for: all 11 deterministic analysis tools (cancel_rate, lead_time, correlation, deposit_type, adr_statistics, seasonal_pricing, weekend_adr, stay_length_adr, upsell_opportunity, repeat_guest, guest_origin)
- URL: https://pandas.pydata.org

**[TOOL-4] n8n**
- Used for: tested retention automation workflow — webhook trigger, booking filter, Gmail send
- URL: https://n8n.io

**[TOOL-5] Tableau Desktop**
- Used for: UC2 Cancellation & No-Show Risk Dashboard (6 views, connected to bookings_clean.csv)
- URL: https://www.tableau.com

**[TOOL-6] Plotly (Python)**
- Used for: AI Adoption Evidence Dashboard — self-contained interactive HTML
- URL: https://plotly.com/python

---

## Data Integrity Notes

- All UC2 analysis numbers (cancellation rates, correlations, ADR figures) derive from [DATA-1] and are confirmed in the deck
- UC1 and UC3 agent tool outputs exist in `raw_insights.json` but were not presented in the deck — those findings should not be quoted without checking that file
- Per-dimension evaluation scores (Relevance, Accuracy, Actionability, Clarity) were not individually recorded in this project run — only the overall average of 4.6/5 is confirmed
- Charts 4 and 6 of the AI Adoption Dashboard (EU competitor maturity, RevPAR uplift by use case) are directional estimates from composite sources, not single independently-audited figures — explicitly flagged in the dashboard footnote
- OTA commission range of 15–25% is an industry-standard figure widely cited across hospitality literature; no single source is cited as it is common knowledge in the sector
