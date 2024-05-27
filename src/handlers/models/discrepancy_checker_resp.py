from pydantic import BaseModel


class PostResponseModel(BaseModel):
    missing: dict
    different: dict
    new_data: dict
