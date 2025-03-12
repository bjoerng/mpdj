'''
Created on 16.02.2025

@author: Bjoern Graebe
'''

from dataclasses import dataclass

@dataclass
class MPD_Connection_Document:
    name: str
    password: str
    hostname: str= "localhost"
    port: int = 6600
    
    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, p_state):
        self.__dict__.update(p_state)