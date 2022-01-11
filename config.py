import names, random, time, copy, math, csv, simpleaudio as sa, pickle, statistics

# you dont get an assist for rebounding and then passing to the scorer (yet!) - DONE
# successful 'block' plays are not mentioned in commentary - DONE
# rebounds have not yet been added to the stat sheet / box score - DONE

# 3 bench players (guard, wing, and big) have not been inserted in the 'team' roster - DONE
# bench players have not found their minutes and rotation implemented in the 'runGame()' method... - DONE
# ...took a screenshot of a rotation scheme, will implement it tomorrow - DONE

# *TIME* : find a way to make each quarter (25 possessions) '12 minutes'

# *SIM* : make a 'sim possession' method so you can quickly get to the results of games - DONE


# fix heat_dict '3' (Game) - DONE
# fix blocks so that better blockers average higher blocks (Player) - DONE
# add block mechanic to heatCheck (Game)
# get more offensive rebounds, especially from big men - DONE

# *** NEW ***
# get better (best) defensive matchups (Game)
# sub in a bench player (to start) if he is better than a starter on the same position
# have more mercy on 3-pointer efficiency(?)
# figure out teams with 0 all-stars

builds = ['facilitator', '3 and d', 'scoring wing', 'stretch big', 'glass cleaner', 'bench guard', 'bench wing', 'bench big']
new_builds = ['guard', 'forward', 'big']
build_dict = {'guard': [1, 2, 6], 'forward': [3, 4, 7, 8], 'big': [5, 9]}
build_grades = ['A', 'B', 'C', 'D']
sub_dict = {12: [(2, 3), (3, 7), (4, 8)], 18: [(1, 6), (3, 2), (5, 9)],
            25: [(6, 1), (2, 6), (7, 3), (8, 4)], 33: [(6, 2), (3, 7), (9, 5)], 43: [(1, 2), (2, 6), (7, 3), (4, 8)],
            50: [(2, 1), (6, 2), (3, 4), (8, 7)], 58: [(2, 6), (4, 3), (7, 4), (5, 9)], 68: [(1, 2), (4, 8), (9, 5)],
            75: [(2, 6), (6, 2), (3, 7), (5, 9)], 81: [(2, 3), (8, 4), (9, 5)], 87: [(6, 1), (3, 2), (7, 3)]}

# yet to implement 'crunch time' - once i >= 90 (sub_dict above), majority of the time ball goes to team's first option - DONE!

g_weights = [0.15, 0.1, 0.15, 0.15, 0.15, 0.05, 0.1, 0, 0, 0.05, 0.1] # all midRange weights are still 0 - DONE!
f_weights = [0.20, 0.15, 0.15, 0.05, 0.05, 0.1, 0.05, 0.05, 0.05, 0.1, 0.05]
b_weights = [0.25, 0.1, 0.05, 0.05, 0, 0.15, 0, 0.15, 0.1, 0.1, 0.05]

MAX = 99
g_ranges = {'A': [(85, 95), (75, MAX), (80, MAX), (85, MAX), (75, MAX), (45, 65), (80, MAX), (40, 65), (55, 55), (70, 85), (85, MAX)],
            'B': [(65, 80), (60, 80), (70, 85), (75, 85), (75, 85), (60, 65), (70, 75), (50, 65), (55, 55), (65, 85), (75, 85)],
            'C': [(60, 65), (60, 65), (65, 80), (70, 80), (75, 80), (55, 60), (60, 70), (45, 55), (55, 55), (60, 80), (70, 80)],
            'D': [(55, 60), (55, 65), (60, 70), (65, 75), (65, 75), (50, 55), (55, 60), (40, 50), (55, 55), (60, 75), (70, 75)]}

