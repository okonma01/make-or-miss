from dataclasses import dataclass


composite_rating_dict = dict()

def update_composite_dict() -> None:
    composite_rating_dict['jump_ball'] =        [('hgt', 'jmp'),
                                                 (1, 0.25)]
    composite_rating_dict['halfcourt_usage'] =  [('pss', 'hndl', 'oiq'),
                                                 (1.5, 0.5, 0.5)]
    composite_rating_dict['fastbreak_usage'] =  [('spd', 'hndl', 'pss', 'oiq'),
                                                 (1, 1, 1.5, 0.5)]
    composite_rating_dict['shot_usage'] =       [('ins', 'mid', 'tp', 'spd', 'hgt', 'reb', 'oiq'),
                                                 (2.5, 1, 1, 0.5, 0.5, 0.5, 0.5)]
    composite_rating_dict['blocking'] =         [('hgt', 'jmp', 'diq'),
                                                 (2.5, 1.5, 0.5)]
    composite_rating_dict['fouling'] =          [(50, 'hgt', 'diq', 'spd'),
                                                 (3, 1, -1, -1)]
    composite_rating_dict['rebounding'] =       [('hgt', 'stre', 'jmp', 'reb', 'oiq', 'diq'),
                                                 (2, 0.1, 0.1, 2, 0.5, 0.5)]
    composite_rating_dict['stealing'] =         [(50, 'spd', 'diq'),
                                                 (1, 1, 2)]
    composite_rating_dict['drawing_foul'] =     [('hgt', 'spd', 'hndl', 'ins', 'oiq'),
                                                 (1, 1, 1, 0.5, 1)]
    composite_rating_dict['defense_inside'] =   [('hgt', 'stre', 'spd', 'jmp', 'diq'),
                                                 (2.5, 1, 0.5, 0.5, 2)]
    composite_rating_dict['defense_perimeter'] = [('hgt', 'stre', 'spd', 'jmp', 'diq'),
                                                 (0.5, 0.5, 2, 0.5, 1)]

update_composite_dict()

# composite ratings are derived ratings; they come from the raw ratings
# they determine who gets what in the game - usage, blocks, steals, etc.
# i also added defense here - to determine a team's defensive rating (summing up the players on the court)

@dataclass
class CompositeRating():
    jump_ball: int = 0
    halfcourt_usage: int = 0
    fastbreak_usage: int = 0
    shot_usage: int = 0
    blocking: int = 0
    fouling: int = 0
    rebounding: int = 0
    stealing: int = 0
    drawing_foul: int = 0
    defense_inside: int = 0
    defense_perimeter: int = 0

    def compose(self, rating) -> None:
        for key in self.__dict__.keys():
            for i in range(len(composite_rating_dict[key][0])):
                raw_rating = composite_rating_dict[key][0][i]
                if type(raw_rating) != str:
                    self.__dict__[key] += raw_rating * composite_rating_dict[key][1][i]
                else:
                    self.__dict__[key] += rating.get(raw_rating) * composite_rating_dict[key][1][i]
            try:
                self.__dict__[key] /= sum(composite_rating_dict[key][1])
            except ZeroDivisionError:
                self.__dict__[key] = 0
            self.__dict__[key] = int(self.__dict__[key])
