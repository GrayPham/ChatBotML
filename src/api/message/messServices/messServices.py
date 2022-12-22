

from api.message.entities.chatCreate import AppUser
from bson import ObjectId
import bson
from core.database.connection import db, chat_collection,mess_collection,payments_collection,createDBChatUser,user_collection
from api.message.dtos.chat_dto import ChatDto
from api.message.dtos.chatPayment import chatPayment
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders   import jsonable_encoder


class messService():
    def user_helper(self, chat) -> dict:
        return {
            "id": str(chat["_id"]),
            "botID":str(chat["botID"]),
            "userID": str(chat["userID"]),
            "message": chat["message"],
            "dateMess": chat["dateMess"],
            
        }
    def binding_chat(self, datas):
        chats = []
        for data in datas:
            chat = {
            "id": str(data["_id"]),
            "botID":str(data["botID"]),
            "userID": str(data["userID"]),
            "message": data["message"],
            "dateMess": data["dateMess"],

            }
            chats.append(chat)
        return chats
            
    def chat_data(self, chatDto: ChatDto): 
        chat =  {
            "botID": chatDto.botID,
            "userID": chatDto.userID,
            "message": chatDto.message,
            "dateMess": chatDto.dateMess,

        }
        return chat
    

    
    def create_mess(self, chatDto: ChatDto):

        data =  self.chat_data(chatDto)
        

        find_chat = chat_collection.count_documents({
            '_id': ObjectId(chatDto.botID)
        }) 

        if find_chat:   
            # Check history_ids for chatbot and user
            user = user_collection.find_one({'_id': ObjectId(chatDto.userID)})
            print(user["messageCurrent"])
            if  chatDto.firstCheck == True:
                if(user["messageCurrent"]["BotId"] =="" ):
                    print("True")
                # Không phải tin nhắn đầu
                else:
                    # Goi Models(False ->True)
                    print("Clear history")
                    removedata= {
                        "BotId" : chatDto.botID,
                        "History": [[31373, 50256]] # Do Model tra ve Bao gom ket qua tin nhan va History

                    }
                    updated = user_collection.update_many(
                        {"_id": ObjectId(chatDto.userID) },
                        {"$set":{"messageCurrent":dict(removedata)}}
                    
                    
                )
            else: 
                print("False")
                # Goi Models(False ->First)
                removedata= {
                    "BotId" : chatDto.botID,
                    "History": [[31373, 50256,15496, 13,50256]] # Do Model tra ve Bao gom ket qua tin nhan va History

                }
                updated = user_collection.update_many(
                    {"_id": ObjectId(chatDto.userID) },
                    {"$set":{"messageCurrent":dict(removedata)}}
                )
            user_collection.update_many({"_id": ObjectId(chatDto.userID) },{"$pull":{"message":""}})
            updated = user_collection.update_many(
                {"_id": ObjectId(chatDto.userID) },
                {"$push":{"message":dict(data)}}
                )
            if(updated.modified_count):
                return {"message":"Chat Success","status": True}
            else:
                return {"message":"User ID not exist","status": True}
            
        else:
            return {"message":"Bot ID is not exist!","status": False}
    def get_all_messAChat(self, chatID: str):

        find_chat = chat_collection.find({
            '_id': ObjectId(chatID)
        }) 

        if find_chat:
            mess = mess_collection.find({'botID': ObjectId(chatID)})
            return self.binding_chat(mess)
            
        else:
            return {"message":"Bot ID is not exist!","status": False}
    def sentMessageBuy(self, chatPayment: chatPayment):
        find_payment = payments_collection.find({
            '$and': [{'_id': ObjectId(chatPayment.securitykey)},
                    {'userID': chatPayment.userID},
                    {'botID': chatPayment.botID},
                    {'status': bool("True")}]
        }) 
        if find_payment:
            mess_collection = createDBChatUser('Message'+chatPayment.username)
            data =  self.chat_data(chatPayment)
            
            mess_collection.insert_one(dict(data))
            return {"message":"Chat Success","status": True}
            
        else:
            return {"message":"404!","status": False}