# our archetypes:
#   - shooting specialist
#   - 3 and D wing
#   - pass first playmaker
#   - slasher
#   - perimeter defender
#   - rebounding specialist
#   - rolling big
#   - playmaking big
#   - stretch big
#   - rim protector

# create a list of archetypes (strings)
import random
from player.position import Position


archetype_list = ['shooting specialist', '3 and D wing', 'pass first playmaker', 'slasher',
                  'perimeter defender', 'rebounding specialist', 'rolling big', 'playmaking big', 'stretch big', 'rim protector']


# create a dict of positions (strings) and their corresponding possible archetypes (string),
# and for each archetype, the probability of it being chosen
# this is a dict of lists
# the key is the position
# the value is a list of archetypes
archetype_dict = {'G': [['shooting specialist', 'pass first playmaker', 'slasher', 'perimeter defender'],
                        [0.25, 0.35, 0.25, 0.15]],
                  'GF': [['3 and D wing', 'pass first playmaker', 'slasher', 'perimeter defender'],
                         [0.35, 0.15, 0.25, 0.25]],
                  'F': [['3 and D wing', 'pass first playmaker', 'slasher', 'perimeter defender', 'rebounding specialist'],
                        [0.30, 0.10, 0.20, 0.15, 0.25]],
                  'FC': [['rolling big', 'playmaking big', 'stretch big', 'rim protector', 'rebounding specialist'],
                         [0.20, 0.05, 0.30, 0.15, 0.30]],
                  'C': [['rolling big', 'playmaking big', 'stretch big', 'rim protector'],
                        [0.30, 0.20, 0.30, 0.20]]}


# create a function that takes a position (Position type) and returns a random archetype (string)
def gen_archetype(pos: Position) -> str:
    # get the list of archetypes for the position
    archetype_list = archetype_dict[pos.name]
    # get an archetype from the list, using a running sum of probabilities
    archetype = random.choices(archetype_list[0], weights=archetype_list[1], k=1)[0]
    return archetype
