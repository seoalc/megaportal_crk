from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import List
from datetime import datetime, date
import re


class SMaterialtitleAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    material_type: int = Field(..., description="ID типа материала")
    material_title: str = Field(..., min_length=1, max_length=128, description="Наименование материала")