from api.botchat.entities.chat import AppChat
from bson import ObjectId
import bson
from core.database.connection import db, chat_collection,payments_collection,user_collection
from api.botchat.dtos.chatbot_dto import ChatBotDto
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders   import jsonable_encoder

class chatServices():
    def chat_helper(self, chat) -> dict:
        return {
            "id": str(chat["_id"]),
            "title":str(chat["title"]),
            "link": str(chat["link"]),
            "status": chat["status"],
            "prices": chat["prices"],
            "linkAvatar": chat["linkAvatar"],
            
        }
    def binding_chat(self, datas):
        chats = []
        for data in datas:
            chat = {
            "id": str(data["_id"]),
            "title":str(data["title"]),
            #"link": str(data["link"]),
            "status": data["status"],
            "prices" : data["prices"],
            "linkAvatar": data["linkAvatar"]

            }
            chats.append(chat)
        return chats
            
    def chat_data(self, chatDto: ChatBotDto): 
        chat =  {
            "title": chatDto.title,
            "link": chatDto.link,
            "status": chatDto.status,
            "prices": chatDto.prices,
            "linkAvatar": chatDto.linkAvatar,
        }
        return chat
    
    def get_all_Chat(self):
        mess = chat_collection.find()
        return self.binding_chat(mess)
    def getchatbotDetail(self,userID,botID):
        find_payment = payments_collection.count_documents({
            '$and': [{'userID': userID},
                        {'botID': botID}]
        })
        if find_payment > 0:
            mess = chat_collection.find({'_id':ObjectId(botID)})
            return {"ChatBot":mess,"status": True}
                
        else:
            return {"Buyer": False,"status": True}    
    def create_bot(self, chatBOTDto: ChatBotDto):

        data =  self.chat_data(chatBOTDto)
        
        chat_collection.insert_one(dict(data))
        return {"message":"Chat Bot Create Success","status": True}
    
    def getlinkbot(self, securitykey: str,userID: str):
        # kiem tra user
        try:
            find_user = user_collection.count_documents({'_id': ObjectId(userID)})
            if find_user:
                
                    payment = payments_collection.find({
                            '$and': [{'_id': ObjectId(securitykey)},
                            {'status': bool("true")}]
                    })
                    if payment:
                        mess = chat_collection.find({
                            '_id': ObjectId(payment.botID)
                        })
                        data = self.chat_data(mess)
                        
                        return {"link":userID + "/" + data.link, "status": True}
                    else:
                        return {"message":"Your invoice has been deleted or does not exist!","status": False}
                
            else:
                return {"message": "KeyError","status": False}
    
        except Exception as e:
                return {"message": str(e),"status": False}
