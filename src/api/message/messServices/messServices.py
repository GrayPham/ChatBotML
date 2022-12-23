

from api.message.entities.chatCreate import AppUser
from bson import ObjectId
import bson
from api.model.model import modelService
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
    
    def chat_datapayment(self, chatDto: ChatDto): 
        chat =  {
            "botID": chatDto.botID,
            "userID": chatDto.userID,
            "message": chatDto.message,
            "firstCheck": chatDto.firstCheck,
            "securitykey": chatDto.securitykey

        }
        return chat

    def create_mess(self, chatDto: ChatDto):
        print(chatDto)
        data =  self.chat_data(chatDto)
        

        find_chat = chat_collection.find_one({
            '_id': ObjectId(chatDto.botID)
        }) 
        print("find_chatlink",find_chat["link"])
        if find_chat:   
            # Check history_ids for chatbot and user
            user = user_collection.find_one({'_id': ObjectId(chatDto.userID)})
            
            mess_services = modelService(find_chat["link"])
            response =""
            generated_responses =""
            past_user_inputs = ""
            if  chatDto.firstCheck == True:
                print("True")
                response, generated_responses, past_user_inputs = mess_services.printChatModel(
                    {"inputs":
                        {"generated_responses":[],
                        "past_user_inputs":[],
                        "text":chatDto.message}
                    }
                )
                print("History", response)
                print("Bot Message", generated_responses)
                removedata= {
                        "BotId" : chatDto.botID,
                        "HistoryBot": generated_responses, # Do Model tra ve Bao gom ket qua tin nhan va History
                        "HistoryUser": past_user_inputs,

                }
                updated = user_collection.update_many(
                        {"_id": ObjectId(chatDto.userID) },
                        {"$set":{"messageCurrent":dict(removedata)}}
                    )

                    
            else: 
                print("False")
                # Goi Models(False ->First)
                history_user = user["messageCurrent"]["HistoryUser"]
                history_bot = user["messageCurrent"]["HistoryBot"]
                response, generated_responses, past_user_inputs = mess_services.printChatModel(
                    {"inputs":
                        {"generated_responses":history_bot,
                        "past_user_inputs":history_user,
                        "text":chatDto.message}
                    }
                )
                print("History", past_user_inputs)
                print("Bot Message", generated_responses)


                removedata= {
                    "BotId" : chatDto.botID,
                    "HistoryBot": generated_responses, # Do Model tra ve Bao gom ket qua tin nhan va History
                    "HistoryUser": past_user_inputs,

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
                return {"message": response,"status": True}
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

        data =  self.chat_datapayment(chatPayment)
        

        find_chat = user_collection.count_documents({
            'payment.paymentID': chatPayment.securitykey
        }) 
        chat = chat_collection.count_documents({
            '_id': ObjectId(chatPayment.botID)
        }) 
        if find_chat:   
            # Check history_ids for chatbot and user
            user = user_collection.find_one({'_id': ObjectId(chatPayment.userID)})
            print(user["messageCurrent"])
            mess_services = modelService(chat["link"])
            response =""
            generated_responses =""
            past_user_inputs = ""
            if  chatPayment.firstCheck == True:
                print("True")
                response, generated_responses, past_user_inputs = mess_services.printChatModel(
                    {"inputs":
                        {"generated_responses":[],
                        "past_user_inputs":[],
                        "text":chatPayment.message}
                    }
                )
                print("History", response)
                print("Bot Message", generated_responses)
                removedata= {
                        "BotId" : chatPayment.botID,
                        "HistoryBot": generated_responses, # Do Model tra ve Bao gom ket qua tin nhan va History
                        "HistoryUser": past_user_inputs,

                }
                updated = user_collection.update_many(
                        {"_id": ObjectId(chatPayment.userID) },
                        {"$set":{"messageCurrent":dict(removedata)}}
                    )

                    
            else: 
                print("False")
                # Goi Models(False ->First)
                history_user = user["messageCurrent"]["HistoryUser"]
                history_bot = user["messageCurrent"]["HistoryBot"]
                response, generated_responses, past_user_inputs = mess_services.printChatModel(
                    {"inputs":
                        {"generated_responses":history_bot,
                        "past_user_inputs":history_user,
                        "text":chatPayment.message}
                    }
                )
                print("History", past_user_inputs)
                print("Bot Message", generated_responses)


                removedata= {
                    "BotId" : chatPayment.botID,
                    "HistoryBot": generated_responses, # Do Model tra ve Bao gom ket qua tin nhan va History
                    "HistoryUser": past_user_inputs,

                }
                updated = user_collection.update_many(
                    {"_id": ObjectId(chatPayment.userID) },
                    {"$set":{"messageCurrent":dict(removedata)}}
                )
            user_collection.update_many({"_id": ObjectId(chatPayment.userID) },{"$pull":{"message":""}})
            updated = user_collection.update_many(
                {"_id": ObjectId(chatPayment.userID) },
                {"$push":{"message":dict(data)}}
                )
            if(updated.modified_count):
                return {"message": response,"status": True,"First": False}
            else:
                return {"message":"User ID not exist","status": True,"First": True}
            
        else:
            return {"message":"Bot ID is not exist!","status": False,"First": True}