'''
Created on 27.02.2021

@author: Bjoern Graebe

'''

from model.global_properties import GlobalProperties

def merge_two_nodes_into_one(p_selection1 : SongSelection,
                             p_selection2 : SongSelection,
                             p_new_name : str,
                             ):
    """Merges two notes into one. white and black list criterias are merged, duration ar
    taken from the first node. Returns a new node. Deletes the source nodes."""
    new_node=p_selection1.deepcopy()
    new_node.set_name(p_new_name)
    new_node.list_of_white_list_criterias.append(
        p_selection2.list_of_white_list_criterias)
    new_node.list_of_black_list_criterias.append(
        p_selection2.list_of_black_list_criterias)
    global_properties = GlobalProperties.get_instance()
    global_properties.mpdj_data.remove_song_selection_by_name(p_selection1.name)
    global_properties.mpdj_data.remove_song_selection_by_name(p_selection2.name)
    global_properties.mpdj_data.add_song_selection(new_node)