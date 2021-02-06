'''
Created on 14.11.2020

@author: Bjoern Graebe
'''
import math
import random
from functools import reduce
from model.mpdj_data import MPDJData
from model.play_data import PlayData
from model.mpd_connection import MPDConnection


class NodeSelectionMinimalAveragePlaycountWeightedProbabilities():
    """The node selector selects the next node by using the count of
        songs in a node divided by (1 + plays of songs in this node)
        and uses this as the weight for a random choice. """
    def get_next_neighbour(self, p_node_name_now : str, p_mpdj_data : MPDJData,
                         p_play_data : PlayData,
                         p_mpd_connection : MPDConnection) -> str:
        """Returns the next neighbour, according to a random choice
            weighted by songs in collected divided by 1 plays
            of songs in this node."""
        random.seed()
        neighbour_node_names = p_mpdj_data.get_neighbours_for_node_name(p_node_name_now)
        if len(neighbour_node_names) > 1 and p_play_data.previous_node in neighbour_node_names:
            neighbour_node_names.remove(p_play_data.previous_node)

        node_weights = []
        for node in neighbour_node_names:
            songs_in_node = p_mpdj_data.get_song_selection_by_name(node).get_songs(p_mpd_connection)
            song_play_count = reduce(lambda x,y: x+y, (map(lambda song:
                                p_play_data.get_play_count_of_song_value(song['file'], 'file'),
                                songs_in_node)))
            node_weights.append(float(len(songs_in_node))/(1.0 + song_play_count))
        choice = random.choices(population=neighbour_node_names,weights=node_weights,k=1)
        print (neighbour_node_names)
        print (node_weights)
        print (choice)
        return choice[0]

    def __init__(self):
        """Constructor"""

class NodeSelectionMinimalAveragePlaycount():
    """The next selected node is the one with the minimum of average play
        count. If there are multiple nodes with the same avaerga play count
        one of the mill be selected randomly."""
    def get_next_neighbour(self, p_node_name_now : str, p_mpdj_data : MPDJData,
                         p_play_data : PlayData,
                         p_mpd_connection : MPDConnection) -> str:
        """Return the next node by selecting the one with minimal
            average play count. When more than on has minimal play
            count, the next one will be on of those with minimum play
            count, selected randomly."""
        random.seed()
        neighbour_node_names = p_mpdj_data.get_neighbours_for_node_name(p_node_name_now)
        print (neighbour_node_names)
        candidates_with_minimal_average_play_count = list()
        min_average = math.inf
        if p_play_data.previous_node and p_play_data.previous_node in neighbour_node_names:
            neighbour_node_names.remove(p_play_data.previous_node)
        for node_name in neighbour_node_names:
            node = p_mpdj_data.song_selections[node_name]
            songs_of_node = node.get_songs(p_mpd_connection)
            song_count = len(songs_of_node)
            if song_count == 0:
                continue
            playcount = reduce(lambda x,y: x+y,
                               (map(lambda song:
                                p_play_data.get_play_count_of_song_value(song['file'], 'file'),
                                songs_of_node)))
            play_count_average = float(playcount) / float (song_count)
            print ("Node: {}: {}".format(node_name,play_count_average))
            if play_count_average < min_average:
                candidates_with_minimal_average_play_count = list()
                min_average = play_count_average
            if play_count_average <= min_average:
                candidates_with_minimal_average_play_count.append(node_name)
        print (candidates_with_minimal_average_play_count)
        choice = random.choice(candidates_with_minimal_average_play_count)
        print (choice)
        return choice

    def __init__(self):
        """Constructor"""

class NodeSelectionMinimalKnotPlayCount():
    """Selects the node as next node where the least plays happened."""

    def get_next_neighbour(self, p_node_now : str, p_mpdj_data : MPDJData,
                         p_play_data : PlayData,
                         p_mpd_connection : MPDConnection) -> str:
        """Returns the node with the minimum playcount, not weighted at all."""
        random.seed()
        neighbour_nodes = p_mpdj_data.get_neighbours_for_node_name(p_node_now)
        min_node_play_count = math.inf
        next_node_candidates = []
        for node in neighbour_nodes:
            node_play_count = p_play_data.node_play_count[node]
            if node_play_count < min_node_play_count:
                min_node_play_count = node_play_count
                next_node_candidates = []
            if node_play_count <= min_node_play_count:
                next_node_candidates.append(node)
        if p_play_data.previous_node and p_play_data in next_node_candidates:
            next_node_candidates.remove(p_play_data.previous_node.get_name())
        return random.choice(next_node_candidates)

    def __init__(self, params):
        '''
        Constructor
        '''
            