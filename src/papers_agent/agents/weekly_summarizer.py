from __future__ import annotations
import json
import datetime
import pathlib
from typing import Dict, Any
from langgraph.graph import Graph
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from papers_agent.store.sqlite_store import recent_trials
from rich import print as rprint

LLM = ChatOpenAI(model="gpt-4o", temperature=0.3)
PROMPT_TEMPLATE = PromptTemplate.from_file("prompts/summarizer.prompt")

OUT_DIR = pathlib.Path("reports")
OUT_DIR.mkdir(exist_ok=True)

def summarizer_node(state: Dict[str, Any]) -> str:
    trials = state.get("trials") or recent_trials(7)
    week_ending = datetime.date.today().isoformat()

    formatted_prompt = PROMPT_TEMPLATE.format(
        trials=json.dumps(trials, indent=2),
        week_ending=week_ending
    )
    md = LLM.invoke(formatted_prompt).content.strip()

    out_path = OUT_DIR / f"weekly_{week_ending}.md"
    out_path.write_text(md, encoding="utf-8")
    rprint(f"[green]📄  Report saved → {out_path}[/]")
    state["report_path"] = str(out_path)
    return state

def build_graph() -> Graph:
    g = Graph()
    g.add_node("summarizer", summarizer_node)
    g.set_entry_point("summarizer")
    return g
