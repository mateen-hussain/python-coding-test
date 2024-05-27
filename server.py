from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, File, UploadFile

from src.handlers.models import discrepancy_checker_resp, error_resp

load_dotenv()

from src.handlers import discrepancy_checker  # noqa: E402

app = FastAPI()
v1_router = APIRouter(prefix="/v1")


@v1_router.post(
    "/discrepancy_checker",
    response_model=discrepancy_checker_resp.PostResponseModel,
    description=discrepancy_checker.HANDLER_DESCRIPTION,
    responses={
        400: {"model": error_resp.ErrorResp},
        404: {"model": error_resp.ErrorResp},
        422: {"model": error_resp.ErrorResp},
    },
)
async def discrepancy_checker_request_handler(file: UploadFile = File(...)):
    return await discrepancy_checker.handler(file)


app.include_router(v1_router, prefix="/api")
