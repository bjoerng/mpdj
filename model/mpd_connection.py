'''
Created on 12.09.2020

@author: hiroaki
'''
class CannotConnectToMPDError(Exception):
    pass

from mpd import MPDClient

class MPDConnection(object):
    def __init__(self,pHost,pPort):
        self.host = pHost
        self.port = pPort
        self.mpdClient = MPDClient()
        self.mpdClient.timeout = 3600

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
    
    def getPossibleValueForTag(self, tag):
        return self.mpdClient.list(tag)
    
    def getFilesMatchingCriteria(self, thingsToFind : dict):
        self.ensureWorkingConnection()
        results = self.mpdClient.find(*sum(thingsToFind.items(),()) )
        return results