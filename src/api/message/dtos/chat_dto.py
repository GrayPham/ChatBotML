from datetime import datetime
from pydantic import BaseModel, Field

class ChatDto(BaseModel):
    botID: str = Field(..., description="User ID")
    userID: str = Field(..., description="User ID")
    message: str = Field(..., description="message")
    firstCheck: bool = Field(..., description="First Message")
    dateMess: datetime =  datetime.now()

