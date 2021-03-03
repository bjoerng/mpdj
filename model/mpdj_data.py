'''
Created on 20.09.2020

@author: Bjoern Graebe
'''
from enum import Enum, unique, auto
from copy import deepcopy
from _collections import defaultdict
from model.song_selection import SongSelection


class UnitPerNodeTouch(Enum):
    """Provides the mechanism to select the limit type of songs per node."""
    MINUTES = 1
    SONGS = 2

    def gui_representation(self):
        """Return a representations of the unit type for use in the GUI."""
        return self.name.lower()

@unique
class ConnectionMergeMode(Enum):
    """Determines if the connections of the two nodes merges will be calculated with
        a logical 'and' or 'or' connection"""
    AND=auto()
    OR=auto()
    NO=auto()

    def calculate_connection(self,p_connection_value1 : int, p_connection_value2 : int):
        """Calculates the new connection value given two old connection """
        if self == ConnectionMergeMode.AND:
            return min(p_connection_value1, p_connection_value2)
        if self == ConnectionMergeMode.OR:
            return max(p_connection_value1, p_connection_value2)
        if self == ConnectionMergeMode.NO:
            return 0

    def gui_representation(self):
        """Return a representations of the unit type for use in the GUI."""
        return self.name.lower()

class MPDJData():
    """This is were the DJ data, the selections and connections are
        stored."""

    def add_function_to_call_on_change(self,p_function_to_add):
        """Add a function to call, when changes happen to this MPDJData."""
        if not hasattr(self, '_functions_to_call_on_update'):
            self._functions_to_call_on_update = []
        self._functions_to_call_on_update.append(p_function_to_add)

    def _run_functions_on_updates(self):
        for function in self._functions_to_call_on_update:
            function()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_functions_to_call_on_update']
        return state

    def __setstate__(self, p_state):
        p_state['_functions_to_call_on_update'] = []
        self.__dict__.update(p_state)

    @property
    def song_selections(self):
        """The song selections in the mpdjData. Change content of this is discouraged
            outside of mpdjData Methods."""
        return self._song_selections

    @song_selections.setter
    def song_selections(self,p_new_value):
        self._song_selections = p_new_value
        self._run_functions_on_updates()

    @song_selections.deleter
    def song_selections(self):
        del self._song_selections

    @property
    def min_units_per_node_touch(self):
        """The minimal song count per node touch.
            If enough different songs are available."""
        return self._min_units_per_node_touch

    @min_units_per_node_touch.setter
    def min_units_per_node_touch(self, p_new_value):
        self._min_units_per_node_touch = p_new_value
        self._run_functions_on_updates()

    @min_units_per_node_touch.deleter
    def min_units_per_node_touch(self):
        del self._min_units_per_node_touch

    @property
    def max_units_per_node_touch(self):
        """The max soung count per node touch."""
        return self._max_units_per_node_touch

    @max_units_per_node_touch.setter
    def max_units_per_node_touch(self, p_new_value):
        self._max_units_per_node_touch = p_new_value
        self._run_functions_on_updates()

    @max_units_per_node_touch.deleter
    def max_units_per_node_touch(self):
        del self._max_units_per_node_touch

    @property
    def unit_per_node_touch(self):
        """The unit used to calculate songs per node touch."""
        return self._unit_per_node_touch

    @unit_per_node_touch.setter
    def unit_per_node_touch(self, p_new_value):
        self._unit_per_node_touch = p_new_value
        self._run_functions_on_updates()

    @unit_per_node_touch.deleter
    def unit_per_node_touch(self):
        del self._unit_per_node_touch

    @property
    def selection_connections(self):
        """The connections of song selections, represented as a dict of dicts."""
        return self._selection_connections

    @selection_connections.setter
    def selections_connections(self, p_new_value):
        self._selection_connections = p_new_value
        self._run_functions_on_updates()

    @selections_connections.deleter
    def selections_connections(self):
        del self._selection_connections

    @property
    def limit_artist_in_node_touch(self):
        """Not used."""
        return self._limit_artist_in_node_touch

    @limit_artist_in_node_touch.setter
    def limit_artist_in_node_touch(self, p_new_value):
        self._limit_artist_in_node_touch = p_new_value
        self._run_functions_on_updates()

    @limit_artist_in_node_touch.deleter
    def limit_artist_in_node_touch(self):
        del self._limit_artist_in_node_touch

    @property
    def graph_is_directed(self):
        """Show if the opposite direction should be markt, while editing the graph."""
        return self._graph_is_directed

    @graph_is_directed.setter
    def graph_is_directed(self, p_new_value):
        self._graph_is_directed = p_new_value
        self._run_functions_on_updates()

    @graph_is_directed.deleter
    def graph_is_directed(self):
        del self._graph_is_directed

    @property
    def functions_to_call_on_update(self):
        """The functions in this list will be called, when changes happen to
            the mpdjdata. This functions should be working without parameters."""
        return self._functions_to_call_on_update

    @functions_to_call_on_update.setter
    def functions_to_call_on_update(self, p_new_value):
        self._functions_to_call_on_update = p_new_value
        self._run_functions_on_updates()

    @functions_to_call_on_update.deleter
    def function_to_call_on_update(self):
        del self._functions_to_call_on_update

    def __init__(self):
        self._song_selections = dict()
        self._min_units_per_node_touch = 1
        self._max_units_per_node_touch = 5
        self._unit_per_node_touch = UnitPerNodeTouch.MINUTES
