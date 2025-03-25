#handles main chatbot logic. https://pypi.org/project/pydori/
import json
import requests
from intent_recog import intent_rec
from config import getGeneral
from gacha import gacha


def process_intent(user_input):
    intents = intent_rec(user_input)
  
    if len(intents) > 1:
        pos_intents = ""
        pos_intents = ", or ".join(intents)
        print(f"I'm a bit confused..did you meant by {pos_intents}? Please select one of those or write 'None' if none of those matches your needs.")
        response = input().lower()
        if response not in {"members", "cards", "gacha", "change tone"}:
            return
        
    if len(intents) == 1:
        print(f"Seems like you would like to ask about {intents[0]} in Bandori! Is that right~?")
    yn_input = input("")
    yn_input = yn_input.lower()
        
    if yn_input.startswith("y"):
        if "members"in intents or "cards" in intents:
            getGeneral(intents[0])
        elif "gacha" in intents:
            gacha()
        elif "change tone" in intents:
            changeBotTone()
    else:
        print("We are sorry for the mistake! Please try to input your intents again:)") 
        return 
   
        
        

    
    
    #the goal is to guide users to different sub methods
    
    
    
#def members(user_input):
    #detect how user look u
    
def changeBotTone():
    return None