f_ranges = {'A': [(90, MAX), (85, MAX), (80, 95), (70, 85), (75, 95), (75, 90), (70, 90), (75, 95), (75, 75), (80, 95), (80, MAX)],
            'B': [(75, 85), (70, 85), (70, 85), (60, 70), (65, 80), (70, 85), (65, 75), (65, 85), (75, 75), (75, 80), (75, 80)],
            'C': [(70, 75), (65, 70), (65, 80), (50, 60), (65, 75), (60, 65), (50, 60), (60, 70), (75, 75), (70, 75), (65, 70)],
            'D': [(65, 70), (55, 65), (55, 65), (45, 60), (65, 70), (55, 60), (50, 50), (55, 65), (75, 75), (65, 70), (60, 65)]}

b_ranges = {'A': [(85, MAX), (65, MAX), (65, 90), (65, 85), (40, 60), (85, MAX), (30, 55), (80, MAX), (85, 85), (90, MAX), (70, 90)],
            'B': [(70, 80), (60, 80), (50, 65), (55, 65), (45, 55), (75, 85), (45, 55), (70, 85), (85, 85), (80, 90), (55, 70)],
            'C': [(65, 70), (55, 60), (45, 50), (45, 50), (40, 55), (70, 80), (40, 50), (65, 75), (80, 80), (75, 85), (50, 55)],
            'D': [(60, 65), (55, 65), (30, 35), (30, 35), (40, 40), (65, 70), (40, 45), (60, 75), (80, 80), (75, 80), (35, 45)]}


foption_dict = {'threePoint': {True:  [(0, 25), (35, 50), (60, 90)], False: [(0, 20), (40, 50), (70, 90)]},
                'midRange':   {True:  [(0, 15), (25, 60), (70, 90)], False: [(0, 15), (35, 60), (80, 90)]},
                'insideShot': {True:  [(0, 45), (55, 65), (75, 90)], False: [(0, 35), (55, 60), (80, 90)]},
                'passing':    {True:  [(0, 20), (40, 50), (70, 90)], False: [(0, 15), (40, 45), (70, 80)]}}

soption_dict = {'threePoint': {True:  [(0, 25), (35, 45), (55, 85)], False: [(0, 15), (35, 40), (60, 80)]},
                'midRange':   {True:  [(0, 15), (25, 60), (70, 85)], False: [(0, 5),  (25, 50), (70, 80)]},
                'insideShot': {True:  [(0, 45), (55, 60), (70, 85)], False: [(0, 30), (50, 55), (75, 80)]},
                'passing':    {True:  [(0, 15), (40, 50), (75, 90)], False: [(0, 10), (40, 45), (75, 80)]}}

tendency_dict = {'threePoint': [(0, 15), (35, 40), (60, 90)],
                 'midRange':   [(0, 10), (25, 55), (70, 85)],
                 'insideShot': [(0, 40), (55, 60), (75, 85)],
                 'passing':    [(0, 15), (40, 50), (75, 90)],}


role_dict = {'threePoint': [(0, 5),  (30, 33), (65, 75)],
             'midRange':   [(0, 5),  (30, 45), (70, 75)],
             'insideShot': [(0, 15), (40, 45), (70, 75)],
             'passing':    [(0, 10), (35, 40), (65, 75)],}

option_dict = {'10': [foption_dict, 7, 2], '01': [soption_dict, 7, 2], '00': [tendency_dict, 0, 0]}

matchup_dict = {'insideShot': (6, 8), 'midRange': (5, 5), 'threePoint': (5, 5), 'passing': (7, 5),
                'guard': [0, 1], 'forward': [2, 3], 'big': [4, 4]}

attr_list = ['name', 'insideShot', 'midRange', 'threePoint', 'passing',
             'onBallDefense', 'insideDefense', 'steal', 'block',
             'offRebound', 'defRebound', 'freeThrow']

attr_dict = {'insideShot': 'shootInside', 'midRange': 'shootMid', 'threePoint': 'shoot3', 'passing': 'pass',
             'shootInside': 'insideShot', 'shootMid': 'midRange', 'shoot3': 'threePoint', 'pass': 'passing',
             'perimeterDefense': 'onBallDefense', 'insideDefense': 'insideDefense', 'block': 'block'}

