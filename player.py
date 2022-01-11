from config import *

class Record():
    def __init__(self, points=[0, None], rebounds=[0, None], assists=[0, None], steals=[0, None], blocks=[0, None],
                 fgm=[0, None], fga=[0, None], threes_m=[0, None], threes_a=[0, None], ftm=[0, None], fta=[0, None]):
        self.points = points
        self.rebounds = rebounds
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.fgm = fgm
        self.fga = fga
        self.threes_m = threes_m
        self.threes_a = threes_a
        self.ftm = ftm
        self.fta = fta

class Player(Record):
    def __init__(self, name, insideShot, midRange, threePoint, passing, onBallDefense, insideDefense, steal, block, offRebound, defRebound, freeThrow):
        super().__init__()
        self.name = name
        self.insideShot = insideShot
        self.midRange = midRange
        self.threePoint = threePoint
        self.passing = passing
        self.onBallDefense = onBallDefense
        self.insideDefense = insideDefense
        self.steal = steal
        self.block = block
        self.offRebound = offRebound
        self.defRebound = defRebound
        self.freeThrow = freeThrow

    def overall(self, off=False, deff=False):  # haven't specified the weights for 'midRange' attribute
        result = 0
        build = self.getBuild()
        index_list = []
        if off and not deff:
            attr_list = list(self.__dict__.values())[11:][1:][:4] + [self.freeThrow]
            index_list = [0, 1, 2, 3, 10]
        elif deff and not off:
            attr_list = list(self.__dict__.values())[11:][1:][4:-1]
            index_list = [4, 5, 6, 7, 8, 9]
        else:
            attr_list = list(self.__dict__.values())[11:][1:]
            index_list = [x for x in range(11)]
        if build == 'guard':
            weights = g_weights
        elif build == 'forward':
            weights = f_weights
        else:
            weights = b_weights
        for attr in range(len(attr_list)):
            result += ((attr_list[attr]/100) * weights[index_list[attr]])
        result = int(result*100/sum([weights[i] for i in index_list]))
        return result

    def bestAttribute(self, d=False, best=False, point=False, heat='neutral', crunchTime=False):
        result = 0
        if d:
            attr_list = list(self.__dict__.values())[11:][5:-3]
        else:
            attr_list = list(self.__dict__.values())[11:][1:5]
        
        if point:
            attr_list = list(self.__dict__.values())[11:][1:4]
        
        index = attr_list.index(max(attr_list)) + 1
        result = attr_dict[action_dict[index]]

        return result

    def getBuild(self):
        if self.offRebound == 55:
            return 'guard'
        elif self.offRebound == 75:
            return 'forward'
        else:
            return 'big'

    def getOffensiveRating(self, move, passed, l_bound=0, u_bound=1, heat=''):
        rating_max = self.__dict__[attr_dict[move]]
        if move == 'shoot3' and heat == 'hot':
            l_bound = 1.5 * l_bound
            u_bound = 1.5 * u_bound
        rating = random.randint(int(l_bound*rating_max), int(u_bound*rating_max))
        return (move, rating)

    def getOffensiveMoveAndRating(self, team, passed, l_bound=0, u_bound=1, heat='', drivekick=False, b_passer=False, crunch=False):
        is_best = team.bestPlayer()==self
        tendency = PlayerTendency(ply=self, first_option=is_best, second_option=team.secondOption()==self, best_attr=self.bestAttribute(), ball_passed=passed, best_passer=b_passer)
        action = tendency.getOffensiveAction()        
        if action == 'shoot3' and heat == 'hot':
            l_bound = 1.5 * l_bound
            u_bound = 1.5 * u_bound
        
        if action == 'shootInside':
            randomRating = random.randint(int(l_bound*self.insideShot), int(u_bound*self.insideShot))
            return ('shootInside', randomRating)
        
        elif action == 'shootMid':
            randomRating = random.randint(int(l_bound*self.midRange), int(u_bound*self.midRange))
            return ('shootMid', randomRating)
        
        elif action == 'shoot3':
            randomRating = random.randint(int(l_bound*self.threePoint), int(u_bound*self.threePoint))
            return ('shoot3', randomRating)
        
        else:
