import names
from typing import List
from player.archetype import gen_archetype
from player.index import PlayerGameSim, pos_dict
from player.position import Position
from player.rating import raw_rating, TypeFactor, gen_raw_rating
from util.player_height import gen_height
from util.helpers import height_rating, bound
from random import gauss, random
from copy import deepcopy

'''
54 = 4'6"
108 = 9'0"
'''

# make changes to gen_player function
# previously, a rating was determined by factor, type_factor, and gauss (normal distribution on raw_rating)
# factor was used in grouping ratings into categories, such as athleticism, shooting, etc.
# type_factor was used to adjust the rating based on the player's position (e.g. a G should have higher passing than a C)
# gauss was used to generate a random rating based on the raw_rating and a standard deviation of 3

# now, we will use a different method to generate ratings
# we will still have gauss, but we will have different "raw_rating" based on different archetypes
# our archetypes: 
#   - shooting specialist
#   - 3 and D wing
#   - pass first playmaker
#   - slasher
#   - perimeter defender
#   - rebound specialist
#   - rolling big
#   - playmaking big
#   - stretch big
#   - rim protector

# we will have a different raw_rating for each archetype

def gen_player(pos_no: int = 0) -> PlayerGameSim:

    # generate player height and position

    pos_height_tuple = gen_position(pos_no)
    pos = pos_height_tuple[0]
    height_in_inches = pos_height_tuple[1]

    # generate player archetype
    p_archetype = gen_archetype(pos)

    # generate player ratings
    p_ratings = deepcopy(gen_raw_rating(p_archetype))
    p_ratings.hgt = height_rating(height_in_inches)
    for key in p_ratings.__dict__.keys():
        if key == 'hgt' or key == 'composite':
            continue
        if key in TypeFactor.factors[pos.name]:
            type_factor = TypeFactor.factors[pos.name][key]
        else:
            type_factor = 1

        rating = type_factor * gauss(p_ratings.__dict__[key], 3)
        rating = bound(rating, 30, 90)
        rating = int(round(rating, 0))
        p_ratings.__dict__[key] = rating

    # generate player badges - based on position

    # generate player tendencies - based on ratings

    # generate player stats

    # generate player name
    p_name = names.get_full_name(gender='male')

    # assemble player
    p = PlayerGameSim()
    p._name = p_name
    p._height_in_inches = height_in_inches
    p._pos = pos
    p._archetype = p_archetype
    p_ratings.update_composite()
    p._rating = p_ratings

    return p


def gen_position(n: int):
    while True:
        height_in_inches = round(gen_height() + random() - 0.5, 0)
        height_in_inches = int(height_in_inches)

        # generate player position
        pos = None
        rand_type = random()
        if height_in_inches >= 82:  # 6'10" or taller
            if rand_type < 0.03:
                pos = Position.G
            elif rand_type < 0.08:
                pos = Position.GF
            elif rand_type < 0.15:
                pos = Position.F
            elif rand_type < 0.45:
                pos = Position.FC
            else:
                pos = Position.C
        elif height_in_inches <= 77:  # 6'5" or shorter
            if rand_type < 0.50:
                pos = Position.G
            elif rand_type < 0.85:
                pos = Position.GF
            elif rand_type < 0.97:
                pos = Position.F
            else:
                pos = Position.FC
        else:  # between 6'6" and 6'9" (inclusive)
            if rand_type < 0.05:
                pos = Position.G
            elif rand_type < 0.25:
                pos = Position.GF
            elif rand_type < 0.75:
                pos = Position.F
            elif rand_type < 0.95:
                pos = Position.FC
            else:
                pos = Position.C

        if n == 0:
            return [pos, height_in_inches]
        if pos in pos_dict[n]:
            return [pos, height_in_inches]
