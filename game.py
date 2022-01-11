from team import *
import pygame
from pygame import mixer

mixer.init()
shot_success = mixer.Sound(file='sounds/shot-success.mp3')
shot_success.set_volume(0.4)
crowd_cheer = mixer.Sound(file='sounds/crowd-cheer.mp3')
crowd_cheer.set_volume(0.9)
crowd_oh = mixer.Sound(file='sounds/crowd-oh.mp3')
crowd_oh.set_volume(0.7)

def loop():
    pygame.init()
    mixer.init()
    mixer.music.load('sounds/ambience.mp3')
    mixer.music.set_volume(0.6)
    mixer.music.play(loops=-1)

def make():
    shot_success.play()
    crowd_cheer.play()
    time.sleep(0.1)

def miss():
    crowd_oh.play()
    time.sleep(0.25)

passResult = 0
myCheck = None
ball_passed = False
pass_count = 0
pass_assist = [False, 0]
heat_dict = {}
friendly = True
class Game():
    def __init__(self, team1=makeTeam(), team2=makeTeam(), team1score=0, team2score=0, team1boxScore={}, team2boxScore={}, score=0, matchups={}, ass_dict={}, pair=(), attrs=[], leave=False):
        global heat_dict, heat_ply
        heat_ply = None
        self.score = 0
        self.team1 = team1
        self.team2 = team2
        saveTeam(self.team1)
        saveTeam(self.team2)
        self.team1boxScore = dict()
        self.team2boxScore = dict()
        self.ass_dict = dict()
        self.pair = pair
        self.attrs = [0 for x in range(11)]
        for player in self.team1.roster:
            self.team1boxScore[player.name] = [{boxstat_dict[x][0]: 0} for x in range(len(boxstat_dict))]
            self.ass_dict[player.name] = [0, 0]
            for a in attr_list[1:]:
                i = attr_list[1:].index(a)
                self.attrs[i] += player.__dict__[a]
        for player in self.team2.roster:
            self.team2boxScore[player.name] = [{boxstat_dict[x][0]: 0} for x in range(len(boxstat_dict))]
            self.ass_dict[player.name] = [0, 0]
            for a in attr_list[1:]:
                i = attr_list[1:].index(a)
                self.attrs[i] += player.__dict__[a]
        self.attrs = [int(x/18) for x in self.attrs]
        self.team1score = 0
        self.team2score = 0
        self.matchups = dict()
        self.leave = leave

    def resetGame(self):
        global heat_dict
        self.ass_dict = dict()
        for player in self.team1.roster:
            self.team1boxScore[player.name] = [{boxstat_dict[x][0]: 0} for x in range(len(boxstat_dict))]
            self.ass_dict[player.name] = [0, 0]
        for player in self.team2.roster:
            self.team2boxScore[player.name] = [{boxstat_dict[x][0]: 0} for x in range(len(boxstat_dict))]
            self.ass_dict[player.name] = [0, 0]
        self.team1score = 0
        self.team2score = 0
        heat_dict = dict()
        for i in range(len(self.team1.roster)):
            p1 = self.team1.roster[i].name
            p2 = self.team2.roster[i].name
            heat_dict[p1] = ['neutral', 0]
            heat_dict[p2] = ['neutral', 0]
        self.leave = False
#         self.team1.turnovers = 0
#         self.team2.turnovers = 0

    def fixture(self):
        return self.team2.name + ' @ ' + self.team1.name
