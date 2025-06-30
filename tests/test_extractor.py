import json
import pytest
from papers_agent.agents.trial_extractor import _extract_one, Trial

SAMPLE = {
    "pmid": "123",
    "title": "Small RCT of atropine",
    "abstract": "OBJECTIVE: To test atropine...",
}

def fake_invoke(self, messages, *args, **kwargs):
    class FakeResp:
        content = json.dumps({
            "pmid": "123",
            "title": "RCT",
            "sample_size": 45,
            "arms": ["Atropine", "Placebo"],
            "primary_outcome": "Visual acuity",
            "abstract": "dummy",
            "pub_date": "2025-01-01",
        })
    return FakeResp()

def get_llm():
    from papers_agent.agents.trial_extractor import _llm
    return _llm

def test_extract_one(monkeypatch):
    monkeypatch.setattr(type(get_llm()), "invoke", fake_invoke)
    trial = _extract_one(SAMPLE)
    assert isinstance(trial, Trial)
    assert trial.sample_size == 45
    assert trial.arms == ["Atropine", "Placebo"]
