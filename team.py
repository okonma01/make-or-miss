from player import *
import os.path
stars = 1
class Team():
    def __init__(self, name, roster, lineup, bench, allstars=0, turnovers=0, offense=0, defense=0, wins=0):
        self.name = name
        self.roster = roster
        self.lineup = lineup
        self.bench = bench
        self.setLineup()
        self.allstars = allstars
        self.turnovers = turnovers
        teamOffense = 0
        teamDefense = 0
        for player in self.roster:
            playerOffense = player.overall(off=True)
            playerDefense = player.overall(deff=True)
            teamOffense += playerOffense
            teamDefense += playerDefense
        self.offense = int(teamOffense / 8)
        self.defense = int(teamDefense / 8)
        self.wins = wins
        
    def setLineup(self):
        for i in range(5, 9):
            for key, val in build_dict.copy().items():
                if i+1 in val:
                    val.remove(i+1)
                    for j in val:
                        if self.roster[i].overall() > self.roster[j].overall() and self.roster[i].getBuild() == self.roster[j].getBuild():
                            self.substitute(self.roster[j], self.roster[i], starting=True)
                            break
                    val.append(i+1)

        self.lineup = self.roster[:5]

    def getAbility(self):
        teamOffense = 0
        teamDefense = 0
        playerOffense = 0
        playerDefense = 0
        for player in self.roster:
            teamOffense += player.overall(off=True)
            teamDefense += player.overall(deff=True)
        teamOffense = teamOffense / 8
        teamDefense = teamDefense / 8
#         off = pow(1.075, teamOffense)
#         deff = pow(1.075, teamDefense)
        return self.name + ':\nOffense: ' + str(int(teamOffense)) + ' | Defense: ' + str(int(teamDefense))
    
#     def pickPlayer(self, i=5):
#         result = None
#         score = 0
#         squad = self.lineup.copy()
#         best_list = [self.bestPlayer(True), self.secondOption(True)]
#         for p in squad:
#             if squad.index(p) == i:
#                 continue
#             pass_score = random.randint(0, int(p.passing*0.75))
#             if pass_score > score:
#                 result = p
#             elif pass_score == score and p in best_list:
#                 result = p
#         return result
    
    def passRank(self, ply):
        result = 0
        arr = {p: p.passing for p in self.lineup}
        arr = sorted(arr.items(), key=lambda x: x[1], reverse=False)
        rank = [x[0] for x in arr]
        result = 0.15 * (rank.index(ply)+1)
        return my_precision(result, 2)
    
    def bestPasser(self):
        result = None
        val = 0
        for player in self.lineup:
            if player.passing > val:
                val = player.passing
                result = player
            elif player.passing == val and player.bestAttribute() == 'passing':
                val = player.passing
                result = player
        return result
    
    def bestPlayer(self, offense=False):
#         best_player = None
        ovr = 0
        for player in self.lineup:
            if player.overall(offense) > ovr:
                best_player = player
                ovr = player.overall(offense)
        return best_player

    def secondOption(self, offense=False):
        second_option = None
        ovr = 0
        lineup_copy = self.lineup.copy()
        lineup_copy.remove(self.bestPlayer(offense))
        for player in lineup_copy:
            if player.overall(offense) > ovr:
                second_option = player
                ovr = player.overall(offense)
        return second_option

    def substitute(self, player_out, player_in, starting=False, sim=False):
        if not sim:
            time.sleep(0.2)
        if starting:
            index_in = self.roster.index(player_out)
            index_out = self.roster.index(player_in)
            self.roster[index_in] = player_in
            self.roster[index_out] = player_out
            self.lineup = self.roster[:5]
            self.bench = self.roster[5:]
        else:
            index = self.lineup.index(player_out)
            self.lineup[index] = player_in
