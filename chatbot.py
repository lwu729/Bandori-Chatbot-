
import json
import requests
from intent_recog import intent_rec
from config import getGeneral
from gacha import gacha


def process_intent(user_input):
    intents = intent_rec(user_input, "raw")
  
    if len(intents) > 1:
        pos_intents = ""
        pos_intents = ", or ".join(intents)
        print(f"I'm a bit confused..did you meant by {pos_intents}? Please select one of those or write 'None' if none of those matches your needs.")
        response = input().lower()
        if response not in {"members","member", "card", "cards", "gacha"}:
            print("We are sorry for the mistake! Please try to input your intents again:)") 
            return
        else:
            if "member" in response or "members" in response:
                intents[0] = "members" 
                print(f"Seems like you would like to ask about member in Bandori! Is that right~?")
            elif "card" in response or "cards" in response:
                intents[0] = "cards" 
                print(f"Seems like you would like to ask about cards in Bandori! Is that right~?")
            elif "gacha" in intents:
                intents[0] = "gacha" 
                print(f"Seems like you would like to use the gacha simulator in Bandori! Is that right~?")
            else:
                print("We are sorry for the mistake! Please try to input your intents again:)") 
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
        #elif "change tone" in intents:
            #changeBotTone()
    else:
        print("We are sorry for the mistake! Please try to input your intents again:)") 
        return 

    
    #the goal is to guide users to different sub methods
    
def members():
    while True:
        print("Would you like to look up a specific member, or look up a list of members with some sort of similarity?")
        idea_input = input()
        idea = intent_rec(idea_input, "member")

        if not idea:
            print("Sorry, I don't understand your intent. Please try again.")
            continue


        if "similar members" in idea and len(idea) == 1:
            handle_similar_members()
        elif "member" in idea and len(idea) == 1:
            handle_single_member()
        else:
            print("Sorry, I don't understand your intent. If you would like to search for a single member, please enter '1', if you would like to go back to the main menu, pleade enter '0', or enter anything else for getting a list of members.")
            choice = input()
            if choice == 1:
                handle_single_member()
            elif choice == 0:
                print("Taking you back....")
                print("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
                return 
            else:
                handle_similar_members()

        print("Would you like to search for another member/list of members?")
        yn_input = input("").lower()
        if yn_input.startswith("y") or yn_input.startswith("c"):
            continue 
        else:
            print("Taking you back....")
            print("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
            return 
            
def handle_single_member():
    print("Who would you like to look up for?")
    name = input()
    all_data = getGeneral("members").get("results")
    matches = match_member_name(name, all_data)

    if not matches:
        print("No matching member found. Please try again.")
        return

    if len(matches) == 1:
        display_member_info(matches[0], all_data)
    else:
        selected = handle_multiple_matches(matches)
        if selected:
            display_member_info(selected, all_data)
            
def match_member_name(user_input, all_data):
    name_list = list(user_input.lower())
    sim_index = 0
    high_sim = []

    all_member = [person["name"] for person in all_data if "name" in person]

    for person_name in all_member:
        person_list = list(person_name.lower())
        name_temp = name_list.copy()
        current_index = 0

        for char in person_list:
            if char in name_temp:
                current_index += 1
                name_temp.remove(char)

        if current_index > sim_index:
            sim_index = current_index
            high_sim = [person_name]
        elif current_index == sim_index:
            high_sim.append(person_name)

    return high_sim


def display_member_info(name, all_data):
    for person in all_data:
        if person.get("name") == name:
            print(f"Here’s what I found for {name}:")
            print(person)
        
        
def handle_multiple_matches(matches):
    print(f"I'm a bit confused... Did you mean {', '.join(matches)}?")
    print("Please select one of those or write 'None' if none of them match your needs.")
    answer = input().strip()

    if answer.lower() == "none":
        return None
    elif any(answer.lower() == name.lower() for name in matches):
        return next(name for name in matches if name.lower() == answer.lower())
    else:
        print("Sorry, I didn't understand that.")
        return None

def handle_similar_members():
    print("Please input the desired characteristics for list of similar members.")
    print("They could be: same astro signs, school, school year, band, or band role.")
    print("Note that members who have gone to university does not have a school year!")
    intent = input()
    intent = intent_rec(intent, "sim_member")
    display_list_of_members(intent[0])
    

                        
def display_list_of_members(intent):
    all_data = getGeneral("members").get("results")
    mem_list = [member for member in all_data if member.get(intent)]
    prompts = {
        "i_astrological_sign": ("astro sign", [
            "Leo", "Aries", "Libra", "Virgo", "Scorpio", "Capricorn",
            "Pisces", "Gemini", "Cancer", "Sagittarius", "Aquarius", "Taurus"
        ]),
        "i_school_year": ("school year", ["First", "Second", "Third", "JrThird"]),
        "school": ("school", [
            "Hanasakigawa Girls' Academy", "Haneoka Girls' Academy",
            "Tsukinomori Girls' High School", "Gejiutsu High School of Fine Arts",
            "Shirayuki Girls' Academy", "Kamogawa Central Middle School",
            "Celosia Girls' Academy", "Yotsuba Women's University", "Keiho Women's University"
        ]),
        "i_band": ("band", [
            "Afterglow", "Poppin'Party", "Hello, Happy World!", "Pastel*Palettes",
            "Roselia", "Morfonica", "RAISE A SUILEN", "MyGO!!!!!", "Ave Mujica"
        ]),
        "instrument": ("band role", [
            "Guitar & Vocals", "Guitar", "Bass", "Drums", "Keyboard", "DJ",
            "Vocals", "Violin", "Rhythm guitar", "Keytar"
        ])
    }

    if intent in prompts:
        display_name, options = prompts[intent]
        print(f"Please select from the list below: {', '.join(options)}")
        print("Make sure that your response is EXACTLY the same as the given choices on the list!")
    else:
        print("Sorry, I don't support this type of filter yet.")
        return

    select = input().strip()
    filtered_list = [m for m in mem_list if m.get(intent) == select]

    if not filtered_list:
        print("No members found with that value. Please try again.")
        return

    print(f"Here’s a list of members with the same {display_name}:")
    for m in filtered_list:
        print(f"♪ {m['name']}")

    



        #detect how user look u
        
#def changeBotTone():
    #return None