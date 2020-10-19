'''
Created on 20.09.2020

@author: Bjoern Graebe
'''
from model.mpd_connection import MPDConnection
from model.mpdj_data import MPDJData
import jsonpickle



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
            

    def saveMPDJDataToFile(self, pFileName):
        with open(pFileName, 'w') as saveFile:
            saveFile.write(jsonpickle.encode(self.mpdjData))
    
    def loadMPDJDataToFile(self, pFileName):
        with open(pFileName, 'r') as loadFile:
            self.mpdjData = jsonpickle.decode(loadFile.read())
        self.informUpdateListener()

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
            self.updateListeners = []
            self.PathOfCurrentFile = ''