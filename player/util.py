from player.index import PlayerGameSim


def stat_line(p: PlayerGameSim) -> str:
    line = ''
    line += (p._name + ':').ljust(20)
    line += (str(p._stat.mp) + ' MIN, ').rjust(10)
    line += (str(p._stat.pts) + ' PTS, ').rjust(8)
    line += ((str(p._stat.orb + p._stat.drb)) + ' REB, ').rjust(8)
    line += (str(p._stat.ast) + ' AST, ').rjust(8)
    line += (str(p._stat.fg) + '/' + str(p._stat.fga) + ' FG, ').rjust(10)
    line += (str(p._stat.fg_threepoint) + '/' + str(p._stat.fga_threepoint) + ' 3PT, ').rjust(10)
    line += (str(p._stat.ft) + '/' + str(p._stat.fta) + ' FT, ').rjust(10)
    line += (str(p._stat.stl) + ' STL, ').rjust(8)
    line += (str(p._stat.blk) + ' BLK, ').rjust(8)
    line += (str(p._stat.tov) + ' TOV, ').rjust(8)
    line += (str(p._stat.pf) + ' PF').rjust(5)
    return line
