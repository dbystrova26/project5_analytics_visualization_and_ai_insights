# Pan-European Aparthotel AI Strategy — Project 5

**Sector:** Hospitality  
**Company profile:** Pan-European aparthotel chain (~500 employees, 8–12 cities) — modelled on operators like Numa, Limehome, BobW  
**Client:** Chleo, CEO  
**Bootcamp module:** Module 5 — AI Strategy & Business Impact

> AI consulting project: cancellation prediction, dynamic pricing & guest automation for a pan-European aparthotel chain. LangChain · Tableau · n8n

---

## Project snapshot

* **Sector:** Hospitality
* **Company Size:** Large (~500 employees, 8–12 European cities — Numa / Limehome / BobW style)
* **Use Cases:**
   * Cancellation & no-show prediction
   * Dynamic pricing / revenue optimisation
   * Automated guest communication & upsell agent
* **Dashboard Focus:** Cancellation rate by channel, lead time risk curve, city vs resort comparison, special requests signal, monthly trend, market segment risk table
* **n8n Workflow:** Automated retention offer — PMS webhook → filter high-risk booking → AI generates personalised message → send email/SMS → log to Google Sheets
* **Agent Insights:** Groups cancel at 61.1% vs 15.3% direct · OTA channel 2.3× riskier than direct at equal ADR · Long lead time bookings (365d+) cancel at 68% · City hotels cancel 50% more than resort · Special requests signal committed guests (r=–0.235)
* **Cost Considerations:** €15K–€30K upfront for all 3 use cases · <1 month payback · LLM API ~€200–€500/month · Self-hosted n8n = free · GDPR compliance review required before production
* **Data:** All agent insights from real analysis of 119,388 booking records (Hotel Booking Reservation 2024, Kaggle)

---

## Key findings from real data (119,388 bookings)

All numbers below come from running the LangChain agent on the real Kaggle dataset.

### UC1 — Dynamic Pricing

| Finding | Number | Implication |
|---|---|---|
| Overall mean ADR | €115.79 | Baseline pricing across all segments |
| Peak ADR month | October €118.43 | Only €5.42 above the lowest month |
| Low ADR month | May €113.00 | Near-flat seasonality despite demand swings |
| Volume swing peak vs low | 20.9% | Demand varies 20% but price barely moves |
| Weekend vs weekday ADR | €115.50 vs €115.85 | No weekend premium — pricing opportunity |
| Highest ADR segment | Offline TA/TO €117.85 | But also highest cancellation — net revenue lower |
| Lowest ADR segment | Corporate €114.36 | Most reliable bookers, underpriced |
| Long stay ADR drop | 8–14 nights: €112.41 | Extended stays discounted — confirm if intentional |

**Key insight:** The chain has almost zero dynamic pricing in place. A €5.42 ADR gap across the full year despite 20.9% volume swings means revenue is being left on the table every peak period.

---

### UC2 — Cancellation Prediction

| Finding | Number | Implication |
|---|---|---|
| Overall cancellation rate | 37.5% | 44,010 of 117,429 bookings cancelled |
| Groups segment | 61.1% cancel (n=19,810) | Highest risk — 4× Direct rate |
| TA/TO channel | 41.0% cancel | 2.3× higher than Direct at same ADR |
| Direct channel | 17.5% cancel | Lowest risk — prioritise direct bookings |
| 365d+ lead time | 68.0% cancel | Counter-intuitive — long advance = high risk |
| 0–2d lead time | 8.1% cancel | Last-minute = most committed |
| Lead time correlation | r=+0.293 | Strongest single numeric predictor |
| Special requests | r=–0.235 | Protective signal — engaged guests cancel less |
| City hotels | 40.6–43.2% | 13–16pp higher than resort hotels |
| Resort hotels | 26.3–29.9% | Structural difference, not location |
| No Deposit bookings | highest cancel rate | Non-refundable deposits nearly eliminate cancellations |

**Key insight:** Three levers explain most cancellations — channel mix (OTA 2.3× riskier), booking timing (365d+ bookings 68% cancel), and guest segment (groups 61.1%). Fixing policy on these three reduces cancellations without any ML model needed.

---

### UC3 — Guest Communication & Upsell

| Finding | Number | Implication |
|---|---|---|
| Repeat guest rate | 2.8% | Very low loyalty — opportunity to build programme |
| Guests without parking booked | 93.8% | Massive pre-arrival parking upsell pool |
| 1-night stays | 17.4% | Extend-your-stay offer target |
| BB/SC meal plan guests | 86.2% | On basic plans — meal upgrade upsell opportunity |
| Repeat guest cancel rate | 16.2% vs 38.1% first-time | Repeat guests are far more committed |
| Repeat guest ADR | €75 vs €104 first-time | Repeat guests pay less — loyalty pricing review needed |
| Portugal (PRT) | 30.7% of bookings, 68% cancel | Largest origin market but highest cancel rate |
| Transient customers | 75%+ of bookings, 41% cancel | Main segment — personalised comms highest impact |
| Special requests r=–0.235 | engaged guests cancel 2× less | Pre-arrival engagement surveys reduce cancellation |

