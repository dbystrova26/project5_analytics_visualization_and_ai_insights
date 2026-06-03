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
│   ├── raw/                        # Original downloaded datasets
│   └── processed/                  # Cleaned CSVs output by preprocessing script
├── research/
│   ├── sector_research.md          # EU aparthotel sector analysis
│   ├── opportunities_risks.md      # AI opportunity & risk mapping
│   └── use_cases.md                # Use case proposals & justification
├── dashboard/
│   ├── dashboard.pbix              # PowerBI dashboard file
│   └── dashboard_documentation.md # Metrics, design rationale, usage guide
├── n8n/
│   ├── workflow.json               # Exported n8n workflow
│   └── workflow_documentation.md  # Workflow explanation & setup
├── agent/
│   ├── agent.py                    # LangChain agent entry point
│   ├── tools.py                    # Data analysis tools
│   └── insights_generator.py      # Insight generation & formatting
├── evaluation/
│   ├── insight_review.md           # Quality review of 5 agent insights
│   └── evaluation_results.json    # Structured scores & feedback
├── cost_estimation/
│   ├── cost_analysis.md            # Upfront cost breakdown
│   └── timeline_estimate.md        # Week-by-week implementation plan
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

All datasets are free, publicly available, and require only a free Kaggle account to download.

---

## Setup instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/bi-dashboard-project.git
cd bi-dashboard-project
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.example .env
# Edit .env and add your Anthropic or OpenAI API key
```

### 5. Download datasets

1. Go to each Kaggle link above
2. Download CSV files into `data/raw/`
3. Run preprocessing:

```bash
python agent/tools.py --preprocess
```

---

## How to run the agent

```bash
python agent/agent.py
```

The agent loads the processed dataset, runs statistical tools, and prints 5+ formatted insights with evidence and limitations. All LLM calls are logged to stdout for transparency.

---

## How to view the dashboard

1. Install [PowerBI Desktop](https://powerbi.microsoft.com/desktop/) (free)
2. Open `dashboard/dashboard.pbix`
3. If prompted for data source, point to `data/processed/bookings_clean.csv`

Key views:
- **Overview page** — RevPAR, occupancy %, ADR by city
- **Cancellation analysis** — cancellation rate by lead time, channel, market segment
- **Pricing intelligence** — ADR distribution, event-driven spikes

---

## How to run evaluations

```bash
python evaluation/run_evaluation.py
```

Results are written to `evaluation/evaluation_results.json`. The LLM-as-judge prompt is documented in `evaluation/insight_review.md`.

---

## Environment variables

```
ANTHROPIC_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here
```

Never commit your `.env` file. It is listed in `.gitignore`.
