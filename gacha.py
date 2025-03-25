# only focus on gacha function
import random

pulls_rec = 0

def evaluate(result):
    if 0 <= result <= 84.5:
        return 2
    elif 84.5 < result <= 93:
        return 3
    elif 93 < result <= 97:
        return 4
    else:
        return 5

def gacha():
    while True:
        total = {"2": 0, "3": 0, "4": 0, "5": 0}
        print("Welcome! Please tell me how many pulls would you like:")
        try:
            pulls = input()
            pulls = int(pulls)
        except ValueError:
            print("Please input a numeric value.")
            continue
        global pulls_rec
        for pull in range(pulls):
            result = random.uniform(0.001, 100)
            pulls_rec += 1
            result = evaluate(result)
            final_result = "★" * result
            if result >= 3:
                pulls_rec = 0
            if pulls_rec == 10:
                result = 3
                final_result = "★" * result
                pulls_rec = 0
            
            if result == 2:
                total["2"] += 1
            elif result == 3: 
                total["3"] += 1
            elif result == 4: 
                total["4"] += 1
            elif result == 5: 
                total["5"] += 1
            
            print(f"{final_result} Congrats! You got a {result} ★ card!")
        print("------Pull ended-------")
        print(f"Congrats! In {pulls} pulls, you got:")
        print(f"{total.get('2')} 2 ★ cards,")
        print(f"{total.get('3')} 3 ★ cards,")
        print(f"{total.get('4')} 4 ★ cards,")
        print(f"{total.get('5')} 5 ★ cards.")
        print("Would you like to continue pulling?")
        yn_input = input("")
        yn_input = yn_input.lower()
            
        if not (yn_input.startswith("y") or yn_input.startswith("c")): #user might say continue
            print("Taking you back....")
            print("Please say what you want to do or enter 'exit' to quit Bandori Bot.")
            break