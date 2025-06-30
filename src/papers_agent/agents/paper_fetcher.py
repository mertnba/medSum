from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from langgraph.graph import Graph
from papers_agent.tools.pubmed import fetch_recent_papers, Paper

OUTPUT_DIR = Path("data/raw")

def paper_fetcher_node(state: Dict[str, Any]) -> str:
    query = state.get("query", "ophthalmology[MeSH Major Topic]")
    days_back = state.get("days_back", 1)
    papers: List[Paper] = fetch_recent_papers(query=query, days_back=days_back)
    state["papers"] = [p.model_dump(mode="json") for p in papers]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{datetime.utcnow():%Y-%m-%d}.json"
    out_file.write_text(json.dumps(state["papers"], indent=2))

    print(f"Saved {len(papers)} papers → {out_file}")
    return state

def build_graph() -> Graph:
    g = Graph()
    g.add_node("paper_fetcher", paper_fetcher_node)
    g.set_entry_point("paper_fetcher")
    return g
