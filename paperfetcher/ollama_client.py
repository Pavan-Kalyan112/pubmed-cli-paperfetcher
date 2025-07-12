# paperfetcher/ollama_client.py

import requests
from typing import Optional

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"


def summarize_paper(title: str, abstract: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    """
    Summarize a paper using Ollama in 3 bullet points.
    
    Args:
        title: Title of the paper.
        abstract: Abstract content.
        model: LLM model name (default: llama3).

    Returns:
        A summarized text or None if failed.
    """
    prompt = f"""Summarize the following research paper in 3 bullet points.

Title: {title}

Abstract: {abstract}

Summary:
"""
    return _call_ollama(prompt, model, task="Summarize")


def ask_question_about_paper(content: str, question: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    """
    Ask a custom question about a paper using Ollama.

    Args:
        content: Full abstract or text.
        question: User's question.
        model: LLM model name.

    Returns:
        The answer string or None if failed.
    """
    prompt = f"""Paper Content:

{content}

Question: {question}

Answer:"""
    return _call_ollama(prompt, model, task="Q&A")


def _call_ollama(prompt: str, model: str, task: str = "LLM") -> Optional[str]:
    """Internal function to call Ollama API with error handling."""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=90  # increase timeout to 90 seconds
        )

        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.RequestException as e:
        print(f"[Ollama Error - {task}] {e}")
        return None
    except ValueError:
        print(f"[Ollama Error - {task}] Invalid JSON response.")
        return None
