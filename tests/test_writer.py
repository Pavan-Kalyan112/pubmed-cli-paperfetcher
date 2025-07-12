# tests/test_writer.py

from paperfetcher.writer import write_csv
import os
import csv

def test_write_csv(tmp_path):
    test_file = tmp_path / "output.csv"
    sample_papers = [{
        "PubmedID": "123",
        "Title": "Test Paper",
        "Publication Date": "2021-01-01",
        "Non-academic Authors": ["Alice"],
        "Company Affiliations": ["Pfizer"],
        "Corresponding Author Email": "alice@pfizer.com"
    }]
    write_csv(sample_papers, str(test_file))

    assert os.path.exists(test_file)
    with open(test_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["Title"] == "Test Paper"
