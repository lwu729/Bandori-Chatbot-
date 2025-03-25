#starts the program, taking user inputs, navigating between different files
from chatbot import process_intent
from gacha import gacha
from intent_recog import intent_rec


print("Welcome!") # print welcome and guide messages
print("member, gacha, cards, change tone")
while True:
    user_input = input("")
    if user_input.lower() == "exit":
        print("See you next time!")
        break
    process_intent(user_input)
    
    