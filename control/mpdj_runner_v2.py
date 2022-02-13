'''
Created on 15.11.2020

@author: Bjoern Graebe
'''
import random
import sys
import datetime
from model.mpd_connection import MPDConnection
from model.mpdj_data import MPDJData
from model.play_data import PlayData
from control.node_selectors import (NodeSelectionMinimalAveragePlaycount,
                                    NodeSelectionMinimalAveragePlaycountWeightedProbabilities)
from control.song_selectors import SongSelectorMinimalPlayCount

DUB_FILTER_KEYS = ['artist', 'albumartist']

def format_timedelta(delta: datetime.timedelta) -> str:
    """Formats a timedelta duration to [N days] %H:%M:%S format"""
    seconds = int(delta.total_seconds())

    secs_in_a_day = 86400
    secs_in_a_hour = 3600
    secs_in_a_min = 60

    days, seconds = divmod(seconds, secs_in_a_day)
    hours, seconds = divmod(seconds, secs_in_a_hour)
    minutes, seconds = divmod(seconds, secs_in_a_min)

    time_fmt = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    if days > 0:
        suffix = "s" if days > 1 else ""
        return f"{days} day{suffix} {time_fmt}"

    return time_fmt

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
        song_count = random.randint(self.mpdj_data.min_units_per_node_touch,
                                     self.mpdj_data.max_units_per_node_touch)
        
        max_overspill=None
        if hasattr(self.mpdj_data, 'limit_overspill_global'):
            if (hasattr(self.mpdj_data, 'global_node_max_overspill') and
                self.mpdj_data.global_node_max_overspill):
                max_overspill = self.mpdj_data.global_node_max_overspill
            else:
                print('Global overspill is limited but not specified. Assuming no overspill limit.')
        
        if (hasattr(current_node, 'limit_overspill') and current_node.limit_overspill):
            if hasattr(current_node, 'overspill_limit'):
                max_overspill = current_node.overspill_limit
            else:
                print('Overspill for node is limited but not specified. Assuming no overspill limit for node.')
        
        print ("current_node: ", current_node, "song_count:", song_count, "max_overspill: ", max_overspill)
        next_songs, songs_length = self.song_selector.get_n_songs(current_node, song_count,
                                                self.mpd_connection,
                                                self.play_data,
                                                DUB_FILTER_KEYS,
                                                self.mpdj_data.unit_per_node_touch,
                                                max_overspill)
        for song in next_songs:
            self.mpd_connection.add_song_to_playlist(song['file'])
            self.play_data.process_played_song(song)
        return songs_length

    def run(self):
        """Runs the mpdj. Configures the mpd to
            run mpdj and ensures it is playing."""
        while self.keep_running:
            self.mpd_connection.ensure_working_connection()
            self.mpd_connection.set_mpd_to_run_mpdj()
            node_play_length = self.add_songs()
            length_in_minutes = str(format_timedelta(datetime.timedelta(minutes=node_play_length)))
            print ('Selected node: {}, Length: {}'.format(self.play_data.current_node, str(length_in_minutes)))
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
        
    def clear_playlist(self):
        self.mpd_connection.clear()
