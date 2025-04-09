
import json
import requests
from intent_recog import intent_rec
from config import getGeneral
from gacha import gacha


def process_intent(user_input):
    print("How may I help you? I'm currently able to handle requests related to members and cards within the game,")
    print("gacha simulator, and you can also change my tone of voice to your favorite character in Bandori!")
    print("Feel free to send your request over in full sentences! I'll try my best to help~♪")
    intents = intent_rec(user_input, "raw")
  
    if len(intents) > 1:
        pos_intents = ""
        pos_intents = ", or ".join(intents)
        print(f"I'm a bit confused..did you meant by {pos_intents}? Please select one of those or write 'None' if none of those matches your needs.")
        response = input().lower()
        if response not in {"members","member", "card", "cards", "gacha", "change tone"}:
            return
        
    if len(intents) == 1:
        print(f"Seems like you would like to ask about {intents[0]} in Bandori! Is that right~?")
    yn_input = input("")
    yn_input = yn_input.lower()
        
    if yn_input.startswith("y"):
        if "members" in intents or "cards" in intents:
            results = getGeneral(intents[0])
            if "members" in intents:
                members()
        elif "gacha" in intents:
            gacha()
        elif "change tone" in intents:
            changeBotTone()
    else:
        print("We are sorry for the mistake! Please try to input your intents again:)") 
        return 

    
    #the goal is to guide users to different sub methods
    
def members():
    while True:
        print("Who would you like to look up for?")
        name = input()
        name_set = set(name.lower())

        sim_index = 0
        high_sim = []
        all_data = getGeneral("members").get("results")
        all_member = []

        for person in all_data:
            # Extract and collect names
            if "name" in person:
                all_member.append(person["name"])

        for person_name in all_member:
            person_set = set(person_name.lower())
            current_index = len(person_set & name_set)
            if current_index > sim_index:
                sim_index = current_index
                high_sim = [person_name] 
            elif current_index == sim_index:
                high_sim.append(person_name) 

        if high_sim:
            print(f"Seems like you would like to ask about {high_sim[0]} in Bandori!")
            for person in all_data:
                if person.get("name") == high_sim[0]:
                    print(person)
            return
        else:
            print("No matching member found.")

        
                    
                
            

        #detect how user look u
        
def changeBotTone():
    return None