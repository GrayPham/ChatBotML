
from fastapi import APIRouter, Depends, Query, UploadFile, status
from typing import List
from typing import Union
from src.api.botchat.chatServices.ChatServices import chatServices
from src.api.botchat.dtos.chatbot_dto import ChatBotDto
from fastapi.responses import JSONResponse
from src.api.auth.auth_bearer import JWTBearer
from datetime import datetime
chat_router = APIRouter()
chat_services = chatServices()

@chat_router.get("/allbot") 
async def getAllBot():
    try:
        print("All bot")
        data = chat_services.get_all_Chat()
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )

@chat_router.get("/bot") 
async def getABot(userID: str, botID: str):
    try:
        print("A bot")
        data = chat_services.getchatbotDetail(userID,botID)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e), "status": False }
            )
@chat_router.post("/createchat")
async def create_chat(chatDto: ChatBotDto):
    try:
        print("A Chat Message has been created")
        data = chat_services.create_bot(chatDto)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@chat_router.put("/deletechat")
async def detete_bot(chatID: str):
    return await "Not active"
@chat_router.get("/getlinkbuy", dependencies=[Depends(JWTBearer())])
async def getlink_bot(securitykey: str, userID: str):
    
    try:
        data = chat_services.getlinkbot(securitykey,userID)
        return data
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
    
