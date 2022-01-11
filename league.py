from dataclasses import dataclass, field
from game import *

# CREATE "HIDDEN" CLASS THAT PLAYER CLASS WILL INHERIT. IT SHOULD CONTAIN HIDDEN ATTRS OF PLAYERS
# MAKE FIRST OPTIONS W/ BEST ATTR AS 'PASSING' TO SHOOT LESS (THESE ARE MOSTLY GUARDS) - DONE

# GO TO CONFIG.PY - MAKE THREE-POINT SHOOTERS SHOOT BETTER (SMARTER): CHANGE THEIR TENDENCIES - DONE

# CHANGE TEAMS' FIRST OPTION TO BE DECIDED FROM OFFENSIVE ATTRIBUTES ONLY! - DONE

# CREATE PLAY() METHOD IN GAME, SO THAT THE USER CAN CONTROL A TEAM

# *** NEW ***
# TWEAK CRUNCH_DICT IN CONFIG (ESPECIALLY SECOND OPTIONS)
# CREATE TREY_HOLD() METHOD TO FIX ALL 3 POINTER PROBLEMS
# REDUCE BONUS IN PLAYPOSESSION() IF A PLAYER IS BLOCKED

@dataclass
class LeagueStats:
    teamWins: dict = field(default_factory=dict)
    teamLosses: dict = field(default_factory=dict)
    teamStats: dict = field(default_factory=dict)
    manoMano: dict = field(default_factory=dict)
    playerStats: dict = field(default_factory=dict)

@dataclass
class PlayerStats:
    stats: dict = field(default_factory=dict)

# self.stats.playerStat = dict()
opp_ppg = {}

@dataclass
class LeagueConstants:
    daysInSeason: int = 24
    totalTeams: int = 10
games_played = 2 * (LeagueConstants.totalTeams-1)

def canScheduleGame(scheduledGames, game, n=6):
    if len(scheduledGames) == 0:
        return True
    else:
        if len(scheduledGames) >= n:
            return False
        else:
            for Game in scheduledGames:
                team_list = [Game.team1, Game.team2]
                if game.team1 in team_list:
                    return False
                elif game.team2 in team_list:
                    return False
                else:
                    result = True
            return result
    #elif len(scheduledGames) > 1:
    #    return False
#     return True



class League():
    def __init__(self, games=[], year=1, stats=LeagueStats(), teams=[], currentDay=1, gameSchedule={}, check_day=1):
        global games_played, attrs
        self.games = games
        self.year = year
        self.stats = stats
        self.stats.manoMano = dict()
        self.stats.playerStats = dict()
        self.teams = teams
        for _ in range(LeagueConstants.totalTeams):
            team = makeTeam()
            self.teams.append(team)
        self.checkTeams()
        self.currentDay = currentDay
        self.gameSchedule = gameSchedule
        self.check_day = check_day
        attrs = [int(x) for x in self.averageAttr()]
    
    def checkTeams(self):
        for tm in self.teams:
            for tm2 in self.teams:
                if tm != tm2 and tm.name == tm2.name:
                    teamName = names.get_last_name()
                    if teamName[-1] == 'z':
                        pass
                    elif teamName[-1] != 's':
                        teamName += 's'
                    elif teamName[-2:] == 'ch' or teamName[-2] == 'sh':
                        teamName += 'es'
                    tm2.name = 'Los ' + teamName
                    break
                    
    
    def getTeam(self, name):
        team = None
        for tm in self.teams:
            if tm.name.lower() == name.lower() or ('los ' + name).lower() == tm.name.lower():
                return tm
            else:
                for ply in tm.roster:
                    if name.lower() == ply.name.lower():
                        team = tm
                        return team
        return 'no team for ' + name
    
    def getTeamStats(self, name, ass=False):
        if name.lower()[:4] != 'los ':
            name = 'los ' + name
        team = None
        for tm in self.teams:
            if tm.name.lower() == name.lower():
                team = tm
        if team == None:
            return 'could not find team: ' + name
        elif not ass:
            print(team.name.upper())
            for ply in team.roster:
                print(ply.name.ljust(25) + ' (' + str(ply.overall(off=True)) + ') : ' + self.getStats(ply.name))
            print(self.teamStatline(team.name))
        else:
            print(''.ljust(33) + 'OPP_FGM'.ljust(10) + 'OPP_FGA'.ljust(10) + 'OPP_FG%'.ljust(10))
            for ply in team.roster:
                def_record = self.stats.manoMano[ply.name]
                percent = my_precision(weird_division(def_record[0]*100, def_record[1]), 1)
                def_record = [my_precision(weird_division(def_record[x], self.gamesPlayed(team)), 1) for x in range(len(def_record))]
                print(ply.name.ljust(25) + ' (' + str(ply.overall(deff=True)) + ') : '
                      + str(def_record[0]).ljust(10) + str(def_record[1]).ljust(10) + str(percent).ljust(10))

    def newSeason(self):
        self.games = []
        self.stats = LeagueStats()
        self.currentDay = 1
        self.gameSchedule = {}

    def addGameToDay(self, game, day=1):
        if day != 1:
            day = self.check_day
        days = LeagueConstants.daysInSeason
        while day >= 1:
            if canScheduleGame(self.gameSchedule[day], game):
                self.gameSchedule[day].append(game)
                self.check_day = day
                break
            else:
                day = (day + 1) % days
    
    def setUpSeason(self):
        self.newSeason()
        self.stats.playerStats.clear()
        for team in range(len(self.teams)):
            self.teams[team].turnovers = 0
            self.stats.teamWins[self.teams[team].name] = 0
            self.stats.teamLosses[self.teams[team].name] = 0
            self.stats.teamStats[self.teams[team].name] = {'ppg': [], 'opp_ppg': []}
            for player in self.teams[team].roster:
                self.stats.manoMano[player.name] = list([0, 0])
                self.stats.playerStats[player.name] = list([0 for x in range(11)])
                for j in range(10):
                    player.__dict__[stat_dict[j]] = [0, None]
