from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import List
from datetime import datetime, date
import re


class SSubscriberNumberSearch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    appearance_date: date = Field(default=..., description="Дата явки ГГГГ-ММ-ДД")
    subscriber_number: int = Field(..., description="Номер устройства абонента")
    subscriber_addres: str = Field(default=..., min_length=10, max_length=250, description="Адрес абонента, не более 250 символов")
    complaint_text: str = Field(None, description="Описание жалобы")
    contact_number: str = Field(default=..., min_length=15, max_length=20, description="Контактный номер абонента, не более 20 символов")
    solution_description: str = Field(None, description="Описание проведенной работы")
    user_id_created_application: int = Field(..., description="ID пользователя забившего заявку")
    application_status: int = Field(..., description="Статус заявки")

class SApplicationAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    appearance_date: date = Field(default=..., description="Дата явки ГГГГ-ММ-ДД")
    subscriber_number: int = Field(..., description="Номер устройства абонента")
    subscriber_addres: str = Field(default=..., min_length=10, max_length=250, description="Адрес абонента, не более 250 символов")
    complaint_text: str = Field(None, description="Описание жалобы")
    contact_number: str = Field(default=..., min_length=10, max_length=20, description="Контактный номер абонента, не более 20 символов")
    user_id_created_application: int = Field(..., description="ID пользователя забившего заявку")
    application_status: int = Field(..., description="Статус заявки")
    remedial_user_id: int = Field(..., description="ID пользователя исполнителя")

class SRemidialUserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    application_id: int = Field(..., description="ID заявки")
    remedial_user_ids: List[int]

class SComplaintTextUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    application_id: int = Field(..., description="ID заявки")
    complaint_text: str = Field(default=..., description="Текст жалобы")

class SClosedText(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    application_id: int = Field(..., description="ID заявки")
    closed_text: str = Field(default=..., description="Текст жалобы")

class SAppearanceDateUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    application_id: int = Field(..., description="ID заявки")
    appearance_date: date = Field(default=..., description="Дата явки ГГГГ-ММ-ДД")

class SDeleteApplication(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    application_id: int = Field(..., description="ID заявки")