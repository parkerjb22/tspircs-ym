from bs4 import BeautifulSoup
import requests
import statistics

encoding = 'cp850'
#encoding = 'utf-8'

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

def getTeams():
    teams = []
    soup = getSoup('http://www.basketball-reference.com/teams')
    advTag = soup.find(id="active")

    bodyTag = advTag.find("tbody")
    for tag in bodyTag.find_all("tr", "full_table"):
        team = tag.find('a')['href'].replace('NJN', 'BRK').replace('NOH', 'NOP').replace('CHA', 'CHO')
        team = team.replace('/teams/', '').replace('/', '')
        teams.append(team)

    return teams

teams = getTeams()
teamMap = []
colHeaders = []

for team in teams:
    req = 'http://www.basketball-reference.com/teams/%s/2015.html' % team
    soup = getSoup(req)
    advTag = soup.find(id="advanced")
    headTag = advTag.find("thead")

    buckets = {}
    colHeaders = []
    for tag in headTag.find_all("tr", ""):
        for child in tag.find_all("th"):
            try:
                key = child['tip']
                newSoup = BeautifulSoup(key)
                if (newSoup.find('b')):
                    key = newSoup.find('b').string
                elif (newSoup.find('strong')):
                    key = newSoup.find('strong').string

            except:
                key = child.string
            colHeaders.append(key)
            buckets[key] = []

    bodyTag = advTag.find("tbody")
    for tag in bodyTag.find_all("tr", ""):
        i = 0
        for child in tag.find_all("td"):
            val = getValue(child.string)
            buckets[colHeaders[i]].append(val)
            i += 1

    teamMap.append((team, buckets))
    print("%s..." % (team))

for col in colHeaders:
    if (col == 'Rank'):
        teamMap.sort(key=lambda x: max(x[1][col]), reverse=True)
        print ("Category: %s" % col)
        for curr in teamMap:
            print("%s: %f" % (curr[0], max(curr[1][col])))
    else:
        try:
            teamMap.sort(key=lambda x: statistics.mean(x[1][col]), reverse=True)
            print ("Category: %s" % col)
            for curr in teamMap:
                print("%s: %f" % (curr[0], statistics.mean(curr[1][col])))
        except:
            pass