#         self.team2.getAbility()
#         self.team1.getAbility()
    
    def scoreLine(self):
        ot = ' (OT)' if self.leave else ''
        return self.team2.name + ' ' + str(self.team2score) + ' - ' + str(self.team1score) + ' ' + self.team1.name + ot
    
    def freeThrows(self, player, n, sim=False):
        result = 0
        threshold = 0
        missed_last = False
        for i in range(n):
            freeThrowRating = random.randint(int(player.freeThrow*0.15), player.freeThrow)
            if not sim:
                time.sleep(1)
            x = random.randint(1, 100)
            threshold = 20 if x in range(15, 85) else 35
            if freeThrowRating >= threshold:
                if not sim:
                    print(random.choice(linesFtGood))
                result += 1
            else:
                if i == n-1:
                    missed_last = True
                if not sim:
                    print(random.choice(linesFtBad))
        return (result, missed_last)

    def boxScore(self):
        print(self.team1.name.upper() + ':')
        box = self.team1boxScore
        for player in self.team1.roster:
            print((player.name).ljust(20) + ': ', end='')
            for i in range(len(boxstat_dict)):
                if i > 4:
                    if i % 2 == 0:
                        continue
                    space = 5
                    print((str(box[player.name][i][boxstat_dict[i][0]]) + '/' + str(box[player.name][i+1][boxstat_dict[i+1][0]])).rjust(space) + boxstat_dict[i][1], end='')
                else:
                    space = 2
                    print(str(box[player.name][i][boxstat_dict[i][0]]).rjust(space) + boxstat_dict[i][1], end='')
            print()
        print('\n' + self.team2.name.upper() + ':')
        box = self.team2boxScore
        for player in self.team2.roster:
            print((player.name).ljust(20) + ': ', end='')
            for i in range(len(boxstat_dict)):
                if i > 4:
                    if i % 2 == 0:
                        continue
                    space = 5
                    print((str(box[player.name][i][boxstat_dict[i][0]]) + '/' + str(box[player.name][i+1][boxstat_dict[i+1][0]])).rjust(space) + boxstat_dict[i][1], end='')
                else:
                    space = 2
                    print(str(box[player.name][i][boxstat_dict[i][0]]).rjust(space) + boxstat_dict[i][1], end='')
            print()

    def teamStats(self):
        stat_list = [0 for x in range(11)]
        print(self.team1.name + ':')
        for player in self.team1.roster:
            for i in range(len(stat_list)):
                stat_list[i] += self.team1boxScore[player.name][i][boxstat_dict[i][0]]
        for i in range(len(abbv_dict)):
            print(abbv_dict[i] + str(stat_list[i]), end='')
        stat_list = [0 for x in range(11)]
        print('\n' + self.team2.name + ':')
        for player in self.team2.roster:
            for i in range(len(stat_list)):
                stat_list[i] += self.team2boxScore[player.name][i][boxstat_dict[i][0]]
        for i in range(len(abbv_dict)):
            print(abbv_dict[i] + str(stat_list[i]), end='')

    def bestMatchup(self, player, off_team, def_team): # haven't done this yet - DONE
        matchup = def_team.getMatchup(player.bestAttribute(point=True), off_team.lineup.index(player))
        return matchup
    
    def getMatchup(self, player, team, i):
        result = None
        m_set = set()
        for p in list(self.matchups.values()):
            if p != None:
                m_set.add(p)
        for ply in team.lineup:
            index = team.lineup.index(ply)
            v_list = [set(matchup_dict[build]) for build in new_builds]
            if ply not in m_set:
                if i == index or {i, index} in v_list:
                    result = ply
                    return result
        if result == None:
            result = team.lineup[i]

        return result

    def setMatchups(self, t1, t2, crunch):
        x = random.randint(1, 100)
        no1 = t1.bestPlayer(True)
        t_range = team_dict[t2.allstars]
        for ply in t1.lineup:
            self.matchups[ply] = None
        if crunch or x in range(40, 60):
            self.matchups[no1] = self.bestMatchup(no1, t1, t2)
        else:
            if x in range(10, 90):
                index = t1.lineup.index(no1)
                self.matchups[no1] = t2.lineup[index]
            else:
                self.matchups[no1] = random.choice(t2.lineup)
        ovr_dict = {ply: ply.overall(off=True) for ply in t1.lineup}
        ovr_list = sorted(ovr_dict.keys(), key=lambda x: x.overall(off=True),  reverse=True)
        ovr_list.remove(no1)
        def_dict = {ply: ply.overall(deff=True) for ply in t2.lineup}
        def_list = sorted(def_dict.keys(), key=lambda x: x.overall(deff=True), reverse=True)
        def_list.remove(self.matchups[no1])
        for player in range(len(ovr_list)):
            ply = ovr_list[player]
            best_attr = ply.bestAttribute(point=True)
            attr_tuple = matchup_dict[best_attr]
            a_list = [attr_list[attr_tuple[0]], attr_list[attr_tuple[1]]]
            m_dict = {ply: ply.overall(deff=True) for ply in def_list}
            m_list = sorted(m_dict.keys(), key=lambda x: x.__dict__[a_list[0]]+x.__dict__[a_list[1]], reverse=True)
            self.matchups[ply] = m_list[0]
            def_list.remove(self.matchups[ply])
    
    def getRebounder(self, team, mode):
        global heat_dict
        offdef = [{True: 0.59, False: 0.51}, {True: 0.45, False: 0.42}]
        result = 0
        boardMan = None
        for player in team.lineup:
            hot = heat_dict[player.name][0] == 'hot'
            def_reb = player.defRebound * reb_dict[player.getBuild()]
            off_reb = player.offRebound
            if mode == 1:
                rating = random.randint(0, int(def_reb*offdef[0][hot]))
            else:
                rating = random.randint(0, int(off_reb*offdef[1][hot]))
            if rating > result:
                result = rating
                boardMan = player
        return (boardMan, result)
    
    def getAction(self, team, ply):
        best = ply.bestAttribute()
        print('\n1: shootInside, 2: shootMid, 3: shoot3, 4: pass')
        print('best attribute: ' + best, end='')
        print('(' + str(ply.__dict__[best]) + ')\n')
        while True:
            action = input()
            if action.isnumeric() and int(action) in action_dict:
                return action_dict[int(action)]

    def getPlayer(self, team):
        for ply in team.lineup:
            i = team.lineup.index(ply)
            print(str(i+1) + ': ' + ply.name, end=' ')
            if ply == team.bestPlayer(offense=True):
                print('(1st) ', end='')
            if ply == team.secondOption(offense=True):
                print('(2nd) ', end='')
            if ply == team.bestPasser():
                print('(best passer) ', end='')
            if i == 1:
                print()
        print('\n')
        lineup_dict = {x+1: team.lineup[x] for x in range(len(team.lineup))}
        while True:
            choice = input()
            if choice.isnumeric() and int(choice) in lineup_dict:
                return lineup_dict[int(choice)]

    def passTo(self, team, player):
        lineup_dict = {x+1: team.lineup[x] for x in range(len(team.lineup))}
        lineup_dict.pop(team.lineup.index(player)+1)
        for ply in team.lineup:
            if ply == player:
                continue
            i = team.lineup.index(ply)
            print(str(i+1) + ': ' + ply.name, end=' ')
            if ply == team.bestPlayer(offense=True):
                print('(1st) ', end='')
            elif ply == team.secondOption(offense=True):
                print('(2nd) ', end='')
            if ply == team.bestPasser():
                print('(best passer) ', end='')
        print('\n')
        while True:
            choice = input()
            if choice.isnumeric() and int(choice) in lineup_dict:
                return lineup_dict[int(choice)]

    def momentum(self):
        diff = self.team1score - self.team2score
        if diff > 0:
            teamAhead = self.team1
            teamBehind = self.team2
        elif diff < 0:
            teamAhead = self.team2
            teamBehind = self.team1
        else:
            return None
        diff = abs(diff)
        if diff > 5:
            editTeam(teamAhead, -diff*2)
            editTeam(teamBehind, diff*2)
    
    def heatCheck(self, result, ply, team, n):
        global heat_dict, heat_ply
        if ply == None:
            heat_ply = None
            return None
        if n == 2:
            heat_ply = None
            ovr = ply.overall()
            heat = heat_dict[ply.name][0]
            if ply == team.bestPlayer(offense=True):
                return rhythm_dict[heat]['A']
            elif ply == team.secondOption(offense=True):
                return rhythm_dict[heat]['B']
            else:
                return rhythm_dict[heat]['C']
        elif n == 3:
            if result > 0:
                if heat_dict[ply.name][1] <= -3:
                    heat_dict[ply.name][1] = 0
                else:
                    heat_dict[ply.name][1] += 1
            else: # result == 0 (missed shot)
                if heat_dict[ply.name][1] <= -3:
                    heat_dict[ply.name][1] = -3
                elif heat_dict[ply.name][1] in range(1, 3):
                    heat_dict[ply.name][1] = 0
                elif heat_dict[ply.name][1] > 3:  # PROBLEM : A PLAYER ON HEAT '3' STUCK ON '3', BECUASE OF >= SIGN
                    heat_dict[ply.name][1] = 3
                else:
                    heat_dict[ply.name][1] -= 1
            first = (ply == team.bestPlayer(offense=True))
            second = (ply == team.secondOption(offense=True))

            if heat_dict[ply.name][1] >= 3:
                heat_dict[ply.name][0] = 'hot'
            elif heat_dict[ply.name][1] <= -2:
                heat_dict[ply.name][0] = 'cold'
            else:
                heat_dict[ply.name][0] = 'neutral'
            heat_ply = None
            return None

    def capRating(self, p1, p1rating, p2rating):
        global heat_dict, heat_ply
        if p1rating >= 100 or p2rating >= 100:
            p1rating = 40
            p2rating = myLog(p1rating, p2rating)
        return (p1rating, p2rating)
    
    def playPossession(self, teamOne, teamTwo, boxScore, passBonus=0, stealBonus=0, crunchTime=False, sim=False, usr=0, passer=False):
        global myCheck, ball_passed, pass_count, passResult, pass_assist
        global heat_dict, heat_ply
        box_dict = {1: self.team1boxScore, 2: self.team2boxScore}
        points = 0
