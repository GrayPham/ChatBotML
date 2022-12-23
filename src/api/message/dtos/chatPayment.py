from datetime import datetime
from pydantic import BaseModel, Field

class chatPayment(BaseModel):
    securitykey: str =Field(...,description= 'securitykey')
    botID: str = Field(..., description="User ID")
    userID: str = Field(..., description="User ID")
    message: str = Field(..., description="message")
    firstCheck: bool = Field(..., description="message")


