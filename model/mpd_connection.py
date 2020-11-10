'''
Created on 12.09.2020

@author: Bjoern Graebe
'''
class CannotConnectToMPDError(Exception):
    pass

from mpd import MPDClient,ConnectionError

class MPDConnection(object):
    def __init__(self,pHost,pPort):
        self.host = pHost
        self.port = pPort
        self.mpdClient = MPDClient()
        #self.mpdClient.timeout = 3600

    def connect(self):
        self.mpdClient.connect(host = self.host, port=self.port)

    def ensureWorkingConnection(self):
        try:
            self.mpdClient.ping()
        except ConnectionError as e:
            self.connect()

        try:
            self.mpdClient.ping()
        except ConnectionError as e:
            raise CannotConnectToMPDError(str(e))
            
    def getPossibleTags(self):
        self.ensureWorkingConnection();
        try:
            return self.mpdClient.tagtypes()
        except ConnectionError as e:
            raise CannotConnectToMPDError(str(e))
    
    def addSong(self, pSongName : str):
        self.mpdClient.add(pSongName)
        
    def clear(self):
        self.mpdClient.clear()
    
    def getPossibleValueForTag(self, tag):
        return self.mpdClient.list(tag)
    
    def idle(self):
        self.ensureWorkingConnection()
        self.mpdClient.idle('player')
        
    def getPlayListLength(self):
        result = self.mpdClient.status()['playlistlength']
        return int(result)
        
    
    def getCurrentSongNumber(self):
        status = self.mpdClient.status()
        if status['state'] == 'play':
            result = int(self.mpdClient.status()['song'])
        else:
            result = - 1
        return result
    
    def isPlaying(self):
        status = self.mpdClient.status()
        result = status['state'] == 'play'
        return result;
    
    def setMPDToRunMPDJ(self):
        self.mpdClient.crossfade(8)
        self.mpdClient.random(0)
        self.mpdClient.replay_gain_mode('track')
        
    def addSongToPlaylist(self, pPathToFile):
        self.ensureWorkingConnection()
        self.mpdClient.add(pPathToFile)
        
    
    def ensureIsPlaying(self):
        status = self.mpdClient.status()
        if status['state'] != 'play':
            self.mpdClient.play()
    
    def getFilesMatchingCriteria(self, thingsToFind : dict):
        self.ensureWorkingConnection()
        results = self.mpdClient.find(*sum(thingsToFind.items(),()) )
        return results
    