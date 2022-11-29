
from fastapi import APIRouter, Depends, Query, UploadFile, status
from typing import List
from typing import Union
from api.message.messServices.messServices import messService
from api.message.dtos.chat_dto import ChatDto
from api.message.dtos.chatPayment import chatPayment
from fastapi.responses import JSONResponse
from api.auth.auth_bearer import JWTBearer
from datetime import datetime
mess_router = APIRouter()
mess_services = messService()

@mess_router.post("/chatmessages", dependencies=[Depends(JWTBearer())])
async def create_chat(chatDto: ChatDto):
    try:
        print("Messeger")
        data = mess_services.create_mess(chatDto)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@mess_router.get("/getallmessages")
async def getAllAChat(botID: str):
    try:
        print("Get All message from bot")
        data = mess_services.get_all_messAChat(botID)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
    
@mess_router.post("/sentmessagesBuy")
async def SentMessagesBuy(datamess: chatPayment):
    try:
        print("Sent message Buy")
        data = mess_services.sentMessageBuy(datamess)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )