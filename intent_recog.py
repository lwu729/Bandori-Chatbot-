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
    find_member = {"name", "a", "member", "look", "up", "search", "specific"}
    find_sim = {"similarity", "similar", "same", "alike", "by", "sort", "list", "of", "members"}

    
    #member similarities:
    #at this point users can search: Astrological Sign, school/school year, fav/least fav food, role, birthday, CV
    astro = {"astro","sign","same", "have"}
    school_year = {"school year","grade", "year", "age", "in", "which", "high", "first", "second", "third", "same year"}
    school = {"school", "in", "same", "high", "university", "enrolled"}
    band = {
    "band", "afterglow", "roselia", "morfonica", "poppinparty", "hello", "happy", "world",
    "pastel", "palettes", "raise", "suilen", "mygo", "mujica", "ppp", "hhw", "ras"
    }

    band_role = {
        "role", "position", "instrument", "instruments",
        "guitar", "bass", "drums", "keyboard", "dj", "vocals", "violin", "keytar", "singer"
    }
    #look up for single card/by attribute/by elements/by character/by band
    single_card = {"single", "card", "one", "search", "specific","look", "up"}
    list_of_cards = {"by", "cards", "stars", "rarity", "attribute", "same", "similarity", "similar", "same", "alike", "by", "sort", "list", "of", "lists"}
    
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
    sim_mem = len(find_sim & intents)
    
    #sim_member:
    astro_index = len(astro & intents)
    school_index = len(school & intents)
    band_index = len(band & intents)
    band_role_index = len(band_role & intents)
    school_year_index = len(school_year & intents)
    
    #card:
    single_card_index = len(single_card & intents)
    list_of_cards_index = len(list_of_cards & intents)
    
    
    if guide == "raw":
        indexes = {"members": mem_index, "cards": card_index, "gacha": gacha_index, "bot":bot_index}
    elif guide == "card":
        indexes = {"single card":single_card_index, "list of cards":list_of_cards_index}
    elif guide == "member":
        indexes = {"member": single_mem, "similar members": sim_mem}
    elif guide == "sim_member":
        indexes = {
            "i_astrological_sign": astro_index,
            "i_school_year": school_year_index,
            "school": school_index,
            "i_band": band_index,
            "instrument": band_role_index
        }
    else:
        print("Unknown guide type.")
        return None




    if indexes == 0:
        print("Sorry, please input something related to the given prompt.")
        return
    max_index = max(indexes, key=indexes.get)
    max_value = indexes[max_index] 
    maxx = []
    for key, value in indexes.items():
        if value == max_value:
            maxx.append(key)
            
    return maxx
