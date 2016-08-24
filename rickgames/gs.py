
from bs4 import BeautifulSoup
import requests

class GameScraper:
    def getSoup(self, url):
        html = requests.get(url)
        text = html.text
        soup = BeautifulSoup(text, "html.parser")
        return soup

    def getRemainingAllowance(self, url):
        soup = self.getSoup(url)
        for tag in soup.findAll(id="InfoTable"):
            for tr in tag.findAll("tr"):
                for td in tr.findAll("td"):
                    if td.text != 'Data Allowance Remaining':
                        continue
                    print(td.next_sibling.next_sibling.text)

