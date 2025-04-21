#starts the program, taking user inputs, navigating between different files
from chatbot import process_intent
from gacha import gacha
from intent_recog import intent_rec

 # print welcome and guide messages
print("Hello! Welcome to Bandori! chatbot, dedicated to players of Bandori!")
print("Just type 'exit' whenever you are done with using Bandori! Chatbot~ Have fun:)")
print("You can search for members and cards, change my tone of voice, and use the gacha simulator in Bandori!")
print("Feel free to send your request over in full sentences! I'll try my best to help~♪")
while True:
    user_input = input("")
    if user_input.lower() == "exit":
        print("See you next time!")
        break
    process_intent(user_input)
    