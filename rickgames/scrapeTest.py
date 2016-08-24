import unittest
from gs import GameScraper

class MyTest(unittest.TestCase):
    def test_getTeams(self):
        actual =GameScraper().getSchedule('333')
        expected = ['400603827', '400603860', '400603850', '400603841', '400603879', '400603899', '400603897', '400603886', '400603905', '400603933', '400603921', '400603913', '400852681']
        self.assertEquals(expected, actual)


    def test_getPlays(self):
        GameScraper().getGame('Derrick Henry', '400603827')
        assert True

    def test_getYards(self):
        actual = GameScraper().getYards('Derrick Henry run for ', '(9:50 - 2nd) Derrick Henry run for 8 yds to the Alab 24 for a 1ST down')
        expected = "8"
        self.assertEquals(expected, actual)

    def test_getStupidTDMsg(self):
        actual = GameScraper().getStupidTDMsg('Derrick Henry', 'Derrick Henry 1 Yd Run (Adam Griffith Kick)')
        expected = True
        self.assertEquals(expected, actual)

    def test_getDownAndDistance(self):
        actual = GameScraper().getDownAndDistance('1st and Goal at FLA 3')
        expected = ['1','3']
        self.assertEquals(expected, actual)

    def test_getDownAndDistance_2(self):
        actual = GameScraper().getDownAndDistance('3rd and 9 at FLA 15')
        expected = ['3','9']
        self.assertEquals(expected, actual)

    def test_getPlayerStats(self):
        gs = GameScraper()
        players = [
            # ['Derrick Henry', '333'],
            # ['Dalvin Cook', '52'],
            # ['Ezekiel Elliott', '194'],
            # ['Christian McCaffrey', '24'],
             ['Leonard Fournette', '99'],
            # ['Royce Freeman', '2483'],
        ]
        for player in players:
            gs.getPlayerStats(player[0], player[1])

        assert True

    def test_getRemainingAllowance(self):
        expected = False
        actual = True
        self.assertEqual(expected, actual)