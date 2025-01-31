'''
Created on 13.02.2022

@author: Bjoern Graebe
'''

import copy
from dns.rdataclass import NONE
KEY_NAME="Name"
KEY_HOSTNAME="Hostname"
KEY_PORT="Port"
KEY_PASSWORD="Password"


class MPDJConfiguration(object):
    '''
    Used to represent the configuration file of MPDJ.
    '''
    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, p_state):
        self.__dict__.update(p_state)
        
    def add_connetion(self, p_name, p_properties):
        self._connections[p_name]=p_properties
        
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

    def __init__(self):
        '''
        Constructor
        '''
        self._connections = dict()
        