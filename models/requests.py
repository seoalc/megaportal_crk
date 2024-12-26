from pydantic import BaseModel
from typing import Optional, List

class Request(BaseModel):
    id: int
    subscriber_id: int
    subscriber_name: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "subscriber_id": 8000000,
                "subscriber_name": "Пупкин Василий"
            }
        }