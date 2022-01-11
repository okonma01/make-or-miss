from league import *
from series import *

check_day = 1
first = 0
last = 0
class Playoffs():
    def __init__(self, league, stats=None, teams=[], rounds=0, series_dict={}, gameSchedule={}, champion=None):
#         super().__init__()
        global check_day, first, last
        self.league = league
        self.teams = league.teams.copy()
        self.stats = copy.copy(league.stats)
        self.rounds = rounds
        self.series_dict = dict()
        self.gameSchedule = dict()
        self.champion = None
        
    def reset(self):
        first = last = 0
        self.teams = self.league.teams.copy()
        self.series_dict = {}
        self.gameSchedule = {}
        self.champion = None
        
    def addGames(self, round_no):
        for i in range(4):
            for series in self.series_dict[round_no]:
                game = series.games[i]
                if round_no == 1:
                    self.addGameToDay(game)
                else:
                    self.addGameToDay(game, day=check_day)
        
    def setUpPlayoffs(self):
        self.reset()
        self.qualifyTeams()
        self.firstRound()
        LeagueConstants.daysInSeason = 60
#         self.gameSchedule = {x+1: [] for x in range(LeagueConstants.daysInSeason)}
#         series_no = len(self.series_dict[1][0].games)
        self.addGames(1)
                
    def sortTeams(self):
        result = self.stats.teamWins
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        self.teams = [self.league.getTeam(result[x][0]) for x in range(len(self.teams))]
    
    def qualifyTeams(self):
        power = 0
        self.sortTeams()
        teamNo = len(self.teams)-1
        for i in range(5):
            if int(pow(2, i)) > teamNo:
                break
            power = i
        self.rounds = power
        power = int(pow(2, power))
        self.series_dict = {x+1: [] for x in range(self.rounds)}
        self.teams = self.teams[:power]
    
    def firstRound(self): # first round series ONLY (so far)
        count = int(pow(2, self.rounds)/2)
        arr = [(x+1, int(pow(2, self.rounds)-x)) for x in range(count)]
        round_no = 1
        for pair in arr:
            team1 = self.teams[pair[0]-1]
            team2 = self.teams[pair[1]-1]
            self.series_dict[round_no].append(Series(team1, team2))
    
    def nextRound(self):
        global check_day
        round_no = 1
        for i in range(self.rounds):
            if not self.roundOver(i+1):
                round_no = i+1
                break
            else:
                round_no += 1
        no_of_series = int(len(self.series_dict[round_no-1])/2)
        for i in range(no_of_series):
            prev = self.series_dict[round_no-1]
            team1 = prev[i].winner
            team2 = prev[-(i+1)].winner
            if self.league.stats.teamWins[team2.name] > self.league.stats.teamWins[team1.name]:
                tmp = team2
                team2 = team1
                team1 = tmp
            new_series = Series(team1, team2)
            self.series_dict[round_no].append(new_series)
        check_day += 2
        self.addGames(round_no)
    
    def getSeries(self, round_no, game):
        for series in self.series_dict[round_no]:
            if game in series.games:
                return series
    
    def fixtures(self, round_no=1):
        for i in range(self.rounds):
            if self.roundOver(i+1):
                round_no += 1
            else:
                break
        for s in self.series_dict[round_no]:
            print(s.fixture())
    
    def roundOver(self, round_no=1):
        if self.series_dict[round_no] == []:
            return False
        else:
            result = True
            for series in self.series_dict[round_no]:
                if series.winner == None:
                    result = False
            return result
    
    def addGameToDay(self, game, day=1):
        global check_day
        if day != 1:
            day = check_day
        days = LeagueConstants.daysInSeason
        while True:
            if day not in self.gameSchedule:
                self.gameSchedule[day] = []
            if canScheduleGame(self.gameSchedule[day], game, 2):
                self.gameSchedule[day].append(game)
                check_day = day
                break
            else:
                day = (day + 2)
    
    def nextDay(self, i, round_no):
        if self.roundOver(round_no):
            return 0
        if i not in self.gameSchedule:
            return 0
        if self.gameSchedule[i] == []:
            return 0
        else:
            print('=========================\nToday is Day ' + str(i))
#             n = 0
#             for gs in self.gameSchedule[i]:
#                 if self.getSeries(1, gs).winner == None:
#                     n += 1
#                 else:
#                     self.gameSchedule[i].remove(gs)
            gamesToday = self.gameSchedule[i]
            print('No. of games today: ' + str(len(gamesToday)))
            print('=========================\n')

#             for game in gamesToday:
#                 print(game.fixture())
            for game in gamesToday:
#                 if not self.getSeries(round_no, game):
#                     continue
                game.simGame(True)

                s = self.getSeries(round_no, game)
                s.updateStats(game)
                bruh = s.checkSeries()
                if bruh == '':
                    self.addGameToDay(s.games[-1], day=check_day)
            print('\n')
        
    def sim(self):
        global first, last
#         self.currentDay = 1
        round_no = 1
        for i in range(self.rounds):
            if not self.roundOver(i+1):
                round_no = i+1
                break
        if round_no == 1:
            last = list(self.gameSchedule.keys())[-1]
            for i in range(last):
                self.nextDay(i+1, round_no)
        while True:
            first = last + 2
            last = list(self.gameSchedule.keys())[-1]
            for i in range(first, last+1):
                self.nextDay(i, round_no)
            if self.roundOver(round_no):
                break
        if self.roundOver(self.rounds):
            self.champion = self.series_dict[self.rounds][0].winner

#     def playRound(self):
def matchups(round_no):
    for s in p.series_dict[round_no]:
        print(s.fixture())

def schedule():
    for d, g in p.gameSchedule.items():
        if g != []:
            print('Day ' + str(d) + ':')
            for gs in g:
                print(gs.fixture())
            print()


l = League()
l.playSeason()
# p = Playoffs(l)
# p.setUpPlayoffs()