#             if heat == 'cold':
            l_bound = 0
            u_bound = 1
            randomRating = random.randint(int(l_bound*self.passing), int(u_bound*self.passing))
            return ('pass', randomRating)

    def getDefensiveMoveAndRating(self, offensiveMove, heat='', pass_rank=0):
        tendency = PlayerTendency(ply=self, best_attr=self.bestAttribute(), move=offensiveMove, heat_check=heat)
        action = tendency.getDefensiveAction()
        x = random.randint(1, 100)
        ins_dict = {True: 'block', False: 'insideDefense'}
        if offensiveMove == 'shootInside':
            if action == 'foul':
                randomRating = random.randint(0, 100)
                return ('shoot2foul', randomRating)
            else:
                if action == 'block':
                    randomRating = random.randint(0, self.block)
                    return ('block', randomRating)
                else:
                    randomRating = random.randint(0, self.insideDefense)
                    return ('insideDefense', randomRating)
        elif offensiveMove == 'shootMid':
            if action == 'normalDefense':
                randomRating = random.randint(0, self.onBallDefense)
                return ('perimeterDefense', randomRating)
            elif action == 'foul':
                randomRating = random.randint(0, 100)
                return ('shoot2foul', randomRating)
            else:
                randomRating = random.randint(0, self.onBallDefense)
                return ('perimeterDefense', randomRating)
        elif offensiveMove == 'shoot3':
            if action == 'normalDefense':
                randomRating = random.randint(0, self.onBallDefense)
                return ('perimeterDefense', randomRating)
            elif action == 'foul':
                randomRating = random.randint(0, 100)
                return ('shoot3foul', randomRating)
            else:
                randomRating = random.randint(0, self.onBallDefense)
                return ('perimeterDefense', randomRating)
        elif offensiveMove == 'pass':
#             beta = 0.33 if pass_rank < 0.60 else 0.12
#             beta = 0.25 if pass_rank < 0.75 else 0.12
            beta = 0.32 if pass_rank < 0.60 else 0.11
            randomRating = random.randint(0, int(self.steal*beta))
            return ('steal', randomRating)

class PlayerTendency():
    def __init__(self, ply=None, first_option=False, second_option=False,
                 best_attr=None, move=None, ball_passed=False, heat_check='', best_passer=False, drive_kick=False,
                 insideShotTendency=range(100), midRangeTendency=range(100), threeTendency=range(100),
                 passTendency=range(100), stealTendency=range(100), blockTendency=range(100), foulTendency=range(100)):
        self.move = move
        self.heat_check = heat_check
        self.ply = ply
        blk_rating = int(ply.block/100)
        op_code = bool_to_int(first_option, second_option)
        attrs = option_dict[op_code][0][best_attr] if op_code == '00' else option_dict[op_code][0][best_attr][ball_passed]
        
        self.insideShotTendency = range(*attrs[0])
        self.midRangeTendency = range(*attrs[1])
        self.threeTendency = range(*attrs[2])
        self.passTendency = range(0, 100)
        self.stealTendency = range(50, 50)
        if best_attr == 'passing' and op_code != '00':
            pass
#             x, y = option_dict[op_code][1], option_dict[op_code][2]
#             if best_passer and op_code == '01':
#                 self.adjustTendency(x, y)
#             elif op_code == '10':
#                 self.adjustTendency(x, y)
        elif best_passer and op_code == '00':
            role_attrs = role_dict['passing'] if best_attr == 'passing' else role_dict[ply.bestAttribute(point=True)]
            self.insideShotTendency = range(*role_attrs[0])
            self.midRangeTendency = range(*role_attrs[1])
            self.threeTendency = range(*role_attrs[2])

        if ply.block < 60:
            self.blockTendency = range(45, 55)
        else:
            if ply.block >= 75:
                self.blockTendency = block_dict[blk_rating-1]
            elif ply.bestAttribute(d=True) == 'block':
                self.blockTendency = block_dict[blk_rating-1]
            else:
                self.blockTendency = block_dict[blk_rating-7]
                
        self.foulTendency = range(min(self.blockTendency)-5, max(self.blockTendency)+6)
        