#         turn = False
#         passResult = 0
        if self.score > 0:
            print('!')
            return 0
        else:
            if pass_count == 0:
                self.score = 0
            counter = True
            while counter: # haven't really done this yet; find a way for everyone to eat (not just the team's primary option)
                if usr != 0:
                    if not ball_passed: # who gets the ball first (brings it up the court)
                        playerOne = self.getPlayer(teamOne)
                    else:
                        playerOne = self.passTo(teamOne, myCheck)
                    counter = False
                else:
                    is_crunch = crunch_dicts[teamOne.allstars][crunchTime]
                    dice = random.randint(0, 99)
                    hot = False
                    best = teamOne.bestPlayer(offense=True)
                    second = teamOne.secondOption(offense=True)
                    point = teamOne.bestPasser()
                    bnep = best != point
                    rm_dict = {True: teamOne.bestPasser(), False: teamOne.secondOption(offense=True)}
                    crunch_zero = (is_crunch[0][0], is_crunch[0][-1]+16) if best.bestAttribute() == 'passing' else is_crunch[0]
                    if dice in range(*crunch_zero):
                        playerOne = teamOne.bestPlayer(offense=True)
                    elif dice in range(*is_crunch[1]):
                        if bnep:
                            playerOne = teamOne.bestPasser()
                        else:
                            playerOne = teamOne.secondOption(offense=True)
                    else:
                        lineup_copy = teamOne.lineup.copy()
