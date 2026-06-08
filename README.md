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

## Recommendation for Cleo

**Should Cleo invest now, wait, or run a pilot?**

**→ PILOT** — 6–8 weeks, 2 properties, €5–10K, clear Go/No-Go at Week 6.

Not invest fully (PMS data quality and GDPR need validation first). Not wait (competitors Numa, Limehome, BobW are not waiting — 71% of hospitality operators say AI is already having significant impact). Run a focused pilot on cancellation prediction + guest comms, measure real cancellation rate change, then decide on full rollout.

Full reasoning: `cost_estimation/timeline_estimate.md` → Recommendation section  
Market evidence: `research/ai_adoption_signals.md`  
Hype vs evidence: `research/hype_vs_evidence.md`

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
│   ├── use_cases.md                # Use case proposals with real data evidence
│   ├── use_case_discovery.md       # Stakeholder mapping, use case selection & justification
│   ├── market_research.md          # AI adoption ROI data, precedents, market signals
│   ├── ai_adoption_signals.md      # 7 adoption signals — what's real vs hype in EU hospitality
│   └── hype_vs_evidence.md         # Claim-by-claim analysis: invest / pilot / hype
├── dashboard/
│   ├── dashboard.twbx              # Tableau dashboard — 6 charts, UC2 cancellation
│   ├── dashboard_documentation.md  # Metrics, design rationale, usage guide
│   ├── tableau_dashboard_prototype.py  # Python prototype — 3 pages, all use cases
│   └── uc2_cancellation_dashboard.html # Interactive Plotly dashboard (open in browser)
├── n8n/
│   ├── workflow.json               # Importable n8n workflow
│   └── workflow_documentation.md  # Node-by-node explanation, test results, known issues
├── agent/
│   ├── agent.py                    # LangChain agent — all 3 use cases
│   ├── tools.py                    # 11 data analysis tools
│   └── insights_generator.py      # 10 real insights from 119,388 booking records
├── evaluation/
│   ├── insight_review.md           # LLM-as-judge evaluation report
│   ├── raw_insights.json           # 10 structured insights from agent run
│   └── evaluation_results.json    # Scores per insight (relevance, accuracy, actionability, clarity)
├── cost_estimation/
│   ├── cost_analysis.md            # Per-use-case cost breakdown + Year 1 ROI estimates
│   └── timeline_estimate.md        # Invest/wait/pilot rec + 4-phase plan + risks + team roles
├── sources.md                      # All sources labelled by type (data/report/case study/vendor)
├── download_data.py                # Downloads all 3 datasets from Kaggle
├── requirements.txt
├── README.md
└── .env.example
```

---

## Datasets

All datasets are free and publicly available with a free Kaggle account.

---

### Primary dataset — Hotel Booking Reservation 2024

**🔗 [kaggle.com/datasets/kundanbedmutha/hotel-booking-reservation](https://www.kaggle.com/datasets/kundanbedmutha/hotel-booking-reservation)**

| Property | Detail |
|---|---|
| Rows | 119,390 (119,388 after cleaning) |
| Columns | 33 |
| Period covered | January 2022 – December 2024 |
| Property types | City Hotels and Resort Hotels |
| Cities / regions | Multiple Indian cities (Mumbai, Delhi, Bangalore, Goa, Jaipur, Kolkata, Chennai, Hyderabad, Indore, Lucknow, Pune, Kochi, Chandigarh, Ahmedabad) across City Hotel and Resort Hotel property types |
| Guest origin | 177 countries — top markets: Portugal (30.7%), UK, France, Spain, Germany, Ireland, Italy |
| File size | 21.3 MB |

**Columns in the dataset:**

| Column | Type | Description |
|---|---|---|
| `hotel` | string | Property type: City Hotel or Resort Hotel |
| `is_canceled` | int (0/1) | Cancellation flag — our prediction target (UC2) |
| `lead_time` | int | Days between booking date and arrival date |
| `arrival_date_year` | int | Year of arrival (2022–2024) |
| `arrival_date_month` | string | Month of arrival (January–December) |
| `arrival_date_week_number` | int | ISO week number |
| `arrival_date_day_of_month` | int | Day of month |
| `stays_in_weekend_nights` | int | Nights staying on Saturday/Sunday |
| `stays_in_week_nights` | int | Nights staying Monday–Friday |
| `adults` | int | Number of adults |
| `children` | int | Number of children |
| `babies` | int | Number of babies |
| `meal` | string | Meal plan: BB (Bed & Breakfast), HB (Half Board), FB (Full Board), SC (Self Catering) |
| `country` | string | Guest country of origin (ISO 3166-1 alpha-3) |
| `market_segment` | string | Direct, Corporate, Online TA, Offline TA/TO, Groups, Aviation, Complementary |
| `distribution_channel` | string | Direct, TA/TO, GDS, Corporate |
| `is_repeated_guest` | int (0/1) | Whether guest has stayed before |
| `previous_cancellations` | int | Number of prior cancellations by this guest |
| `previous_bookings_not_canceled` | int | Number of prior completed stays |
| `reserved_room_type` | string | Room category reserved (A–L) |
| `assigned_room_type` | string | Room category actually assigned |
| `booking_changes` | int | Number of modifications to booking |
| `deposit_type` | string | No Deposit / Non Refund / Refundable |
| `agent` | int | Travel agent ID (nullable) |
| `company` | int | Corporate account ID (nullable) |
| `days_in_waiting_list` | int | Days on waiting list before confirmation |
| `customer_type` | string | Transient, Transient-Party, Contract, Group |
| `adr` | float | Average Daily Rate in € |
| `required_car_parking_spaces` | int | Parking spaces requested |
| `total_of_special_requests` | int | Number of special requests made |
| `reservation_status` | string | Check-Out, Canceled, No-Show |
| `reservation_status_date` | date | Date of last status change |

**Why this dataset is ideal for Cleo's business case:**

1. **Covers exactly the signals we need.** `is_canceled`, `lead_time`, `distribution_channel`, `market_segment`, `deposit_type`, and `total_of_special_requests` are all present and clean. These are precisely the fields a real PMS captures — making findings directly applicable to Cleo's actual data.

2. **Large enough to be statistically meaningful.** At 119,388 rows, even sub-segments have enough data to calculate reliable cancellation rates. The Groups segment alone has 19,810 bookings — sufficient for confident analysis.

3. **Real booking behaviour, not synthetic data.** The dataset captures genuine booking and cancellation patterns including the counter-intuitive lead time effect (365d+ = 68% cancel) that synthetic data would not reproduce.

4. **Covers all three use cases.** One dataset supports dynamic pricing analysis (ADR, month, segment), cancellation prediction (is_canceled, lead_time, channel), and upsell opportunity analysis (meal, parking, stay length, repeat guest).

5. **Industry-standard column structure.** The columns map directly to standard PMS field names. `adr`, `market_segment`, `distribution_channel`, `deposit_type` are terminology Cleo's revenue managers will immediately recognise.

6. **Multi-year coverage.** Three years of data (2022–2024) captures post-pandemic demand normalisation — more representative of current booking behaviour than pre-COVID datasets.

**Limitation to disclose to Cleo:** The dataset covers Indian hotel properties, not EU aparthotels specifically. ADR levels (€103–€118) and city/resort split differ from EU markets. Cancellation rate patterns (37.5% overall, 68% for 365d+ bookings) are directional benchmarks — Cleo should validate against her own PMS data before committing to model thresholds.

---

### Supporting datasets

| Dataset | Link | Rows | Used for |
|---|---|---|---|
| Hotel Prices in Europe 2024 | [Kaggle](https://www.kaggle.com/datasets/maelysboudier/hotel-prices-in-europe) | ~15,000 | Event-driven pricing benchmarks, Barcelona & Marseille |
| Tourism & Hospitality Industry Analysis | [Kaggle](https://www.kaggle.com/datasets/smithmurphy/tourism-and-hospitality-industry-analysis-dataset) | ~500 | Sector KPI benchmarks (RevPAR, occupancy) |

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
