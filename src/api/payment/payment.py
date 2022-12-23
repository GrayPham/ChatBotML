from fastapi import APIRouter, Depends, Query, UploadFile, status
from typing import List
from typing import Union
from api.payment.services.PaymentService import PaymentService
from api.payment.dtos.PaymentDto import PaymentDto

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from os import getenv
from paypalcheckoutsdk.orders import OrdersCreateRequest

from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime
from api.auth.auth_bearer import JWTBearer

payment_router = APIRouter()
payment_services = PaymentService()
# API thanh toan san pham
@payment_router.post("/payment", dependencies=[Depends(JWTBearer())])
async def create_payment(paymentDto: PaymentDto):
    try:
        print("Creating payment")
        data = payment_services.payment_Abot(paymentDto)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
    
@payment_router.get("/getpaymentuser")
async def getAllUserPayment(userID: str):
    try:
        print("Get All message from bot")
        data = payment_services.allChatBotPayment(userID)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@payment_router.get("/getpayment")
async def getAllPayment():
    try:
        print("Get All message from bot")
        data = payment_services.allPayment()
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@payment_router.put("/deletepayment")
async def deletePayment(_id: str):
    try:
        
        data = payment_services.deletePayment(_id)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
    
@payment_router.post("/testPaymentPaypal")
async def test_Payment(request: Request):
    client_id = getenv("CLIENT_ID")
    client_secret = getenv("CLIENT_SECRET")
    enviroment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(enviroment)
    try:
        data = await request.json()
        sum = 0.0
        for item in data['items']:
            sum += float(item['unit_amount']['value'])
        print(sum)
        request = OrdersCreateRequest()

        request.prefer('return=representation')
        request.request_body(
                {
                    "intent": "CAPTURE",
                    "purchase_units": [
                        {
                            "amount": {
                                "currency_code": "USD",
                                "value": str(sum)
                            }
                        }
                    ],
                    "items": data
                }
            )
        response = client.execute(request)
        return JSONResponse(content={"id": response.result.id})

    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )

# API kiem tra san pham da duoc thanh toan hay chua
@payment_router.get("/checkpayment")
async def Checkpayment(userID: str, botID: str):
    try:
        data = payment_services.checkpayment(userID,botID)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )