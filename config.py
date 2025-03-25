#api look up for: member, card, in game item, area items
import json
import requests
def getGeneral(intent):
    base = f"https://bandori.party/api/{intent}/?page_size=100" #make sure all the items are fetched
    page = requests.get(base)
    data  = page.json()    #turn the information into a json object
    return data
    
    