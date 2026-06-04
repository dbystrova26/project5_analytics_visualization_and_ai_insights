"""
agent.py — LangChain agent covering all 3 aparthotel use cases.

UC1 — Dynamic pricing / revenue optimisation
UC2 — Cancellation & no-show prediction
UC3 — Guest communication & upsell

Run:
    python agent.py

Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file first.
"""

import os
from dotenv import load_dotenv
load_dotenv()

from tools import (
    # UC1 — Dynamic Pricing
    adr_statistics,
    seasonal_pricing_analysis,
    weekend_vs_weekday_adr,
    stay_length_adr_analysis,
    # UC2 — Cancellation Prediction
    cancellation_rate_by_segment,
    lead_time_analysis,
    correlation_with_cancellation,
    deposit_type_cancellation,
    # UC3 — Guest Communication & Upsell
    upsell_opportunity_analysis,
    repeat_guest_analysis,
    guest_origin_analysis,
)

TOOLS = [
    # UC1
    adr_statistics,
    seasonal_pricing_analysis,
    weekend_vs_weekday_adr,
    stay_length_adr_analysis,
    # UC2
    cancellation_rate_by_segment,
    lead_time_analysis,
    correlation_with_cancellation,
    deposit_type_cancellation,
    # UC3
    upsell_opportunity_analysis,
    repeat_guest_analysis,
    guest_origin_analysis,
]

SYSTEM_PROMPT = """You are an AI data analyst working for a pan-European aparthotel chain (~500 employees, 8-12 cities).
Your CEO (Chleo) is sceptical of AI and needs transparent, evidence-based recommendations.

You must generate insights covering ALL THREE use cases:

UC1 — DYNAMIC PRICING: Which months/segments are underpriced? Where is revenue being left on the table?
  Tools: adr_statistics, seasonal_pricing_analysis, weekend_vs_weekday_adr, stay_length_adr_analysis

UC2 — CANCELLATION PREDICTION: What drives cancellations? Which segments/channels are highest risk?
  Tools: cancellation_rate_by_segment, lead_time_analysis, correlation_with_cancellation, deposit_type_cancellation

UC3 — GUEST COMMUNICATION & UPSELL: What upsell opportunities exist? How do repeat guests behave?
  Tools: upsell_opportunity_analysis, repeat_guest_analysis, guest_origin_analysis

Generate at least 2 insights per use case (6+ total). For each insight use this format:

[UC1/UC2/UC3] INSIGHT N: [headline]
Evidence: [specific numbers from the data]
Source: [tool name used]
Limitation: [one honest caveat]
Action: [what Chleo should do]

End with a 3-sentence executive summary for Chleo covering all three use cases.
"""


def get_llm():
    if os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        print("Using Anthropic Claude")
        return ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)
    elif os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        print("Using OpenAI GPT-4o")
        return ChatOpenAI(model="gpt-4o", temperature=0)
    else:
        raise EnvironmentError("No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env")


def run_analysis():
    print("\n" + "=" * 65)
    print("Aparthotel AI Agent — All 3 Use Cases")
    print("UC1: Dynamic Pricing | UC2: Cancellation | UC3: Upsell")
    print("=" * 65 + "\n")

    llm = get_llm()
    llm_with_tools = llm.bind_tools(TOOLS)

    from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            "Analyse the booking dataset and generate insights covering all 3 use cases: "
            "dynamic pricing, cancellation prediction, and guest communication/upsell. "
            "Use all available tools to gather evidence. "
            "Generate at least 2 insights per use case."
        ))
    ]

    for i in range(20):
        print(f"[Step {i+1}] Calling LLM...")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            print("\n" + "=" * 65)
            print("FINAL INSIGHTS — ALL 3 USE CASES")
            print("=" * 65)
            print(response.content)
            break

        for tc in response.tool_calls:
            print(f"  → [{tc['name'].split('_')[0].upper()}] {tc['name']}({tc['args']})")
            tool_fn = next((t for t in TOOLS if t.name == tc["name"]), None)
            try:
                result = tool_fn.invoke(tc["args"]) if tool_fn else f"Tool '{tc['name']}' not found."
            except Exception as e:
                result = f"Error: {e}"
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
    else:
        print("Max iterations reached.")


if __name__ == "__main__":
    run_analysis()
