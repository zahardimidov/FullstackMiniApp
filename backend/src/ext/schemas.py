from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str

class DetailResponse(BaseModel):
    detail: str