#                 self.stats.teamStats[team][self.teams[team].name].append({player.name: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
#             truncTeams = self.teams.copy()
#             truncTeams.remove(self.teams[team])
            for opp in self.teams:
                if self.teams[team] != opp:
                    team1 = self.teams[team]
                    team2 = opp
                    self.games.append(Game(team1, team2))
                    self.games[-1].attrs = [int(x) for x in self.averageAttr()]
        random.shuffle(self.games)
        self.gameSchedule = {x+1: [] for x in range(LeagueConstants.daysInSeason)}
        for i in range(len(self.games)):
            self.addGameToDay(self.games[i])

    def gamesPlayed(self, team):
        result = self.stats.teamWins[team.name] + self.stats.teamLosses[team.name]
        return result

    def updateStats(self, game):
        if game.team1score > game.team2score:
            teamW = game.team1
            teamL = game.team2
        else:
            teamW = game.team2
            teamL = game.team1
        self.stats.teamWins[teamW.name] += 1
        self.stats.teamLosses[teamL.name] += 1
        self.stats.teamStats[game.team1.name]['ppg'].append(game.team1score)
        self.stats.teamStats[game.team1.name]['opp_ppg'].append(game.team2score)
        self.stats.teamStats[game.team2.name]['ppg'].append(game.team2score)
        self.stats.teamStats[game.team2.name]['opp_ppg'].append(game.team1score)
        t1 = game.team1.roster
        t2 = game.team2.roster
        index1 = self.teams.index(game.team1)
        index2 = self.teams.index(game.team2)
        for i in range(len(t1)):
            p1, p2 = t1[i], t2[i]
            self.stats.manoMano[p1.name][0] += game.ass_dict[p1.name][0]
            self.stats.manoMano[p1.name][1] += game.ass_dict[p1.name][1]
            self.stats.manoMano[p2.name][0] += game.ass_dict[p2.name][0]
            self.stats.manoMano[p2.name][1] += game.ass_dict[p2.name][1]
            for j in range(11):
                value1, value2 = list(game.team1boxScore[p1.name][j].values())[0], list(game.team2boxScore[p2.name][j].values())[0]
                self.stats.playerStats[p1.name][j] += value1
                self.stats.playerStats[p2.name][j] += value2
                if value1 > p1.__dict__[stat_dict[j]][0]:
                    p1.__dict__[stat_dict[j]][0] = value1
                    p1.__dict__[stat_dict[j]][1] = game
                if value2 > p2.__dict__[stat_dict[j]][0]:
                    p2.__dict__[stat_dict[j]][0] = value2
                    p2.__dict__[stat_dict[j]][1] = game

    def getStats(self, name):
        player = None
        team = None
        for tm in self.teams:
            for ply in tm.roster:
                if name.lower() == ply.name.lower():
                    player = ply
                    team = tm
                    break
        if player == None:
            return 'couldn\'t find ' + name
        statline = ''
        name = name.title()
        for i in range(11):
            stat = self.stats.playerStats[name][i]
            stat = weird_division(stat, self.gamesPlayed(team))
            stat = my_precision(stat, 1)
            statline += str(stat).ljust(7)
        for i in range(5, 11):
            if i % 2 == 1:
                temp = self.stats.playerStats[name][i+1]
                stat = (self.stats.playerStats[name][i] / temp) if temp != 0 else 0
                stat = my_precision(stat*100, 1)
                statline += str(stat).ljust(5)
        return statline

    def getGames(self, t1, t2):
        a = []
        for d, g in self.gameSchedule.items():
            for gs in g:
                ar = [gs.team1.name.lower()[4:], gs.team2.name.lower()[4:]]
                if t1.lower() in ar and t2.lower() in ar:
                    a.append(gs)
        return a

    def teamStatline(self, name):
        team = None
        arr = [0 for x in range(11)]
        for tm in self.teams:
            if name.lower() == tm.name.lower():
                team = tm
                break
        if team == None:
            return 'couldn\'t find ' + name
        for j in range(len(team.roster)):
            player = team.roster[j]
            for i in range(11):
                stat = self.stats.playerStats[player.name][i]
                stat = weird_division(stat, self.gamesPlayed(team))
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
                statline += str(arr[i]).ljust(7)
            elif i < 11:
                arr[i] = my_precision(arr[i], 1)
                statline += str(arr[i]).ljust(7)
            else:
                statline += str(arr[i]) + ' '
        return statline
    
    def averageStats(self, option=-1):
        if option not in range (-1, 10):
            return "Option Invalid"
        if option == -1:
            length = 9
        else:
            length = 1
        o_dict = {1: {x for x in range(11)}, 9: {0}}
        if option > 5:
            field = 'bench'
            option -= 5
        else:
            field = 'lineup'

        result = [0 for x in range(11)]
        player = None
        team = None
        player_count = LeagueConstants.totalTeams * length
        for tm in self.teams:
            t_list = tm.roster[:5] if field == 'lineup' else tm.roster[5:]
            if length == 1:
                td = {x: x.overall(off=True) for x in t_list}
                t_sorted = sorted(td.keys(), key=lambda x: x.overall(True), reverse=True)
            for ply in tm.roster:
                if length == 1:
                    if ply not in t_sorted:
                        continue
                    elif option != t_sorted.index(ply)+1:
                        continue
