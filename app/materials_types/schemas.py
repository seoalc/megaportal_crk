from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import List
from datetime import datetime, date
import re


class SMaterialtypeAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    material_type: str = Field(..., min_length=1, max_length=128, description="Название типа материала")