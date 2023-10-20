import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class FBField:
    '''
    Visual representation of a football field
    '''
    XMIN = -10
    XMAX = 110
    YMIN = 0
    YMAX = 53.3

    def __init__(self):
        self.build_field()
        self.add_yard_markers()
        return
    
    def build_field(self):
        '''
        Draw an empty field
        '''

        self.fig, self.ax = plt.subplots(figsize=(10,5.33))

        self.ax.set_xlim([self.XMIN, self.XMAX])
        self.ax.set_ylim([self.YMIN, self.YMAX])
        
        # went with astroturf, and looked up the RGBA at: https://icolorpalette.com/color/astroturf
        self.ax.set_facecolor([0.404,0.631,0.349,0.5])
        return
    
    def add_yard_markers(self):
        # End zone lines as thick black
        self.ax.plot([0,0],[self.YMIN, self.YMAX], 
                     color='k', 
                     linewidth=2
                     )
        self.ax.plot([100,100],
                     [self.YMIN, self.YMAX], 
                     color='k',
                     linewidth=2
                     )
        
        # Every 10 yard markers
        for z in range(1,10):
            self.ax.plot([z*10, z*10], 
                         [self.YMIN, self.YMAX], 
                         '-w', 
                         alpha=0.5
                         )
        # Labels
        self.ax.set_xticks([z*10 for z in range(1,10)])
        self.ax.set_xticklabels([z*10 if z<6 else 100-z*10 for z in range(1,10)])
        self.ax.set_yticks([])

        return
    
    def mark_players(self,
                     x: int,
                     y: int,
                     m: str
                     ):
        '''
        Add the players to the figure
        '''

        # Make sure we have numpy arrays
        x = np.array(x)
        y = np.array(y)
        m = np.array(m)

        # Clear the figure
        self.ax.clear()

        # Redraw the lines. Depending what front end we're using (e.g., Streamlit or not),
        # there's often a more efficient way, i.e. don't replot things that don't change...
        # ... Keeping the code simple (not efficient) for this example
        self.add_yard_markers()

        # Since we can't pass markers as lists,
        # need to issue separate plot commands for each marker style (i.e., x or o)
        for mtype in np.unique(m):
            idx = (m == mtype)
            if mtype == 'x':
                self.ax.scatter(x[idx], y[idx], 
                                marker = mtype, 
                                color ='k'
                                )
            else:
                self.ax.scatter(x[idx], y[idx], 
                                marker = mtype, 
                                color ='k',
                                facecolor = 'none'
                                )
        return self.fig
    
    def mark_players_from_df(self, 
                             df: pd.DataFrame
                             ):
        self.mark_players(df['x'],
                          df['y'],
                          df['m']
                          )
        return