#             except ValueError:
#                 print('player: ' + ply.name, '\nteam: ' + tm.name)
#                 pass
                player = ply
                team = tm
                for i in range(11):
                    stat = self.stats.playerStats[player.name][i]
                    stat = weird_division(stat, self.gamesPlayed(team))
                    stat = my_precision(stat, 1)
                    result[i] += stat
        for i in range(5, 11):
            if i % 2 == 1:
                temp = result[i+1]
                stat = (result[i] / temp) if temp != 0 else 0
                stat = my_precision(stat*100, 1)
                result.append(stat)
        
        for i in range(len(result)):
            if i in o_dict[length]:
                result[i] = my_precision(result[i]/player_count, 1)
            elif i in range(1, 11):
                result[i] = my_precision(result[i]/len(self.teams), 1)
        
        return result
    
    def averageAttr(self):
        result = [0 for x in range(11)]
        player_count = LeagueConstants.totalTeams * len(self.teams[0].roster)
        for tm in self.teams:
            for ply in tm.roster:
                for i in range(11):
                    result[i] += list(ply.__dict__.values())[11:][1:][i]
        result = [my_precision(result[x]/player_count, 1) for x in range(len(result))]
        return result
    
    def standings(self):
        result = self.stats.teamWins
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print('Pos'.ljust(8) + 'Team'.ljust(20) + ' Wins'.ljust(10) + ' GP '.ljust(10) + 'Offense '.ljust(10) + 'Defense '.ljust(10) + 'All-Stars'.ljust(10))
        for pair in result:
            team = self.getTeam(pair[0])
            i = str(result.index(pair) + 1) + '.'
            print(i.ljust(8) + pair[0].ljust(20) + ' ' + str(pair[1]).ljust(9) + ' ' + (str(self.gamesPlayed(self.getTeam(pair[0])))+' ').ljust(9) +
                  (str(team.offense)).ljust(10) + str(team.defense).ljust(10) + str(team.allstars).ljust(10))
            if i == '8.':
                print('-'*80)
        
    def turnovers(self):
        result = self.stats.teamWins
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print('Pos'.ljust(8) + 'Team'.ljust(20) + ' Wins'.ljust(10) + ' Turnovers Per Game'.ljust(10))
        for pair in result:
            i = str(result.index(pair) + 1) + '.'
            print(i.ljust(8) + pair[0].ljust(20) + ' ' + str(pair[1]).ljust(9) + ' ' + (str(my_precision(weird_division(self.getTeam(pair[0]).turnovers, self.gamesPlayed(self.getTeam(pair[0]))), 1))+' ').ljust(9))
            if i == '8.':
                print('-'*60)
            
    def leaders(self, stat='points', n=10, bench=False):
        if stat.lower() not in list(stat_dict.values()):
            return 'no records of ' + str(stat)
        stat = stat.lower()
        index = list(stat_dict.values()).index(stat)
        team = None
        gp = 0
        avg_dict = {}
        for t in self.teams:
            gp = self.gamesPlayed(t)
            for ply in t.roster:
                if bench and ply not in t.roster[5:]:
                    continue
                avg_dict[ply] = weird_division(self.stats.playerStats[ply.name][index], gp)
                avg_dict[ply] = my_precision(avg_dict[ply], 1)
        result = sorted(avg_dict.items(), key=lambda x: x[1], reverse=True)
        print('Player'.ljust(25) + '(team)'.ljust(20) + '1st option'.ljust(15) + 'Best passer?'.ljust(15) + stat.title() + ' (avg)')
        try:
            for i in range(n):
                pair = result[i]
                team = self.getTeam(pair[0].name)
                print(pair[0].name.ljust(25) + ('(' + team.name.lower() + ')').ljust(20) + str(pair[0]==team.bestPlayer(True)).ljust(15) + str(pair[0]==team.bestPasser()).ljust(15) + str(pair[1]))
        except IndexError:
            pass

    def records(self, stats='points', n=10, bench=False, res=False):
        if stats.lower() not in list(stat_dict.values()):
            return 'no records of ' + str(stats)
        r_list = []
        stats = stats.lower()
        team = None
        s_dict = {}
        for t in self.teams:
            for ply in t.roster:
                if bench and ply not in t.roster[5:]:
                    continue
                s_dict[ply] = ply.__dict__[stats][0]
        result = sorted(s_dict.items(), key=lambda x: x[1], reverse=True)
        if not res:
            print('Player'.ljust(25) + '(build)'.ljust(15) + '(team)'.ljust(20) + ' ' + stats.title().ljust(10) + 'Game')
        try:
            for i in range(n):
                pair = result[i]
                team = self.getTeam(pair[0].name)
                game = pair[0].__dict__[stats][1]
                r_list.append(game)
                if not res:
                    print(pair[0].name.ljust(25) + ('(' + pair[0].getBuild() + ')').ljust(15) + ('(' + team.name.lower() + ')').ljust(20) + ' ' + str(pair[1]).ljust(10) + game.scoreLine())
        except IndexError:
            pass
        if res:
            print()
            return r_list
        else:
            return None
    
    def percents(self, stat, n=5, best=False):
        within_arc = False
        attr = ''
        if stat == '3':
            stat = '3P'
        if stat.lower() not in percent_dict:
            return 'no records of ' + str(stat)
        stat = stat.lower()
        if stat == 'fg':
            within_arc = True
            attr = 'insideShot'.ljust(13) + 'midRange'.ljust(8)
        else:
            attr = percent_dict[stat][2].ljust(10)
        index = percent_dict[stat][1][0]
        qual = percent_dict[stat][0]
        gp = 0
        avg_dict = {}
        for t in self.teams:
            gp = self.gamesPlayed(t)
            best_list = [t.bestPlayer(True), t.secondOption(True)]
            for ply in t.roster:
                if self.stats.playerStats[ply.name][index+1] < gp*qual:
                    continue
                if best and ply not in best_list:
                    continue
                elif not best and ply in best_list:
                    continue
                avg_dict[ply] = weird_division(self.stats.playerStats[ply.name][index], self.stats.playerStats[ply.name][index+1])
                avg_dict[ply] = my_precision(avg_dict[ply]*100, 1)
        result = sorted(avg_dict.items(), key=lambda x: x[1], reverse=True)
        makes = stat_dict[index].upper() + ' (avg)'
        attempts = stat_dict[index+1].upper() + ' (avg)'
        if index in (6, 7):
            makes = '3PM (avg)'
            attempts = '3PA (avg)'
        print('Player'.ljust(20) + '(team)'.ljust(20) + (stat.upper() + ' %').ljust(10) + makes.ljust(12) + attempts.ljust(12) + attr)
        try:
            for i in range(n):
                pair = result[i]
                team = self.getTeam(pair[0].name)
                gp = self.gamesPlayed(team)
                makes = my_precision(weird_division(self.stats.playerStats[pair[0].name][index], gp), 1)
                attempts = my_precision(weird_division(self.stats.playerStats[pair[0].name][index+1], gp), 1)
                print(pair[0].name.ljust(20) + ('(' + team.name.lower() + ')').ljust(20) + str(pair[1]).ljust(10) + str(makes).ljust(12) + str(attempts).ljust(12), end='')
                if within_arc:
                    print(str(pair[0].__dict__[percent_dict[stat][2]]).ljust(13) + str(pair[0].__dict__[percent_dict[stat][3]]).ljust(8))
                else:
                    print(str(pair[0].__dict__[percent_dict[stat][2]]).ljust(10))
        except IndexError:
            pass

    def tripleDoubles(self, n=5, res=False):
        r_list = list()
        td_list = list()
        heading = 'PTS'.ljust(10) + 'REB'.ljust(10) + 'AST'.ljust(10)
        box = {1: 'team1boxScore', 2: 'team2boxScore'}
        for games in self.gameSchedule.values():
            for g in games:
                for ply in g.team1.roster:
                    if g.team1boxScore[ply.name][0]['points'] < 10:
                        continue
                    elif g.team1boxScore[ply.name][1]['rebounds'] < 10:
                        continue
                    elif g.team1boxScore[ply.name][2]['assists'] < 10:
                        continue
                    else:
                        td_list.append((ply, g, 1))
                for ply in g.team2.roster:
                    if g.team2boxScore[ply.name][0]['points'] < 10:
                        continue
                    elif g.team2boxScore[ply.name][1]['rebounds'] < 10:
                        continue
                    elif g.team2boxScore[ply.name][2]['assists'] < 10:
                        continue
                    else:
                        td_list.append((ply, g, 2))
        if not res:
            print('Player'.ljust(20) + '(build)'.ljust(12) + '(team)'.ljust(20) + heading + 'Game')
        try:
            for i in range(n):
                statline = ''
                ply = td_list[i][0]
                team = self.getTeam(ply.name)
                game = td_list[i][1]
                x = td_list[i][2]
                boxScore = game.__dict__[box[x]]
                for j in range(3):
                    statline += str(boxScore[ply.name][j][stat_dict[j]]).ljust(10)
                if not res:
                    print(ply.name.ljust(20) + ('(' + ply.getBuild() + ')').ljust(12) + ('(' + team.name.lower() + ')').ljust(20) + statline + game.scoreLine())
                else:
                    r_list.append(game)
        except IndexError:
            pass
        if res:
            print()
            return r_list

    def xPoints(self, x, stat='points', n=5, res=False):
        if stat[-1] == 'm' or stat[-1] == 'a':
            stat = stat.upper()
        r_list = list()
        x_list = list()
        box = {1: 'team1boxScore', 2: 'team2boxScore'}
        for games in self.gameSchedule.values():
            for g in games:
                for ply in g.team1.roster:
                    if g.team1boxScore[ply.name][stat_dict[stat]][stat] < x:
                        continue
                    else:
                        x_list.append((ply, g, 1))
                for ply in g.team2.roster:
                    if g.team2boxScore[ply.name][stat_dict[stat]][stat] < x:
                        continue
                    else:
                        x_list.append((ply, g, 2))
        if not res:
            print('Player'.ljust(20) + '(build)'.ljust(15) + '(team)'.ljust(20) + ' ' + stat.title().ljust(10) + 'Game')
        try:
            for i in range(n):
                ply = x_list[i][0]
                team = self.getTeam(ply.name)
                game = x_list[i][1]
                score = x_list[i][2]
                boxScore = game.__dict__[box[score]]
                statline = str(boxScore[ply.name][stat_dict[stat]][stat]).ljust(10)
                if not res:
                    print(ply.name.ljust(20) + ('(' + ply.getBuild() + ')').ljust(15) + ('(' + team.name.lower() + ')').ljust(20) + ' ' + statline + game.scoreLine())
                else:
                    r_list.append(game)
        except IndexError:
            pass
        if res:
            print()
            return r_list

    def teamAvg(self, x=1, n=5):
        stat = None
        if x == 1:
            stat = 'ppg'
        elif x == 2:
            stat = 'opp_ppg'
        if stat.lower() not in {'ppg', 'opp_ppg'}:
            return 'no team stats for ' + str(stat)
        stat = stat.lower()
        avg_dict = {}
        pos_list = sorted(self.stats.teamWins.items(), key=lambda x: x[1], reverse=True)
        pos_list = [i[0] for i in pos_list]
        order = True if stat == 'ppg' else False
        for t in self.teams:
            total = sum(self.stats.teamStats[t.name][stat])
            gp = self.gamesPlayed(t)
            avg_dict[t.name] = my_precision(weird_division(total, gp), 1)
        result = sorted(avg_dict.items(), key=lambda x: x[1], reverse=order)
        print('Team'.ljust(20) + stat.upper().ljust(10) + 'Pos'.ljust(10))
        try:
            for i in range(n):
                pair = result[i]
                team = self.getTeam(pair[0])
                print(pair[0].ljust(20) + str(pair[1]).ljust(10) + str(pos_list.index(pair[0])+1))
        except IndexError:
            pass

    def nextDay(self, _, print_text=False):
        if self.gameSchedule[_] == []:
            self.currentDay += 1
            return 0
        if print_text:
            print('=========================\nToday is Day ' + str(self.currentDay))
            print('No. of games today: ' + str(len(self.gameSchedule[_])))
            print('=========================')
        gamesToday = self.gameSchedule[_]