#                         lineup_copy.remove(teamOne.bestPlayer(offense=True))
                        lineup_copy.remove(rm_dict[bnep])
                        if (bnep and second not in {best, point}) and dice in range(is_crunch[0][-1]+25, is_crunch[1][-1]+6):
                            playerOne = teamOne.secondOption(offense=True)
                        else:
                            playerOne = random.choice(lineup_copy)
                    for ply in teamOne.lineup:
                        if heat_dict[ply.name][0] == 'hot' and dice in range(20, 80):
                            hot = True
                            playerOne = ply
#                             playerOne.defRebound = 
                            break

                    if playerOne == myCheck:
                        continue
                    else:
                        counter = False

            myCheck = playerOne

            playerTwo = self.matchups[playerOne]

            if not sim:
                print('\n' + playerOne.name + ' has the ball for ' + teamOne.name + '...', end='')
                if usr != 0:
                    print('(' + heat_dict[playerOne.name][0] + ')')
                else:
                    print(' (matchup: ' + playerTwo.name + ')')
                time.sleep(1)

            p_heat = heat_dict[playerOne.name][0]
            lbound = self.heatCheck(0, playerOne, teamOne, 2)[0]
            ubound = self.heatCheck(0, playerOne, teamOne, 2)[1]
            
#             editHeat(playerOne, p_heat)
            
            best_passer = playerOne == teamOne.bestPasser()
            
            if usr == 0:
                playerOneOffense = playerOne.getOffensiveMoveAndRating(teamOne, passed=ball_passed, l_bound=lbound, u_bound=ubound, heat=p_heat, drivekick=passer, b_passer=best_passer)
            else:
                p1_move = self.getAction(teamOne, playerOne)
                playerOneOffense = playerOne.getOffensiveRating(move=p1_move, passed=ball_passed, l_bound=lbound, u_bound=ubound, heat=p_heat, crunch=crunchTime)
                print()

            playerOneMove = playerOneOffense[0]
            playerOneRating = playerOneOffense[1] + passBonus
            
            playerTwoDefense = playerTwo.getDefensiveMoveAndRating(playerOneMove, heat=p_heat, pass_rank=teamOne.passRank(playerOne))
            playerTwoMove = playerTwoDefense[0]
            playerTwoRating = playerTwoDefense[1] + stealBonus
            
            if playerOneMove in {'shootInside', 'shootMid'} and playerTwoMove in {'insideDefense', 'perimeterDefense'}:
                playerTwoRating = shot_hold(playerTwo, playerTwoRating, playerTwoMove, self.attrs)
            else:
                playerTwoRating = hold(playerOne, playerOneMove, playerTwoRating, teamOne, ball_passed)
                

            if playerOne in self.team1.roster:
                check = {False: 1.01, True: 1.03}
                playerOneRating = int(pow(abs(playerOneRating), check[crunchTime]))

            if playerTwoMove == 'shoot2foul':
                playerTwoRating = int(pow(playerTwoRating, 1.2))

            cap_tuple = self.capRating(playerOne, playerOneRating, playerTwoRating)
            playerOneRating = cap_tuple[0]
            playerTwoRating = cap_tuple[1]
            
            
            if not sim and playerOneMove == 'shoot3':
                print(playerOne.name.split()[1] + random.choice(linesShoot3))
                time.sleep(0.85)

            is_sim = sim
            box = box_dict[boxScore]
            
            is_usr = usr
            
            if not sim:
                print('P1 rating: ' + str(playerOneRating))
                print('P2 rating: ' + str(playerTwoRating))

            
            if playerOneRating > playerTwoRating:
                mini_dict = {True: 11, False: 10}
                if playerOneRating < mini_dict[playerOne == teamOne.bestPasser()]:
                    if not sim:
                        print('Turnover!')
                    teamOne.turnovers += 1
                    ball_passed = False
                    pass_assist[0] = False
                    heat_ply = playerOne
#                     turn = True
                    return 0

                if playerOneMove != 'pass':
                    pts = make_dict[playerOneMove][0]
                    if not sim:
                        make()
                        lines = make_dict[playerOneMove][1]
                        print(random.choice(lines)[:-pts], end='')# + '\n~~~~~~~~~~~~~~~~~~~~~~~~~')
