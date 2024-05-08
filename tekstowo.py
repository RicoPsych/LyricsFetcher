
from bs4 import BeautifulSoup
import requests

agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}

def lyrics(artist,title):


    url = f"https://www.tekstowo.pl/piosenka,{artist},{title}.html"

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    lyrics = soup.find_all("div", attrs={"class": "inner-text"})
    if not lyrics:
        return {'Error': 'Unable to find '+title+' by '+artist}
    elif lyrics:
        lyrics = [x.getText() for x in lyrics]
        return lyrics
