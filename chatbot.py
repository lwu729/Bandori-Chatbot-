
import json
import requests
from intent_recog import intent_rec
from config import getGeneral
from gacha import gacha
from characters import tone, stylize_name
tone_enabled = False
tone_index = 0


#In the future i will improve methods in this file to combine similar methods into one. 


def process_intent(user_input):
    intents = intent_rec(user_input, "raw")
  
    if len(intents) > 1:
        pos_intents = ""
        pos_intents = ", or ".join(intents)
        printf(f"I'm a bit confused..did you meant by {pos_intents}? Please select one of those or write 'None' if none of those matches your needs.")
        response = input().lower()
        if response not in {"members","member", "card", "cards", "gacha", "bot"}:
            printf("We are sorry for the mistake! Please try to input your intents again:)") 
            return
        else:
            if "member" in response or "members" in response:
                intents[0] = "members" 
                printf("Seems like you would like to ask about member in Bandori! Is that right~?")
            elif "card" in response or "cards" in response:
                intents[0] = "cards" 
                printf("Seems like you would like to ask about cards in Bandori! Is that right~?")
            elif "gacha" in intents:
                intents[0] = "gacha" 
                printf("Seems like you would like to use the gacha simulator in Bandori! Is that right~?")
            elif "bot" in intents:
                intents[0] = "bot" 
                printf("Seems like you would like to change my tone of voice! Is that right~?")
            else:
                printf("We are sorry for the mistake! Please try to input your intents again:)") 
                return 
        
    if len(intents) == 1:
        printf(f"Seems like you would like to ask about {intents[0]} in Bandori! Is that right~?")
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
        elif "bot" in intents:
            changeBotTone()
    else:
        printf("We are sorry for the mistake! Please try to input your intents again:)") 
        return 

