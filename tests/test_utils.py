from paperfetcher.utils import is_non_academic, extract_email

def test_is_non_academic_true():
    assert is_non_academic("Pfizer Inc., New York, USA") is True

def test_is_non_academic_false():
    assert is_non_academic("University of California, Berkeley, USA") is False

def test_extract_email_found_string():
    text = "Contact: john.doe@pfizer.com"
    assert extract_email(text) == "john.doe@pfizer.com"

def test_extract_email_found_list():
    lines = ["Reach out: support@biotech.com", "Thanks"]
    assert extract_email(lines) == "support@biotech.com"

def test_extract_email_none():
    lines = ["No contact info here"]
    assert extract_email(lines) == "N/A"
