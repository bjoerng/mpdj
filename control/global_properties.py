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

def inform_about_changes_in_mpdj():
    """This informs global_properties about changes in the current mpdj_data."""
    global_properties = GlobalProperties.get_instance()
    global_properties.changes_happened_since_last_save = True
    global_properties.inform_update_listener()

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

    @property
    def changes_happened_since_last_save(self):
        """Indicates if changes happened since last save."""
        return self._changes_happened_since_last_save

    @changes_happened_since_last_save.setter
    def changes_happened_since_last_save(self, p_new_value):
        self._changes_happened_since_last_save = p_new_value

    @changes_happened_since_last_save.deleter
    def changes_happened_since_last_save(self):
        del self._changes_happened_since_last_save

    @property
    def path_of_current_file(self):
        """The currently opened file."""
        if not hasattr(self, '_path_of_current_file'):
            self._path_of_current_file = ''
        return self._path_of_current_file
    
    @path_of_current_file.setter
    def path_of_current_file(self,p_new_path):
        self._path_of_current_file = p_new_path
        
    @path_of_current_file.deleter
    def path_of_current_file(self):
        del self._path_of_current_file

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
        with open(p_file_name, 'r') as load_file:
            self.mpdj_data = jsonpickle.decode(load_file.read())
        self.mpdj_data.add_function_to_call_on_change(inform_about_changes_in_mpdj)
        self.changes_happened_since_last_save = False
        self.path_of_current_file = p_file_name
        self.inform_update_listener()

    def new_mpdj(self):
        """Creates a new mpdj data to work on (empties all the data
            currently loaded)"""
        self.mpdj_data = MPDJData()
        self.mpdj_data.add_function_to_call_on_change(inform_about_changes_in_mpdj)
        self.path_of_current_file = ''
        self.changes_happened_since_last_save = False
        self.inform_update_listener()

    def __init__(self):
        """ Virtually private constructor. """
        if GlobalProperties.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GlobalProperties.__instance = self
            # Configuration Document for mpdj_Builder.
            # The momentary connection we are using.
            self.mpd_connection = MPDConnection('localhost', '6600')
            self.mpd_connection.connect()
            # The momentary MPDJ data.
            self.mpdj_data = MPDJData()
            self.mpdj_data.add_function_to_call_on_change(inform_about_changes_in_mpdj)
            # The update listeners which are informed about changes.
            self.update_listeners = []
            # The path of the file which we are working on
            self._path_of_current_file = ''
            # Indicates changes since the last save or load operation.
            self._changes_happened_since_last_save = False
            # Edit connections so the graph the graph simulates an undirected graph
#            self.edit_both_directions = True
            # The current opened windows.
            self.opened_windows = list()
