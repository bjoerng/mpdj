'''
Created on 06.03.2022

@author: Bjoern Graebe
'''

class MPDConnectionDocument(object):
    '''
    Represents a mpdj-Connection. 
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
        self.name = ''
        self.host = ''
        self.port = ''
        self.password = ''