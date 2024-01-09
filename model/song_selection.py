'''
Created on 13.09.2020

@author: Bjoern Graebe
'''

from model.mpd_connection import MPDConnection

def is_song_matching_criteria(p_song : dict, p_criteria : dict) -> bool :
    """Indicates if p_song is matched by p_criteria"""
    if len(p_criteria) == 0:
        return False
    for key in p_criteria:
        if key not  in p_song.keys() or p_song[key] != p_criteria[key]:
            if key not  in p_song.keys():
                print ( "Missing key" + key + " in " + str(p_song) )
            return False
    return True

def filter_black_listed_songs_from_set(p_in_song_list : list, p_list_of_blacklist_criterieas):
    """Filters all songs which meet a criteria in pListOfBlacklistCriterias.
    This changes the contents of p_in_song_list."""
    filtered_results = []
    for song in p_in_song_list:
        song_is_matching = False
        for criteria in p_list_of_blacklist_criterieas:
            song_is_matching = song_is_matching or is_song_matching_criteria(song, criteria)
            if song_is_matching:
                break
        if not song_is_matching:
            filtered_results.append(song)
    return filtered_results

class SongSelection():
    """This class represents a song selection, this means it contains a
    whitelist and a blacklist of criterias and is able to get matcvhing
    songs from a mpd connection."""
    def __init__(self, p_name):
        self.list_of_white_list_criterias = []
        self.list_of_black_list_criterias = []
        self.name = p_name
        self.min_duration = 0
        self.max_duration = 0
        # This overwrites min and max units per node from mpdj_data if
        # != -1
        self.min_song_units_per_node_touch = -1
        self.max_song_units_per_node_touch = -1
        self._limit_overspill = False
        self._overspill_limit = -1 


    def set_white_list_criterias(self, p_white_list_criterias : list):
        """Set the whitelist criterias to p_white_list_criterias."""
        self.list_of_white_list_criterias = p_white_list_criterias

    def add_white_list_criteria(self, p_criteria: dict):
        """Add a new white list criteria to the existing list."""
        self.list_of_white_list_criterias += p_criteria

    def set_black_list_criterias(self, p_black_list_criterias : list):
        """Add a new whtie list criteria to the existing list."""
        self.list_of_black_list_criterias = p_black_list_criterias

    def add_black_list_criterias(self, p_criteria: dict):
        """Add a new black list criteria to the existing list."""
        self.list_of_black_list_criterias += p_criteria

    def get_songs_matching_whitelist_from_mpdconnection(
            self,p_mpd_connection : MPDConnection) -> list:
        """Retrieves the songs matching on the the white list criterias in
        self.list_of_white_list_criterias."""
        results = []
        for criteria in self.list_of_white_list_criterias:
            criteria_results = p_mpd_connection.get_files_matching_criteria(criteria)
            results += criteria_results
        return results

    def get_songs(self,p_mpdconnection) -> list():
        """Retrieves the songs which match on of the whitelist criterias,
        filters out those songs matched by one blacklist criteria and
        those who are to long or to short."""
        song_result_list = self.get_songs_matching_whitelist_from_mpdconnection(
            p_mpdconnection)
        #print('Songs got from mpd: {}'.format(len(song_result_list)))
        if hasattr(self, 'min_duration') and self.min_duration != 0:
            tmp_result_list = [song for song in song_result_list
                               if 'time' in song.keys() and int(song['time']) >= self.min_duration]
            song_result_list = tmp_result_list
        #print('Filtered by minimum: {}'.format(len(song_result_list)))
        if hasattr(self, 'max_duration') and self.max_duration != 0:
            tmp_result_list = [ song for song in song_result_list
                               if 'time' in song.keys() and int(song['time']) <= self.max_duration]
            song_result_list = tmp_result_list
        #print('Filtered by maximum: {}'.format(len(song_result_list)))
        song_result_list = filter_black_listed_songs_from_set(
            song_result_list, self.list_of_black_list_criterias)
        #print('Filtered by blacklist: {}'.format(len(song_result_list)))
        return song_result_list

    def __str__(self) -> str:
        """ Returns the string representation of a song selection."""
        return self.name.__str__() + '\n' + 'Whiteliste:\n'\
            + self.list_of_white_list_criterias.__str__()\
            + '\nBlacklist:\n' + self.list_of_black_list_criterias.__str__()

    def get_name(self):
        """Returns the name of the song selection."""
        return self.name

    def set_name(self, p_new_name):
        """Sets the name of the so selection to the given value,"""
        self.name = p_new_name

    def __repr__(self):
        """ Returns a string representation of an object of this type."""
        return "Name: " + self.name + ", WhiteList: "\
            + self.list_of_white_list_criterias.__repr__()\
            + ", BlackList: " + self.list_of_black_list_criterias.__repr__()
            
    @property
    def limit_overspill(self):
        """Limits overspill, overwrites the global setting for this node."""
        if not hasattr(self, '_limit_overspill'):
            self._limit_overspill = False
        return self._limit_overspill

    @limit_overspill.setter
    def limit_overspill(self,p_new_limit_overspill):
        self._limit_overspill = p_new_limit_overspill

    @limit_overspill.deleter
    def limit_overspill(self):
        del self._limit_overspill
        
    @property
    def overspill_limit(self):
        """Limits overspill for this node, overwrites the globl overspill limit."""
        if not hasattr(self, '_limit_overspill'):
            self._overspill_limit = False
        return self._overspill_limit

    @overspill_limit.setter
    def overspill_limit(self,p_new_overspill_limit):
        self._overspill_limit = p_new_overspill_limit

    @overspill_limit.deleter
    def overspill_limit(self):
        del self._overspill_limit        

