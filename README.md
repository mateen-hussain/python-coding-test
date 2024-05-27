# Data discrepancy checker

This task mirrors a system we recently built internally, and will give you an
idea of the problems we need to solve.

Every quarter, new company data is provided to us in PDF format. We need to use
an external service to extract this data from the PDF, and then validate it
against data we have on file from another source.

Complete the API so that:

A user can provide a PDF and a company name data is extracted from the PDF via
the external service and compared to the data stored on file a summary of the
data is returned, containing all fields from both sources, noting which fields
did not match.

A selection of example PDFs have been uploaded, and the PDF
extraction service has been mocked for use in `src/pdf_service.py` - DO NOT
EDIT THIS FILE. There is simple documentation of the service in
`PDF_SERVICE_DOCS.md`. You can treat this as just another microservice.

The existing data we have on file is available in the `data/database.csv` file.

Treat this code as if it will be deployed to production, following best
practices where possible.

## Setup using Poetry

The easiest way to set up the repository is to use `python-poetry`. The lock file
was generated using version `1.8.3`

1. Ensure `poetry` is installed
2. Run `make install`

## Setup without Poetry

Alternatively it's possible to `pip install` directly using the
`pyproject.toml` or `requirements.txt`.
---------------

## Dev notes
Functional programming was preferred over class based. 
As it makes it easy to write unit tests.

Happy to use class based (if needed).

### Run app
1. Install packages `make install`
2. create `.env` file at root of repo (rename `.env.example`)
3. Run service `make dev`
4. To test the app, go to `http://localhost:8000/docs#` for swagger docs 
5. Alternatively use your choice of Postman or curl
6. The REST api built is a `post` and you need to upload a PDF (mimicking actual PDF upload)
   1. Make sure the filename uploaded is what is expected to test (or upload the file from assets folder)
   2. Please read the description of the API in swagger to understand the output

#### Screenshot of working examples
![Alt text](/readme-screenshots/Screenshot 2024-05-27-1.png)

![Alt text](/readme-screenshots/Screenshot 2024-05-27-2.png)

### Unit tests
1. Solitary unit tests pattern was preferred (happy to use sociable too)
2. Used pytest framework instead of inbuilt unittest
3. every testable package has a `tests` folder
4. to run tests `make test`

### Code Format
1. Code uses black, flake8, autopep and isort to lint and format code
2. run `make format`

### Pre-commit hook
1. Runs format and test on commit