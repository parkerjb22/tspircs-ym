from bs4 import BeautifulSoup, Comment
import requests

def getSoup(url):
    html = requests.get(url)
    text = html.text
    soup = BeautifulSoup(text)
    return soup

def getPlayerStats(url):
    stats = {}
    soup = getSoup(url)
    advTag = soup.find(id="per_game")
    headTag = advTag.find("thead")

    colHeaders = []
    for tag in headTag.find_all("tr", ""):
        for child in tag.find_all("th"):
            key = child.string
            colHeaders.append(key)

    bodyTag = advTag.find("tfoot")
    for tag in bodyTag.find_all("tr", " stat_total"):
        if tag.find("td").string != 'Career':
            continue
        i = 0
        for child in tag.find_all("td"):
            val = getValue(child.string)
            if colHeaders[i] in gathered:
                stats[colHeaders[i]] = val
            i += 1

    return stats