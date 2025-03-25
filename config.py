
import json
import requests
def getGeneral(intent):
    base = f"https://bandori.party/api/{intent}/?page_size=100" #make sure all the items are fetched
    page = requests.get(base)
    print(page.status_code) 
    weather  = page.json()    #turn the information into a json object
    print(json.dumps(weather, indent = 2))
    
    