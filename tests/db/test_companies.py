from unittest.mock import patch

import pandas as pd

from src.db.companies import get_company_details

data = {
    "Company Name": ["Company A", "Company B", "Company C"],
    "Detail 1": ["Detail A1", "Detail B1", "Detail C1"],
    "Detail 2": ["Detail A2", "Detail B2", "Detail C2"],
}
df = pd.DataFrame(data)


@patch("src.db.companies.df", df)
def test_get_company_details_found():
    result = get_company_details("Company B")
    expected = {
        "Company Name": "Company B",
        "Detail 1": "Detail B1",
        "Detail 2": "Detail B2",
    }
    assert result == expected


@patch("src.db.companies.df", df)
def test_get_company_details_not_found():
    result = get_company_details("Non Existent Company")
    assert result is None


@patch("src.db.companies.df", df)
def test_get_company_details_case_insensitivity():
    result = get_company_details("company a")
    expected = {
        "Company Name": "Company A",
        "Detail 1": "Detail A1",
        "Detail 2": "Detail A2",
    }
    assert result == expected
