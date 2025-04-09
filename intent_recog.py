# figure out user intent to guide to different functions of chatbot
import re

#raw allows: member, gacha, cards, bot tone, assets
def intent_rec(raw_user_input, guide):
    #define list of possible keywords for matching, "raw"
    maybe_members = {"member", "members", "character", "characters", "look", "up", "search", "find", "who", "info", "details", "person","people", "game", "in-game"}
    maybe_cards = {"look", "up", "card", "cards", "game", "in-game", "info", "details","search", "find","ability", "battle", "compare"}
    maybe_gacha = {"gacha", "pull", "pulls", "roll", "draw", "scout","get", "simulator"}
    maybe_bot = {"bot", "tone", "character", "change", "voice", "speak", "style", "modify", "sound","like","chatbot"}
    
    #member branch, "member":
    #at this point users can: find a member, find all the members in a band
    find_member = {"name", "a", "member", "look", "up", "search"}
    find_band = {"all", "members", "from", "certain", "band", "roselia", "ppp", "poppin'party", "ag", "afterglow"}
    
    #member specifics, "mem_specifics":
    #at this point users can search: Astrological Sign, school/school year, fav/least fav food, role, birthday, CV, list of cards
    astro = {}
    school = {}
    school_year = {}
    likes_dislikes = {}
    band_role = {}
    birthday = {}
    cv = {}
    list_of_cards = {}
    
    intents = raw_user_input
    intents = set(re.findall(r'\b\w+\b', raw_user_input.lower()))
    # this line is from asking chatgpt because I don't know how to efficiently solve the problem with punctuations
 
    #matching algo is acheived through matching with keywords list
    #raw:
    mem_index = len(maybe_members & intents)
    card_index = len(maybe_cards & intents)
    gacha_index = len(maybe_gacha & intents)
    bot_index = len(maybe_bot & intents)
    
    #member:
    single_mem = len(find_member & intents)
    sim_mem = len(find_band & intents)
    
    
    if guide == "raw":
        indexes = {"members":mem_index, "cards":card_index, "gacha":gacha_index, "change tone":bot_index}
    if guide == "member":
        indexes = {"member": single_mem, "similar members": sim_mem}

    max_index = max(indexes, key=indexes.get)
    max_value = indexes[max_index] 
    maxx = []
    for key, value in indexes.items():
        if value == max_value:
            maxx.append(key)
            
    return maxx
