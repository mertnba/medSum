from __future__ import annotations
from typing import Dict, Any
from langgraph.graph import Graph
from papers_agent.agents.paper_fetcher import paper_fetcher_node
from papers_agent.agents.trial_extractor import trial_extractor_node
from papers_agent.agents.weekly_summarizer import summarizer_node

def build_pipeline() -> Graph:
    g = Graph()

    # Fetcher
    g.add_node("fetch", paper_fetcher_node)

    # Extractor (takes state['papers'] from previous node)
    g.add_node("extract", trial_extractor_node)

    # (reads DB directly; no edge input required)
    g.add_node("summarize", summarizer_node)

    # ── Edges ─────────────────────────
    g.add_edge("fetch", "extract")
    g.add_edge("extract", "summarize")

    g.set_entry_point("fetch")
    g.set_finish_point("summarize")
    return g
