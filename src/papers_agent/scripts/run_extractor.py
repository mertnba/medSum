from papers_agent.agents.trial_extractor import build_graph
import json, pathlib

json_path = max(pathlib.Path("data/raw").glob("*.json"))  # latest file
papers = json.loads(json_path.read_text())

graph = build_graph().compile()
graph.invoke({"papers": papers})