#                         time.sleep(0.25)
                    self.score = pts
                    box[playerOne.name][0]['points'] += self.score
                    box[playerOne.name][5]['FGM'] += 1
                    box[playerOne.name][6]['FGA'] += 1
                    self.ass_dict[playerTwo.name][0] += 1
                    self.ass_dict[playerTwo.name][1] += 1
                    if playerOneMove == 'shoot3':
                        box[playerOne.name][7]['3PM'] += 1
                        box[playerOne.name][8]['3PA'] += 1

                    if playerTwoMove == 'shoot2foul' or playerTwoMove == 'shoot3foul':
                        if not sim:
                            time.sleep(0.5)
                            print(', and 1!')
                            time.sleep(1)
                            line = make_dict[playerOneMove][2]
                            print('\n' + playerOne.name.split()[1] + line)

                        result = self.freeThrows(playerOne, 1, is_sim)

                        if result[0] > 0:
                            box[playerOne.name][0]['points'] += 1
                            box[playerOne.name][9]['FTM'] += 1
                            
                        if not result[1]:
                            self.score += 1
                            
                        box[playerOne.name][10]['FTA'] += 1
                        
                        if result[1]:
                            self.score = 0
                            defBoard, offBoard = self.getRebounder(teamTwo, 1), self.getRebounder(teamOne, 2)
                            defBoardMan, offBoardMan = defBoard[0], offBoard[0]
                            defBoardManRating, offBoardManRating = defBoard[1], offBoard[1]
                            if defBoardManRating >= offBoardManRating:
                                if not sim:
                                    time.sleep(1.5)
                                    print(defBoardMan.name + ' grabs the rebound for ' + teamTwo.name + '...')
                                passResult = 0
                                pass_count = 0
                                if defBoardMan in self.team2.lineup:
                                    self.team2boxScore[defBoardMan.name][1]['rebounds'] += 1
                                else:
                                    self.team1boxScore[defBoardMan.name][1]['rebounds'] += 1
                                if not sim:
                                    time.sleep(0.5)
#                                 self.score = 0
                            else:
                                if not sim:
                                    time.sleep(1.5)
                                    print('Offensive Rebound by ' + offBoardMan.name + '!')
                                    time.sleep(1)
                                ball_passed = False
                                pass_count = 3
                                if offBoardMan in self.team1.lineup:
                                    self.team1boxScore[offBoardMan.name][1]['rebounds'] += 1
                                    self.score = self.playPossession(self.team1, self.team2, boxScore=1, passBonus=playerOneOffense[1], sim=is_sim, usr=is_usr)
                                else:
                                    self.team2boxScore[offBoardMan.name][1]['rebounds'] += 1
                                    self.score = self.playPossession(self.team2, self.team1, boxScore=2, passBonus=playerOneOffense[1], sim=is_sim, usr=is_usr)
                                if passResult > 0 and offBoardMan != myCheck:
                                    ball_passed = False
                                    pass_assist[0] = True
                                    pass_assist[1] = self.score
                                    if not sim:
                                        time.sleep(0.75)
                                        print(offBoardMan.name + ' gets the assist!')

                                    box[offBoardMan.name][3]['assists'] += 1

                                    self.score = passResult
                                    passResult = 0
                                
                            self.score += pts
                            self.score += result[0]
                                
# --------------------------------------------------------------------------------------------------------------


                    else:
                        if not sim:
                            print('!'*make_dict[playerOneMove][0])
                elif playerOneMove == 'pass':
                    ball_passed = True
                    pass_count += 1
                    if pass_count > 7:
                        if not sim:
                            print('\nShot clock violation!\n')
                            time.sleep(0.5)
                            print(teamTwo.name + ' ball...')
                        ball_passed = False
                        pass_count = 0
                        teamOne.turnovers += 1
#                         turn = True
                        return 0
                    if not sim:
                        print(playerOne.name.split()[1] + ' passes the ball...')
                        time.sleep(1)
                    
#                     if best_passer:
#                         bonus = 0.8
#                     else:
#                         bonus = 0.2
                    bonus = teamOne.passRank(playerOne)
                    if playerOne in self.team1.lineup:
                        self.score = self.playPossession(self.team1, self.team2, boxScore=1, passBonus=int(playerOneOffense[1]*bonus), sim=is_sim, usr=is_usr, passer=best_passer)
                    else:
                        self.score = self.playPossession(self.team2, self.team1, boxScore=2, passBonus=int(playerOneOffense[1]*bonus), sim=is_sim, usr=is_usr, passer=best_passer)
                    if passResult > 0:
                        ball_passed = False
                        pass_assist[0] = True
                        pass_assist[1] = self.score
                        if not sim:
                            time.sleep(0.75)
                            print(playerOne.name + ' gets the assist!')

                        box[playerOne.name][2]['assists'] += 1

                        self.score = passResult
                        passResult = 0

            else:
                pass_assist[0] = False
                if playerTwoMove == 'shoot2foul' or playerTwoMove == 'shoot3foul':
                    if not sim:
                        print('Foul!')
                        time.sleep(0.5)
                        print('It\'s a foul on ' + playerTwo.name + '...')
                        time.sleep(1)
                        print('...and ' + playerOne.name.split()[1] + foul_dict[playerTwoMove][1])
                        time.sleep(1)
                        
                    result = self.freeThrows(playerOne, foul_dict[playerTwoMove][0], is_sim)
                    if result[0] > 0:
                        box[playerOne.name][9]['FTM'] += result[0]
                        box[playerOne.name][0]['points'] += result[0]
                        
                    if not result[1]:
                        self.score = result[0]

                    box[playerOne.name][10]['FTA'] += foul_dict[playerTwoMove][0]
                    
                    if result[1]:
                        defBoard, offBoard = self.getRebounder(teamTwo, 1), self.getRebounder(teamOne, 2)
                        defBoardMan, offBoardMan = defBoard[0], offBoard[0]
                        defBoardManRating, offBoardManRating = defBoard[1], offBoard[1]
                        if defBoardManRating >= offBoardManRating:
                            if not sim:
                                time.sleep(1.5)
                                print(defBoardMan.name + ' grabs the rebound for ' + teamTwo.name + '...')
                            passResult = 0
                            pass_count = 0
                            if defBoardMan in self.team2.lineup:
                                self.team2boxScore[defBoardMan.name][1]['rebounds'] += 1
                            else:
                                self.team1boxScore[defBoardMan.name][1]['rebounds'] += 1
                            if not sim:
                                time.sleep(0.5)
