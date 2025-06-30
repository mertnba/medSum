from papers_agent.agents.paper_fetcher import build_graph

graph = build_graph().compile()
graph.invoke(
    {
        "query": "ophthalmology[Title/Abstract]",
        "days_back": 3,
    }
)
