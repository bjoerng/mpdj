'''
Created on 15.11.2020

@author: Bjoern Graebe
'''
import random
import sys
from model.mpd_connection import MPDConnection
from model.mpdj_data import MPDJData
from model.play_data import PlayData
from control.node_selectors import (NodeSelectionMinimalAveragePlaycount,
                                    NodeSelectionMinimalAveragePlaycountWeightedProbabilities)
from control.song_selectors import SongSelectorMinimalPlayCount

DUB_FILTER_KEYS = ['artist', 'albumartist']

class MPDJRunnerV2():
    """Runs an mpdj."""

    def add_songs(self):
        """Selects and add the next songs based on the mpdj data,
            the playData and the node and song selector"""
        current_node_name = ''
        if not self.play_data.current_node:
            random.seed()
            possible_node_names = list(self.mpdj_data.song_selections.keys())
            if len(possible_node_names) ==0:
                sys.stderr.write('No nodes, exiting')
            current_node_name = random.choice(possible_node_names)
        else:
            current_node_name = self.node_selector.get_next_neighbour(self.play_data.current_node,
                                                             self.mpdj_data,
                                                             self.play_data,
                                                             self.mpd_connection)
        current_node = self.mpdj_data.song_selections[current_node_name]
        self.play_data.process_played_node(current_node_name)
        song_count = random.randrange(self.mpdj_data.min_units_per_node_touch,
                                     self.mpdj_data.max_units_per_node_touch + 1)

        next_songs = self.song_selector.get_n_songs(current_node, song_count,
                                                self.mpd_connection,
                                                self.play_data,
                                                DUB_FILTER_KEYS,
                                                self.mpdj_data.unit_per_node_touch)
        for song in next_songs:
            self.mpd_connection.add_song_to_playlist(song['file'])
            self.play_data.process_played_song(song)

    def run(self):
        """Runs the mpdj. Clears the playlist, configures the mpd to
            run mpdj and ensures it is playing."""
        self.mpd_connection.clear()
        while self.keep_running:
            self.mpd_connection.set_mpd_to_run_mpdj()
            self.add_songs()
            print ('Selected node: {}'.format(self.play_data.current_node))
            print ('______________________________________________________________________')
            self.mpd_connection.ensure_is_playing()
            next_nodes_with_probabilities = self.node_selector.get_possible_next_nodes_with_probabilities(
            self.play_data.current_node,self.mpdj_data,self.play_data,self.mpd_connection)
            print ('Next nodes with probability:')
            for node_prob in sorted(next_nodes_with_probabilities.items(), key=lambda x: x[1]):
                print ('{}: {:.2%}'.format(node_prob[0], node_prob[1]))
            print ('______________________________________________________________________')
            while (self.mpd_connection.get_current_song_number() + 1
            < self.mpd_connection.get_play_list_length()):
                self.mpd_connection.idle()

    def __init__(self,pHost,pPort):
        '''
        Constructor
        '''
        self.mpdj_data = MPDJData()
        self.mpd_connection = MPDConnection(pHost,pPort)
        self.keep_running = True
        self.play_data = PlayData()
        self.node_selector = NodeSelectionMinimalAveragePlaycountWeightedProbabilities()
        self.song_selector = SongSelectorMinimalPlayCount()
