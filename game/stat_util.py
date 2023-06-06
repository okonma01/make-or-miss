from player.util import stat_line

def box_score(g) -> None:
    stat_lines = ''
    for t in g.teams:
        stat_lines += t._name + ':\n'
        for p in t._lineup:
            stat_lines += stat_line(p) + '\n'
        for p in t._bench:
            stat_lines += stat_line(p) + '\n'
        stat_lines += '\n\n'
    print(stat_lines)
    