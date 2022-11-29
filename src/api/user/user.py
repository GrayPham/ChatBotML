from fastapi import APIRouter, Depends, Query, UploadFile, status
from typing import List
from typing import Union
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

@user_router.put("/update/{id}")
async def update_user(id: str):
    return {"message": "User updated"}

@user_router.delete("/delete/{id}")
async def delete_user(id: str):
    return {"message": "User deleted"}

@user_router.post('/login')
async def login(login: LoginrDto ):
    data = user_services.login_user(login)
    
    return data