def changeBotTone():
    global tone_enabled, tone_index

    while True:
        print("Would you like to speak with a character from Bandori? Please enter 'Yes' or 'No'. ")
        choice = input().lower()
        if choice.startswith("y"):
            tone_enabled = True
            print("Choose a character: 0 for Sakiko, 1 for Ako, 2 for Rinko")
            try:
                index = int(input())
                if index in [0, 1, 2]:
                    tone_index = index
                    printf("Yay! I'm ready to help in character voice.")
                    break
                else:
                    print("Invalid input. Please try again.")
            except ValueError:
                print("Invalid input. Please try again.")
        else:
            print("Okay! Taking you back to the main menu...")
            break

    print("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
            
            
    #the goal is to guide users to different sub methods
def cards():
    while True:
        printf("Would you like to look up a specific card, or look up for a list of cards?")
        idea_input = input()
        idea = intent_rec(idea_input, "card")

        if not idea:
            printf("Sorry, I `don't understand your intent. Please try again.")
            continue


        if "single card" in idea and len(idea) == 1:
            handle_single_card()
        elif "list of cards" in idea and len(idea) == 1:
            handle_list_of_cards()
        else:
            printf("Sorry, I don't understand your intent. If you would like to search for a single card, please enter '1', if you would like to go back to the main menu, pleade enter '0', or enter anything else for getting a list of cards.")
            choice = input()
            if choice == 1:
                handle_single_card()
            elif choice == 0:
                printf("Taking you back....")
                printf("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
                return 
            else:
                handle_list_of_cards()

        printf("Would you like to search for another card/list of cards?")
        yn_input = input("").lower()
        if yn_input.startswith("y") or yn_input.startswith("c"):
            continue 
        else:
            printf("Taking you back....")
            printf("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
            return 
        
        
def handle_single_card():
    printf("What card would you like to look up for? Please make sure that the name of the card is as accurate as possible so I could get you the results quickly!")
    name = input()
    all_data = getGeneral("cards").get("results")
    matches = match_member_name(name, all_data) #see match_member_name for why i call this method.

    if not matches:
        printf("No matching card found. Please try again.")
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
            printf(f"Here’s what I found for {name}:")
            print(f"Card ID: {card.get('id')}")
            print(f"Rarity: {card.get('i_rarity')}★")
            print(f"Name of the card: {card.get('name')}")
            print(f"Japanese Name of the card: {card.get('japanese_name')}")
            if card.get("performance_trained_max") == 0:
                print(f"Max Stats: {card.get('performance_max') + card.get('visual_max') + card.get('technique_max')}")
            else:
                print(f"Max Stats: {card.get('performance_trained_max') + card.get('visual_trained_max') + card.get('technique_trained_max')}")

            print(f"Release date: {card.get('release_date')}")
            print(f"Skill name: {card.get('skill_name')}")
            print(f"Japanese skill name: {card.get('japanese_skill_name')}")
            print(f"Skill type: {card.get('i_skill_type')}")
            print(f"Side skill: {card.get('i_side_skill_type')}")
            print(f"Skill template: {card.get('skill_template')}")
           
            
def handle_list_of_cards():
    
    while True:
        printf("Please input the desired filters for your customized card list! You can have as many filters as you want!")
        printf("Input multiple numbers if you want to have multiple filters. Don't put spaces between numbers.")
        printf("If you choose character and band both as filters, we will assume that you want filter by character.")
        printf("Enter 0 for sorting cards by stars.")
        printf("Enter 1 for sorting cards by attributes.")
        printf("Enter 2 for sorting cards by character.")
        printf("Enter 3 for sorting cards by band.")
        printf("Enter 4 for sorting cards by skills.")
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
            printf("Input NUMERIC value greater than 0 and smaller than 5 only please!")
      
    intent = list(set(intent))    #remove duplicates

    display_list_of_cards(intent)

def display_list_of_cards(intent):
    printf("Got it! Since Bandori has a super laaaaaaaarge database, please wait for processing! I'll be ready in a minute!")
    data = getGeneral("cards").get("results")

    #i_rarity: 12345
    for num in intent:
        if num == 0:
            printf("Please enter 1, 2, 3, 4 or 5 of the rarity you want to cards to have.")
            rarity = input()
            while True:
                try:
                    rarity = int(rarity)
                    if rarity > 5 or rarity < 1:
                        raise ValueError
                    break
                except ValueError:
                    printf("Please input a correct value!")
                    printf("Please enter 1, 2, 3, 4 or 5 of the rarity you want to cards to have.")
                    
            data = [card for card in data if card.get("i_rarity") == rarity]
                    
        #i_attribute: Power, Cool, Cute, Happy
        if num == 1:
            attribute = ""
            while True:
                printf("Please enter the desired attribute of the cards!")
                printf("The four attributes are: Power, Cool, Cute and Happy.")
                printf("Remember that there is only one attribute for the card.")
                attribute = input()
                attribute.strip()
                attribute = attribute.lower()
                attribute = attribute.capitalize()
                if attribute not in {"Power","Cool", "Cute", "Happy"}:
                    printf("Please input a correct attribute!")
                    continue
                break
            data = [card for card in data if card.get("i_attribute") == attribute]
            
            
        #member: find member name -> id match
        if num == 2:
            id = 0
            while True:
                printf("Please input the name of desired character")
                name = input()
                mem_data = getGeneral("members").get("results")
                matches = match_member_name(name, mem_data)

                if not matches:
                    printf("No matching member found. Please try again.")
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
            printf("Please enter the desired band name:")
            printf("Available bands: Afterglow, Poppin'Party, Hello, Happy World!, Pastel*Palettes, Roselia, Morfonica, RAISE A SUILEN, MyGO!!!!!")
            printf("Note that while you can still input Ave Mujica, their cards are not up in the game yet so I won't return any result.")
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
                printf("Invalid band name. Please try again.")
                return

            member_data = getGeneral("members").get("results")
            member_ids = [m["id"] for m in member_data if m.get("i_band") == band_name]

            if not member_ids:
                printf("No members found for that band.")
                return

            data = [card for card in data if card.get("member") in member_ids]
        
            
        #i_skill_type: Score up, Life guard, Life recovery, Perfect Lock
        if num == 4:
            skill = ""
            while True:
                printf("Please enter the desired skill of the cards!")
                printf("The four skills are: Score up, Life guard, Life recovery, Perfect lock.")
                printf("Remember that there is only one skill for the card.")
                skill = input()
                skill.strip()
                skill = skill.lower()
                
                if skill not in {"score up", "life guard", "life recovery", "perfect lock"}:
                    printf("Please input a correct skill!")
                    continue
                skill = skill.capitalize()
                break
            
            data = [card for card in data if card.get("i_skill_type") == skill]
        
        
    #End of filter
    if len(data) == 0:
        printf("Sorry, there are no cards that matched your search.")  
    else:  
        printf(f"{len(data)} cards matched your search.")
        printf(f"Here’s a list of cards based on your filter choice:")
        for card in data:
            print(f"♪ {card['name']}")
                

    
    
    
def members():
    while True:
        printf("Would you like to look up a specific member, or look up a list of members with some sort of similarity?")
        idea_input = input()
        idea = intent_rec(idea_input, "member")

        if not idea:
            printf("Sorry, I don't understand your intent. Please try again.")
            continue


        if "similar members" in idea and len(idea) == 1:
            handle_similar_members()
        elif "member" in idea and len(idea) == 1:
            handle_single_member()
        else:
            printf("Sorry, I don't understand your intent. If you would like to search for a single member, please enter '1', if you would like to go back to the main menu, pleade enter '0', or enter anything else for getting a list of members.")
            choice = input()
            if choice == 1:
                handle_single_member()
            elif choice == 0:
                printf("Taking you back....")
                printf("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
                return 
            else:
                handle_similar_members()

        printf("Would you like to search for another member/list of members?")
        yn_input = input("").lower()
        if yn_input.startswith("y") or yn_input.startswith("c"):
            continue 
        else:
            printf("Taking you back....")
            printf("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
            return 
            
def handle_single_member():
    printf("Who would you like to look up for?")
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

    all_member = [person["name"] for person in all_data if isinstance(person.get("name"), str)]

    

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
            if tone_enabled:
                name = stylize_name(name, tone_index)
            printf(f"You asked about {name}, right?")
            printf(f"Here’s what I found for {name}:")
            printf(f"{name}'s Profile")
            printf(f"Band: {person.get('i_band', 'N/A')}")
            printf(f"School: {person.get('school', 'N/A')}")
            printf(f"School Year: {person.get('i_school_year', 'N/A') or 'N/A'}")
            printf(f"Birthday: {person.get('birthday', 'N/A')}")
            printf(f"Astrological Sign: {person.get('i_astrological_sign', 'N/A')}")
            printf(f"Instrument: {person.get('instrument', 'N/A')}")
            printf(f"Likes: {person.get('food_like', 'N/A')}")
            printf(f"Dislikes: {person.get('food_dislike', 'N/A')}")
            printf(f"Japanese CV: {person.get('CV', 'N/A')}")
            printf(f"Romaji CV: {person.get('romaji_CV', 'N/A')}")
            printf("Description:")
            printf(person.get("description", "N/A"))
            return
        
        
def handle_multiple_matches(matches):
    printf(f"I'm a bit confused... Did you mean {', '.join(matches)}?")
    printf("Please select one of those or write 'None' if none of them match your needs.")
    answer = input().strip()

    if answer.lower() == "none":
        return None
    elif any(answer.lower() == name.lower() for name in matches):
        return next(name for name in matches if name.lower() == answer.lower())
    else:
        printf("Sorry, I didn't understand that.")
        return None

def handle_similar_members():
    printf("Please input the desired characteristics for list of similar members.")
    printf("They could be: same astro signs, school, school year, band, or band role.")
    printf("Note that members who have gone to university does not have a school year!")
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
        printf(f"Please select from the list below: {', '.join(options)}.")
        printf("Make sure that your response is EXACTLY the same as the given choices on the list!")
    else:
        printf("Sorry, I don't support this type of filter yet.")
        return

    select = input().strip()
    filtered_list = [m for m in mem_list if m.get(intent) == select]
    

    if not filtered_list:
        printf("No members found with that value. Please try again.")
        return
        #End of filter
    else:  
        printf(f"{len(filtered_list)} members matched your search:")
        for member in filtered_list:
            print(f"♪ {member['name']}")

        #detect how user look upy
        
def printf(message):
    if tone_enabled:
        print(tone(message, tone_index))
    else:
        print(message)
