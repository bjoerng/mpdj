'''
Created on 14.11.2020

@author: Björn Gräbe
'''
from builtins import isinstance
from collections import defaultdict
from model.song_selection import SongSelection

class PlayData():
    """Holds the data of played songs."""
    def process_played_song(self, p_song : dict):
        """Registers a played song to the data of played songs."""
        for key in p_song.keys():
            if isinstance(p_song[key], list):
                for single_val in set(p_song[key]):
                    self.song_play_data[key][single_val] += 1
            else:
                self.song_play_data[key][p_song[key]] += 1
        self.previous_song = p_song

    def get_play_count_of_song_value(self, p_value : str, p_key : str):
        """Return how often songs have been played where the value of
            p_key is p_value."""
        return self.song_play_data[p_key][p_value]

    def process_played_node(self, p_node : SongSelection):
        """Processes the given node p_node in the play_data."""
        self.node_play_count[p_node] += 1
        self.previous_node = self.current_node
        self.current_node = p_node

    def __init__(self):
        """Initiates the play data with empty values."""
        self.song_play_data = defaultdict (lambda: defaultdict(lambda: 0))
        self.node_play_count = defaultdict (lambda: 0)
        self.previous_node = None
        self.previous_song = None
        self.current_node = None
        