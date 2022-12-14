from bson import ObjectId
from schematics.models import Model
from schematics.types import EmailType, StringType, DateTimeType, DecimalType
from schematics.transforms import blacklist

import uuid
from typing import Optional
from pydantic import BaseModel, Field

class AppUser(Model):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    role: str = Field("user") # Default role is "user"
    username: str =  Field(...)
    password: str = Field(...)
    phone: str = Field(...)
    email: str = Field(...)
    address: str = Field(...)
    status: bool = Field(True)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "username": "tamnhu",
                "password": "tamnhu",
                "phone": "098765432",
                "email": "ttnithcmute@gmail.com",
                "address":"Vo Van Ngan HCMUTe",
                "status": "true"
            }
        }
        