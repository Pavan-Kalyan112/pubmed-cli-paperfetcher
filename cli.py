import argparse
from paperfetcher.core import search_pubmed, fetch_paper_details, filter_non_academic
from paperfetcher.writer import write_csv, print_results
from paperfetcher.ollama_client import summarize_paper, ask_question_about_paper

def main():
    parser = argparse.ArgumentParser(description="Fetch and summarize PubMed research papers.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("--file", "-f", type=str, help="Output CSV file name (optional)")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging")
    parser.add_argument("--use-ollama", action="store_true", help="Use Ollama for summarization/Q&A")
    parser.add_argument("--ask", type=str, help="Ask a question about each paper (requires --use-ollama)")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Limit the number of papers to show (after filtering)")

    args = parser.parse_args()

    if args.debug:
        print(f"[DEBUG] Query: {args.query}")
        print(f"[DEBUG] Limit: {args.limit}")
        if args.file:
            print(f"[DEBUG] Output File: {args.file}")
        if args.use_ollama:
            print("[DEBUG] Ollama enabled")
        if args.ask:
            print(f"[DEBUG] User Question: {args.ask}")

    # Step 1: Search - Fetch more to allow filtering
    pubmed_ids = search_pubmed(args.query, max_results=args.limit * 5)
    if not pubmed_ids:
        print("No results found.")
        return

    if args.debug:
        print(f"[DEBUG] Fetched {len(pubmed_ids)} PubMed IDs")

    # Step 2: Fetch and parse paper metadata
    all_papers = fetch_paper_details(pubmed_ids)

    if args.debug:
        print(f"[DEBUG] Parsed {len(all_papers)} papers")

    # Step 3: Filter for non-academic affiliations
    filtered_papers = filter_non_academic(all_papers)

    if args.debug:
        print(f"[DEBUG] Filtered down to {len(filtered_papers)} non-academic papers")

    # Step 4: Limit to user-defined count
    filtered_papers = filtered_papers[:args.limit]

    # Step 5: LLM support (summarization and Q&A)
    if args.use_ollama:
        for paper in filtered_papers:
            if args.debug:
                print(f"[DEBUG] Summarizing: {paper['Title'][:60]}...")
            paper["Summary"] = summarize_paper(paper["Title"], paper.get("Abstract", ""))

            if args.ask:
                full_text = f"{paper['Title']}\n\n{paper.get('Abstract', '')}"
                if args.debug:
                    print(f"[DEBUG] Asking question: {args.ask}")
                paper["Answer"] = ask_question_about_paper(full_text, args.ask)

    # Step 6: Output
    if args.file:
        write_csv(filtered_papers, args.file)
    else:
        print_results(filtered_papers)


if __name__ == "__main__":
    main()
