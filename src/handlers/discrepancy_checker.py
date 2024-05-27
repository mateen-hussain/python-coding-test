import os

from fastapi import File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.db.companies import get_company_details
from src.logger import logger
from src.pdf_service import PdfService
from src.utils.dict_comparer import dict_differences
from src.utils.pdf_checker import PdfParseStatus, verify_pdf

API_KEY = os.getenv("PDF_SERVICE_KEY", "TEST_KEY")
pdf_service = PdfService(API_KEY)


class ResponseModel(BaseModel):
    missing: dict
    different: dict
    new_data: dict


HANDLER_DESCRIPTION = (
    "Returns all discrepancies in data stored in company database "
    "vs data extracted from uploaded PDF."
    "Http 200 response has three fields; missing, different & new_data."
    " 'missing': this data is in database but missing from extracted PDF data."
    " 'different': this data doesnt match with what is in database."
    " 'new_data': this data is in extracted PDF data but not found in database. "
)


async def handler(file: UploadFile = File(...)):
    """
    Handler for discrepancy_checker post request.

    Args:
        file (UploadFile): Uploaded file

    Returns:
        JSONResponse or HTTPException.
    """
    status = await verify_pdf(file)
    if status != PdfParseStatus.SUCCESS:
        logger.error("Failed to process uploaded PDF")
        raise HTTPException(status_code=400, detail=status.value)
    try:
        company_name = file.filename[: file.filename.index(".pdf")]
        company_details_from_db = get_company_details(company_name)
        if not company_details_from_db:
            logger.error("Error finding company {} from database".format(company_name))
            raise HTTPException(
                status_code=404, detail="can't find company details in our database"
            )

        extracted_data = pdf_service.extract("assets/{}".format(file.filename))

        diff = dict_differences(extracted_data, company_details_from_db)
        return JSONResponse(content=diff)

    except FileNotFoundError:
        logger.error("Error extracting data from PDF {}".format(file.filename))
        raise HTTPException(
            status_code=422, detail="pdf service can't extract data for uploaded file"
        )
