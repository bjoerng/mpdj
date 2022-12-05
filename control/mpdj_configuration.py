'''
Created on 13.02.2022

@author: Bjoern Graebe
'''

from collections import defaultdict

class MPDJConfiguration(object):
    '''
    Used to represent the configuration file of MPDJ.
    '''
    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, p_state):
        self.__dict__.update(p_state)

    def __init__(self):
        '''
        Constructor
        '''
        self.connections = dict()
        