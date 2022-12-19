
from api.user.entities.registerUser import AppUser
from bson import ObjectId
import bson
from core.database.connection import db, user_collection
from api.user.dtos.register_dto import RegisterDto
from api.user.dtos.login_dto import LoginrDto
from api.auth.auth_handler import signJWT
from datetime import datetime



class UserService():
    def user_helper(self, user) -> dict:
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "phone": user["phone"],
            "email": user["email"],
            "address": user["address"],
        }
    def binding_user(self, datas):
        users = []
        for data in datas:
            user = {
            "id": str(data["_id"]),
            "username": data["username"],
            "password": data["password"],
            "phone": data["phone"],
            "email": data["email"],
            "address": data["address"],
            "status": data["status"],
            }
            users.append(user)
        return users
            
    def user_data(self, registerDto: RegisterDto): 
        user =  {
            "username": registerDto.username,
            "password": registerDto.password,
            "phone": registerDto.phone,
            "role": "user",
            "email": registerDto.email,
            "address": registerDto.address,
            "status": registerDto.status,
            "message": [],
            "payment": []
        }
        return user
    
    def get_all_user(self):
        data = user_collection.find({}).limit(100)
        
        return self.binding_user(data) 
    def create_user(self, registerDto: RegisterDto):

        data =  self.user_data(registerDto)
        print(registerDto.password == registerDto.re_password)
        if registerDto.password != registerDto.re_password:
            return {"message":"Password not match, please input again","status": False}
 
        find_user = user_collection.count_documents({
            '$or': [{'email': registerDto.email},
            {'username': registerDto.username}]
        }) 

        if find_user > 0:
            return {"message":"Email already exist!","status": False}
        else:
            user_collection.insert_one(dict(data))
            return {"message":"User Created","status": True}
    def login_user(self, login: LoginrDto):
        print(login)
        # JWT token
        find_user = user_collection.find_one({
            '$and': [{'username': login.username},
            {'password': login.password}]
        })
        if find_user:
            
            return  {"data": self.user_helper(find_user),"token": signJWT(login.username)}
        else:
            return {"error":"Invalid login details!","status":False}
