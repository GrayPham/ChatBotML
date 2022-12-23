from transformers import AutoModelWithLMHead, AutoTokenizer
import numpy as np
import json
import requests
import time
class modelService():
    API_URL = ""
    headers = ""
    def __init__(self, namemodel:str):
        self.API_URL = "https://api-inference.huggingface.co/models/satvikag/chatbot"
        self.headers = {"Authorization": "Bearer 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"}
    def printChatModel(self, payload ):
        data = json.dumps(payload)
        response = requests.post(self.API_URL, headers=self.headers, data=data)
        if (response.status_code == 503):  # This means we need to wait for the model to load 😴.
            estimated_time = response.json()["estimated_time"]
            time.sleep(estimated_time)
            data = json.loads(data)
            data["options"] = {"use_cache": False, "wait_for_model": True}
            data = json.dumps(data)
            response = requests.post(self.API_URL, headers=self.headers, data=data)
        generated_responses = json.loads(response.content.decode("utf-8"))["conversation"]["generated_responses"]
        past_user_inputs = json.loads(response.content.decode("utf-8"))["conversation"]["past_user_inputs"]
        response = json.loads(response.content.decode("utf-8"))["generated_text"]

        return response, generated_responses, past_user_inputs
    
