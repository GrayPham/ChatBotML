
from src.api.payment.entities.PaymentEntitiy import AppPayment
from bson import ObjectId
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from os import getenv

from src.core.database.connection import db, user_collection,payments_collection
from src.api.payment.dtos.PaymentDto import PaymentDto
from paypalcheckoutsdk.orders import OrdersCreateRequest
from fastapi import Request
from fastapi.responses import JSONResponse


from datetime import datetime



class PaymentService():
    
    def user_helper(self, payment) -> dict:
        return {
            "id": str(payment["_id"]),
            "userID": payment["userID"],
            "botID": payment["botID"],
            "dateBought": payment["dateBought"],
            "price": payment["price"],
            "paymentMethod": payment["paymentMethod"],
            "status": True,
        }
    def binding_payment(self, datas):
        payments = []
        for data in datas:
            payment = {
            "SERECTKEY": str(data["_id"]),
            "paymentID": data["paymentID"],
            "botID": data["botID"],
            "dateBought": data["dateBought"],
            "price": data["price"],
            "paymentMethod": data["paymentMethod"],
            }
            payments.append(payment)
            print(payments)
        return payments
    def payment_data(self, paymentDto: PaymentDto): 
        payment =  {
            "paymentID": paymentDto.paymentID,
            "botID": paymentDto.botID,
            "dateBought": paymentDto.dateBought,
            "price": paymentDto.price,
            "paymentMethod" : paymentDto.paymentMethod,
            "status": True,

        }
        return payment
    def payment_Abot(self, paymentDto: PaymentDto): 
        print(paymentDto)
        data =  self.payment_data(paymentDto)
        # 
        # find_payment = payments_collection.find({
        #     '$and': [{'botID': paymentDto.botID},
        #     {'userID': paymentDto.userID}]
        # }) 

        if paymentDto.userID:
            user_collection.update_many(
                {"_id": ObjectId(paymentDto.userID) },
                {"$push":{"payment":dict(data)}}
                )
            return {"message":"Payment Successfully","status": True}
            
        else:
            return {"message":"You already bought this chatbot!","status": False}
    def allChatBotPayment(self, userID: str):
        payment = payments_collection.find({
                '$and': [{'userID': userID},
                {'status': bool("true")}]
        })
        return self.binding_payment(payment)
    def allPayment(self):
        payment = payments_collection.find()
        return self.binding_payment(payment)
    
    def deletePayment(self, idpayment: str):
        myquery = { '$and': [{"_id": ObjectId(idpayment)},{'status': bool("true")} ] }
        
        newvalues = { "$set": { 'status': bool(0) } }
        print(newvalues)
        payment = payments_collection.update_many(myquery,newvalues)
        if payment.modified_count >0:
            
            return {"message":"You already delete this chatbot!","status": True}
        else:
            return {"message":"Your invoice has been deleted or does not exist!","status": False}
    def checkpayment(self, userId, botID):
        find_payment = user_collection.find_one({
            '$and': [{'_id': ObjectId(userId)},
                    {'payment.botID': botID},
                    ]
        }) 
        if find_payment:
            return {"message": True, "status": True}
        else:
            return {"message":False,"status": True}
    
        