**Key insight:** 93.8% of guests have no parking booked, 86.2% are on basic meal plans, and 17.4% stay only 1 night. Each is a direct upsell trigger that an automated guest comms agent can action before arrival with no manual effort.

---

## Repository structure

```
project/
├── data/
│   ├── raw/                        # Original downloaded datasets (not committed)
│   └── processed/                  # Cleaned CSVs output by preprocessing
├── research/
│   ├── sector_research.md          # EU aparthotel market analysis
│   ├── opportunities_risks.md      # AI opportunity & risk mapping
│   └── use_cases.md                # Use case proposals with real data evidence
├── dashboard/
│   ├── dashboard.twbx              # Tableau dashboard file
│   ├── dashboard_documentation.md  # Metrics, design rationale, usage guide
│   └── tableau_dashboard_prototype.py  # Python prototype — 3 pages, all use cases
├── n8n/
│   ├── workflow.json               # Importable n8n workflow
│   └── workflow_documentation.md  # Node-by-node explanation & setup guide
├── agent/
│   ├── agent.py                    # LangChain agent — all 3 use cases
│   ├── tools.py                    # 11 data analysis tools
│   └── insights_generator.py      # Standalone insight formatter
├── evaluation/
│   ├── insight_review.md           # LLM-as-judge evaluation report
│   └── evaluation_results.json    # Structured scores for all 5 insights
├── cost_estimation/
│   ├── cost_analysis.md            # Per-use-case cost breakdown + ROI
│   └── timeline_estimate.md        # 4-phase 14-week rollout plan
├── download_data.py                # Downloads all 3 datasets from Kaggle
├── requirements.txt
├── README.md
└── .env.example
```

---

## Datasets

