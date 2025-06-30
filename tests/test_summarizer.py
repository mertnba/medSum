import json
import pathlib
from papers_agent.agents.weekly_summarizer import summarizer_node, LLM

def test_summary(tmp_path, monkeypatch):
    fake_trial = {
        "pmid": "1",
        "title": "Test Trial",
        "sample_size": 30,
        "arms": ["A", "B"],
        "primary_outcome": "Vision improvement",
        "abstract": "Very short abstract for test."
    }

    def stub_invoke(self, prompt_text, *args, **kwargs):
        class R:
            content = "# Weekly Ophthalmology Trial Digest (Week of 2025-01-01)\n\n## Key trends this week\n- Test passed\n\n## Trial snapshots\n### Test Trial (n = 30)\n**Primary outcome:** Vision improvement\n**Arms:** A, B\n**PMID:** 1\n\n> Very short abstract for test.\n"
        return R()

    monkeypatch.setattr(type(LLM), "invoke", stub_invoke)
    monkeypatch.setattr("papers_agent.agents.weekly_summarizer.OUT_DIR", tmp_path)

    state = {"trials": [fake_trial]}
    summarizer_node(state)
    md_files = list(tmp_path.glob("weekly_*.md"))
    assert md_files, "Markdown report not generated"
    assert "Vision improvement" in md_files[0].read_text()
