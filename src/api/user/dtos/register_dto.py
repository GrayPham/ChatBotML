from datetime import datetime
from pydantic import BaseModel, Field


class RegisterDto(BaseModel):
    username: str = Field(..., description='Username')
    password: str = Field(..., description="Password")
    re_password: str = Field(..., description="Pre-password to verify")
    phone: str =  Field(..., description="Phone")
    email: str =  Field(..., description="Email")
    address: str = Field(..., description='Address')