#         if drive_kick:
#             for i in attr_list:
#                 attr = i[:-8][:3]
#                 if i == best_attr[:3]:
#                     self.__dict__[i] = range(min(self.__dict__[i])-5, max(self.__dict__[i])+6)
#                 else:
#                     self.__dict__[i] = range(min(self.__dict__[i])-2, max(self.__dict__[i])+3)
        
        if self.heat_check in {'hot'}:
            self.foulTendency = range(self.foulTendency[0]-5, self.foulTendency[-1]+2)
        elif self.move == 'shootInside':
            self.foulTendency = range(self.foulTendency[0]-5, self.foulTendency[-1]+6)
        else:
            self.foulTendency = range(self.foulTendency[0]+5, self.foulTendency[-1])

    def getOffensiveAction(self):
        randomNum = random.randint(0, 100)
        if randomNum in self.insideShotTendency:
            return 'shootInside'
        elif randomNum in self.midRangeTendency:
            return 'shootMid'
        elif randomNum in self.threeTendency:
            return 'shoot3'
        else:
            return 'pass'

    def getDefensiveAction(self):
        randomNum = random.randint(0, 100)
        if randomNum in self.blockTendency:
            return 'block'
        elif randomNum in self.stealTendency:
            return 'steal'
        elif randomNum in self.foulTendency:
            return 'foul'
        else:
            return 'normalDefense'

    def adjustTendency(self, x, y):
        attr_list = ['insideShotTendency', 'midRangeTendency', 'threeTendency']
        for i in attr_list:
            attr = i[:-8][:3]
            if attr == self.ply.bestAttribute(point=True)[:3]:
                self.__dict__[i] = range(min(self.__dict__[i]), max(self.__dict__[i])+x)
            else:
                self.__dict__[i] = range(min(self.__dict__[i]), max(self.__dict__[i])+y)
    
def editHeat(ply, heat):
    pass

def createPlayer(pos, grade):
    name = names.get_full_name(gender='male')
    values = []
    if pos == 'guard':
        ranges = g_ranges
    elif pos == 'forward':
        ranges = f_ranges
    elif pos == 'big':
        ranges = b_ranges
    for i in range(11):
        value = random.randint(*ranges[grade][i])
        values.append(value)
    return Player(name, *values)

def makePlayer(build):
    playerName = names.get_full_name(gender='male')
    if build.lower() == 'guard':
        insideShot = random.randint(50, 65)
        midRange = random.randint(50, 80)
        threePoint = random.randint(50, 65)
        passing = random.randint(65, 75)
        onBallDefense = random.randint(60, 70)
        insideDefense = random.randint(50, 55)
        steal = random.randint(60, 70)
        block = random.randint(30, 50)
        offRebound = random.randint(55, 55)
        defRebound = random.randint(55, 75)
        freeThrow = random.randint(60, 75)
    elif build.lower() == 'forward':
        insideShot = random.randint(60, 70)
        midRange = random.randint(50, 80)
        threePoint = random.randint(50, 65)
        passing = random.randint(40, 60)
        onBallDefense = random.randint(60, 65)
        insideDefense = random.randint(50, 60)
        steal = random.randint(60, 65)
        block = random.randint(50, 55)
        offRebound = random.randint(75, 75)
        defRebound = random.randint(70, 75)
        freeThrow = random.randint(60, 70)
    elif build.lower() == 'big':
        insideShot = random.randint(60, 65)
        midRange = random.randint(40, 75)
        threePoint = random.randint(30, 45)
        passing = random.randint(30, 45)
        onBallDefense = random.randint(30, 40)
        insideDefense = random.randint(65, 75)
        steal = random.randint(30, 40)
        block = random.randint(60, 70)
        offRebound = random.randint(85, 85)
        defRebound = random.randint(75, 80)
        freeThrow = random.randint(30, 55)

    return Player(playerName, insideShot, midRange, threePoint, passing, onBallDefense, insideDefense, steal, block, offRebound, defRebound, freeThrow)

def checkPlayer(player):
    for i in list(player.__dict__.items())[11:]:
        attr, value = i[0], i[1]
        if attr == 'name':
            continue
        elif attr == 'freeThrow':
            continue
        elif attr == 'offRebound':
            continue
        elif attr == 'defRebound':
            continue
        else:
            if value > 100:
                value = 99
                #print('!')
            elif value < 20:
                value = 20
#                 print('!')

def ovrRange(pos, grade):
    my_min = my_max = 0
    values_min = []
    values_max = []
    name = names.get_full_name(gender='male')
    if pos == 'guard':
        ranges = g_ranges
    elif pos == 'forward':
        ranges = f_ranges
    elif pos == 'big':
        ranges = b_ranges
    for i in range(11):
        value_min = min(*ranges[grade][i])
        value_max = max(*ranges[grade][i])
        values_min.append(value_min)
        values_max.append(value_max)
#     print(values_min)
    player_min = Player(name, *values_min)
    player_max = Player(name, *values_max)
    my_min, my_max = player_min.overall(), player_max.overall()

    return (my_min, my_max)

def allRanges():
    for b in new_builds:
        print(b.upper())
        for g in build_grades:
            print(g + ': ', end='')
            print(ovrRange(b, g))
        print()

# print('big A: ', ovrRange('big', 'A'))
# print('big B: ', ovrRange('big', 'B'))
# print('big C: ', ovrRange('big', 'C'))
# print('big D: ', ovrRange('big', 'D'))