from datetime import datetime
from pydantic import BaseModel, Field

class UserDto(BaseModel):
    id: str = Field(..., description='Id user')
    username: str = Field(..., description='Username')
    password: str = Field(..., description="Password")
    phone: str =  Field(..., description="Phone")
    email: str =  Field(..., description="Email")
    address: str = Field(..., description='Address')


