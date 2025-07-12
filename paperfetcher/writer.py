# paperfetcher/writer.py

from typing import List, Dict
from rich.console import Console
from rich.table import Table
import csv

console = Console()

def write_csv(papers: List[Dict], filename: str) -> None:
    """Write papers to CSV with the required output fields."""
    fieldnames = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for paper in papers:
            writer.writerow({
                "PubmedID": paper.get("PubmedID", ""),
                "Title": paper.get("Title", ""),
                "Publication Date": paper.get("Publication Date", ""),
                "Non-academic Author(s)": ", ".join(paper.get("Non-academic Authors", [])),
                "Company Affiliation(s)": ", ".join(paper.get("Company Affiliations", [])),
                "Corresponding Author Email": paper.get("Corresponding Author Email", "")
            })

    console.print(f"[green]Results saved to [bold]{filename}[/bold][/green]")


def print_results(papers: List[Dict]) -> None:
    """Display papers in a formatted table using rich."""
    if not papers:
        console.print("[yellow]⚠ No non-academic papers found.[/yellow]")
        return

    table = Table(title="Filtered PubMed Papers")

    table.add_column("PMID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white", max_width=60, overflow="fold")
    table.add_column("Companies", style="magenta", max_width=30)
    table.add_column("Email", style="green", no_wrap=True)

    for paper in papers:
        title = paper.get("Title", "N/A")[:1000]
        companies = ", ".join(paper.get("Company Affiliations", [])) or "N/A"
        email = paper.get("Corresponding Author Email", "N/A")

        table.add_row(
            paper.get("PubmedID", "N/A"),
            title,
            companies,
            email,
        )

    console.print(table)

    # Print summaries and LLM answers if present
    for paper in papers:
        if paper.get("Summary"):
            console.rule(f"📄 Summary for {paper.get('PubmedID', '')}")
            console.print(paper["Summary"])

        if paper.get("Answer"):
            console.print(f"[blue]💬 Answer to your question:[/blue] {paper['Answer']}\n")
