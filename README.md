# Pan-European Aparthotel AI Strategy — Project 5

**Sector:** Hospitality  
**Company profile:** Pan-European aparthotel chain (~500 employees, 8–12 cities) — modelled on operators like Numa, Limehome, BobW  
**Client:** Chleo, CEO  
**Bootcamp module:** Module 5 — AI Strategy & Business Impact

---

## Project overview

Chleo runs a tech-forward aparthotel chain across multiple European cities. The business model blends short-stay OTA bookings with longer corporate and relocation stays. She is sceptical of AI — she fears it is a black box and cannot be explained to her team or investors.

This project demonstrates that AI can be transparent, auditable, and immediately valuable for her business. It covers sector research, a BI dashboard, an AI agent that generates insights, an n8n automation proof of concept, and a full cost/timeline estimate.

**Three use cases addressed:**
1. Dynamic pricing / revenue optimisation
2. Cancellation & no-show prediction
3. Automated guest communication & upsell agent

---

## Repository structure

```
bi-dashboard-project/
├── data/
│   ├── raw/                        # Original downloaded datasets (not committed)
│   └── processed/                  # Cleaned CSVs output by preprocessing script
├── research/
│   ├── sector_research.md
│   ├── opportunities_risks.md
│   └── use_cases.md
├── dashboard/
│   ├── dashboard.pbix              # PowerBI dashboard file
│   └── dashboard_documentation.md
├── n8n/
│   ├── workflow.json               # Exportable n8n workflow
│   └── workflow_documentation.md
├── agent/
│   ├── agent.py                    # LangChain agent entry point
│   ├── tools.py                    # Data analysis tools
│   └── insights_generator.py      # Insight generation & formatting
├── evaluation/
│   ├── insight_review.md
│   └── evaluation_results.json
├── cost_estimation/
│   ├── cost_analysis.md
│   └── timeline_estimate.md
├── download_data.py                # Downloads all datasets from Kaggle
├── requirements.txt
├── README.md
└── .env.example
```

---

## Datasets used

| Dataset | Source | Use |
|---|---|---|
| Hotel Booking Reservation 2024 | [Kaggle](https://www.kaggle.com/datasets/kundanbedmutha/hotel-booking-reservation) | Cancellation prediction, pricing analysis |
| Hotel Prices in Europe (2024) | [Kaggle](https://www.kaggle.com/datasets/maelysboudier/hotel-prices-in-europe) | Event-driven pricing, ADR benchmarks |
| Tourism & Hospitality Industry Analysis | [Kaggle](https://www.kaggle.com/datasets/smithmurphy/tourism-and-hospitality-industry-analysis-dataset) | Sector KPI benchmarks |

All datasets are free and publicly available. A free Kaggle account is required.

---

## Setup instructions

### 1. Clone the repository

```bash
git clone https://github.com/dbystrova26/project5_analytics_visualization_and_ai_insights.git
cd project5_analytics_visualization_and_ai_insights
```

### 2. Install dependencies

**On Windows with Miniconda (recommended):**

```bash
# Scientific stack via conda — avoids C++ compiler errors on Windows
conda install pandas numpy scipy -y

# LangChain stack via pip
pip install langchain>=0.3 langgraph>=0.2 langchain-anthropic>=0.2 langchain-openai>=0.2 \
    python-dotenv anthropic openai langsmith tiktoken httpx kaggle
```

**On Mac/Linux:**

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

```bash
cp .env.example .env
# Edit .env — add your Anthropic or OpenAI key, and Kaggle credentials
```

Your `.env` should contain:
```
ANTHROPIC_API_KEY=your_key_here
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

To get your Kaggle API key: kaggle.com → Account → API → Create New Token → downloads `kaggle.json`

### 4. Download datasets

```bash
python download_data.py
```

This downloads all three datasets into `data/raw/` automatically.

### 5. Preprocess data

```bash
python tools.py --preprocess
```

Cleans the raw CSVs and writes `data/processed/bookings_clean.csv`.

---

## How to run the agent

```bash
python agent.py
```

The agent loads the processed dataset, calls 5 analysis tools, and prints structured insights with evidence and limitations. All LLM calls are printed to stdout — every step is visible and auditable.

---

## How to view the dashboard

1. Install [PowerBI Desktop](https://powerbi.microsoft.com/desktop/) (free, Windows only)
2. Open `dashboard/dashboard.pbix`
3. If prompted for data source, point to `data/processed/bookings_clean.csv`

**Dashboard pages:**
- Executive overview — RevPAR, ADR, occupancy, cancellation rate by city
- Cancellation analysis — rate by channel, lead time, monthly trend
- Pricing intelligence — ADR seasonality, occupancy vs ADR scatter

---

## How to run the evaluation

```bash
python insights_generator.py   # generates evaluation/raw_insights.json
```

Results and scores are in `evaluation/evaluation_results.json`.  
Full LLM-as-judge report with bias discussion is in `evaluation/insight_review.md`.

---

## Troubleshooting

**pandas/numpy build errors on Windows:**  
Use `conda install pandas numpy scipy -y` instead of pip. See setup instructions above.

**Kaggle download fails:**  
Make sure `KAGGLE_USERNAME` and `KAGGLE_KEY` are set in your `.env` file, or place `kaggle.json` in `~/.kaggle/kaggle.json`.

**No API key error:**  
Copy `.env.example` to `.env` and fill in at least one of `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | One of these two | Anthropic Claude API key |
| `OPENAI_API_KEY` | One of these two | OpenAI API key |
| `KAGGLE_USERNAME` | For download_data.py | Kaggle account username |
| `KAGGLE_KEY` | For download_data.py | Kaggle API key |
| `LANGCHAIN_API_KEY` | Optional | LangSmith tracing |
| `LANGCHAIN_PROJECT` | Optional | LangSmith project name |

Never commit your `.env` file — it is in `.gitignore`.