#                             self.score = 0
                        else:
                            if not sim:
                                time.sleep(1.5)
                                print('Offensive Rebound by ' + offBoardMan.name + '!')
                                time.sleep(1)
                            ball_passed = False
                            pass_count = 3
                            if offBoardMan in self.team1.lineup:
                                self.team1boxScore[offBoardMan.name][1]['rebounds'] += 1
                                self.score = self.playPossession(self.team1, self.team2, boxScore=1, passBonus=playerOneOffense[1], sim=is_sim, usr=is_usr)
                            else:
                                self.team2boxScore[offBoardMan.name][1]['rebounds'] += 1
                                self.score = self.playPossession(self.team2, self.team1, boxScore=2, passBonus=playerOneOffense[1], sim=is_sim, usr=is_usr)
                            if passResult > 0 and offBoardMan != myCheck:
                                ball_passed = False
                                pass_assist[0] = True
                                pass_assist[1] = self.score
                                if not sim:
                                    time.sleep(0.75)
                                    print(offBoardMan.name + ' gets the assist!')

                                box[offBoardMan.name][3]['assists'] += 1

                                self.score = passResult
                                passResult = 0
                                
                        self.score += result[0]
                            
# --------------------------------------------------------------------------------------------------------------


                elif playerTwoMove == 'insideDefense' or playerTwoMove == 'perimeterDefense':
                    if not sim:
                        miss()
                        lines = reb_dict[playerOneMove][0]
                        if playerOneMove == 'shootInside':
                            print(random.choice(lines) + playerTwo.name + '!\n')
                        else:
                            print(random.choice(lines) + '\n')
                            
                    if playerOneMove == 'shoot3':
                        box[playerOne.name][8]['3PA'] += 1
                    box[playerOne.name][6]['FGA'] += 1
                    self.ass_dict[playerTwo.name][1] += 1

                    defBoard, offBoard = self.getRebounder(teamTwo, 1), self.getRebounder(teamOne, 2)
                    defBoardMan, offBoardMan = defBoard[0], offBoard[0]
                    defBoardManRating, offBoardManRating = defBoard[1], offBoard[1]
                    if defBoardManRating >= offBoardManRating:
                        if not sim:
                            time.sleep(1.5)
                            print(defBoardMan.name + ' grabs the rebound for ' + teamTwo.name + '...')
                        passResult = 0
                        pass_count = 0
                        if defBoardMan in self.team2.lineup:
                            self.team2boxScore[defBoardMan.name][1]['rebounds'] += 1
                        else:
                            self.team1boxScore[defBoardMan.name][1]['rebounds'] += 1
                        if not sim:
                            time.sleep(0.5)
                        return 0
                    else:
                        if not sim:
                            time.sleep(1.5)
                            print('Offensive Rebound by ' + offBoardMan.name + '!')
                            time.sleep(1)
                        ball_passed = False
                        pass_count = 3
                        if offBoardMan in self.team1.lineup:
                            self.team1boxScore[offBoardMan.name][1]['rebounds'] += 1
                            self.score = self.playPossession(self.team1, self.team2, boxScore=1, passBonus=playerOneOffense[1], sim=is_sim, usr=is_usr)
                        else:
                            self.team2boxScore[offBoardMan.name][1]['rebounds'] += 1
                            self.score = self.playPossession(self.team2, self.team1, boxScore=2, passBonus=playerOneOffense[1], sim=is_sim, usr=is_usr)
                        if passResult > 0 and offBoardMan != myCheck:
                            ball_passed = False
                            pass_assist[0] = True
                            pass_assist[1] = self.score
                            if not sim:
                                time.sleep(0.75)
                                print(offBoardMan.name + ' gets the assist!')

                            box[offBoardMan.name][3]['assists'] += 1

                            self.score = passResult
                            passResult = 0

                elif playerTwoMove == 'block':
                    if not sim:
                        miss()
                        print(random.choice(linesBlock) + playerTwo.name + '!\n')
                        time.sleep(1)
                    if boxScore == 1:
                        self.team2boxScore[playerTwo.name][4]['blocks'] += 1
                    else:
                        self.team1boxScore[playerTwo.name][4]['blocks'] += 1
                    box[playerOne.name][6]['FGA'] += 1
                    self.ass_dict[playerTwo.name][1] += 1

                    if playerTwo in self.team2.lineup:
                        if not sim:
                            print(self.team1.name + ' inbound the ball...')
                            time.sleep(1)
                        self.score = self.playPossession(self.team1, self.team2, boxScore=1, sim=is_sim, usr=is_usr)
                    else:
                        if not sim:
                            print(self.team2.name + ' inbound the ball...')
                            time.sleep(1)
                        self.score = self.playPossession(self.team2, self.team1, boxScore=2, sim=is_sim, usr=is_usr)
                
                elif playerTwoMove == 'steal':
                    self.score = 0
                    if boxScore == 1:
                        self.team2boxScore[playerTwo.name][3]['steals'] += 1
                    else:
                        self.team1boxScore[playerTwo.name][3]['steals'] += 1
                    if not sim:
                        miss()
                        print('It\'s tipped by ' + playerTwo.name + '!')
                    teamOne.turnovers += 1
