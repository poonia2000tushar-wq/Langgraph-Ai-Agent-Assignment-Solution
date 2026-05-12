from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import os

load_dotenv()

# =====================================
# STATE DEFINITION
# =====================================

class AgentState(TypedDict):
    user_query: str
    search_results: List[str]
    summary: str
    reflection: str
    retry_count: int
    final_output: str


# =====================================
# TOOL 1: SEARCH TOOL
# =====================================

def search_tool(query: str):
    """
    Simulated search tool.
    In a real-world application, this could call:
    - Tavily API
    - SerpAPI
    - DuckDuckGo Search
    """

    print(f"\nSearching for: {query}")

    results = [
        "Renewable energy reduces greenhouse gas emissions.",
        "Solar and wind energy are sustainable alternatives to fossil fuels.",
        "Renewable energy lowers long-term electricity costs.",
        "Clean energy improves public health by reducing pollution.",
        "Governments worldwide are investing heavily in green technology."
    ]

    return results


# =====================================
# TOOL 2: SUMMARIZER TOOL
# =====================================

def summarizer_tool(search_results):
    """
    Combines research results into a summary.
    """

    summary = " ".join(search_results)

    return summary


# =====================================
# TOOL 3: FILE SAVER TOOL
# =====================================

def save_to_file_tool(content: str):

    os.makedirs("outputs", exist_ok=True)

    file_path = "outputs/research_report.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Report saved to {file_path}"


# =====================================
# NODE 1: SEARCH NODE
# =====================================

def search_node(state: AgentState):

    print("\n========== SEARCH NODE ==========")

    query = state["user_query"]

    results = search_tool(query)

    return {
        "search_results": results
    }


# =====================================
# NODE 2: SUMMARIZE NODE
# =====================================

def summarize_node(state: AgentState):

    print("\n========== SUMMARIZE NODE ==========")

    search_results = state["search_results"]

    summary = summarizer_tool(search_results)

    return {
        "summary": summary
    }


# =====================================
# NODE 3: REFLECTION NODE
# =====================================

MAX_RETRIES = 2

def reflection_node(state: AgentState):

    print("\n========== REFLECTION NODE ==========")

    summary = state["summary"]

    retry_count = state.get("retry_count", 0)

    # Basic quality check
    if len(summary.split()) < 25:

        reflection = (
            "Summary is too short and lacks detail. Retry required."
        )

        retry_count += 1

    else:

        reflection = (
            "Summary quality is acceptable."
        )

    print(f"Reflection: {reflection}")

    return {
        "reflection": reflection,
        "retry_count": retry_count
    }


# =====================================
# CONDITIONAL ROUTING
# =====================================

def should_retry(state: AgentState):

    """
    Determines whether the graph should loop back.
    """

    if (
        "Retry required" in state["reflection"]
        and state["retry_count"] < MAX_RETRIES
    ):

        print("\nRetrying workflow...\n")

        return "retry"

    return "continue"


# =====================================
# NODE 4: SAVE NODE
# =====================================

def save_node(state: AgentState):

    print("\n========== SAVE NODE ==========")

    save_status = save_to_file_tool(state["summary"])

    final_output = f"""
FINAL RESEARCH REPORT
---------------------

{state['summary']}

Status:
{save_status}
"""

    return {
        "final_output": final_output
    }


# =====================================
# BUILD LANGGRAPH WORKFLOW
# =====================================

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("search", search_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("reflect", reflection_node)
workflow.add_node("save", save_node)

# Entry point
workflow.set_entry_point("search")

# Linear edges
workflow.add_edge("search", "summarize")
workflow.add_edge("summarize", "reflect")

# Conditional cyclic routing
workflow.add_conditional_edges(
    "reflect",
    should_retry,
    {
        "retry": "search",
        "continue": "save"
    }
)

# Final edge
workflow.add_edge("save", END)


# =====================================
# MEMORY / CHECKPOINTER
# =====================================

memory = MemorySaver()

app = workflow.compile(
    checkpointer=memory
)


# =====================================
# MAIN EXECUTION
# =====================================

if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "research-thread-1"
        }
    }

    user_input = input(
        "\nEnter your research topic: "
    )

    result = app.invoke(
        {
            "user_query": user_input,
            "retry_count": 0
        },
        config=config
    )

    print("\n===================================")
    print("FINAL OUTPUT")
    print("===================================")

    print(result["final_output"])
