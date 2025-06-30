from __future__ import annotations
import json
import pathlib
from typing import Dict, Any, List
import os
from langgraph.graph import Graph
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from papers_agent.store.sqlite_store import upsert_trial
from papers_agent.store.vector_store import add_paper

class Trial(BaseModel):
    pmid: str
    title: str
    sample_size: int | None
    arms: List[str] | None
    primary_outcome: str | None
    abstract: str
    pub_date: str | None = None

parser = PydanticOutputParser(pydantic_object=Trial)

raw_template = pathlib.Path("prompts/extractor.prompt").read_text()
PROMPT_TEMPLATE = PromptTemplate(
    template=raw_template,
    input_variables=["title", "abstract", "pmid", "format_instructions"]
)

_llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
    temperature=0,
)

def _extract_one(paper: dict) -> Trial | None:
    try:
        prompt_text = PROMPT_TEMPLATE.format(
            title=paper["title"],
            abstract=paper.get("abstract", ""),
            pmid=paper["pmid"],
            format_instructions=parser.get_format_instructions()
        )

        if any(bad in prompt_text for bad in ["{title}", "{abstract}", "{format_instructions}", "{{", "}}"]):
            raise RuntimeError(f"Prompt still contains unresolved placeholders:\n{prompt_text}")

        print(f"[debug] Prompt for PMID {paper['pmid']}:\n\n{prompt_text}\n")

        response = _llm.invoke([HumanMessage(content=prompt_text)]).content
        trial = parser.parse(response)
        return trial

    except Exception as e:
        print(f"[warn] Failed to parse trial for PMID {paper.get('pmid', 'unknown')}: {e}")
        return None

def trial_extractor_node(state: Dict[str, Any]) -> str:
    raw_papers: list[dict] = state["papers"]
    extracted: list[dict] = []

    for p in raw_papers:
        trial = _extract_one(p)
        if not trial:
            continue
        rec = trial.model_dump()
        upsert_trial(rec)
        add_paper(rec["pmid"], rec["abstract"])
        extracted.append(rec)

    state["trials"] = extracted
    print(f" Extracted {len(extracted)}/{len(raw_papers)} papers")
    return state

def build_graph() -> Graph:
    g = Graph()
    g.add_node("trial_extractor", trial_extractor_node)
    g.set_entry_point("trial_extractor")
    return g
