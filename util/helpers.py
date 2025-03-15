from typing import List
import secrets, string
# import game
# import game.index
# import player
# import player.index
# import team
# import team.index


def weights(n: int = 10, sum: int = 100, delta: float = 0.2) -> List[float]:
    if n <= 1:
        return [sum]

    init_list = [round(sum/n, 2) for i in range(n)]

    for i in range(round(n/2)+1):
        init_list[i] += delta * i
        init_list[i] = round(init_list[i], 1)
        init_list[-i] -= delta * i
        init_list[-i] = round(init_list[-i], 1)

    init_list.sort()
    init_list.reverse()
    return init_list


def bound(x: float = 0, low: float = 0, high: float = 100) -> float:
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x


def height_in_feet(height_in_inches: int) -> str:
    feet = height_in_inches // 12
    inches = height_in_inches % 12
    return str(feet) + '\'' + str(inches) + '\"'


def height_rating(height_in_inches: int) -> int:
    min_hgt = 66    # 5'6"
    max_hgt = 93    # 7'9"
    hgt = bound((100 * (height_in_inches - min_hgt)) / (max_hgt - min_hgt))
    return int(hgt)


def generate_id(obj_type, len=4) -> str:
    # if isinstance(obj_type, player.index.PlayerGameSim):
    #     prefix = 'p'
    # elif isinstance(obj_type, team.index.TeamGameSim):
    #     prefix = 't'
    # elif isinstance(obj_type, game.index.Game):
    #     prefix = 'g'
    # # to add: league, season, etc.
    # else:
    #     prefix = ''

    prefix = type(obj_type).__name__[0].lower()
    
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    random_id = ''.join(secrets.choice(characters) for _ in range(len))
    
    return prefix + random_id