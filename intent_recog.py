# figure out user intent to guide to different functions of chatbot
import re

#raw allows: member, gacha, cards, bot tone, assets
def intent_rec(raw_user_input):
    #define list of possible keywords for matching
    maybe_members = {"member", "members", "character", "characters", "look", "up", "search", "find", "who", "info", "details", "person","people", "game", "in-game"}
    maybe_cards = {"look", "up", "card", "cards", "game", "in-game", "info", "details","search", "find","ability", "battle", "compare"}
    maybe_gacha = {"gacha", "pull", "pulls", "roll", "draw", "scout","get", "simulator"}
    maybe_bot = {"bot", "tone", "character", "change", "voice", "speak", "style", "modify", "sound","like","chatbot"}
    
    #member branch:
    #at this point users can: find a member, find a band
    find_member = {"name", "band", "look", "up", "search"}
    
    #member specifics:
    #at this point users can search: Astrological Sign, school/school year, fav/least fav food, role, birthday, CV, list of cards
    
    intents = raw_user_input
    intents = set(re.findall(r'\b\w+\b', raw_user_input.lower()))
    # this line is from asking chatgpt because I don't know how to efficiently solve the problem with punctuations

    #matching algo is acheived through matching with keywords list
    mem_index = len(maybe_members & intents)
    card_index = len(maybe_cards & intents)
    gacha_index = len(maybe_gacha & intents)
    bot_index = len(maybe_bot & intents)
    
    
    
    indexes = {"members":mem_index, "cards":card_index, "gacha":gacha_index, "change tone":bot_index}

    max_index = max(indexes, key=indexes.get)
    max_value = indexes[max_index] 
    maxx = []
    for key, value in indexes.items():
        if value == max_value:
            maxx.append(key)
            
    return maxx