#        self.played_artists = dict()
        self._selection_connections = dict()
        self._limit_artist_in_node_touch = True
        self._graph_is_directed = False
        self._functions_to_call_on_update = []

    def is_connected(self, p_selection_1, p_selection_2):
        """Returns 1 if p_selection_1 has an edge to p_selection_2."""
        if p_selection_1 in self._selection_connections:
            if p_selection_2 in self._selection_connections[p_selection_1]:
                return self._selection_connections[p_selection_1][p_selection_2]
        return 0

    def get_neighbours_for_node_name(self, p_node_name : str):
        """Returns the neighbours for the node by the name
            p_node_name."""
        result = []
        if p_node_name in self._selection_connections.keys():
            result = [ key for key in self._selection_connections[p_node_name].keys()
                      if self._selection_connections[p_node_name][key] == 1]
        return result

    def set_connected(self, p_selection_1, p_selection_2,p_is_connected : int,
                      p_mark_opposit_direction=True):
        """Sets the value for the connection from p_selection_1 to p_selection_2,
           to p_is_connected. If p_mark_opposit_direction is True, the connection
           from p_selection_2 to p_selection_1 will also be set."""
        if not p_selection_1 in self._selection_connections:
            self._selection_connections[p_selection_1] = dict()
        self._selection_connections[p_selection_1][p_selection_2] = p_is_connected
        if p_mark_opposit_direction :
            self.set_connected(p_selection_2,p_selection_1,p_is_connected,
                               p_mark_opposit_direction=False)
        self._run_functions_on_updates()

    def add_song_selection(self, p_song_selection):
        """Add p_song_selection to the mpdj-data."""
        self._song_selections[p_song_selection.name]=p_song_selection
        self._run_functions_on_updates()

    def get_song_selection_names(self):
        """Return a list of all song selection names in the mpdj data."""
        result = list(map(lambda songSelection: songSelection.get_name(),
                          self._song_selections.values()))
        return result

    def selection_with_name_exists(self,p_selection_name : str):
        """Return True id a selection by the name p_selection_name
            exists in this mpdj data. It returns false if not."""
        selection_names = list(map(lambda selection: selection.get_name(),
                                   self._song_selections.values()))
        return p_selection_name in selection_names

    def remove_song_selection_by_name(self, p_song_selection_name):
        """Removes the song selection with the name
            p_son_selection_name from this mpdj data.
            Removes all connections, too."""
        del self._song_selections[p_song_selection_name]
        if p_song_selection_name in self._selection_connections:
            del self._selection_connections[p_song_selection_name]
        for selection_connection in self._selection_connections.values():
            if p_song_selection_name in selection_connection:
                del selection_connection[p_song_selection_name]
        self._run_functions_on_updates()

    def get_song_selection_by_name(self,p_selection_name):
        """Return the song selection with the name p_selection_name.
            Returns None if none such selections exists."""
        return self._song_selections.get(p_selection_name, None)

    def change_song_selection(self, p_old_name,p_new_selection : SongSelection):
        """Replaces the song the selection with the name p_old_name
            with the song selection p_new_selection."""
        if p_old_name in self._song_selections:
            del self._song_selections[p_old_name]
        self.add_song_selection(p_new_selection)
        if p_old_name in self._selection_connections:
            self._selection_connections[p_new_selection.get_name()]\
            = self._selection_connections.pop(p_old_name)
        for song_selection_name in self._selection_connections:
            if p_old_name in self._selection_connections[song_selection_name]:
                self._selection_connections[song_selection_name][p_new_selection.get_name()]\
                = self._selection_connections[song_selection_name].pop(p_old_name)
        self._run_functions_on_updates()

    def make_bidirectional(self, bool_func):
        """Turns the connections graph into a bidirectional graph. Uses bool_func
            to calculate the new value. all and any are possible functions."""
        copied_selection_connections = deepcopy(self._selection_connections)
        # We read from a copy, because we will change the length of the original.
        for name1 in copied_selection_connections:
            for name2 in copied_selection_connections[name1]:
                if bool_func([copied_selection_connections[name1][name2],
                              name2 in copied_selection_connections.keys() and
                              name1 in copied_selection_connections[name2].keys() and
                              copied_selection_connections[name2][name1]]):
                    self.set_connected(name1, name2, 1, True)
                else:
                    self.set_connected(name1, name2, 0, True)
        self._run_functions_on_updates()

    def merge_two_nodes_into_one(self, p_selection1_name : str,
                                 p_selection2_name : str,
                                 p_new_name : str, p_connection_mode : ConnectionMergeMode):
        """Merges two notes into one. white and black list criterias are merged, duration are
            taken from the first node. Returns a new node. Deletes the source nodes."""
        new_node = deepcopy(self.get_song_selection_by_name(p_selection1_name))
        new_node.set_name(p_new_name)
        new_node.list_of_white_list_criterias.extend(
            self.get_song_selection_by_name(p_selection2_name).list_of_white_list_criterias)
        new_node.list_of_black_list_criterias.extend(
            self.get_song_selection_by_name(p_selection2_name).list_of_black_list_criterias)
        new_connections = defaultdict(dict)
        for node in self.get_song_selection_names():
            new_connections[node][p_new_name]=p_connection_mode.calculate_connection(
                self.is_connected(node, p_selection1_name),
                self.is_connected(node, p_selection2_name))
            new_connections[p_new_name][node] = p_connection_mode.calculate_connection(
                self.is_connected(p_selection1_name, node),
                self.is_connected(p_selection2_name, node))
        self.remove_song_selection_by_name(p_selection1_name)
        self.remove_song_selection_by_name(p_selection2_name)
        self.add_song_selection(new_node)
        for first_node_name in new_connections.keys():
            for second_node_name in new_connections[first_node_name]:
                if new_connections[first_node_name][second_node_name]:
                    self.set_connected(first_node_name, second_node_name, 1, False)
        self._run_functions_on_updates()