action_dict = {1: 'shootInside', 2: 'shootMid', 3: 'shoot3', 4: 'pass'}

crunch_dicts = [{True:[(0, 30), (65, 90)], False: [(0, 9), (40, 80)]}, # 0 all-stars
               {True: [(0, 35), (60, 90)], False: [(0, 9), (40, 80)]}, # 1 all-star
               {True: [(0, 30), (65, 90)], False: [(0, 9), (40, 80)]}] # 2 all-stars

hold_dict = {True:  {'guard': (0.85, 0.90), 'forward': (0.85, 0.95), 'big': (1.05, 1.10)},   # ball passed
             False: {'guard': (1.05, 1.10), 'forward': (1.05, 1.15), 'big': (1.20, 1.25)}}   # ball not passed

twos_dict = {True:  (1.00, 1.05),     # ball passed
             False: (1.15, 1.20)}     # ball not passed

allstars_dict = {0: (35, 75), 1: (40, 60), 2: (45, 55)}

qtr_dict = {25: ['It\'s the end of the 1st Quarter!', '\nQ1 Score: '],
            50: ['It\'s half-time! 2nd Quarter draws to a close', '\n1st Half Score:'],
            75: ['It\'s the end of the 3rd!', '\nQ3 Score: '],
            100: ['We\'re going to overtime!', '\nQ4 Score: ']}

rhythm_dict = {'hot':     {'A': (1.50, 1.75), 'B': (1.50, 1.75), 'C': (1.50, 2.00)},
               'neutral': {'A': (0.00, 1.00), 'B': (0.00, 1.00), 'C': (0.00, 1.00)},
               'cold':    {'A': (0.00, 0.10), 'B': (0.00, 0.15), 'C': (0.00, 0.15)}}

stat_dict = {0: 'points', 1: 'rebounds', 2: 'assists', 3: 'steals', 4: 'blocks',
             5: 'fgm', 6: 'fga', 7: 'threes_m', 8: 'threes_a', 9: 'ftm', 10: 'fta',
             'points': 0, 'rebounds': 1, 'assists': 2, 'steals': 3, 'blocks': 4,
             'FGM': 5, 'FGA': 6, '3PM': 7, '3PA': 8, 'FTM': 9, 'FTA': 10}

abbv_dict = {0: 'PTS: ', 1: ' REB: ', 2: ' AST: ', 3: ' STL: ', 4: ' BLK: ',
             5: ' FGM: ', 6: ' FGA: ', 7: ' 3PM: ', 8: ' 3PA: ', 9: ' FTM: ', 10: ' FTA: '}

boxstat_dict = {0: ['points', ' pts, '], 1: ['rebounds', ' reb, '], 2: ['assists', ' ast, '],
                3: ['steals', ' stl, '], 4: ['blocks', ' blk, '],
                5: ['FGM', ' FG, '], 6: ['FGA'], 7: ['3PM', ' 3PT, '], 8: ['3PA'], 9: ['FTM', ' FT'], 10: ['FTA']}

foul_dict = {'shoot2foul': [2, ' will go to the free throw line for 2...'],
             'shoot3foul': [3, ' will take 3 free throws...']}


lines2 = ['...and he lays it in!!', '...it\'s in for 2!!', '...and it\'s good!!', '...the layup\'s good!!', '...he gets the layup!!']
linesMid = ['...butter!!', '...jumper\'s good!!', '...and he hits it from mid range!!', '...and he banks in the jumpshot!!', '...mid-range bucket!!']
lines3 = ['...and he drills the 3!!!', '...BANG!!!', '...drills it from deep!!!', '...and it\'s in from beyond the arc!!!', '...hits it from downtown!!!']

