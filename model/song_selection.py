'''
Created on 13.09.2020

@author: Bjoern Graebe
'''
from model.mpd_connection import MPDConnection

def isSongMatchingCriteria(pSong : dict, pCriteria : dict) -> bool :
    """Indicates if pSong is matched by pCriteria"""
    if len(pCriteria) == 0:
        return False
    for key in pCriteria:
        if pSong[key] == None or pSong[key] != pCriteria[key]:
            return False
    return True
    
def filterBlackListedSongsFromSet(pInOutSongList : list,
                                  pListOfBlacklistCriterieas):
    """Filters all songs which meet a criteria in pListOfBlacklistCriterias.
    This changes the contents of pInOutSongList."""
    for song in pInOutSongList:
        for criteria in pListOfBlacklistCriterieas:
            if isSongMatchingCriteria(song, criteria):
                pInOutSongList.remove(song)

class SongSelection(object):
    '''
    This class represents a song selection, this means it contains a
    whitelist and a blacklist of criterias and is able to get matcvhing
    songs from a mpd connection.
    '''

    def __init__(self, pName):
        self.listOfWhiteListCriterias = []
        self.listOfBlackListCriterias = []
        self.name = pName
        
    def setWhiteListCriterias(self, pWhiteListCriterias : list):
        """Set the whitelist criterias to pWhiteListCriterias."""
        self.listOfWhiteListCriterias = pWhiteListCriterias
        
    def addWhiteListCriteria(self, pCriteria: dict):
        """Add a new white list criteria to the existing list."""
        self.listOfWhiteListCriterias += pCriteria
        
    def setBlackListCriterias(self, pBlackListCriterias : list):
        """Add a new whtie list criteria to the existing list."""
        self.listOfBlackListCriterias = pBlackListCriterias
        
    def addBlackListCriterias(self, pCriteria: dict):
        """Add a new black list criteria to the existing list."""
        self.listOfBlackListCriterias += pCriteria
        

    def getSongsMatchingWhitelistFromMPDConnection(
            self,pMPDConnection : MPDConnection) -> list:
        """Retrieves the songs matching on the the white list criterias in
        self.listOfWhiteListCriterias."""
        results = []
        for criteria in self.listOfWhiteListCriterias:
            criteriaResults = pMPDConnection.getFilesMatchingCriteria(criteria)
            results += criteriaResults
        return results
        
    def getSongs(self,pMPDConnection) -> list():
        """Retrieves the songs which match on of the whitelist criterias,
        filtern out those songs matched by one blacklist criteria."""
        songResultList = self.getSongsMatchingWhitelistFromMPDConnection(
            pMPDConnection)
        print('sonResultList: {}'.format(str(songResultList)))
        filterBlackListedSongsFromSet(songResultList, self.listOfBlackListCriterias)
        print('sonResultList: {}'.format(str(songResultList)))
        return songResultList
        
        
    def __str__(self) -> str:
        """ Returns the string representation of a song selection."""
        return self.name.__str__() + '\n' + 'Whiteliste:\n'
        + self.listOfWhiteListCriterias.__str__() + '\nBlacklist:\n'
        + self.listOfBlackListCriterias.__str__()
    
    def getName(self):
        """Returns the name of the song selection."""
        return self.name
    
    def __repr__(self):
        """ Returns a string representation of an object of this type."""
        return "Name: " + self.name + ", WhiteList: "
        + self.listOfWhiteListCriterias.__repr__() + ", BlackList: "
        + self.listOfBlackListCriterias.__repr__()