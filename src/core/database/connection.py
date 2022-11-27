from pymongo import MongoClient
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODBURL = os.environ.get("MONGODBURL")
DBNAME = os.environ.get("DBNAME")
PORT = os.environ.get("PORT")


client = MongoClient(MONGODBURL, int(PORT))
db = client['ChatbotDB']
user_collection = db.get_collection('User')
chat_collection = db.get_collection('Botchat')
mess_collection = db.get_collection('MessageHung')
payments_collection = db.get_collection('Payment')
def createDBChatUser(namedb: str):
    mess_collectionUser = db.get_collection(namedb)
    return mess_collectionUser