
import json
import random
import requests
from intent_recog import intent_rec
from config import getGeneral
from gacha import gacha
from characters import characters
#In the future i will improve methods in this file to combine similar methods into one. 


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
            if "members" in intents:
                members()
            elif "cards" in intents:
                cards()
        elif "gacha" in intents:
            gacha()
        #elif "change tone" in intents:
            #changeBotTone()
    else:
        print("We are sorry for the mistake! Please try to input your intents again:)") 
        return 

    
    #the goal is to guide users to different sub methods
def cards():
    while True:
        print("Would you like to look up a specific card, or look up for a list of cards?")
        idea_input = input()
        idea = intent_rec(idea_input, "card")

        if not idea:
            print("Sorry, I `don't understand your intent. Please try again.")
            continue


        if "single card" in idea and len(idea) == 1:
            handle_single_card()
        elif "list of cards" in idea and len(idea) == 1:
            handle_list_of_cards()
        else:
            print("Sorry, I don't understand your intent. If you would like to search for a single card, please enter '1', if you would like to go back to the main menu, pleade enter '0', or enter anything else for getting a list of cards.")
            choice = input()
            if choice == 1:
                handle_single_card()
            elif choice == 0:
                print("Taking you back....")
                print("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
                return 
            else:
                handle_list_of_cards()

        print("Would you like to search for another card/list of cards?")
        yn_input = input("").lower()
        if yn_input.startswith("y") or yn_input.startswith("c"):
            continue 
        else:
            print("Taking you back....")
            print("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
            return 
        
        
def handle_single_card():
    print("What card would you like to look up for? Please make sure that the name of the card is as accurate as possible so I could get you the results quickly!")
    name = input()
    all_data = getGeneral("cards").get("results")
    matches = match_member_name(name, all_data) #see match_member_name for why i call this method.

    if not matches:
        print("No matching card found. Please try again.")
        return

    if len(matches) == 1:
        display_card_info(matches[0], all_data)
    else:
        selected = handle_multiple_matches(matches)
        if selected:
            display_card_info(selected, all_data)
            
            
def display_card_info(name, all_data):
    for card in all_data:
        if card.get("name") == name:
            print(f"Here’s what I found for {name}:")
            print(card)
            
def handle_list_of_cards():
    
    while True:
        print("Please input the desired filters for your customized card list! You can have as many filters as you want!")
        print("Input multiple numbers if you want to have multiple filters. Don't put spaces between numbers.")
        print("If you choose character and band both as filters, we will assume that you want filter by character.")
        print("Enter 0 for sorting cards by stars.")
        print("Enter 1 for sorting cards by attributes.")
        print("Enter 2 for sorting cards by character.")
        print("Enter 3 for sorting cards by band.")
        print("Enter 4 for sorting cards by skills.")
        intent = input()
        intent = intent.split()
        intent = "".join(intent)#just in case if the user input spaces
        

        try:
            intent = list(set(int(x) for x in intent))
            if 2 in intent and 3 in intent:
                intent.remove(3)
            for num in intent:
                if num > 4 or num < 0:
                    raise ValueError
            break
                
        except ValueError:
            print("Input NUMERIC value greater than 0 and smaller than 5 only please!")
      
    intent = list(set(intent))    #remove duplicates

    display_list_of_cards(intent)

def display_list_of_cards(intent):
    print("Got it! Since Bandori has a super laaaaaaaarge database, please wait for processing! I'll be ready in a minute!")
    data = getGeneral("cards").get("results")

    #i_rarity: 12345
    for num in intent:
        if num == 0:
            print("Please enter 1, 2, 3, 4 or 5 of the rarity you want to cards to have.")
            rarity = input()
            while True:
                try:
                    rarity = int(rarity)
                    if rarity > 5 or rarity < 1:
                        raise ValueError
                    break
                except ValueError:
                    print("Please input a correct value!")
                    print("Please enter 1, 2, 3, 4 or 5 of the rarity you want to cards to have.")
                    
            data = [card for card in data if card.get("i_rarity") == rarity]
                    
        #i_attribute: Power, Cool, Cute, Happy
        if num == 1:
            attribute = ""
            while True:
                print("Please enter the desired attribute of the cards!")
                print("The four attributes are: Power, Cool, Cute and Happy.")
                print("Remember that there is only one attribute for the card.")
                attribute = input()
                attribute.strip()
                attribute = attribute.lower()
                attribute = attribute.capitalize()
                if attribute not in {"Power","Cool", "Cute", "Happy"}:
                    print("Please input a correct attribute!")
                    continue
                break
            data = [card for card in data if card.get("i_attribute") == attribute]
            
            
        #member: find member name -> id match
        if num == 2:
            id = 0
            while True:
                print("Please input the name of desired character")
                name = input()
                mem_data = getGeneral("members").get("results")
                matches = match_member_name(name, mem_data)

                if not matches:
                    print("No matching member found. Please try again.")
                    continue

                if len(matches) == 1:
                    for member in mem_data:
                        if member.get("name") == matches[0]:
                            id = member.get("id")
                    break
                else:
                    selected = handle_multiple_matches(matches)
                    if selected:
                        for member in mem_data:
                            if member.get("name") == matches[0]:
                                id = member.get("id")
                        break
                    
            data = [card for card in data if card.get("member") == id]
            
            
        #band: find band name -> multiple id matches
        if num == 3:
            print("Please enter the desired band name:")
            print("Available bands: Afterglow, Poppin'Party, Hello, Happy World!, Pastel*Palettes, Roselia, Morfonica, RAISE A SUILEN, MyGO!!!!!")
            print("Note that while you can still input Ave Mujica, their cards are not up in the game yet so I won't return any result.")
            band_input = input().strip().lower()
            #i included nicknames
            band_map = {
                "afterglow": "Afterglow",
                "ag": "Afterglow",
                "poppinparty": "Poppin'Party",
                "poppin'party": "Poppin'Party",
                "ppp": "Poppin'Party",
                "hello happy world": "Hello, Happy World!",
                "hhw": "Hello, Happy World!",
                "pastel palettes": "Pastel*Palettes",
                "pastel*palettes": "Pastel*Palettes",
                "pp": "Pastel*Palettes",
                "roselia": "Roselia",
                "morfonica": "Morfonica",
                "monica": "Morfonica",
                "raise a suilen": "RAISE A SUILEN",
                "ras": "RAISE A SUILEN",
                "mygo": "MyGO!!!!!",
                "mygo!!!!!": "MyGO!!!!!",
                "ave mujica": "Ave Mujica",
                "mujica": "Ave Mujica"
            }

            band_name = band_map.get(band_input)
            if not band_name:
                print("Invalid band name. Please try again.")
                return

            member_data = getGeneral("members").get("results")
            member_ids = [m["id"] for m in member_data if m.get("i_band") == band_name]

            if not member_ids:
                print("No members found for that band.")
                return

            data = [card for card in data if card.get("member") in member_ids]
        
            
        #i_skill_type: Score up, Life guard, Life recovery, Perfect Lock
        if num == 4:
            skill = ""
            while True:
                print("Please enter the desired skill of the cards!")
                print("The four skills are: Score up, Life guard, Life recovery, Perfect lock.")
                print("Remember that there is only one skill for the card.")
                skill = input()
                skill.strip()
                skill = skill.lower()
                
                if skill not in {"score up", "life guard", "life recovery", "perfect lock"}:
                    print("Please input a correct skill!")
                    continue
                skill = skill.capitalize()
                break
            
            data = [card for card in data if card.get("i_skill_type") == skill]
        
        
    #End of filter
    if len(data) == 0:
        print("Sorry, there are no cards that matched your search.")  
    else:  
        print(f"{len(data)} cards matched your search.")
        print(f"Here’s a list of cards based on your filter choice:")
        for card in data:
            print(f"♪ {card['name']}")
                

    
    
    
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
    #when i wrote this method i didnt thought about cards but now i realized that this method works for cards as well
    #in the future i will change the variable names in this method for clarity but now i will keep it like this.
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

    

    



        #detect how user look u
        
def get_random_word(index):
    if 'additional_words' in characters[index]:
        return random.choice(index['additional_words'])
    return 
        
#def changeBotTone():
    #return None