linesShoot3 = [' from long range...', ' pulls up for 3...', ' from downtown...', ' for 3...', ' shoots it from distance...']
linesMiss3 = ['...it\'s no good', '...doesn\'t go', '...it\'s short', '...can\'t get it to fall', '...he misses the 3']

linesInsideD = ['...missed shot, good defense from ', '...inside shot is short, great D from ', '...but it\'s no good, great contest by ', '...his shot doesn\'t go. Good D by ']
linesBlock = ['...and it\'s REJECTED by ', '...the shot is BLOCKED by ', '...but his shot is BLOCKED by ']

linesFtGood = ['...he knocks it down!', '...he gets it to fall!', '...he makes the free throw!', '...and the free throw is good!']
linesFtBad = ['...can\'t get it to fall', '...he misses the free throw', '...it\'s short', '...the free throw won\'t go']

reb_dict = {'shootInside': [linesInsideD, ' grabs the rebound for '],
            'shootMid': [linesMiss3[:-1], ' gets the rebound for '],
            'shoot3': [linesMiss3, ' with the rebound for '],
            'guard': 1.0, 'forward': 1.01, 'big': 1.03}

make_dict = {'shootInside': [2, lines2, ' at the line to complete the three-point play...'],
             'shootMid': [2, linesMid, ' at the line to complete the three-point play...'],
             'shoot3': [3, lines3, ' heads to the line to complete the four-point play...']}

usr_dict = {1: {0: 0, 1: 1, 2: 0},
            2: {0: 0, 1: 0, 2: 2}}

percent_dict = {'fg':  [9.5, (5, 6), 'insideShot', 'midRange'],
                '3p':  [4.0, (7, 8), 'threePoint'],
                'ft':  [3.5, (9, 10), 'freeThrow']}

block_dict = {x: range(30-5*int((x-1)/2 + 0.5), 70+5*int(x/2 + 0.5)) for x in range(-8, 11)}

team_dict = {0: (20, 80), 1: (40, 60), 2: (45, 55)}

eat_dict = {0: [(18, 20), (15, 17), (11, 13), (9, 11), (7, 9), (10, 12), (5, 7), (4, 5), (3, 5)],
            1: [(19, 21), (15, 17), (10, 12), (9, 11), (6, 8), (9, 11), (5, 7), (4, 5), (3, 4)],
            2: [(18, 20), (15, 17), (11, 13), (9, 11), (7, 9), (10, 12), (5, 7), (4, 5), (3, 5)]}

fun_dict = {'min': [1.06, 14, 102],
            'max': [1.05, 21, 106],
            't_min': [1.09, 5, 107],
            't_max': [1.06, 44, 106]}

ply_dict = {'insideShot': ((-1, 1.15, -1, 105, 65), (+1, 1.15, -1, 106, 74)),
            'midRange':   ((-1, 1.30, -1, 107, 53), (-1, 1.10, -1, 115, 84)),
            'threePoint': ((+1, 1.06, +1, 16, -44), (-1, 1.39, -1, 103, 52)),
            'freeThrow':  ((), ())}

trft_dict = {'insideShot': ({True: 0.25,  False: 0.20},  0.35),        # this dict is for fraction for 3PA and FTA
             'midRange':   ({True: 0.30,  False: 0.30},  0.25),
             'threePoint': ({True: 0.425, False: 0.625}, 0.225),
             'passing':    ({True: 0.40,  False: 0.375}, 0.325)}

def porcientos(x, attr):
    if attr == 'freeThrow':
        minn = (0.41 * x) + 48
        maxx = (0.36 * x) + 57
        res = random.uniform(minn, maxx)
        return my_precision(res, 1)
    vals = ply_dict[attr]
    lb = vals[0]
    hb = vals[1]
    minn = lb[0] * math.log(x*lb[2]+lb[3], lb[1]) + lb[4]
    maxx = hb[0] * math.log(x*hb[2]+hb[3], hb[1]) + hb[4]
    res = random.uniform(minn, maxx)
    return my_precision(res, 1)

