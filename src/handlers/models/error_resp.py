from pydantic import BaseModel


class ErrorResp(BaseModel):
    detail: str
