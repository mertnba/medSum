import pytest, json, os
from papers_agent.agents.paper_fetcher import build_graph

@pytest.mark.network
def test_paper_fetcher_runs(tmp_path, monkeypatch):
    monkeypatch.setattr("papers_agent.agents.paper_fetcher.OUTPUT_DIR", tmp_path)

    runner = build_graph().compile()
    result = runner.invoke({"query": "glaucoma[Title]", "days_back": 1})

    assert isinstance(result, dict)
    assert "papers" in result
    assert isinstance(result["papers"], list)

    saved_files = list(tmp_path.glob("*.json"))
    assert saved_files, "no output JSON written"
    with saved_files[0].open() as fh:
        data = json.load(fh)
    assert all("pmid" in p for p in data)
