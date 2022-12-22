from transformers import AutoModelWithLMHead, AutoTokenizer
import torch

class modelService():
    tokenizer = ""
    model = ""
    def __init__(self, namemodel:str):
        # tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium', padding_side='left')
        tokenizer = AutoTokenizer.from_pretrained('output-medium')
        tokenizer.padding_side = 'left'
        model = AutoModelWithLMHead.from_pretrained('output-medium')

        # torch.save(model.state_dict(), "model.pt")
    def printChatModel(self, message):
        firstLine = True
        while True:
            # encode the new user input, add the eos_token and return a tensor in Pytorch
            new_user_input_ids = self.tokenizer.encode(input(">> User:") + self.tokenizer.eos_token, return_tensors='pt')
            # print(new_user_input_ids)

            # append the new user input tokens to the chat history
            # bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if not firstLine else new_user_input_ids

            # generated a response while limiting the total chat history to 1000 tokens, 
            chat_history_ids = self.model.generate(
                bot_input_ids, max_length=200,
                pad_token_id=self.tokenizer.eos_token_id,  
                no_repeat_ngram_size=3,       
                do_sample=True, 
                top_k=100, 
                top_p=0.7,
                temperature=0.8
            )

            firstLine = False
            
            # pretty print last ouput tokens from bot
            print("Harry: {}".format(self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True, padding_side='left')))