#             self.lineup = self.roster[:5]
#         self.bench = self.roster[5:]

    def getMatchup(self, attr, i):
        result = None
        rating = 0
        attr = matchup_dict[attr]
        for player in self.lineup:
            index = self.lineup.index(player)
            v_list = [set(matchup_dict[build]) for build in new_builds]
            if i == index or {i, index} in v_list:
                p_rating = list(player.__dict__.values())[11:][attr[0]] + list(player.__dict__.values())[11:][attr[1]]
                if p_rating > rating:
                    rating = p_rating
                    result = player
        
        return result

    def getLineup(self):
        print('\n' + self.name.upper() + ':')
        for player in self.lineup:
            print((player.name).ljust(20) + ' [' + player.getBuild().upper()[0] + ']')
    
    def getBench(self):
        print('\n' + self.name.upper() + ':')
        for player in self.bench:
            print((player.name).ljust(20) + ' [' + player.getBuild().upper()[0] + ']')

    def getAttributes(self):
        attr_list = list(self.roster[0].__dict__)[12:]
        print('\n' + (self.name.upper() + ':').ljust(36), end='')
        for attr in attr_list:
            print(attr[:3].ljust(8), end='')
        print()
        for ply in self.roster:
            p_attr = list(ply.__dict__.values())[12:]
            print(ply.name.ljust(24), end='')
            print('[%s] [%s]   ' % (ply.overall(off=True), ply.overall(deff=True)), end='')
            print(*p_attr, sep=''.ljust(6))
    
    def copyTeam(self, player):
        result = copy.copy(self)
        result.roster.remove(player)
        return result

def generate(team, i):
    if i not in range(1, 10):
        return 'invalid index'
    best_set = {team.bestPlayer(True), team.secondOption(True)}
    t_list = team.roster[:5] if i < 6 else team.roster[5:]
    fga = eat_dict[team.allstars][i-1]
    fga = my_precision(random.uniform(*fga), 1)
    td = {x: x.overall(off=True) for x in t_list}
    t_sorted = sorted(td.keys(), key=lambda x: x.overall(True), reverse=True)
    ply = t_sorted[i-6] if i >= 6 else t_sorted[i-1]
    is_best = ply in best_set
    best_attr = ply.bestAttribute()
    trft = (trft_dict[best_attr][0][is_best], trft_dict[best_attr][1])
    threes_a = my_precision(fga*trft[0], 1)
    fta = my_precision(fga*trft[1], 1)
    twos_a = fga - threes_a
    two_eff = (porcientos(ply.insideShot, 'insideShot') + porcientos(ply.midRange, 'midRange')) / 2
    twos_m = my_precision(twos_a * (two_eff/100), 1)
    three_eff = porcientos(ply.threePoint, 'threePoint')
    threes_m = my_precision(threes_a * (three_eff/100), 1)
    ft_eff = porcientos(ply.freeThrow, 'freeThrow')
    ftm = my_precision(fta * (ft_eff/100), 1)
    print('\n' + ply.name.upper() + '\n')
    print('fg:   %s / %s' % (round(twos_m + threes_m, 1), fga))
    print('fg%:'.ljust(5), str(my_precision(100*(twos_m+threes_m)/fga, 1)))
    print('3p:   %s / %s' % (threes_m, threes_a))
    print('3p%:'.ljust(5), str(my_precision((threes_m * 100)/threes_a, 1)))
    print('ft:   %s / %s' % (ftm, fta))
    print('ft%:'.ljust(5), str(my_precision((ftm * 100)/fta, 1)))
    res = 3*threes_m + 2*twos_m + ftm
    res = my_precision(res, 1)
    print('\nPPG:', str(res))
    

def isBestPlayer(player, team):
    if player == team.bestPlayer():
        return True
    else:
        return False

def makeTeam(all_stars=0):
    global stars
    all_stars = stars % 3
#     all_stars = 1
    stars += 1
#     all_stars = int(all_stars/2.75)
    grade_dict = {x:'' for x in range(1, 10)}
#     print('all stars: ', all_stars)
    grade_list = [x+1 for x in range(5)]
    for i in range(all_stars):
        pos = random.choice(grade_list)
        grade_dict[pos] = 'A'
        grade_list.remove(pos)
    for i in range(len(grade_dict)):
        if grade_dict[i+1] != 'A':
            if i+1 <= 5:
                grade_dict[i+1] = random.choice(['B', 'C'])
            else:
                grade_dict[i+1] = random.choice(['C', 'D'])
    teamRoster = []
    teamLineup = []
    teamBench = []
    for build in range(1, 10):
        for key, val in build_dict.items():
            if build in val:
                newPlayer = createPlayer(key, grade_dict[build])
                break
        teamRoster.append(newPlayer)
        if build <= 5:
            teamLineup.append(newPlayer)
        else:
            teamBench.append(newPlayer)
    teamName = names.get_last_name()
    if teamName[-1] == 'z':
        pass
    if teamName[-2:] == 'ch' or teamName[-2:] == 'sh':
        teamName += 'es'
    elif teamName[-1] != 's':
        teamName += 's'
    if teamName[:2] == 'Mc':
        teamName = teamName[:2] + teamName[2:].title()
    teamName = 'Los ' + teamName

    return Team(teamName, teamRoster, teamLineup, teamBench, allstars=all_stars)

