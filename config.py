#api look up for: member, card, in game item, area items
import json
import requests

def getGeneral(intent):
    url = f"https://bandori.party/api/{intent}/?page_size=100"
    results = []
    page_num = 1
    #I also asked chatGPT for help on the page num issue because at first i didnt know why its not fetching correctly.
    while url:
        print(f"Fetching page {page_num} from {intent} endpoint...") #tell the user im processing
        response = requests.get(url)
        data = response.json()
        results.extend(data["results"])
        url = data.get("next")
        page_num += 1

    print("Done!")
    return {"results": results}
    