#                     turn = True

            points = self.score
            self.score = 0
            
            if ball_passed:
                passResult = points
            
            ball_passed = False
            
            if playerOneMove != 'pass':
                heat_ply = playerOne
                pass_count = 0
                pass_assist[0] = False
            
#             if pass_assist[0]:
#                 points = pass_assist[1]

            if playerTwoRating >= playerOneRating:
                if playerTwoMove == 'shoot2foul' or playerTwoMove == 'shoot3foul':
                    passResult = 0
                    return points
            
#             self.pair = (playerOne, playerTwo, playerTwoMove, turn)
            return points
    
    def pointsReturn(self, i, is_sim=False, user=0):
        try:
            global heat_ply
            if not is_sim:
                print('\n\n\n*************************')
                print(self.team2.name + ' ' + str(self.team2score) + ' - ' + str(self.team1score) + ' ' + self.team1.name)
                print('*************************\n')
                time.sleep(1.5)
            self.setMatchups(self.team1, self.team2, crunch=(i>=90))
            user = usr_dict[1][user]
            result = self.playPossession(self.team1, self.team2, boxScore=1, crunchTime=(i>=90), sim=is_sim, usr=user)
            self.team1score += result
            self.heatCheck(result, heat_ply, self.team1, 3)
            self.matchups.clear()
            if not is_sim:
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~')
                time.sleep(0.75)
            self.setMatchups(self.team2, self.team1, crunch=(i>=90))
            user = usr_dict[2][user]
            result = self.playPossession(self.team2, self.team1, boxScore=2, crunchTime=(i>=90), sim=is_sim, usr=user)
            self.team2score += result
            self.heatCheck(result, heat_ply, self.team2, 3)
            self.matchups.clear()
            if not is_sim:
                print('\n~~~~~~~~~~~~~~~~~~~~~~~~~')
                time.sleep(1.5)
    #         print(str(i))
#             self.momentum()
        except KeyboardInterrupt:
            quit()
    
    def commentary(self, j):
        print(qtr_dict[j][0])
        time.sleep(1)
        print(qtr_dict[j][1])
        print(self.team1.name + ': ' + str(self.team1score) + ' points\n' + self.team2.name + ': ' + str(self.team2score) + ' points\n')
        while True:
            if input() == '':
                break 
        
    def skip(self, i):
        pass
    
    def shotStats(self, team):
        box = self.team2boxScore.values() if team == self.team1 else self.team1boxScore.values()
        makes = []
        attempts = []
        for r in box:
            makes.append(r[5]['FGM'])
            attempts.append(r[6]['FGA'])
        makes = sum(makes)
        attempts = sum(attempts)
        print((team.name.upper() + ':').ljust(25) + str(makes).ljust(5) + str(attempts).ljust(5) + '(%)')
        for ply in team.roster:
            record = self.ass_dict[ply.name]
            percent = my_precision(record[1]*100/attempts, 1)
            print(ply.name.ljust(25) + str(record[0]).ljust(5) + str(record[1]).ljust(5) + ('(' + str(percent) + ')').ljust(5))

    def runGame(self):
        global counter
        counter = 0
        self.resetGame()
        try:
            print('Welcome to tonight\'s game...')
            time.sleep(2)
            print('...and it\'s ' + self.team2.name + ' @ ' + self.team1.name + '\n')
            time.sleep(2)
            print('Here are the lineups: ')
            time.sleep(2)
            self.team1.getLineup()
            self.team2.getLineup()
            print('\npress \'Enter\' to begin!')
            while True:
                if input() == '':
                    for i in range(100):
                        counter = i
                        if i in sub_dict.keys():
                            print('And ' + self.team1.name + ' making some personnel changes here...')
                            print('And ' + self.team2.name + ' making some personnel changes here...')
                            for sub in sub_dict[i]:
                                p_out = [self.team1.roster[sub[0]-1], self.team2.roster[sub[0]-1]]
                                p_in  = [self.team1.roster[sub[1]-1], self.team2.roster[sub[1]-1]]
