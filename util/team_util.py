from team.index import TeamGameSim
import pickle
import os

path = '/Users/daniel/Documents/Python/mom/app/'
def save_team(t: TeamGameSim) -> None:
    fp = path + 'db/teams/' + t._name + '.pickle'
    # if not os.path.exists(fp):
    #     os.makedirs(fp)
    pickle_out = open(fp, 'wb')
    pickle.dump(t, pickle_out)
    pickle_out.close()
    print('Save successful: File path: ' + fp)
    return

def load_team(name: str) -> TeamGameSim:
    fp = path + 'db/teams/' + str(name) + '.pickle'
    if os.path.exists(fp):
        pickle_in = open(fp, 'rb')
        print('Loaded successfully!')
        return pickle.load(pickle_in)
    else:
        print('Load failed: No saved team named ' + str(name))
        return
