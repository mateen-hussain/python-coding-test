from io import BytesIO

import pytest

from src.utils.pdf_checker import PdfParseStatus, verify_pdf


class MockUploadFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
        self.size = len(content)

    async def read(self):
        return self.content


@pytest.mark.asyncio
async def test_no_file_uploaded():
    result = await verify_pdf(None)
    assert result == PdfParseStatus.NO_FILE_UPLOADED


@pytest.mark.asyncio
async def test_not_pdf():
    file = MockUploadFile("test.txt", b"Sample text content")
    result = await verify_pdf(file)
    assert result == PdfParseStatus.NOT_PDF


@pytest.mark.asyncio
async def test_empty_file():
    file = MockUploadFile("test.pdf", b"")
    result = await verify_pdf(file)
    assert result == PdfParseStatus.EMPTY_FILE


@pytest.mark.asyncio
async def test_success_response():
    # Creating a simple valid PDF in memory
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.drawString(100, 100, "Hello World")
    can.save()
    valid_pdf_content = packet.getvalue()

    file = MockUploadFile("test.pdf", valid_pdf_content)
    result = await verify_pdf(file)
    assert result == PdfParseStatus.SUCCESS
