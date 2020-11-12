'''
Created on 20.09.2020

@author: Bjoern Graebe
'''
from model.mpd_connection import MPDConnection
from model.mpdj_data import MPDJData
import jsonpickle


class GlobalProperties(object):
    '''
    This singleton contains stuff, which needs to be accessible
    from everywhere.
    '''
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if GlobalProperties.__instance == None:
            GlobalProperties()
        return GlobalProperties.__instance

    def addListener(self, pListener):
        """Adds a listener so if anything changes the listener will be
        informed."""
        self.updateListeners.append(pListener)
        
    def informUpdateListener(self):
        """This method inform all added listeners about changes."""
        for updateListener in self.updateListeners:
            updateListener.update()
            

    def saveMPDJDataToFile(self, pFileName):
        """ Write the momentary MPDJ-data to pFileName."""
        with open(pFileName, 'w') as saveFile:
            saveFile.write(jsonpickle.encode(self.mpdjData))
        self.changesHappenedSinceLastSave = False
        self.pathOfCurrentFile = pFileName
        self.informUpdateListener()

    
    def loadMPDJDataToFile(self, pFileName):
        """ Loads a mpdj file, overwrite the momentary MPDJ-data. """
# TODO Error handling!
# TODO Asking if the file should replace the momentary MPDJ-data!
        with open(pFileName, 'r') as loadFile:
            self.mpdjData = jsonpickle.decode(loadFile.read())
        self.informUpdateListener()
        self.changesHappenedSinceLastSave = False
        self.pathOfCurrentFile = pFileName
        self.informUpdateListener()
        
    def newMPDJ(self):
        self.mpdjData = MPDJData()
        self.pathOfCurrentFile = ''
        self.changesHappenedSinceLastSave = 'False'
        self.informUpdateListener()

    def __init__(self):
        """ Virtually private constructor. """
        if GlobalProperties.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GlobalProperties.__instance = self
            # The momentary connection we are using.
            self.mpdConnection = MPDConnection('localhost', '6600')
            self.mpdConnection.connect()
            # The momentary MPDJ data.
            self.mpdjData = MPDJData()
            # The update listeners which are informed about changes.
            self.updateListeners = []
            # The path of the file which we are working on
            self.pathOfCurrentFile = ''
            self.changesHappenedSinceLastSave = False