def saveTeam(team):
    teamName = team.name.lower()
    teamName = teamName.split()[0] + '_' + teamName.split()[1] + '.csv'
    teamName = 'teams/' + teamName
    if not os.path.exists(teamName):
        teamFile = open(teamName, 'w', newline='')
        teamWriter = csv.writer(teamFile)
        for row in range(len(team.roster)):
            player = team.roster[row]
            teamWriter.writerow([player.name, player.insideShot, player.midRange, player.threePoint, player.passing,
                                 player.onBallDefense, player.insideDefense, player.steal, player.block,
                                 player.offRebound, player.defRebound, player.freeThrow])
        teamFile.close()

def loadTeam(team):
    teamName = team.name.lower()
    teamName = teamName.split()[0] + '_' + teamName.split()[1] + '.csv'
    teamName = 'teams/' + teamName
    teamFile = open(teamName)
    teamReader = csv.reader(teamFile)
    index = 0
    for row in teamReader:
        player = team.roster[index]
        player.insideShot = int(row[1])
        player.midRange = int(row[2])
        player.threePoint = int(row[3])
        player.passing = int(row[4])
        player.onBallDefense = int(row[5])
        player.insideDefense = int(row[6])
        player.steal = int(row[7])
        player.block = int(row[8])
        index += 1
    teamFile.close()


def editTeam(team, delta, all_attr=False):
    teamName = team.name.lower()
    teamName = teamName.split()[0] + '_' + teamName.split()[1] + '.csv'
    teamName = 'teams/' + teamName
    teamFile = open(teamName)
    teamReader = csv.reader(teamFile)
    index = 0
    delta = int((myround(delta) / 5))
    for row in teamReader:
        player = team.roster[index]
        if all_attr:
            player.onBallDefense = int(row[5]) + delta
            player.insideDefense = int(row[6]) + delta

        player.onBallDefense = int(row[5]) + delta
        player.insideDefense = int(row[6]) + delta
#         player.steal = int(row[3]) + delta
#         player.block = int(row[8]) + delta
        checkPlayer(player)
        index += 1
    teamFile.close()
    
def editPlayers(team, delta):
    delta = int((myround(delta) / 5))
    for player in team.lineup:
        checkPlayer(player)
        player.threePoint    += delta
#         player.passing = int(row[4]) + delta
        player.onBallDefense += delta
        player.insideDefense += delta
#         player.block         += delta
        checkPlayer(player)

def trey_hold(x):
    index = x - 62
    expo = math.pow(1.082, index)
    intercept = 11.2
    result = expo + intercept
    return result

def shot_hold(p2, rating, move, avg_list):
    attr = attr_dict[move]
    index = attr_list.index(attr) - 1
    delta = p2.__dict__[attr] - avg_list[index]
    rating = int(pow(rating, def_log(delta, 2)))
    return rating

def hold(p1, move, p2_rating, team, b_passed):
#     best_list = [team.bestPlayer(True), team.secondOption(True)]
    twos_list = ['shootInside', 'shootMid']
    ball_passed = b_passed
    playerTwoRating = p2_rating
    playerOneMove = move
    playerOne = p1
    if playerOneMove in twos_list:
        hold = random.uniform(*twos_dict[ball_passed])
        playerTwoRating = int(pow(playerTwoRating, hold))
            
    elif playerOneMove == 'shoot3':
        
        three_ability = playerOne.threePoint/100
        x = trey_hold(three_ability*100)
        hold = math.exp(three_ability) * math.exp(three_ability/2)
        hold = weird_division(hold, x)

#         phi = 0.95 if ball_passed else 1.00
        phi = random.uniform(*hold_dict[ball_passed][playerOne.getBuild()])
        phi = my_precision(phi, 2)
        
        hold += phi
        playerTwoRating = int(pow(playerTwoRating, hold))
    return playerTwoRating

# t = makeTeam()