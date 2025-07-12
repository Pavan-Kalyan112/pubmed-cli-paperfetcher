# tests/test_ollama_client.py

from paperfetcher.ollama_client import summarize_paper, ask_question_about_paper

def test_summarize_paper_mock(monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResp:
            def raise_for_status(self): pass
            def json(self): return {"response": "• Summary point 1\n• Summary point 2"}
        return MockResp()
    import requests
    monkeypatch.setattr(requests, "post", mock_post)

    result = summarize_paper("Test Title", "Test Abstract")
    assert "Summary point" in result

def test_ask_question_mock(monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResp:
            def raise_for_status(self): pass
            def json(self): return {"response": "The main contribution is XYZ."}
        return MockResp()
    import requests
    monkeypatch.setattr(requests, "post", mock_post)

    result = ask_question_about_paper("Full abstract here", "What is the main contribution?")
    assert "main contribution" in result.lower()
