'''
Created on 14.11.2020

@author: Bjoern Graebe
'''
import math
import random
import sys
from functools import reduce
from model.mpdj_data import MPDJData
from model.play_data import PlayData
from model.mpd_connection import MPDConnection

def calculate_node_weight_with_song_play_count(p_play_data : PlayData,
                                               p_song_lists : list):
    """Takes the p_play_data and p_song_lists as a list of songlists. This function
        will calculate weight of each songlist in p_song_lists, to use in
        random.choice. The result will be based on the playcound for each
        of those lists."""
    result = []
    for songs_in_list in p_song_lists:
        song_play_count = reduce(lambda x, y:x + y, (map(lambda song:
                    p_play_data.get_play_count_of_song_value(song['file'], 'file'),
                    songs_in_list)), 0)
        result.append(float(len(songs_in_list)) / (1.0 + song_play_count))
    return result

class NodeSelectionMinimalAveragePlaycountWeightedProbabilities():
    """The node selector selects the next node by using the count of
        songs in a node divided by (1 + plays of songs in this node)
        and uses this as the weight for a random choice. """

    def get_possible_next_neighbours(self, p_node_name_now : str, p_mpdj_data : MPDJData,
                                     p_play_data : PlayData, p_mpd_connection : MPDConnection):
        """Returns those neighbors who could be selected as next neighbors. Dependent of
            p_node_name_now, p_mpdj_data, p_play_data and p_mpd_connection."""
        neighbours_in_graph = p_mpdj_data.get_neighbours_for_node_name(p_node_name_now)
        if len(neighbours_in_graph) < 1:
            print('No neighbours for {} considering all nodes as next'.format(p_node_name_now))
            neighbours_in_graph = p_mpdj_data.get_song_selection_names()
        if len(neighbours_in_graph) > 1 and p_play_data.previous_node in neighbours_in_graph:
            neighbours_in_graph.remove(p_play_data.previous_node)
        neighbours_with_song_count_not_zero = dict()
        for node in neighbours_in_graph:
            songs_in_node = p_mpdj_data.get_song_selection_by_name(node).get_songs(p_mpd_connection)
            if len(songs_in_node) == 0:
                sys.stderr.write('Node {} has now songs, ignoring it.'.format(node))
                sys.stderr.flush()
                continue
            neighbours_with_song_count_not_zero[node] = songs_in_node
        return neighbours_with_song_count_not_zero

    def get_next_neighbour(self, p_node_name_now : str, p_mpdj_data : MPDJData,
                         p_play_data : PlayData,
                         p_mpd_connection : MPDConnection) -> str:
        """Returns the next neighbour, according to a random choice
            weighted by songs in collected divided by 1 plays
            of songs in this node."""
        random.seed()
        neighbour_node_names = p_mpdj_data.get_neighbours_for_node_name(p_node_name_now)
        # If node does not have any neighbours, we will select a random one from the set
        # of all neighbours.
        if len(neighbour_node_names) < 1:
            print('No neighbours for {} considering all nodes as next'.format(p_node_name_now))
            neighbour_node_names = p_mpdj_data.get_song_selection_names()
        if len(neighbour_node_names) > 1 and p_play_data.previous_node in neighbour_node_names:
            neighbour_node_names.remove(p_play_data.previous_node)

        nodes_with_song_count_not_zero = self.get_possible_next_neighbours(p_node_name_now,
                                                                           p_mpdj_data,
                                                                           p_play_data,
                                                                           p_mpd_connection)
        node_weights = calculate_node_weight_with_song_play_count(
            p_play_data,
            list(nodes_with_song_count_not_zero.values()))
        choice = random.choices(population=[*nodes_with_song_count_not_zero],
                                weights=node_weights,k=1)
        return choice[0]

    def get_possible_next_nodes_with_probabilities(self, p_node_name_now : str,
                                                 p_mpdj_data : MPDJData, p_play_data : PlayData,
                                                 p_mpd_connection : MPDConnection):
        """Returns next next possible neighbours with probabilities."""
        possible_next_neighbours = self.get_possible_next_neighbours(p_node_name_now, p_mpdj_data,
                                     p_play_data, p_mpd_connection)
        node_weights= calculate_node_weight_with_song_play_count(
            p_play_data,
            list(possible_next_neighbours.values()))
        weight_sum = reduce(lambda x,y: x+y, node_weights,0.0)
        probabilities_per_node = [weight / weight_sum for weight in node_weights]
        nodes_with_probabilities = dict(zip(possible_next_neighbours,probabilities_per_node))
        return nodes_with_probabilities

    def __init__(self):
        """Constructor"""

class NodeSelectionMinimalAveragePlaycount():
    """The next selected node is the one with the minimum of average play
        count. If there are multiple nodes with the same average play count
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

