# 🧪 ResearchPaper CLI - PubMed Paper Fetcher with LLM Support

`researchpaper-cli` is a command-line tool that allows users to search for research papers from **PubMed**, extract structured metadata (like title, authors, affiliations, email), and optionally summarize or ask questions using a **Large Language Model (LLM)** (e.g., via [Ollama](https://ollama.com)).

---
# How the Code is Organized
The project follows a modular structure to keep the logic clean, testable, and maintainable.
## 📂 Project Structure

```text
researchpaper_cli/
├── paperfetcher/
│   ├── core.py               # Main logic for search, fetch, and parse
│   ├── writer.py             # Handles writing CSV or printing to terminal
│   ├── utils.py              # Helper functions (cleaning, regex, filters)
    ├── cli.py                # CLI entry point script
│   ├── ollama_client.py      # Optional: Summarize or Q&A using LLM

├── tests/                    # Unit tests for all core modules
│   ├── __init__.py
│   ├── test_core.py          # Tests for search, parsing, affiliation, email logic
│   ├── test_utils.py         # Tests for utility functions like email extraction
│   ├── test_writer.py        # Tests for output writing
│   ├── test_ollama_client.py # Tests LLM summary and question-answering (mocked)
├── pyproject.toml            # Poetry configuration and metadata
├── README.md                 # Documentation
└── LICENSE                   # MIT License
```
# Module Breakdown
**cli.py**
Parses command-line arguments and coordinates the flow: search → fetch → filter → summarize → output.

**core.py**
Implements:

search_pubmed(query) – fetches PubMed IDs

fetch_paper_details(ids) – downloads full MEDLINE records

parse_medline(text) – converts MEDLINE text into structured dictionaries

**utils.py**
Includes:

extract_email() – gets email from various fields

is_non_academic() – identifies company/industry affiliations

clean_text() – text preprocessing

**ollama_client.py**
Calls a local LLM like Ollama to:

Summarize abstracts

Answer questions like “What is the main contribution?”

**writer.py**
Handles:

Terminal output using rich

Writing results to CSV

**tests/**
Unit tests organized by component, runnable with poetry run pytest.

# PubMed CLI Tool – Architecture Diagram
```text
                      +-----------------------+
                      |     CLI (cli.py)      |
                      | get-papers-list cmd   |
                      +-----------------------+
                                 |
                                 v
           +-------------------------------------------+
           |    Core Logic (core.py)                   |
           | - search_pubmed(query)                    |
           | - fetch_paper_details(pubmed_ids)         |
           | - parse_medline(medline_text)             |
           +-------------------------------------------+
                                 |
                                 v
           +-------------------------------------------+
           |          Filtering Logic                  |
           |     filter_non_academic(papers)           |
           +-------------------------------------------+
                                 |
                                 v
         +------------------+         +---------------------------+
         |  Email + Org     |         |   LLM Module (optional)   |
         |  Utils (utils.py)|         |   ollama_client.py        |
         | - extract_email  |         | - summarize_paper         |
         | - is_non_academic|         | - ask_question_about_paper|
         +------------------+         +---------------------------+
                                 |
                                 v
           +-------------------------------------------+
           |        Output (writer.py)                 |
           | - print_results(papers)                   |
           | - write_csv(papers, file_name)            |
           +-------------------------------------------+

```
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/90894c9a-a825-4f1b-9a9a-77b1bae68b80" />

# Tools & Libraries Used
```table
| Tool/Library     | Purpose                                                         | Link                                                                                               |
| ---------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Python 3.10+** | Core programming language                                       | [https://www.python.org](https://www.python.org)                                                   |
| **Poetry**       | Dependency management and packaging                             | [https://python-poetry.org](https://python-poetry.org)                                             |
| **Biopython**    | To interact with the PubMed (Entrez) API and parse MEDLINE data | [https://biopython.org](https://biopython.org)                                                     |
| **Requests**     | HTTP requests for interacting with APIs (e.g., Ollama)          | [https://docs.python-requests.org](https://docs.python-requests.org)                               |
| **Pandas**       | Data structuring, optional for tabular output                   | [https://pandas.pydata.org](https://pandas.pydata.org)                                             |
| **Rich**         | Beautiful CLI output formatting                                 | [https://rich.readthedocs.io](https://rich.readthedocs.io)                                         |
| **Argparse**     | Parsing CLI arguments                                           | [https://docs.python.org/3/library/argparse.html](https://docs.python.org/3/library/argparse.html) |
| **Pytest**       | Unit testing framework                                          | [https://docs.pytest.org](https://docs.pytest.org)                                                 |
```
#LLM Integration
| Tool                  | Purpose                                | Link                                     |
| --------------------- | -------------------------------------- | ---------------------------------------- |
| **Ollama**            | LLM backend for summarization and Q\&A | [https://ollama.com](https://ollama.com) |
| **Custom API Client** | Communicates with Ollama via HTTP      | *Local code (`ollama_client.py`)*        |





# Features
🔍 Fetch papers by query from PubMed

🧾 Parse title, authors, affiliations, emails, and abstract

🧪 Filter for non-academic affiliations (e.g., pharma/biotech)

🧠 Summarize and ask custom questions using an LLM (Ollama)

📤 Export results to CSV

# 🚀 Installation
📦 From Test PyPI
```bash

pip install -i https://test.pypi.org/simple/ researchpaper-cli==1.1.1
```
⚠️ If you don't want optional dependencies (like LLM support):

```bash

pip install -i https://test.pypi.org/simple/ --no-deps researchpaper-cli==1.1.1
```
🧪 For Development (Locally)
```bash

git clone https://github.com/Pavan-Kalyan112/pubmed-cli-paperfetcher.git
cd pubmed-cli-paperfetcher
poetry install
```
# 🧾 Usage
```bash
get-papers-list "cancer vaccine" --limit 5
```
# Optional Flags
Flag	Description
--limit / -l	Number of papers to fetch (default: 20)
--file / -f	Save results to a CSV file
--use-ollama	Use LLM for summarizing papers
--ask	Ask a custom question (requires --use-ollama)
--debug / -d	Show debug logs

Example:
```bash

get-papers-list "covid-19" --limit 10 --use-ollama --ask "What is the primary result of this study?
```






## 🔗 Project Links

- 🐙 **GitHub Repository**: [View on GitHub](https://github.com/Pavan-Kalyan112/pubmed-cli-paperfetcher)
- 🧪 **Test PyPI Package**: [View on TestPyPI](https://test.pypi.org/project/researchpaper-cli/)


👤 Author
Pavan Kalyan Neelam
📧 pavaneelam95@gmail.com
