
import streamlit as st
from src.football_viz import FBField
from src.football_db import FootballDB

class FBApp:
    PLAY_ID = "play_id"

    def __init__(self):

        self.field = FBField()
        self.db = FootballDB()
        
        if self.PLAY_ID not in st.session_state:
            st.session_state[self.PLAY_ID] = 1


        self.build_page()
        self.streamlit_defaults()
        return
    
    def play_id(self):
        return st.session_state[self.PLAY_ID]
    
    def next_play(self):
        st.session_state[self.PLAY_ID]+=1
        return
    
    def prev_play(self):
        st.session_state[self.PLAY_ID]-=1
        return
    
    def build_page(self):
        
        st.header("Football!")
        games = self.db.get_games()
        game_id_selector = st.selectbox("Pick a game",
                                     games,
                                     index=0
                                     )
        game_data = self.db.get_game_data(game_id_selector)

        play_control = st.columns(3)
        with play_control[0]:
            st.button("Previous play",
                      on_click=self.prev_play
                      )
        with play_control[1]:
            st.write(
                    "Play: " + str(self.play_id())
                    )
        with play_control[2]:
            st.button("Next play",
                      on_click=self.next_play
                      )

        idx = game_data["play_id"] == self.play_id()
        player_data = game_data[idx]

        self.field = FBField()
        self.field.mark_players_from_df(player_data)

        st.pyplot(self.field.fig)

        return
    
    def streamlit_defaults(self):
        '''
        Remove some auto-generated stuff by streamlit
        '''
        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
        return
      
if __name__ == '__main__':
    FBApp()