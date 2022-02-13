'''
Created on 15.11.2020
@author: Bjoern Graebe
'''
import math
import random
from collections import defaultdict
from model.song_selection import SongSelection
from model.mpd_connection import MPDConnection
from model.play_data import PlayData
from model.mpdj_data import UnitPerNodeTouch

def song_is_equal_in_value_to_song(p_song_1 : dict, p_song_2 : dict,
                             p_key_list : list) -> bool:
    """Determines if a song is equal to another one by going through
        keys in p_key_list. If one of the values is similar, this
        returns True. False if this is not the case."""
    for key in p_key_list:
        if p_song_1.get(key,None) and p_song_2.get(key,None):
            if p_song_1[key] == p_song_2[key]:
                return True
            # Some tags may contain a list, this is  why this  is a
            # little more complicated
            if not isinstance(p_song_1[key], list):
                list1 =  [p_song_1[key]]
            else:
                list1 = p_song_1
            if not isinstance(p_song_2[key], list):
                list2 = [p_song_2[key]]
            else:
                list2 = p_song_2
            for element in list1:
                if element in list2:
                    return True
    return False

def get_song_duration_value(song : dict, p_song_accounting_value=UnitPerNodeTouch.SONGS):
    """Return the duration value of song, dependent on p_song_accounting_value."""
    if p_song_accounting_value == UnitPerNodeTouch.MINUTES:
        return float(song['duration']) / 60.0
    return 1

class SongSelectorMinimalPlayCount():
    """This selector selects songs which have minimal play count."""

    def get_n_songs(self, p_song_selection : SongSelection, p_duration_max : int,
                    p_mpd_connection : MPDConnection, p_play_data : PlayData,
                    p_dup_attr_fltr_lst : list, p_song_account_value=UnitPerNodeTouch.SONGS,
                    p_max_overspill=None):
        """Returns p_duration_max if there are enough different songs
            available. If there are less songs available, this could
            return less than p_duration_max. The other parameters of this
            method evaluated to generate a song selection."""
        random.seed()
        songs_in_collection = p_song_selection.get_songs(p_mpd_connection)
        song_count_in_collection = len(songs_in_collection)
        songs_in_collection = [song_url for song_url in songs_in_collection if not
                             self.song_block_list[p_song_selection.get_name()]
                             [song_url['file']] > 0 ]
        minimal_play_count = math.inf
        song_candidates = list()
        # Filter out all songs play more often than others songs of this node. So songs
        # with minimal playcount stay.
        for song_url in songs_in_collection:
            song_play_count = p_play_data.song_play_data['file'][song_url['file']]
            if song_play_count < minimal_play_count:
                minimal_play_count = song_play_count
                song_candidates = list()
            if song_play_count <= minimal_play_count:
                song_candidates.append(song_url)
        
        # Build list of results.
        result = list()
        results_length = 0
        while results_length <= p_duration_max and song_candidates:
            if (p_song_account_value == UnitPerNodeTouch.MINUTES
                and p_song_selection and p_max_overspill and p_max_overspill != -1):
                # Filter out songs which would are to long for the overspill.
                song_candidates = [ song for song in song_candidates
                                   if results_length
                                   + get_song_duration_value(song, p_song_account_value)
                                   < p_duration_max + p_max_overspill]
            if song_candidates:
                selected_song = random.choice(song_candidates)
                result.append(selected_song)
                results_length += get_song_duration_value(selected_song, p_song_account_value)
                song_candidates = [ song for song in song_candidates
                                   if not song_is_equal_in_value_to_song(selected_song,
                                                          song,
                                                          p_dup_attr_fltr_lst)]
        # Update song block list to prevent playing songs to often.
        for song in result:
            # Reducing the block count for all songs in 
            for key in self.song_block_list[p_song_selection.get_name()].keys():
                self.song_block_list[p_song_selection.get_name()][key]\
                    = max(0, self.song_block_list[p_song_selection.get_name()][key] - 1)
            # Aadd song to blacklist for a random time. To make sure it isn't played
            # again for some time.  
            self.song_block_list[p_song_selection.get_name()][song['file']]\
                = random.randrange(int(0.5 * song_count_in_collection),
                                   int(0.9 * song_count_in_collection))
        random.shuffle(result)
        return result, results_length

    def __init__(self):
        """Constructor"""
        self.song_block_list = defaultdict(lambda: defaultdict(lambda: 0))