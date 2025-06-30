from papers_agent.pipeline import build_pipeline

def test_graph_nodes():
    g = build_pipeline()
    assert set(g.nodes) == {"fetch", "extract", "summarize"}

def test_graph_entry_and_exit():
    g = build_pipeline()
    assert g.entry_point == "fetch"
    assert g.finish_point == "summarize"
