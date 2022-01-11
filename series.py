from game import *

class Series():
    def __init__(self, team1, team2, games=[], stats={}, winner=None):
        self.team1 = team1
        self.team2 = team2
        self.team1.wins = 0
        self.team2.wins = 0
        self.games = list()
        for i in range(4):
            if i >= 2:
                self.games.append(Game(team2, team1))
            else:
                self.games.append(Game(team1, team2))
        self.stats = dict()
        for ply in range(len(self.team1.roster)):
            p1, p2 = self.team1.roster[ply], self.team2.roster[ply]
            self.stats[p1.name] = list([0 for x in range(11)])
            self.stats[p2.name] = list([0 for x in range(11)])
        self.winner = None
    
    def fixture(self):
        return self.team1.name + ' vs ' + self.team2.name
    
    def play(self):
        print('\n' + self.fixture() + '\n\n')
        for i in range(7):
            game = self.games[i]
            print('Game ' + str(i+1) + ': ' + game.fixture() + '\n', end='')
            game.simGame(True)
            self.updateStats(game)
            print('\n')
            if self.checkSeries():
                break
    
    def gamesPlayed(self):
        result = 0
        for g in self.games:
            if g.team1score == 0 and g.team2score == 0:
                break
            result += 1
        return result
    
    def getStats(self, name):
        player = None
        team = None
        for ply, val in self.stats.items():
            if name.lower() == ply.lower():
                player = ply
                team = self.team1 if ply in self.team1.roster else self.team2
                break
        if player == None:
            return 'couldn\'t find ' + name
        statline = ''
        name = name.title()
        for i in range(11):
            stat = self.stats[name][i]
            stat = weird_division(stat, self.gamesPlayed())
            stat = my_precision(stat, 1)
            statline += str(stat).ljust(6)
        for i in range(5, 11):
            if i % 2 == 1:
                temp = self.stats[name][i+1]
                stat = (self.stats[name][i] / temp) if temp != 0 else 0
                stat = my_precision(stat*100, 1)
                statline += str(stat).ljust(5)
        return statline
    
    def teamStats(self, name):
        if type(name) == str and name.lower()[:3] != 'los':
            name = 'los ' + name
        team = None
        arr = [0 for x in range(11)]
        if name == 1 or (type(name) == str and name.lower() == self.team1.name.lower()):
            team = self.team1
        elif name == 2 or (type(name) == str and name.lower() == self.team2.name.lower()):
            team = self.team2
        else:
            return 'couldn\'t find ' + str(name)
        print(team.name.upper())
        for j in range(len(team.roster)):
            player = team.roster[j]
            for i in range(11):
                stat = self.stats[player.name][i]
                stat = weird_division(stat, self.gamesPlayed())
                stat = my_precision(stat, 1)
                arr[i] += stat
        for i in range(5, 11):
            if i % 2 == 1:
                temp = arr[i+1]
                stat = (arr[i] / temp) if temp != 0 else 0
                stat = my_precision(stat*100, 1)
                arr.append(stat)
        statline = ''.ljust(31)
        statline += ': '
        for i in range(14):
            if i < 3:
                arr[i] = my_precision(arr[i]/len(team.roster), 1)
                statline += str(arr[i]).ljust(6)
            elif i < 11:
                arr[i] = my_precision(arr[i], 1)
                statline += str(arr[i]).ljust(6)
            else:
                statline += str(arr[i]) + ' '
        
        for ply in team.roster:
            print(ply.name.ljust(25) + ' (' + str(ply.overall()) + ') : ' + self.getStats(ply.name))
        print(statline)
    
    def updateStats(self, game):
        if game.team1.wins > 4 or game.team2.wins > 4:
            return 0
        if game.team1score > game.team2score:
            game.team1.wins += 1
        else:
            game.team2.wins += 1
        t1 = game.team1.roster
        t2 = game.team2.roster
        for i in range(len(t1)):
            name1, name2 = t1[i].name, t2[i].name
            for j in range(11):
                value1, value2 = list(game.team1boxScore[name1][j].values())[0], list(game.team2boxScore[name2][j].values())[0]
                self.stats[name1][j] += value1
                self.stats[name2][j] += value2
        
    def checkSeries(self):
        if self.team1.wins == 4 or self.team2.wins == 4:
            if self.team1.wins == 4:
                self.winner = self.team1
                loser = self.team2
            else:
                self.winner = self.team2
                loser = self.team1
            print('\nWinner of Series: ' + self.winner.name + '!\n')
            print(self.winner.name + ' ' + str(self.winner.wins) + ' - ' + str(loser.wins) + ' ' + loser.name + '\n\n')
            index = self.winner.wins + loser.wins
            self.games = [self.games[x] for x in range(index)]
            return True
        else:
            if self.team1.wins > 4 or self.team2.wins > 4:
                print('PROBLEM!')
            total_wins = self.team1.wins + self.team2.wins
            game_no = len(self.games)
            if game_no == total_wins and game_no < 7:
                game = Game(self.team1, self.team2) if game_no % 2 == 0 else Game(self.team2, self.team1)
                self.games.append(game)
                return ''
            else:
                return None
            
#             
# t1 = makeTeam()
# t2 = makeTeam()
# t3 = makeTeam()
# s = Series(t1, t2)
# s12 = Series(t1, t2)
# s13 = Series(t1, t3)
# s12.games[0].simGame()
# s12.updateStats(s12.games[0])
# Series(t1, t2).stats[t1.roster[0].name] == Series(t1, t3).stats[t1.roster[0].name]
