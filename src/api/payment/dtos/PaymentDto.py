from datetime import datetime
from pydantic import BaseModel, Field

class PaymentDto(BaseModel):
    paymentID: str = Field(..., description=" paymentID")
    userID: str = Field(..., description="Username")
    botID: str = Field(..., description="Password")
    dateBought: datetime = Field(..., description="dateBought")
    price: float =  Field(..., description="Price")
    paymentMethod: str = Field(..., description='Payment Method')
