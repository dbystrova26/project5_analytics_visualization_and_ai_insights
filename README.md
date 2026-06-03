# Pan-European Aparthotel AI Strategy — Project 5

**Sector:** Hospitality  
**Company profile:** Pan-European aparthotel chain (~500 employees, 8–12 cities) — modelled on operators like Numa, Limehome, BobW  
**Client:** Chleo, CEO  
**Bootcamp module:** Module 5 — AI Strategy & Business Impact

---

## Project overview

Chleo runs a tech-forward aparthotel chain across multiple European cities. The business model blends short-stay OTA bookings with longer corporate and relocation stays. She is sceptical of AI — she fears it is a black box and cannot be explained to her team or investors.

This project demonstrates that AI can be transparent, auditable, and immediately valuable for her business. It covers sector research, a BI dashboard, an AI agent that generates insights from real booking data, an n8n automation proof of concept, and a full cost/timeline estimate.

**Three use cases addressed:**
1. Dynamic pricing / revenue optimisation
2. Cancellation & no-show prediction
3. Automated guest communication & upsell agent

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
│   └── use_cases.md                # Use case proposals & justification
├── dashboard/
│   ├── dashboard.pbix              # PowerBI dashboard file
│   └── dashboard_documentation.md # Metrics, design rationale, usage guide
├── n8n/
│   ├── workflow.json               # Exportable n8n workflow
│   └── workflow_documentation.md  # Node-by-node explanation
├── agent/
│   ├── agent.py                    # LangChain agent entry point
│   ├── tools.py                    # 5 data analysis tools + preprocessing
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
| Hotel Booking Reservation 2024 | [Kaggle](https://www.kaggle.com/datasets/kundanbedmutha/hotel-booking-reservation) | 119,390 | Primary — cancellation prediction, ADR analysis, lead time |
| Hotel Prices in Europe 2024 | [Kaggle](https://www.kaggle.com/datasets/maelysboudier/hotel-prices-in-europe) | ~15,000 | Event-driven pricing benchmarks (Barcelona, Marseille) |
| Tourism & Hospitality Industry Analysis | [Kaggle](https://www.kaggle.com/datasets/smithmurphy/tourism-and-hospitality-industry-analysis-dataset) | ~500 | Sector KPI benchmarks |

All datasets are free and publicly available with a free Kaggle account.

---

## Setup

### Windows with Miniconda (recommended)

```bash
# 1. Scientific stack via conda — avoids C++ compiler errors on Windows
conda install pandas numpy scipy -y

# 2. LangChain + API stack via pip
pip install langchain>=0.3 langgraph>=0.2 langchain-anthropic>=0.2 langchain-openai>=0.2 \
    python-dotenv anthropic openai langsmith tiktoken httpx kaggle
```

### Mac / Linux

```bash
pip install -r requirements.txt
```

### API keys

```bash
cp .env.example .env
# Edit .env — add your Anthropic or OpenAI key and Kaggle token
```

Minimum `.env` needed to run everything:
```
ANTHROPIC_API_KEY=your_key_here
KAGGLE_API_TOKEN=KGAT_your_token_here
```

To get your Kaggle token: kaggle.com → profile → Settings → API → Create New Token.

---

## Step 1 — Download datasets

```bash
python download_data.py
```

### What this does

The script reads credentials from `.env` and calls the Kaggle API to download all three datasets. It supports three credential formats automatically — `KAGGLE_API_TOKEN` (new single-token format), `KAGGLE_USERNAME` + `KAGGLE_KEY` (classic), or `~/.kaggle/kaggle.json` (file-based).

Each dataset is downloaded as a zip, extracted, and saved as CSV files in `data/raw/`. Already-downloaded files are skipped automatically.

### Expected output

```
Kaggle credentials loaded from KAGGLE_API_TOKEN
Downloading: Hotel Booking Reservation 2024
  Saved: hotel_bookings.csv (21.3 MB)
Downloading: Hotel Prices in Europe 2024
  Saved: booking_bcn1.csv, booking_bcn2.csv, booking_mar1.csv, booking_mar2.csv
Downloading: Tourism & Hospitality Industry Analysis 2025
  Saved: Tourism_Hospitality_Industry_Analysis.csv

Done. 6 CSV file(s) in data/raw/
```

---

## Step 2 — Preprocess data

```bash
python tools.py --preprocess
```

### What this does

The preprocessing function inside `tools.py` cleans the raw booking dataset and saves a clean version to `data/processed/bookings_clean.csv`. Steps performed:

1. **Loads** `data/raw/hotel_bookings.csv` (119,390 rows, 33 columns)
2. **Drops columns** with more than 40% missing values
3. **Fills nulls** in key columns: `children` → 0, `country` → "Unknown", `agent` → 0, `company` → 0
4. **Removes invalid ADR rows** — any row where `adr < 0` or `adr >= 5000` is dropped (removes ~2 rows)
5. **Casts** `is_canceled` to integer (0/1)
6. **Saves** cleaned file to `data/processed/bookings_clean.csv`

### Expected output

```
Loading hotel_bookings.csv...
Loaded 119,390 rows, 33 columns
Removed 2 rows with invalid ADR
Saved: data/processed/bookings_clean.csv (119,388 rows)
```

### Key columns in the cleaned dataset

| Column | Type | Description |
|---|---|---|
| `is_canceled` | int (0/1) | Target variable — whether booking was cancelled |
| `lead_time` | int | Days between booking date and arrival |
| `adr` | float | Average Daily Rate (€) |
| `market_segment` | string | Direct, Corporate, OTA, Groups, etc. |
| `distribution_channel` | string | Direct, TA/TO, GDS, Corporate |
| `hotel` | string | City Hotel or Resort Hotel |
| `arrival_date_month` | string | Month of arrival |
| `arrival_date_year` | int | Year of arrival |
| `total_special_requests` | int | Number of special requests made |
| `required_car_parking_spaces` | int | Parking spaces requested |
| `previous_cancellations` | int | Prior cancellations by this guest |

---

## Step 3 — Run the agent

```bash
python agent.py
```

### What the agent does

The agent is a LangChain tool-calling loop that connects an LLM (Claude) to 5 data analysis functions. It works as follows:

**Step 1 — LLM plans the analysis**  
The LLM receives a system prompt describing its role (data analyst for an aparthotel CEO) and a user message asking for 5 business insights. It decides which tools to call and in what order.

**Step 2 — Tools execute against real data**  
Each tool loads `bookings_clean.csv`, runs a pandas/numpy calculation, and returns a formatted string. No data leaves your machine — all computation is local.

**Step 3 — LLM interprets results**  
After all tools return, the LLM synthesises the numbers into structured insights following a fixed format: headline, evidence, source, limitation, action.

**Step 4 — Output printed to terminal**  
All tool calls are printed as they happen (`→ Calling tool: ...`) so every step is visible and auditable — directly addressing Chleo's transparency concern.

### The 5 tools

| Tool | What it calculates | Key parameter |
|---|---|---|
| `cancellation_rate_by_segment` | Cancellation % grouped by any categorical column | `column` — e.g. `market_segment`, `distribution_channel`, `hotel` |
| `adr_statistics` | Mean, median, min, max ADR overall or by group | `group_by` — e.g. `arrival_date_month`, `market_segment` |
| `lead_time_analysis` | Cancellation rate per lead time bucket (0–2d, 3–6d, etc.) | fixed buckets |
| `booking_volume_trend` | Booking count by month/year | `period` — `month` |
| `correlation_with_cancellation` | Pearson r between numeric features and `is_canceled` | `top_n` — number of features to return |

### Agent output — 5 insights generated (actual run results)

**INSIGHT 1: Group bookings are your highest cancellation risk**  
Groups cancel at 61.1% (n=19,810) vs 15.3% for Direct and 18.7% for Corporate — 4x higher than the lowest-risk segment.  
*Action: Non-refundable deposits and binding group coordinator agreements.*

**INSIGHT 2: Long lead time bookings are cancellation time bombs**  
365+ day bookings cancel at 68.0% vs only 8.1% for 0–2 day bookings. Rate increases monotonically: 30–59d = 36.3%, 90–364d = 49.4%.  
*Action: Higher deposits for >90 day bookings; automated re-confirmation campaigns at 60/30/14 days.*

**INSIGHT 3: Travel agent channels underperform direct by 2.3x**  
TA/TO channel: 41.0% cancellation vs Direct: 17.5% — yet both have near-identical ADR (€117.96 vs €117.69). Equal pricing for 2.3x higher risk.  
*Action: Renegotiate TA/TO contracts; invest in direct channel marketing.*

**INSIGHT 4: City hotels cancel at 41–43% vs resort hotels at 27–30%**  
Gap is consistent across all locations (13–16pp), suggesting a property-type pattern not a location issue.  
*Action: Apply resort hotel retention practices to city portfolio.*

**INSIGHT 5: Special requests signal committed customers**  
Special requests correlate negatively with cancellation (r=–0.235); parking: r=–0.195. Lead time is the strongest positive predictor (r=+0.293).  
*Action: Flag zero-request bookings for retention campaigns; send pre-arrival preference surveys.*

---

## How to view the dashboard

1. Install [PowerBI Desktop](https://powerbi.microsoft.com/desktop/) (free, Windows)
2. Open `dashboard/dashboard.pbix`
3. If prompted for data source, point to `data/processed/bookings_clean.csv`

**Dashboard pages:**
- Executive overview — RevPAR, ADR, occupancy %, cancellation rate by city
- Cancellation analysis — by channel, lead time, monthly trend
- Pricing intelligence — ADR seasonality, occupancy vs ADR scatter

---

## How to run the evaluation

```bash
python insights_generator.py
```

Results are in `evaluation/evaluation_results.json`.  
Full LLM-as-judge report with judge prompt, scores, bias discussion, and recommendations is in `evaluation/insight_review.md`.

**Average scores across 5 insights:** Relevance 5.0 · Accuracy 4.6 · Actionability 4.8 · Clarity 4.8 · Overall 4.6

---

## Troubleshooting

| Error | Fix |
|---|---|
| `pandas build error` on Windows | Use `conda install pandas numpy scipy -y` instead of pip |
| `No Kaggle credentials found` | Add `KAGGLE_API_TOKEN=KGAT_xxx` to `.env` |
| `No API key found` | Add `ANTHROPIC_API_KEY=xxx` to `.env` |
| `model: claude-xxx not found` | Check available models: `python -c "import anthropic; from dotenv import load_dotenv; load_dotenv(); c=anthropic.Anthropic(); [print(m.id) for m in c.models.list().data]"` |
| `Processed dataset not found` | Run `python tools.py --preprocess` first |
| `ImportError: AgentExecutor` | Your LangChain version is newer — use the `agent.py` in this repo which uses `bind_tools` instead |

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | One of these two | Anthropic Claude API key |
| `OPENAI_API_KEY` | One of these two | OpenAI API key |
| `KAGGLE_API_TOKEN` | For download_data.py | New single-token format from Kaggle settings |
| `KAGGLE_USERNAME` + `KAGGLE_KEY` | Alternative to above | Classic Kaggle credential format |
| `LANGCHAIN_API_KEY` | Optional | LangSmith tracing key |
| `LANGCHAIN_PROJECT` | Optional | LangSmith project name |

Never commit your `.env` file — it is listed in `.gitignore`.
