from enum import Enum

from fastapi import UploadFile


class PdfParseStatus(Enum):
    SUCCESS = "success"
    NO_FILE_UPLOADED = "No file uploaded"
    NOT_PDF = "Uploaded file is not a PDF"
    EMPTY_FILE = "Uploaded file is empty"


async def verify_pdf(file: UploadFile) -> PdfParseStatus:
    """
    Given a file, checks if it is valid pdf or not

    Args:
        file (UploadFile): File to check

    Returns:
        PdfParseStatus: Enum with file parse status
    """
    if not file:
        return PdfParseStatus.NO_FILE_UPLOADED
    if not file.filename.endswith(".pdf"):
        return PdfParseStatus.NOT_PDF
    if not file.size:
        return PdfParseStatus.EMPTY_FILE
    return PdfParseStatus.SUCCESS
