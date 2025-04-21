import random
saki = 0
ako = 1
rinko = 2
# index of the characters, default is the default robot
characters = [
    {'name':'Sakiko Togawa','self_name':'Watakushi',"end":' desuwa.', 'name_type':'first','name_others':'-san'}, 
    {'name':'Ako Udagawa', 'self_name':'Ako',"end":['!','~','...!'],'name_type':'first','name_others':'-chan', 'additional_words':['Bang!', 'Dong!','cu cu cu...']},
    {'name':'Rinko Shirokane','self_name':'Watashi','comma':'......',"end":'......','name_type':'last', 'name_others':'-san','additional_words':['......(シ_ _)シ', '(づ ◕‿◕ )づ','...(´∀｀)']}
    ]

def tone(message, index):
    msg = f" {message.strip()} "
    char = characters[index]
    replacements = {
        " i ": f" {char['self_name']} ",
        " i'm ": f" {char['self_name']} is ",
        " me ": f" {char['self_name']} ",
        " my ": f" {char['self_name']}'s ",
        " you ": f" user{char['name_others']} ",
        " your ": f" user{char['name_others']}'s ",
        ".": f"",
        "~?": f"",
        "?": f"",
        "!": f"",
        "~!": f"",
        "...!": f"",
        "...?": f"",
        "...": f"",
        "......": f"",
        "~": f"",
    }

    for word, replacement in replacements.items():
        msg = msg.replace(word, replacement)

    msg = msg.strip()
    comma = char.get("comma", "")

    end = random.choice(char["end"]) if isinstance(char["end"], list) else char["end"]
    extra = random.choice(char.get("additional_words", [""]))

    return f"{msg}{comma}{end} {extra}".strip()


def stylize_name(name, tone_index):
    suffix = characters[tone_index].get("name_others", "")
    return f"{name}{suffix}"