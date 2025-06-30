# medstractor

medstractor is an agentic pipeline for monitoring PubMed, extracting structured clinical trial data, and generating weekly summaries. It consists of three modular agents: one for fetching papers, one for extracting trials, and one for summarizing results.

## Components

- `paper_fetcher`: Queries PubMed and saves paper metadata as JSON.  
- `trial_extractor`: Parses structured trial data using LLMs.  
- `weekly_summarizer`: Generates weekly Markdown reports.  

## Running

Run the full pipeline:  
`python src/papers_agent/scripts/run_pipeline.py --query "..." --days-back 3`

Run individual agents:  
`python src/papers_agent/scripts/run_fetcher.py`  
`python src/papers_agent/scripts/run_extractor.py`  
`python src/papers_agent/scripts/run_summarizer.py`

## Setup

`python3 -m venv venv`  
`source venv/bin/activate`  
`pip install -e .`

Environment variables required:  
`OPENAI_API_KEY=...`  
`NCBI_EMAIL=...`  
`NCBI_API_KEY=...` (optional)


