from papers_agent.pipeline import build_pipeline

def test_graph_shape():
    g = build_pipeline()
    assert set(g.nodes) == {"fetch", "extract", "summarize"}
    assert g.entry_point == "fetch"
    assert g.finish_point == "summarize"
