
from fastapi import HTTPException
from src.api.botchat.dtos.chatbot_dto import ChatBotDto
from src.api.payment.dtos.PaymentDto import PaymentDto
from src.api.user.dtos.user_dto import UserDto
from src.api.user.entities.registerUser import AppUser
from bson import ObjectId
from src.core.database.connection import db, user_collection,chat_collection
from src.api.user.dtos.register_dto import RegisterDto
from src.api.user.dtos.login_dto import LoginrDto
from src.api.user.dtos.update_dto import UpdateDto
from src.api.auth.auth_handler import signJWT
from datetime import datetime



class UserService():
    def user_helper(self, user) -> dict:
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "phone": user["phone"],
            "email": user["email"],
            "address": user["address"],
            "role": user["role"]
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
            "status": True,
            "messageCurrent": {
                "BotId": "",
                "History": [[]]
            },
            "message": [],
            "payment": []
        }
        return user
    def user_dataDist(self, data): 
        user =  {
            "username": data["username"],
            "phone": data["phone"],
            "role": "user",
            "email": data["email"],
            "address": data["address"],
            "status": data["status"],
            "message" :data["message"],
            "payment": data["payment"],
        }
        return user
    def user_datafull(self,data ):
        user = {
            "id": str(data["_id"]),
            "username": data["username"],
            "phone": data["phone"],
            "email": data["email"],
            "address": data["address"],
            "message" :data["message"],
            "payment": data["payment"],
            }
        return user
    def chat_data(self, chatDto): 
        print("Chatbot convert")
        chat =  {
            
            "title": chatDto["title"],
            "link": chatDto["link"],
            "status": chatDto["status"],

        }
        return chat
    def payment_data(self, data): 
        payment =  {
            "payment": data["payment"]
        }
        return payment
    
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
    def countChatbotUsers(self, userid: str):
        print("User full", len(userid))
        find_user = user_collection.find_one({
            "_id": ObjectId(userid)
        })
        
        if find_user:
            data = self.user_datafull(find_user)
            return {"data": data}
        else:
            return {"data": "User not found"}
    def updateuser(self, user: UpdateDto):
        update_result =  user_collection.update_one({"_id":ObjectId(user.id)},{"$set":{
            "username":user.username,
            "password":user.password,
            "phone":user.phone,
            "email":user.email,
            "address": user.address
            }})
        if update_result.modified_count == 1:
            updated_user =  user_collection.find_one({"_id":ObjectId(user.id)})
            return self.user_dataDist(updated_user)


        existing_student = user_collection.find_one({"_id":ObjectId(user.id)})
        if ( existing_student):
            return {"data": "User information no new content"}
            
        else:
            return HTTPException(status_code=404, detail=f"User {user.id} not found")
    def getlinkbot(self,userID: str, securitykey: str):
        # kiem tra user

            find_user = user_collection.find_one({'_id': ObjectId(userID)})

            if find_user:

                payment = user_collection.find_one({'_id': ObjectId(userID)},{"payment":{"$elemMatch":{"paymentID": securitykey,"status": True}}})

                if payment:
                    paymentdata = self.payment_data(payment)
                    print("Payment data", paymentdata)
                    mess = chat_collection.find_one({
                        '_id': ObjectId(paymentdata["payment"][0]["botID"])
                    })
                    data = self.chat_data(mess)
                    print("data",data["link"])
                    return {"userID":str(userID) , "botID":str(paymentdata["payment"][0]["botID"]),"securitykey":str(securitykey), "status": True}
                else:
                    return {"message": "KeyError","status": False}
            else:
                return {"message": "KeyError","status": False}
    def delete(self,userID: str):
        updated = user_collection.update_one(
            {"_id": ObjectId(userID) },         
            {"$set":{"status":False}}
        )
        if(updated.modified_count):
            return {"message":"Delete Success","status": True}
        else:
            return {"message":"User ID not exist","status": True}
    def activeBot(self,userID: str):
        updated = user_collection.update_one(
            {"_id": ObjectId(userID) },         
            {"$set":{"status":True}}
        )
        if(updated.modified_count):
            return {"message":"Active Success","status": True}
        else:
            return {"message":"User ID not exist","status": True}
