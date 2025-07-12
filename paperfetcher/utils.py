import re
from typing import List, Union

# Improved heuristic: include more common non-academic indicators
NON_ACADEMIC_KEYWORDS = [
    "pharma", "pharmaceutical", "biotech", "inc", "ltd", "gmbh", "llc", "corp",
    "company", "industries", "research", "solutions", "biosciences", "laboratories",
    "clinic", "medtech", "institute", "diagnostic", "therapeutics", "medical center"
]

def is_non_academic(affiliation: str) -> bool:
    """Check if an affiliation likely belongs to a non-academic org."""
    affil_lower = affiliation.lower()
    return any(keyword in affil_lower for keyword in NON_ACADEMIC_KEYWORDS)

def extract_email(text: Union[str, List[str]]) -> str:
    """Extract the first email found in the input string or list."""
    if isinstance(text, list):
        text = " ".join(text)
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "N/A"


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
