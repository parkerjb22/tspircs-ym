from bs4 import BeautifulSoup, Comment
import requests
import statistics

encoding = 'cp850'
#encoding = 'utf-8'

gathered = ['PTS', 'AST', 'STL', 'TRB', 'BLK']

players = [ 'Larry Bird',
'Jerry West',
'Michael Jordan',
'Clyde Drexler',
'Scottie Pippen',
'Rick Barry',
'Karl Malone',
'Charles Barkley',
'Connie Hawkins',
'Magic Johnson',
]

def getValue(s):
    try:
        return float(s.strip(' "'))
    except :
        return s

def getSoup(url):
    html = requests.get(url)
    text = html.text
    soup = BeautifulSoup(text)
    return soup

def getInductees():
    inductees = []
    soup = getSoup('http://www.basketball-reference.com/awards/hof.html')
    advTag = soup.find(id="hof")

    bodyTag = advTag.find("tbody")
    for tag in bodyTag.find_all("tr"):
        i = 0
        url = ''
        name = ''
        for tag2 in tag.find_all("td"):
            if (i == 2):
                if (tag2.string == 'Player' and url != ''):
                    inductees.append((name, url))
                break

            name = [text for text in tag2.stripped_strings][0]
            link = tag2.find('a')
            if (link and link.string == 'Player'):
                url = link['href']

            i += 1

    return inductees

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

def diff(stats1, stats2):
    diff = 0
    for key, value in stats1.items():
        V1 = value
        V2 = stats2[key]
        if (V2 == 'None'):
            raise Exception
        pctDiff = ( abs(V1 - V2) / ((V1 + V2)/2) )
        pctDiff = abs(V1-V2)
        diff += pctDiff
        print(key, V1, V2, pctDiff)

    return diff

lbjStats = getPlayerStats('http://www.basketball-reference.com/players/j/jamesle01.html')
#print(getPlayerStats('http://www.basketball-reference.com/players/r/rodgegu01.html'))

diffMap = []
inductees = getInductees()

for player in inductees:
    if player[0] not in players:
        continue
    name = player[0]
    url = "http://www.basketball-reference.com" + player[1]
    print(name)
    stats = getPlayerStats(url)
    try:
        diffMap.append((name, diff(lbjStats, stats)))
    except:
        pass


diffMap.sort(key=lambda x: x[1], reverse=False)
i = 1
for curr in diffMap:
    print("#%d %s: %.3f" % (i, curr[0], curr[1]))
    i += 1