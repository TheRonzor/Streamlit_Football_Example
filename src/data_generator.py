import numpy as np
import pandas as pd
from datetime import datetime as dt

# Some code to generate random game data
#
# In practice, this would be replaced by either code to download data,
# or instructions for a user to manually download data.

# Relative to where this file is RUN FROM (not stored), the data will be saved with a file path starting:
WHERE_TO_SAVE_DATA = './data/unloaded/GAME_'

class Player:
    # Just to make the data generation process a little cleaner
    def __init__(self,
                 p_id: int, 
                 x:int, 
                 y:int, 
                 marker:str
                 ):
        self.p_id = p_id
        self.x = x
        self.y = y
        self.m = marker
        return
    
    def move(self,
             dx:int,
             dy:int
             ):
        
        self.x += dx
        self.y += dy
        return
    
def  make_data(filename):
    '''
    Generate some random data and save it as a .csv file.

    The filename will contain the game_id

    The data will contain:
        t:      time index
        p_id:   player id
        x:      x coordinates
        y:      y coordinates
        m:      marker style (x or o)
    '''
    offense = []
    defense = []

    for p_id in range(11):
        if p_id == 0: p_id = 13 # Dan Marino
        p = Player(p_id,
                   np.random.randint(5,25), 
                   np.random.randint(15,35),
                   'x')
        offense.append(p)
    
    for p_id in range(11):
        # So they don't match the offense id's
        p_id += 20
        p = Player(p_id,
                   np.random.randint(25,35), 
                   np.random.randint(15,35),
                   'o')
        defense.append(p)

    data = []

    for t in range(1,21):
        for p in offense:
            dx = np.random.randint(1,6)
            dy = np.random.randint(-1,2)
            p.move(dx,dy)
            data.append([t, p.p_id, p.x, p.y, p.m])
        for p in defense:
            dx = np.random.randint(1,6)
            dy = np.random.randint(-1,2)
            p.move(dx,dy)
            data.append([t, p.p_id, p.x, p.y, p.m])

    df = pd.DataFrame(data, columns = ['play_id', 'player_id', 'x', 'y' , 'm'])
    df.to_csv(filename, index=False)
    return

def make_new_game_data():
    # get the current time
    t = dt.now()
    # hash it and use that as a random game id
    #  (just taking absolute value to avoid minus signs in the file name)
    game_id = abs(hash(t))

    # Save it to a folder designated for new data that hasn't been loaded into the database
    filename = WHERE_TO_SAVE_DATA + str(game_id) + '.csv'
    print('Generating new game data and saving as: ' + filename)
    make_data(filename)
    return