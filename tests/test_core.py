import pytest
from paperfetcher import core

MOCK_MEDLINE_WITH_EM = """
PMID- 12345678
TI  - COVID-19 mRNA Vaccine Study
DP  - 2024 Jan
AB  - This paper investigates...
AU  - Jane Doe
AD  - Pfizer Inc., NY, USA
EM  - jane.doe@pfizer.com
"""

MOCK_MEDLINE_FALLBACK_EMAIL = """
PMID- 22222222
TI  - Vaccine Efficacy Results
DP  - 2024 Feb
AB  - Email: support@vaccinebio.com
AU  - John Smith
AD  - VaccineBio Inc., California
"""

MOCK_MEDLINE_ACADEMIC = """
PMID- 33333333
TI  - Immune Response Study
DP  - 2023 Mar
AB  - No email here
AU  - Alice Johnson
AD  - University of Cambridge, UK
"""

def test_parse_medline_extracts_em_field_email():
    papers = core.parse_medline(MOCK_MEDLINE_WITH_EM)
    assert papers[0]["Corresponding Author Email"] == ["jane.doe@pfizer.com"]

def test_parse_medline_extracts_email_fallback():
    papers = core.parse_medline(MOCK_MEDLINE_FALLBACK_EMAIL)
    assert papers[0]["Corresponding Author Email"] == "support@vaccinebio.com"

def test_parse_medline_handles_no_email():
    papers = core.parse_medline(MOCK_MEDLINE_ACADEMIC)
    assert papers[0]["Corresponding Author Email"] == "N/A"

def test_filter_non_academic_filters_correctly():
    combined = "\n".join([MOCK_MEDLINE_WITH_EM, MOCK_MEDLINE_ACADEMIC])
    parsed = core.parse_medline(combined)
    filtered = [p for p in parsed if p["Company Affiliations"]]
    assert len(filtered) == 1
    assert filtered[0]["PubmedID"] == "12345678"
