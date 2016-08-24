from bs4 import BeautifulSoup
import requests
import re

class GameScraper:
    def getSoup(self, url):
        html = requests.get(url)
        text = html.text
        soup = BeautifulSoup(text)
        return soup

    def getSchedule(self, teamId):
        games = []
        url = 'http://espn.go.com/college-football/team/schedule/_/id/' + teamId
        soup = self.getSoup(url)
        for tag in soup.findAll("li", { "class":"score" }):
            if 'Canceled' in tag:
                continue
            games.append(tag.find('a')['href'].replace('/ncf/recap?id=', ''))

        return games

    def getPlayerStats(self, playerName, teamId):
        games = self.getSchedule(teamId)
        playCount = 0
        successCount = 0
        for game in games:
            p, s = self.getGame(playerName, game)
            playCount += p
            successCount += s

        # print(playerName, '%d plays' % playCount,'%d successful' % successCount, '%.2f' % (successCount/playCount * 100))
        print(playerName, '%d/%d' % (successCount, playCount), '%.2f%%' % (successCount/playCount * 100))

    def getGame(self, playerName, gameId):
        playCount = 0
        successCount = 0
        prefix = playerName + ' run for '
        regexp = re.compile(playerName + r' \d+ Yd Run')
        url = 'http://espn.go.com/college-football/playbyplay?gameId=' + gameId
        soup = self.getSoup(url)
        for tag in soup.findAll('h3'):
            liTag = tag.parent
            spanTag = liTag.find("span")
            play = spanTag.getText()
            if prefix in play or regexp.search(play) is not None :
                playCount += 1
                if prefix not in play:
                    successCount += 1
                    continue
                if "a loss of" in play:
                    continue
                elif "no gain" in play:
                    continue
                else:
                    down, distance = self.getDownAndDistance(tag.getText())
                    if down == '1':
                        PTG = .4
                    elif down == '2':
                        PTG = .6
                    else:
                        PTG = 1
                    play = self.getYards(prefix, play.strip())

                    success = int(play) >= (PTG * int(distance))
                    if success:
                        successCount += 1

        if (playCount > 0):
            print(playerName, gameId, '%d plays' % playCount,'%d successful' % successCount, '%.2f' % (successCount/playCount * 100))
        else:
            print(playerName, gameId, '0 plays')
        return playCount, successCount

    def getYards(self, prefix, str):
        regex = r"^.*" + re.escape(prefix)  + r"(\d+).*$"
        yards = re.sub(regex, r"\1", str)

        return yards

    def getDownAndDistance(self, str):
        if 'Goal' in str:
            regex = r"^(\d).. and Goal at [a-zA-Z&;]+ (\d+)$"
        else:
            regex = r"^(\d).. and (\d+) at.*$"

        return re.sub(regex, r"\1 \2", str).split()

    def getStupidTDMsg(self, player, msg):
        regexp = re.compile(player + r' \d+ Yd Run')
        return regexp.search(msg) is not None