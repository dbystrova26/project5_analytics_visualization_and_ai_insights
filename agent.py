"""
agent.py — LangChain agent for aparthotel booking data analysis.

Run:
    python agent.py

Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file first.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from tools import (
    cancellation_rate_by_segment,
    adr_statistics,
    lead_time_analysis,
    booking_volume_trend,
    correlation_with_cancellation,
)

TOOLS = [
    cancellation_rate_by_segment,
    adr_statistics,
    lead_time_analysis,
    booking_volume_trend,
    correlation_with_cancellation,
]

SYSTEM_PROMPT = """You are an AI data analyst working for a pan-European aparthotel chain.
Your job is to analyse booking data and generate clear, evidence-based business insights
that can be presented to the CEO (Chleo) to demonstrate the value and transparency of AI.

You have access to these tools:
- cancellation_rate_by_segment: find which booking channels / market segments cancel most
- adr_statistics: analyse average daily rate patterns
- lead_time_analysis: examine how lead time relates to cancellations
- booking_volume_trend: identify seasonal patterns in bookings
- correlation_with_cancellation: find numeric features most predictive of cancellation

For each insight you generate, you must:
1. State the insight clearly in plain business language
2. Quote the specific numbers from the data that support it
3. Name the tool and column you used as evidence
4. State one limitation or assumption Chleo should know about

Generate exactly 5 numbered insights. Format each as:
INSIGHT [N]: [one-line headline]
Evidence: [specific numbers from the data]
Source: [tool name + column]
Limitation: [one honest caveat]
Action: [what Chleo should do with this information]
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
        raise EnvironmentError(
            "No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file."
        )


def run_analysis():
    print("\n" + "=" * 60)
    print("Aparthotel AI Agent — Booking Data Analysis")
    print("=" * 60 + "\n")

    llm = get_llm()
    llm_with_tools = llm.bind_tools(TOOLS)

    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            "Analyse the booking dataset and generate 5 business insights "
            "for the CEO of a pan-European aparthotel chain. Focus on: "
            "cancellation patterns, pricing opportunities, and operational risks. "
            "Use all available tools to gather evidence before writing insights."
        ))
    ]

    # Agentic loop — keep calling tools until the LLM stops
    max_iterations = 10
    for i in range(max_iterations):
        print(f"[Step {i+1}] Calling LLM...")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # If no tool calls, we have the final answer
        if not response.tool_calls:
            print("\n" + "=" * 60)
            print("FINAL INSIGHTS")
            print("=" * 60)
            print(response.content)
            break

        # Execute each tool call
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"  → Calling tool: {tool_name}({tool_args})")

            # Find and run the matching tool
            tool_fn = next((t for t in TOOLS if t.name == tool_name), None)
            if tool_fn:
                try:
                    result = tool_fn.invoke(tool_args)
                except Exception as e:
                    result = f"Error running {tool_name}: {e}"
            else:
                result = f"Tool '{tool_name}' not found."

            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
    else:
        print("Max iterations reached.")


if __name__ == "__main__":
    run_analysis()
