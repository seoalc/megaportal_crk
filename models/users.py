from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "ruslan",
                "password": "strong!!!"
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str