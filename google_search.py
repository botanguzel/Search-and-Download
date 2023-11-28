import requests
import tkinter as tk

class GoogleCustomSearch:
    def __init__(self, api_key, cx):
        self.api_key = api_key
        self.cx = cx
        self.query = ''
        self.i = 0

    def search(self, query, colorType, dominantColor, imgSize, imgType, num, startNum):
        self.query = query
        url = f"https://customsearch.googleapis.com/customsearch/v1?cx={self.cx}&imgColorType={colorType}&imgDominantColor={dominantColor}&imgSize={imgSize}&imgType={imgType}&num={num}&q={query}&searchType=image&start={startNum}&key={self.api_key}"
        response = requests.get(url)
        return response.json()

    def display_results(self, response):
        items = response.get("items", [])
        links = {}
        if items:
            for item in items:
                if 'link' in item:
                        link = item.get('link')
                        key = f"{self.query}_{self.i}"
                        links[key] = link
                        self.i += 1
                else:
                    return "No link found for item."
        else:
            return "No items found in the response."
        return links
    
    def reset_i(self):
        self.i = 0