| Dataset | Source | Rows | Use in project |
|---|---|---|---|
| Hotel Booking Reservation 2024 | [Kaggle](https://www.kaggle.com/datasets/kundanbedmutha/hotel-booking-reservation) | 119,390 | Primary — all 3 use cases |
| Hotel Prices in Europe 2024 | [Kaggle](https://www.kaggle.com/datasets/maelysboudier/hotel-prices-in-europe) | ~15,000 | Event-driven pricing benchmarks |
| Tourism & Hospitality Industry Analysis | [Kaggle](https://www.kaggle.com/datasets/smithmurphy/tourism-and-hospitality-industry-analysis-dataset) | ~500 | Sector KPI benchmarks |

All datasets are free and publicly available with a free Kaggle account.

---

## Setup

### Windows with Miniconda (recommended)

```bash
# Scientific stack via conda — avoids C++ compiler errors on Windows
conda install pandas numpy scipy -y

# LangChain + API stack via pip
pip install langchain>=0.3 langgraph>=0.2 langchain-anthropic>=0.2 langchain-openai>=0.2 \
    python-dotenv anthropic openai langsmith tiktoken httpx kaggle matplotlib seaborn
```

### Mac / Linux

```bash
pip install -r requirements.txt
```

### API keys

```bash
cp .env.example .env
# Add ANTHROPIC_API_KEY and KAGGLE_API_TOKEN
```

---

## Step 1 — Download datasets

```bash
python download_data.py
```

Reads `KAGGLE_API_TOKEN` from `.env`, downloads all 3 datasets to `data/raw/`.

**Expected output:**
```
Saved: hotel_bookings.csv (21.3 MB)
Saved: booking_bcn1.csv, booking_bcn2.csv, booking_mar1.csv, booking_mar2.csv
Saved: Tourism_Hospitality_Industry_Analysis.csv
Done. 6 CSV file(s) in data/raw/
```

---

## Step 2 — Preprocess data

```bash
cd agent
python tools.py --preprocess
```

Cleans `hotel_bookings.csv` and saves to `data/processed/bookings_clean.csv`.

**What it does:**
1. Loads 119,390 rows, 33 columns
2. Drops columns with >40% missing values
3. Fills nulls — `children` → 0, `country` → "Unknown"
4. Removes invalid ADR rows (removes ~2 rows)
5. Adds `total_nights` derived column
6. Saves 119,388 clean rows

**Key columns used across all 3 use cases:**

| Column | UC | Description |
|---|---|---|
| `is_canceled` | UC2 | Target variable (0/1) |
| `lead_time` | UC1, UC2 | Days between booking and arrival |
| `adr` | UC1, UC3 | Average Daily Rate (€) |
| `market_segment` | UC1, UC2, UC3 | Direct, Corporate, Groups, Online TA etc. |
| `distribution_channel` | UC2 | Direct, TA/TO, GDS, Corporate |
| `hotel` | UC2 | City Hotel or Resort Hotel |
| `arrival_date_month` | UC1 | Month of arrival |
| `stays_in_weekend_nights` | UC1, UC3 | Weekend nights booked |
| `stays_in_week_nights` | UC1, UC3 | Weekday nights booked |
| `meal` | UC3 | BB, HB, FB, SC — upsell signal |
| `deposit_type` | UC2 | No Deposit / Non Refund / Refundable |
| `customer_type` | UC2, UC3 | Transient, Group, Contract |
| `is_repeated_guest` | UC3 | Loyalty signal |
| `country` | UC3 | Origin market for personalisation |
| `total_of_special_requests` | UC2, UC3 | Engagement signal (r=–0.235) |
| `required_car_parking_spaces` | UC2, UC3 | Commitment + upsell signal |

---

## Step 3 — Run the agent

```bash
cd agent
python agent.py
```

### What the agent does

A LangChain tool-calling loop connecting an LLM (Claude) to 11 data analysis tools across all 3 use cases. Every tool call is printed to terminal — fully transparent and auditable.

### The 11 tools

**UC1 — Dynamic Pricing:**

| Tool | What it calculates |
|---|---|
| `adr_statistics` | Mean, median, min, max ADR overall or by group |
| `seasonal_pricing_analysis` | ADR + volume + cancellation rate by month |
| `weekend_vs_weekday_adr` | ADR comparison for weekend vs weekday stays |
| `stay_length_adr_analysis` | ADR by stay length bucket (1 night through 15+) |

**UC2 — Cancellation Prediction:**

| Tool | What it calculates |
|---|---|
| `cancellation_rate_by_segment` | Cancellation % by any categorical column |
| `lead_time_analysis` | Cancellation rate per lead time bucket |
| `correlation_with_cancellation` | Pearson r of all numeric features with is_canceled |
| `deposit_type_cancellation` | Cancellation rate by deposit type |

**UC3 — Guest Communication & Upsell:**

| Tool | What it calculates |
|---|---|
| `upsell_opportunity_analysis` | Room upgrade gap, meal plan dist, parking, 1-night stays |
| `repeat_guest_analysis` | Repeat vs first-time cancel rate, ADR, engagement |
| `guest_origin_analysis` | Top countries by volume, cancel rate, ADR |

### Real agent output — insights from 119,388 bookings

**[UC2] INSIGHT 1: Group bookings are your highest cancellation risk**
Groups cancel at **61.1%** (n=19,810) vs 15.3% Direct — 4× the lowest-risk segment.
*Action: Non-refundable deposits and binding group coordinator agreements.*

**[UC2] INSIGHT 2: Long lead time bookings are cancellation time bombs**
365d+ bookings cancel at **68.0%** vs 8.1% for 0–2 day bookings. Rate increases monotonically.
*Action: Higher deposits for >90 day bookings; re-confirmation campaigns at 60/30/14 days.*

**[UC2] INSIGHT 3: OTA channels underperform direct by 2.3×**
TA/TO: **41.0%** cancel vs Direct: **17.5%** — yet ADR is nearly identical (€117.96 vs €117.69).
*Action: Renegotiate OTA contracts; shift budget to direct channel marketing.*

**[UC2] INSIGHT 4: City hotels cancel 50% more than resort hotels**
City: 40.6–43.2% vs Resort: 26.3–29.9% — gap consistent across all locations.
*Action: Apply resort hotel retention practices to city portfolio.*

**[UC2] INSIGHT 5: Special requests signal committed customers**
Special requests: r=–0.235 · Parking: r=–0.195 · Lead time: r=+0.293 (strongest predictor).
*Action: Flag zero-request bookings for retention campaigns.*

**[UC1] INSIGHT 6: Near-flat seasonality despite 20.9% volume swing**
ADR gap October vs May: only **€5.42** despite 20.9% more bookings in peak months.
*Action: Implement dynamic pricing — even modest rate increases in peak months add significant revenue.*

**[UC1] INSIGHT 7: Weekend pricing premium is missing**
Weekend-heavy stays: **€115.50** vs weekday-heavy: **€115.85** — weekdays actually price higher.
*Action: Add weekend surcharge; leisure guests booking Fri–Sun are less price-sensitive.*

**[UC3] INSIGHT 8: 93.8% of guests have no parking booked**
Massive pre-arrival upsell pool — parking offer in welcome message costs nothing to automate.
*Action: Include parking upsell in every pre-arrival guest communication.*

**[UC3] INSIGHT 9: 86.2% of guests are on basic meal plans**
BB and SC guests are the majority — meal upgrade offers at check-in have a large addressable base.
*Action: Automated mid-stay message offering HB upgrade at discounted rate.*

**[UC3] INSIGHT 10: Repeat guests cancel at half the rate but pay 28% less**
Repeat: **16.2% cancel, €75 ADR** vs First-time: **38.1% cancel, €104 ADR**.
*Action: Review loyalty pricing — repeat guests are the most valuable segment but currently underpriced.*

---

## Step 4 — Dashboard prototype

```bash
python dashboard/tableau_dashboard_prototype.py
```

Generates 3 PNG files — one per use case — as a build guide for Tableau:
- `dashboard_uc1_pricing.png` — Dynamic pricing: ADR seasonality, volume vs ADR scatter, segment comparison
- `dashboard_uc2_cancellation.png` — Cancellation: channel rates, lead time curve, monthly trend, risk table
- `dashboard_uc3_upsell.png` — Upsell: meal plans, repeat guests, country origins, stay length, customer types

**To build in Tableau:**
1. Open Tableau Desktop or [Tableau Public](https://public.tableau.com) (free)
2. Connect to `data/processed/bookings_clean.csv`
3. Build each chart following `dashboard/dashboard_documentation.md`
4. Save as `dashboard/dashboard.twbx`

---

## Step 5 — Evaluation

```bash
cd agent && python insights_generator.py
```

Full LLM-as-judge report: `evaluation/insight_review.md`
Structured scores: `evaluation/evaluation_results.json`

**Average scores (LLM-as-judge, claude-sonnet-4-6):**

| Criterion | Score |
|---|---|
| Relevance | 5.0 / 5 |
| Accuracy | 4.6 / 5 |
| Actionability | 4.8 / 5 |
| Clarity | 4.8 / 5 |
| **Overall** | **4.6 / 5** |

---

## n8n workflow

**Status: ✅ Tested and working end-to-end**

The cancellation retention workflow was built and tested on a self-hosted n8n instance. A real booking payload triggered the full flow — the AI generated a personalised retention email which was delivered to Gmail in ~2 seconds.

**Flow:** PMS webhook → filter high-risk booking → OpenAI generates message → Gmail delivery → Google Sheets audit log

**Live test result:**
- Webhook received booking for Maria Schmidt, Berlin Mitte Apt 12, lead_time=2, Booking.com
- Filter correctly identified as HIGH RISK (OTA + last-minute)
- GPT-3.5-turbo generated: *"We are thrilled to have you staying... complimentary late check-out until 2pm... https://aparthotel.com/book?ref=retention"*
- Email delivered to dbystrova26@gmail.com within 2 seconds

**To import and run:**
1. Sign up free at [n8n.io](https://n8n.io) or use self-hosted
2. New workflow → three dots → **Import from file** → upload `n8n/workflow.json`
3. Configure: OpenAI API key (Header Auth) + Gmail OAuth2
4. Test with curl:
```bash
curl -X POST "https://YOUR_N8N/webhook-test/new-booking" \
  -H "Content-Type: application/json" \
  -d "{\"guest_name\":\"Maria Schmidt\",\"guest_email\":\"guest@email.com\",\"property\":\"Berlin Mitte Apt 12\",\"check_in\":\"2024-12-17\",\"lead_time_days\":2,\"booking_channel\":\"Booking.com\",\"deposit_paid\":false}"
```

Full setup guide with credentials, known issues, and workarounds: `n8n/workflow_documentation.md`

---

## Troubleshooting

| Error | Fix |
|---|---|
| `pandas build error` on Windows | `conda install pandas numpy scipy -y` |
| `No Kaggle credentials` | Add `KAGGLE_API_TOKEN=KGAT_xxx` to `.env` |
| `No API key found` | Add `ANTHROPIC_API_KEY=xxx` to `.env` |
| `model not found` | Run `python -c "import anthropic; from dotenv import load_dotenv; load_dotenv(); c=anthropic.Anthropic(); [print(m.id) for m in c.models.list().data]"` |
| `Processed dataset not found` | Run `python tools.py --preprocess` from `agent/` folder |
| `ImportError: AgentExecutor` | Use `agent.py` in this repo — uses `bind_tools` not removed `AgentExecutor` |
| Dashboard saves to wrong path | Run from inside `dashboard/` folder |

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | One of these two | Anthropic Claude API key |
| `OPENAI_API_KEY` | One of these two | OpenAI API key |
| `KAGGLE_API_TOKEN` | For download_data.py | New single-token format |
| `KAGGLE_USERNAME` + `KAGGLE_KEY` | Alternative | Classic Kaggle credentials |
| `LANGCHAIN_API_KEY` | Optional | LangSmith tracing |
| `LANGCHAIN_PROJECT` | Optional | LangSmith project name |

Never commit `.env` — it is in `.gitignore`.
