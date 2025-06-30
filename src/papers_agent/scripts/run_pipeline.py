import argparse
from papers_agent.pipeline import build_pipeline

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="ophthalmology[Title/Abstract]")
    ap.add_argument("--days-back", type=int, default=1)
    args = ap.parse_args()

    graph = build_pipeline().compile()
    graph.invoke({"query": args.query, "days_back": args.days_back})

if __name__ == "__main__":
    main()
