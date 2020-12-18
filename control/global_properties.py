'''
Created on 20.09.2020

@author: Bjoern Graebe
'''
import os
import jsonpickle
from model.mpd_connection import MPDConnection
from model.mpdj_data import MPDJData

def new_mpdj_data():
    """Discard the mpdj data and create a new on."""
    global_properties = GlobalProperties.get_instance()
    global_properties.new_mpdj()

class GlobalProperties():
    """This singleton contains stuff, which needs to be accessible
    from everywhere in mpdj."""
    __instance = None
    @staticmethod
    def get_instance():
        """Static access method."""
        if GlobalProperties.__instance is None:
            GlobalProperties()
        return GlobalProperties.__instance

    def add_listener(self, p_listener):
        """Adds a listener so if anything changes the listener will be
        informed."""
        self.update_listeners.append(p_listener)

    def load_config_from_file(self):
        """This sould load a config from a config file.
            Not implemented, yet."""
        #TODO

    def inform_update_listener(self):
        """This method inform all added listeners about changes."""
        for update_listener in self.update_listeners:
            update_listener.update()

    def save_mpdj_data_to_file(self, p_file_name):
        """Write the momentary MPDJ-data to p_file_name."""
        with open(p_file_name, 'w') as save_file:
            save_file.write(jsonpickle.encode(self.mpdj_data))
        self.changes_happened_since_last_save = False
        self.path_of_current_file = p_file_name
        self.inform_update_listener()

    def load_mpdjdata_from_file(self, p_file_name):
        """Loads a mpdj file, overwrite the momentary MPDJ-data."""
        #TODO Asking if the file should replace the momentary MPDJ-data!
        with open(p_file_name, 'r') as load_file:
            self.mpdj_data = jsonpickle.decode(load_file.read())
        self.inform_update_listener()
        self.changes_happened_since_last_save = False
        self.path_of_current_file = p_file_name
        self.inform_update_listener()

    def new_mpdj(self):
        """Creates a new mpdj data to work on (empties all the data
            currently loaded)"""
        self.mpdj_data = MPDJData()
        self.path_of_current_file = ''
        self.changes_happened_since_last_save = False
        self.inform_update_listener()

    def __init__(self):
        """ Virtually private constructor. """
        if GlobalProperties.__instance is not None:
            raise Exception("This class is a singleton!")
        if os.path.isfile('./path_of_file'):
            self.load_config_from_file()
        else:
            GlobalProperties.__instance = self
            # The momentary connection we are using.
            self.mpd_connection = MPDConnection('localhost', '6600')
            self.mpd_connection.connect()
            # The momentary MPDJ data.
            self.mpdj_data = MPDJData()
            # The update listeners which are informed about changes.
            self.update_listeners = []
            # The path of the file which we are working on
            self.path_of_current_file = ''
            # Indicates changes since the last save or load operation.
            self.changes_happened_since_last_save = False
            # Edit connections so the graph the graph simulates an undirected graph
            self.edit_both_directions = True
