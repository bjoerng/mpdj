'''
Created on 20.09.2020

@author: Bjoern Graebe
'''
from enum import Enum
from model.song_selection import SongSelection

class UnitPerNodeTouch(Enum):
    """Provides the mechanism to select the limit type of songs per node."""
    MINUTES = 1
    SONGS = 2

    def gui_representation(self):
        """Return a represantions of the unit type for use in the GUI."""
        return self.name.lower()

class MPDJData():
    """This is were the DJ data, the selections and connections are
        stored."""

    def __init__(self):
        self.song_selections = dict()
        self.min_units_per_node_touch = 1
        self.max_units_per_node_touch = 5
        self.unit_per_node_touch = UnitPerNodeTouch.MINUTES
        self.played_artists = dict()
        self.selection_connections = dict()
        self.limit_artist_in_node_touch = True
        self.graph_is_directed = True

    def is_connected(self, p_selection_1, p_selection_2):
        """Returns 1 if p_selection_1 has an edge to p_selection_2."""
        if p_selection_1 in self.selection_connections:
            if p_selection_2 in self.selection_connections[p_selection_1]:
                return self.selection_connections[p_selection_1][p_selection_2]
        return 0

    def get_neighbours_for_node_name(self, p_node_name : str):
        """Returns the neighbours for the node by the name
            p_node_name."""
        result = []
        if p_node_name in self.selection_connections.keys():
            result = [ key for key in self.selection_connections[p_node_name].keys()
                      if self.selection_connections[p_node_name][key] == 1]
        return result

    def set_connected(self, p_selection_1, p_selection_2,p_is_connected : bool,
                      p_mark_opposit_direction=True):
        """Sets the value for the connection from p_selection_1 to p_selection_2,
           to p_is_connected. If p_mark_opposit_direction is True, the connection
           from p_selection_2 to p_selection_1 will also be set."""
        if not p_selection_1 in self.selection_connections:
            self.selection_connections[p_selection_1] = dict()
        self.selection_connections[p_selection_1][p_selection_2] = p_is_connected
        if p_mark_opposit_direction :
            self.set_connected(p_selection_2,p_selection_1,p_is_connected,
                               p_mark_opposit_direction=False)

    def add_song_selection(self, p_song_selection):
        """Add p_song_selection to the mpdj-data."""
        self.song_selections[p_song_selection.name]=p_song_selection

    def get_song_selection_names(self):
        """Return a list of all song selection names in the mpdj data."""
        result = list(map(lambda songSelection: songSelection.get_name(),
                          self.song_selections.values()))
        return result

    def selection_with_name_exists(self,p_selection_name : str):
        """Return True id a selection by the name p_selection_name
            exists in this mpdj data. It returns false if not."""
        selection_names = list(map(lambda selection: selection.get_name(),
                                   self.song_selections.values()))
        return p_selection_name in selection_names

    def remove_song_selection_by_name(self, p_song_selection_name):
        """Removes the song selection with the name
            p_son_selection_name from this mpdj data.
            Removes all connections, too."""
        del self.song_selections[p_song_selection_name]
        if p_song_selection_name in self.selection_connections:
            del self.selection_connections[p_song_selection_name]
        for selection_connection in self.selection_connections.values():
            if p_song_selection_name in selection_connection:
                del selection_connection[p_song_selection_name]

    def get_song_selection_by_name(self,p_selection_name):
        """Return the song selection with the name p_selection_name.
            Returns None if none such selections exists."""
        return self.song_selections.get(p_selection_name, None)

    def change_song_selection(self, p_old_name,p_new_selection : SongSelection):
        """Replaces the song the selection with the name p_old_name
            with the song selection p_new_selection."""
        if p_old_name in self.song_selections:
            del self.song_selections[p_old_name]
        self.add_song_selection(p_new_selection)
        if p_old_name in self.selection_connections:
            self.selection_connections[p_new_selection.get_name()]\
            = self.selection_connections.pop(p_old_name)
        for song_selection_name in self.selection_connections:
            if p_old_name in self.selection_connections[song_selection_name]:
                self.selection_connections[song_selection_name][p_new_selection.get_name()]\
                = self.selection_connections[song_selection_name].pop(p_old_name)
