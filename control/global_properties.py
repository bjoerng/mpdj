'''
Created on 20.09.2020

@author: hiroaki
'''
from model.mpd_connection import MPDConnection
from model.mpdj_data import MPDJData


class GlobalProperties(object):
    '''
    classdocs
    '''
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if GlobalProperties.__instance == None:
            GlobalProperties()
        return GlobalProperties.__instance
    
    def addListener(self, pListener):
        self.updateListeners.append(pListener)
        
    def informUpdateListener(self):
        for updateListener in self.updateListeners:
            updateListener.update()
            

    
    def __init__(self):
        """ Virtually private constructor. """
        if GlobalProperties.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GlobalProperties.__instance = self
            self.host = 'localhost'
            self.port = '6600'
            self.mpdConnection = MPDConnection(self.host, self.port)
            self.mpdConnection.connect()
            self.mpdjData = MPDJData()
            self.updateListeners = []#
            self.graphIsDirected = False