'''
Created on 13.09.2020

@author: hiroaki
'''
from control.global_properties import GlobalProperties

def isSongMatchingCriteria(pSong : dict, pCriteria : dict):
    if len(pCriteria) == 0:
        return False
    for key in pCriteria:
        if pSong[key] == None or pSong[key] != pCriteria[key]:
            return False
        
    return True
    
def filterBlackListedSongsFromSet(pInOutSongList : list, pListOfBlacklistCriterieas):
    for song in pInOutSongList:
        for criteria in pListOfBlacklistCriterieas:
            if isSongMatchingCriteria(song, criteria):
                pInOutSongList.remove(song)

class SongSelection(object):
    '''
    classdocs
    '''

    def __init__(self, pName):
        self.listOfWhiteListCriterias = []
        self.listOfBlackListCriterias = []
        self.name = pName
        self.liftOfNeibours = []
        
    def setWhiteListCriterias(self, pWhiteListCriterias : list):
        self.listOfWhiteListCriterias = pWhiteListCriterias
        
    def addWhiteListCriteria(self, pCriteria: dict):
        self.listOfWhiteListCriterias += pCriteria
        
    def setBlackListCriterias(self, pBlackListCriterias : list):
        self.listOfBlackListCriterias = pBlackListCriterias
        
    def addBlackListCriterias(self, pCriteria: dict):
        self.listOfBlackListCriterias += pCriteria
        
    def getSongsMatchingWhitelist(self):
        results = []
        connection = GlobalProperties.getInstance().mpdConnection
        for criteria in self.listOfWhiteListCriterias:
            criteriaResults = connection.getFilesMatchingCriteria(criteria)
            results += criteriaResults
        return results
        
    def getSongs(self,):
        print('getSongs')
        songResultList = self.getSongsMatchingWhitelist()
        filterBlackListedSongsFromSet(songResultList, self.listOfBlackListCriterias)
        return songResultList
        
        
    def __str__(self):
        return self.name.__str__() + '\n' + 'Whiteliste:\n' + self.listOfWhiteListCriterias.__str__() + '\nBlacklist:\n' + self.listOfBlackListCriterias.__str__()
    
    def getName(self):
        return self.name