def my_precision(x, n):
    return float('{:.{}f}'.format(x, n))

def myround(x, base=5):
    return base * round(x/base)

def weird_division(n, d):
    return n / d if d else 0

def myLog(x, y):
    y = 1 if y < 1 else y
    result = math.log((y/x), 100)
    result = my_precision(result, 2)
    result = int(x + (x*result))
    return result

def bool_to_int(x, y):
    bool_dict = {True: '1', False: '0'}
    return bool_dict[x] + bool_dict[y]

def def_log(x, y):
    local_dict = {2: ['min', 'max', 100], 3: ['t_min', 't_max', 100]}
    minn = fun_dict[local_dict[y][0]]
    maxx = fun_dict[local_dict[y][1]]
    low = pow(minn[0], x + minn[1]) + minn[2]
    high = pow(maxx[0], x + maxx[1]) + maxx[2]
    res = random.uniform(low, high) / local_dict[y][2]
    res = my_precision(res, 2)
    return res


def is_fitted(l, avg):
    return statistics.mean(l) >= avg-0.25 and statistics.mean(l) <= avg+0.5

def fit_mean(l, mean):
    l = l.copy()
    while True:
        if min(l) >= 0:
            break
        l[l.index(min(l))] = 0
    length = len(l)
    key = True if is_fitted(l, mean) else False
    while key:
        delta = mean - statistics.mean(l)
        weight = round(1/length, 3)
        iterations = abs(int(delta / weight))
        for i in range(iterations):
            l[i%length] += int(delta/abs(delta))
            if is_fitted(l, mean):
                key = False
                break
    return l

def get_points(ppg=20, n=10, consty=2):
    if consty not in range(1, 5):
        consty = 2
    scale = myround(ppg, 5)
    std = (scale/5 * 0.5) + 1
    std = std * consty
    raw_list = [int(round(random.gauss(ppg, std), 0)) for i in range(n)]
    return fit_mean(raw_list, ppg)

# REDUCE TENDENCIES FOR 3 POINTERS - GUYS WHO CANT SHOOT SHOULDNT SHOOT - DONE!

# FIX GETMATCHUP() FROM GAME CLASS... IMPROVE ON IT... TAKE INTO ACCOUNT PLAYER ONE'S MOVE AS A PARAMETER IN THE METHOD - DONE!

# MAKE GUARDS (B, C AND D-CLASS) BETTER AT PASSING IN GENERAL - DONE
# GET THE BEST 3PT SHOOTERS (ESP THE ALL STARS) TO SHOOT AT A HIGHER CLIP (~40%) - DONE

# CREATE 'PLAYOFF' CLASS THAT INHERITS THE LEAGUE CLASS, AS A REPRESENTATION OF THE POST-SEASON - DONE (ISH?)
# INCREASE (DOUBLE) PASS_BONUS IN PLAYPOSSESSION (GAME CLASS), TO GIVE GUARDS HIGHER ASSIST NUMBERS - DONE
# REDUCE (SLIGHTLY) CRUNCH_DICT RANGE FOR ONE-MAN TEAMS (NOT SURE ABOUT THIS, THOUGH) - DONE
# EXPAND GETTEAM(), TO ALSO RETURN THE TEAM OBJECT IF THE TEAM NAME IS PASSED AS AN ARGUMENT - DONE
# ADD PLAYERS' OVR RATINGS TO TEAM.GETLINEUP() METHOD IN TEAM CLASS - DONE

# FIX LARRY BALA (SEE SHELL BELOW) - DONE

# IN PLAYPOSSESSION() MAKE PASS BONUS HIGHER FOR TEAM'S BEST PASSER THAN OTHERS IN THE LINEUP - DONE
# MAKE B, C, D SHOOTERS SHOOT AT A HIGHER CLIP (FROM PLAYPOSSESSION()) - DONE
