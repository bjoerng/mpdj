'''
Created on 13.02.2022

@author: Bjoern Graebe
'''

import copy
from model.mpd_connection_document import MPD_Connection_Document

class MPDJConfiguration(object):
    '''
    Used to represent the configuration file of MPDJ.
    '''
    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, p_state):
        self.__dict__.update(p_state)
        
    def add_connection(self, p_connection: MPD_Connection_Document):
        self._connections[p_connection.name]=p_connection
        self.last_selected_connection = p_connection.name
        
    def get_connections_copy(self):
        return copy.deepcopy(self._connections)
    
    def get_connection_by_name(self,p_name):
        if p_name in self._connections:
            return copy.deepcopy(self._connections[p_name])
        else:
            return None

    def remove_connection_by_name(self,p_name):
        print(self._connections)
        if p_name in self._connections:
            self._connections.pop(p_name)
        print(self._connections)
        
    def modify_selected_connection(self,p_modifications: MPD_Connection_Document):
        if self.last_selected_connection:
            del self._connections[self.last_selected_connection]
        self._connections[p_modifications.name]=p_modifications
        self.last_selected_connection = p_modifications.name

    def __init__(self):
        '''
        Constructor
        '''
        self._connections = dict()
        self.last_selected_connection = None
        