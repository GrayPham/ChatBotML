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
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Web form</title>
            </head>
            <body>
                <form>
                    <div>"""+paymentKEY["link"]+"""</div>
                </form>
            </body>
        </html>
        """
        return data
        
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )