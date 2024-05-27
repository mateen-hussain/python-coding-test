import io
import json
from unittest.mock import patch

import pytest
from fastapi import HTTPException, UploadFile

from src.handlers.discrepancy_checker import handler
from src.pdf_service import PdfService
from src.utils.pdf_checker import PdfParseStatus

extracted_pdf_data = {
    "Company Name": "RetailCo",
    "Industry": "Retail",
    "Market Capitalization": 2000,
    "Revenue (in millions)": 800,
    "EBITDA (in millions)": 150,
    "Net Income (in millions)": 40,
    "Debt (in millions)": 110,
    "Equity (in millions)": 400,
    "Enterprise Value (in millions)": 2100,
    "P/E Ratio": 20,
    "Revenue Growth Rate (%)": 8,
    "EBITDA Margin (%)": 18.75,
    "ROE (Return on Equity) (%)": 10,
    "ROA (Return on Assets) (%)": 6.5,
    "Current Ratio": 1.8,
    "Debt to Equity Ratio": 0.25,
    "Location": "Chicago, IL",
    "CEO": "Bob Johnson",
    "Number of Employees": 2000,
}
company_details = {
    "Company Name": "RetailCo",
    "Industry": "Retail",
    "Market Capitalization": 2000,
    "Revenue (in millions)": 800,
    "EBITDA (in millions)": 150,
    "Net Income (in millions)": 40,
    "Debt (in millions)": 100,
    "Equity (in millions)": 400,
    "Enterprise Value (in millions)": 2100,
    "P/E Ratio": 20,
    "Revenue Growth Rate (%)": 8,
    "EBITDA Margin (%)": 18.75,
    "Net Income Margin (%)": 5.0,
    "ROE (Return on Equity) (%)": 10.0,
    "ROA (Return on Assets) (%)": 6.5,
    "Current Ratio": 1.8,
    "Debt to Equity Ratio": 0.25,
    "Location": "Chicago",
}
expected_diff = {
    "missing": {"Net Income Margin (%)": 5.0},
    "different": {
        "Debt (in millions)": [110, 100],
        "Location": ["Chicago, IL", "Chicago"],
    },
    "new_data": {"CEO": "Bob Johnson", "Number of Employees": 2000},
}
company_name = "retailco"
file_name = "{}.pdf".format(company_name)


@pytest.fixture
def mock_upload_file():
    return UploadFile(filename=file_name, file=io.BytesIO(b"test content"), size=10)


@pytest.mark.asyncio
@patch(
    "src.handlers.discrepancy_checker.get_company_details", return_value=company_details
)
@patch.object(PdfService, "extract", return_value=extracted_pdf_data)
async def test_handler_success(
    mock_extract, mock_get_company_details, mock_upload_file
):

    response = await handler(mock_upload_file)

    assert response.status_code == 200
    assert json.loads(response.body) == expected_diff

    mock_extract.assert_called_once_with("assets/{}".format(file_name))
    mock_get_company_details.assert_called_once_with(company_name)


@pytest.mark.asyncio
async def test_handler_pdf_verification_failure():
    mock_upload_file = UploadFile(
        filename="test.pdf", file=io.BytesIO(b"test content"), size=0
    )

    with pytest.raises(HTTPException) as excinfo:
        await handler(mock_upload_file)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == PdfParseStatus.EMPTY_FILE.value


@pytest.mark.asyncio
@patch("src.handlers.discrepancy_checker.get_company_details", return_value=None)
async def test_handler_company_not_found_in_db(
    mock_get_company_details, mock_upload_file
):
    with pytest.raises(HTTPException) as excinfo:
        await handler(mock_upload_file)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "can't find company details in our database"
    mock_get_company_details.assert_called_once_with(company_name)


@pytest.mark.asyncio
@patch(
    "src.handlers.discrepancy_checker.get_company_details", return_value=company_details
)
@patch.object(PdfService, "extract", side_effect=FileNotFoundError)
async def test_handler_pdf_service_extraction_failure(
    mock_extract, mock_get_company_details, mock_upload_file
):

    with pytest.raises(HTTPException) as excinfo:
        await handler(mock_upload_file)

    assert excinfo.value.status_code == 422
    assert excinfo.value.detail == "pdf service can't extract data for uploaded file"