#         for game in gamesToday:
#             game.fixture()
        if gamesToday != None:
            for game in gamesToday:
                game.simGame(print_text)
#                 if game.team1score > game.team2score:       # team 1 won
#                     editTeam(game.team1, 5, all_attr=True)
#                     editTeam(game.team2, -5, all_attr=True)
#                 else:                                       # team2 won
#                     editTeam(game.team2, 10, all_attr=True)
#                     editTeam(game.team1, -10, all_attr=True)
                self.updateStats(game)
            if print_text:
                print('\n')
        self.currentDay += 1

    def nextWeek(self):
        for _ in range(1, 8):
            self.nextDay(_)

    def playSeason(self, text=False):
        self.setUpSeason()
        self.currentDay = 1
        for _ in self.gameSchedule.keys():
            self.nextDay(_, text)
        saveLeague(self)

def saveLeague(instance):
    i = 1
    while True:
        if not os.path.exists('leagues/'):
            os.mkdir('leagues')
        file_name = 'leagues/l' + str(i) + '.pickle'
        if os.path.exists(file_name):
            i += 1
        else:
            pickle_out = open(file_name, 'wb')
            pickle.dump(instance, pickle_out)
            pickle_out.close()
            print('Save successful: File path: ' + file_name)
            break


def loadLeague(name):
    file_name = 'leagues/' + str(name) + '.pickle'
    if os.path.exists(file_name):
        pickle_in = open(file_name, 'rb')
        print('Loaded successfully!')
        return pickle.load(pickle_in)
    else:
        return 'Load failed: No saved league named ' + str(name)
    


# l = League()
# l.playSeason()
# l.setUpSeason()

# first = Game()
# first.fixture()
