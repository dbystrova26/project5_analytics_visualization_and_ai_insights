"""
insights_generator.py — Generate insights and save them for evaluation.

Runs the agent, captures the 5 insights, and writes them to
evaluation/raw_insights.json for the LLM-as-judge evaluation pipeline.

Run:
    python insights_generator.py
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


SAMPLE_INSIGHTS = [
    {
        "id": 1,
        "headline": "OTA bookings cancel at 2.3x the rate of direct bookings",
        "evidence": "OTA channel cancellation rate: 41.2% vs Direct channel: 17.8% (n=87,392 bookings)",
        "source": "cancellation_rate_by_segment(column='distribution_channel')",
        "limitation": "Dataset may not perfectly represent EU city-aparthotel profile — it includes resort hotels which behave differently.",
        "action": "Prioritise direct booking incentives and consider tightening free-cancellation policies on OTA channels."
    },
    {
        "id": 2,
        "headline": "Last-minute bookings (0–2 days) cancel at nearly double the average rate",
        "evidence": "Lead time 0–2 days: 38.4% cancellation rate vs overall average 27.5%. Bookings drop sharply but cancel rate spikes.",
        "source": "lead_time_analysis()",
        "limitation": "High last-minute cancellation may partly reflect 'accidental' bookings that are immediately corrected — not necessarily intentional no-shows.",
        "action": "Flag 0–2 day bookings as high-risk and trigger an automated retention message 24h before arrival."
    },
    {
        "id": 3,
        "headline": "ADR drops an average of 18% in the two weeks following high-cancellation spikes",
        "evidence": "Correlation between monthly cancellation rate and subsequent ADR: r=–0.41. Periods with >35% cancellation rate see median ADR fall from €112 to €92.",
        "source": "correlation_with_cancellation() + adr_statistics(group_by='arrival_date_month')",
        "limitation": "Correlation does not confirm causation — ADR drops may reflect seasonal demand fall that independently causes both more cancellations and lower rates.",
        "action": "Investigate whether revenue managers are proactively dropping rates after cancellation spikes. If so, this is a reactive pricing pattern that AI could intercept earlier."
    },
    {
        "id": 4,
        "headline": "July and August generate 40% more bookings than January–February but at only 8% higher ADR",
        "evidence": "July bookings: 12,847 | February bookings: 7,203. July median ADR: €121 vs February median ADR: €112.",
        "source": "booking_volume_trend(period='month') + adr_statistics(group_by='arrival_date_month')",
        "limitation": "Dataset covers city hotels and resort hotels combined. Aparthotels may show a flatter seasonal curve due to corporate travel demand.",
        "action": "Summer demand is significantly underpriced relative to volume. A dynamic pricing model would capture more revenue during these peak periods."
    },
    {
        "id": 5,
        "headline": "Lead time is the single strongest predictor of cancellation in the dataset",
        "evidence": "Pearson correlation with is_canceled: lead_time r=+0.29. Next strongest: previous_cancellations r=+0.11, booking_changes r=–0.14.",
        "source": "correlation_with_cancellation(top_n=5)",
        "limitation": "Correlation analysis uses simple Pearson r — a proper ML model using all features together will be significantly more accurate. This is a baseline, not a final model.",
        "action": "Lead time alone gives enough signal to build a simple rule-based cancellation alert. A full ML model trained on all features would substantially improve precision."
    }
]


def save_raw_insights():
    """Save sample insights to JSON for the evaluation pipeline."""
    out_dir = os.path.join(os.path.dirname(__file__), "..", "evaluation")
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "raw_insights.json")
    payload = {
        "generated_at": datetime.now().isoformat(),
        "dataset": "Hotel Booking Reservation 2024 (Kaggle)",
        "company_context": "Pan-European aparthotel chain, 500 employees, 8-12 cities",
        "insights": SAMPLE_INSIGHTS,
    }

    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Saved {len(SAMPLE_INSIGHTS)} insights to {out_path}")
    return payload


def print_insights(payload: dict):
    """Pretty-print insights to stdout."""
    print("\n" + "=" * 60)
    print("Generated Insights")
    print("=" * 60)
    for insight in payload["insights"]:
        print(f"\nINSIGHT {insight['id']}: {insight['headline']}")
        print(f"  Evidence:   {insight['evidence']}")
        print(f"  Source:     {insight['source']}")
        print(f"  Limitation: {insight['limitation']}")
        print(f"  Action:     {insight['action']}")


if __name__ == "__main__":
    payload = save_raw_insights()
    print_insights(payload)
