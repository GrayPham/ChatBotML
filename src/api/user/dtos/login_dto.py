from datetime import datetime
from pydantic import BaseModel, Field

class LoginrDto(BaseModel):
    username: str = Field(..., description='Username')
    password: str = Field(..., description="Password")

