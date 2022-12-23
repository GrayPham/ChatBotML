from fastapi import APIRouter, Depends, Query, UploadFile, status
from typing import List
from typing import Union
from api.user.dtos.update_dto import UpdateDto
from api.user.userService.user_service import UserService
from api.user.dtos.register_dto import RegisterDto
from api.user.dtos.login_dto import LoginrDto
from fastapi.responses import JSONResponse
from datetime import datetime

from api.auth.auth_bearer import JWTBearer
user_router = APIRouter()
user_services = UserService()

@user_router.post("/register")
async def create_user(registerDto: RegisterDto):
    try:
        print("Creating user")
        data = user_services.create_user(registerDto)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )


@user_router.get('/get-all-user', dependencies=[Depends(JWTBearer())], tags=["Admin get all users"])
async def get_all_user():
    return user_services.get_all_user()

@user_router.put("/update")
async def update_user(user: UpdateDto):
    try:
        print("User full", user)
        data = user_services.updateuser(user)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@user_router.put("/active/{id}")
async def active_user(userid: str):
    try:
        data = user_services.activeBot(userid)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )
@user_router.delete("/delete/{id}")
async def delete_user(id: str):
    try:
        data = user_services.delete(id)
        return data
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )

@user_router.post('/login')
async def login(login: LoginrDto ):
    data = user_services.login_user(login)
    
    return data
@user_router.get('/userfull')
async def userfull(userid: str ):
    try:
        print("User full", userid)
        data = user_services.countChatbotUsers(userid)
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )

@user_router.get('/paymentdetails')
async def paymentdetails(userid: str, paymentid: str ):
    try:
        paymentKEY = user_services.getlinkbot(userid,paymentid)
        data = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <script>
            var securitykey = """""+"\""+paymentKEY["securitykey"]+"\"" +""";
            var botID = """+"\""+paymentKEY["botID"]+"\""+""";
            var userID = """+"\""+paymentKEY["userID"]+"\""+""";
            var message = "string";
            var firstCheck = true;
            
    </script>
    <div class="containerChat">
        <div class="chatbox">
            <div class="chatbox__support">
                <div class="chatbox__header">
                    <div class="chatbox__content--header">
                        <h4 class="chatbox__heading--header">Chat support</h4>
                    </div>
                </div>
                <div class="chatbox__messages">
                        
                </div>
                <div class="chatbox__footer">
                    <img src="https://cdn.jsdelivr.net/gh/thienan01/ChatCDNs/emojis.svg" alt="">
                    <img src="https://cdn.jsdelivr.net/gh/thienan01/ChatCDNs/microphone.svg" alt="">
                    <input type="text" placeholder="Write a message..." id="inputMessage">
                    <p class="chatbox__send--footer" id="btnSend" onclick="handleSendMsg()">Send</p>
                    <img src="https://cdn.jsdelivr.net/gh/thienan01/ChatCDNs/attachment.svg" alt="">
                </div>
            </div>
            <div class="chatbox__button">
                <button>button</button>
            </div>
        </div>
    </div>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,300;0,400;0,600;1,300&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/thienan01/ChatCDNs/chat.css">
    <script src="https://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/thienan01/ChatCDNs/handleChat.js"></script>
</body>
</html>
        """
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )