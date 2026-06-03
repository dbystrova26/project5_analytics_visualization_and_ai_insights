"""
agent.py — LangChain agent for aparthotel booking data analysis.

The agent has access to 5 data analysis tools and uses an LLM to:
1. Decide which tools to call
2. Interpret the results
3. Generate business insights with evidence and limitations

Run:
    python agent.py

Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file first.
"""

import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

load_dotenv()

# ── Import tools ──────────────────────────────────────────────────────────────
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

# ── LLM setup — tries Anthropic first, falls back to OpenAI ──────────────────
def get_llm():
    """Return an LLM instance — Anthropic preferred, OpenAI as fallback."""
    if os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        print("Using Anthropic Claude")
        return ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
    elif os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        print("Using OpenAI GPT-4o")
        return ChatOpenAI(model="gpt-4o", temperature=0)
    else:
        raise EnvironmentError(
            "No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your .env file."
        )


# ── System prompt ─────────────────────────────────────────────────────────────
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

Generate exactly 5 numbered insights. Be concise but specific — Chleo is a CEO, not a data scientist.
She needs to trust the numbers and understand what to do with them.

Format each insight as:
INSIGHT [N]: [one-line headline]
Evidence: [specific numbers from the data]
Source: [tool name + column]
Limitation: [one honest caveat]
Action: [what Chleo should do with this information]
"""

# ── Build agent ───────────────────────────────────────────────────────────────
def build_agent():
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,           # Shows every tool call and result — transparency for Chleo's concern
        handle_parsing_errors=True,
        max_iterations=15,
    )
    return executor


# ── Main ──────────────────────────────────────────────────────────────────────
def run_analysis():
    print("\n" + "=" * 60)
    print("Aparthotel AI Agent — Booking Data Analysis")
    print("=" * 60 + "\n")

    agent = build_agent()

    query = (
        "Analyse the booking dataset and generate 5 business insights "
        "for the CEO of a pan-European aparthotel chain. Focus on: "
        "cancellation patterns, pricing opportunities, and operational risks. "
        "Use all available tools to gather evidence before writing insights."
    )

    result = agent.invoke({"input": query})

    print("\n" + "=" * 60)
    print("FINAL INSIGHTS")
    print("=" * 60)
    print(result["output"])


if __name__ == "__main__":
    run_analysis()