#                                 heat_dict[p_out[0].name] = ['neutral', 0]
#                                 heat_dict[p_out[1].name] = ['neutral', 0]
                                self.team1.substitute(p_out[0], p_in[0])
                                self.team2.substitute(p_out[1], p_in[1])
                        if i in qtr_dict.keys():
                            self.commentary(i)                   
                        self.pointsReturn(i)
                    if self.team1score == self.team2score:
                        self.commentary(100)
                        self.leave = False
                        while not self.leave:
                            for i in range(10):
                                self.pointsReturn(i)
                            if self.team1score != self.team2score:
                                self.leave = True
                    time.sleep(1)
                    print('\nFinal Score: ' + self.team2.name + ' ' + str(self.team2score) + ' - ' + str(self.team1score) + ' ' + self.team1.name, end='')
                    if self.leave:
                        print(' (OT)\n')
                    else:
                        print('\n')
#                     loadTeam(self.team1)
#                     loadTeam(self.team2)
                    break
                else:
                    continue
        except KeyboardInterrupt:
            for i in range(100-counter):
                if i in sub_dict.keys():
                    for sub in sub_dict[i]:
                        p_out = [self.team1.roster[sub[0]-1], self.team2.roster[sub[0]-1]]
                        p_in  = [self.team1.roster[sub[1]-1], self.team2.roster[sub[1]-1]]
                        heat_dict[p_out[0].name] = ['neutral', 0]
                        heat_dict[p_out[1].name] = ['neutral', 0]
                        self.team1.substitute(p_out[0], p_in[0], sim=True)
                        self.team2.substitute(p_out[1], p_in[1], sim=True)
                self.pointsReturn(i, is_sim=True)
            print('\nFinal Score: ' + self.team2.name + ' ' + str(self.team2score) + ' - '
                  + str(self.team1score) + ' ' + self.team1.name, end='')

    def simGame(self, is_print=False):
        global heat_dict, heat_ply
        self.resetGame()
#         print(self.team2.name + ' @ ' + self.team1.name)
#         print('\npress \'Enter\' to begin!')
#         while input() != '':
#             continue
        for i in range(100):
            if i in sub_dict.keys():
                for sub in sub_dict[i]:
                    b_set = {self.team1.bestPlayer(True), self.team1.secondOption(True),
                             self.team2.bestPlayer(True), self.team2.secondOption(True)}
                    p_out = [self.team1.roster[sub[0]-1], self.team2.roster[sub[0]-1]]
                    p_in  = [self.team1.roster[sub[1]-1], self.team2.roster[sub[1]-1]]
                    if p_out[0] in self.team1.roster[:5] or p_out[0] in b_set:
                        heat_dict[p_out[0].name] = ['neutral', 0]
                    if p_out[1] in self.team2.roster[:5] or p_out[1] in b_set:
                        heat_dict[p_out[1].name] = ['neutral', 0]
                    self.team1.substitute(p_out[0], p_in[0], sim=True)
                    self.team2.substitute(p_out[1], p_in[1], sim=True)
            self.pointsReturn(i, is_sim=True)
        if self.team1score == self.team2score:
            self.leave = False
            while not self.leave:
                for i in range(10):
                    self.pointsReturn(i, is_sim=True)
                if self.team1score != self.team2score:
                    self.leave = True
        if is_print:
            print('\nFinal Score: ' + self.team2.name + ' ' + str(self.team2score) + ' - ' + str(self.team1score) + ' ' + self.team1.name, end='')
        if self.leave and is_print:
            print(' (OT)\n')
        elif is_print:
            print('\n')
#         loadTeam(self.team1)
#         loadTeam(self.team2)

g = None
def demo(x, y):
    global g
    game = Game(makeTeam(x), makeTeam(y))
    game.resetGame()
    game.fixture()
    saveTeam(game.team1)
    saveTeam(game.team2)
    print('Pick team to control:')
    time.sleep(1)
    choice_dict = {0: 'neither team', 1: game.team1.name, 2: game.team2.name}
    print('1 for ' + game.team1.name)
    print('2 for ' + game.team2.name + '\n')
    time.sleep(1)
    while True:
        usr = str(input())
        if usr.lower() in {'0', '1', '2'}:
            break
        else:
            usr = ''
    print('You are controlling ' + choice_dict[int(usr)])
    loop()
    g = game
    for i in range(5):
        game.pointsReturn(i, user=int(usr))
    mixer.music.stop()
    return None

def gee():
    g = Game()
    return g

def loo(g, n=3):
    for i in range(n):
        g.simGame()
#         g.teamStats()
#         g.boxScore()
        print()
        g.shotStats(g.team1)
        print()
        g.shotStats(g.team2)