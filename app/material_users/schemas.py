from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict, conint
from typing import List
from datetime import datetime, date
import re


class SMaterialtouserAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    material_title_id: int = Field(..., description="ID наименования материала")
    user_id: int = Field(..., description="ID наименования материала")
    quantity: conint(ge=1)