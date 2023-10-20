import os
import sqlite3
import pandas as pd
from glob import glob

# Minimal example code to implement a database (with minimal documentation!)
# No error handling has been implemented, so catastrophic failure is possible.

class FootballDB:

    # File paths are all relative to where the code is run from, not where this module is saved!
    # The idea is that if we're using this code, we'll be importing it into a file that lives in the main project directory
    # Otherwise, you could remove the hardcoded file paths here, and instead supply them as parameters when instantiating the class

    PATH_DB = './data/Football.db'
    
    # Files for new games go here
    PATH_UNLOADED = './data/unloaded/'

    # Files for games already in the DB get moved here
    PATH_LOADED = './data/loaded/'

    # Usually have a naming convention for data files, 
    # in case other files accidentally make their way into the directory
    FLAG_GAMEFILES = 'GAME_*.csv'

    def __init__(self
                 ):
        '''
        Create the database if it doesn't exist
        '''
        if not os.path.exists(self.PATH_DB):
            print('Creating the database')
            conn = sqlite3.connect(self.PATH_DB)
            conn.close()
        return
    
    def connect(self):
        '''
        Establish a connection and cursor
        '''
        self.conn = sqlite3.connect(self.PATH_DB)
        self.curs = self.conn.cursor()
        return
    
    def close(self):
        '''
        Close the connection
        '''
        self.conn.close()
        return
    
    def get_games(self):
        '''
        Return a list of game_id in the database
        '''
        games = self.run_query("SELECT DISTINCT game_id FROM tGameData;")['game_id']
        return list(games)
    
    def get_game_data(self, 
                      game_id
                      ) -> pd.DataFrame:
        sql = "SELECT * FROM tGameData WHERE game_id = ?;"
        return self.run_query(sql, (game_id,))
    
    def run_query(self, 
                  sql: str, 
                  params: tuple|dict = None
                  ) -> pd.DataFrame:
        '''
        Run a SELECT query
        '''
        self.connect()
        if params is not None:
            results = pd.read_sql(sql, 
                                  self.conn, 
                                  params=params
                                  )
        else:
            results = pd.read_sql(sql,
                                  self.conn
                                  )
        self.close()
        return results
    
    def build_tables(self, 
                     are_you_sure:bool=False
                     ):
        '''
        Build the tables (with a safety flag to be sure we don't run this by accident!)
        '''
        if not are_you_sure:
            raise Exception("You almost deleted the database by accident!")
        
        # and as a double-double check!!!
        really_sure = input("Are you really sure you want to drop all tables and rebuild? Enter y if so.")
        if really_sure != 'y':
            print("OK - we won't do it then! Quitting.")
            return

        print('Building the tables')
        self.connect()
        self.curs.execute("DROP TABLE IF EXISTS tGameData;")

        sql = """
            CREATE TABLE tGameData (
                game_id INTEGER,
                play_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                m TEXT NOT NULL,
                PRIMARY KEY(game_id, play_id, player_id)
            )
            ;"""
        self.curs.execute(sql)
        self.close()
        return
    
    def load_new_data(self):
        '''
        Find new game files to load and then move them to the LOADED directory
        '''
        
        # Connect
        self.connect()
        
        # Our INSERT statement
        sql = """
            INSERT INTO tGameData (game_id, play_id, player_id, x, y, m)
            VALUES (:game_id, :play_id, :player_id, :x, :y, :m)
            ;"""

        files_to_load = glob(self.PATH_UNLOADED + self.FLAG_GAMEFILES)

        for file in files_to_load:
            print('Loading a file:', file)
            df = pd.read_csv(file)

            # The game_id is in the filename. This logic is specific to the randomly generated data
            game_id = file.split('GAME_')[1].split('.csv')[0]

            # Load the data
            for row in df.to_dict(orient='records'):
                row['game_id'] = game_id
                self.curs.execute(sql, row)

            # Move the file to the LOADED directory
            os.rename(file, file.replace(self.PATH_UNLOADED, self.PATH_LOADED))
        
        # Commit the changes and close the connection
        self.conn.commit()
        self.close()
        return