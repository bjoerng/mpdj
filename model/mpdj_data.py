'''
Created on 20.09.2020

@author: Bjoern Graebe
'''
from model.artist import Artist

class MPDJData(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.songSelections = []
        self.minSongsPerGenre = 1
        self.maxSongsPerGenre = 5
        self.playedArtists = dict()
        self.artistConnections = dict()
        self.graphIsDirected = False
        
    def playTitle(self, pArtist : str, pTitle : str):
        if not pArtist in self.playedArtists:
            newArtist = Artist(pArtist)
            newArtist.playTitle(pTitle)
        self.playedArtists[pArtist] = newArtist

    def isConnected(self, pArstist1, pArtist2):
        if pArstist1 in self.artistConnections:
            if pArtist2 in self.artistConnections[pArstist1]:
                return self.artistConnections[pArstist1][pArtist2]
        return 0
    
    def setConnected(self, pArtist1, pArtist2,pIsConnected,pMarkOppositDirection=True):
        if not pArtist1 in self.artistConnections:
            self.artistConnections[pArtist1] = dict()
        self.artistConnections[pArtist1][pArtist2]=pIsConnected
        if pMarkOppositDirection and not self.graphIsDirected:
            self.setConnected(pArtist2,pArtist1,pIsConnected,pMarkOppositDirection=False)

    def getPlayCountArtist(self, pArtist : str):
        if pArtist in self.playedArtists:
            return self.playedArtists.__getitem__()
        else:
            return 0

    def getPlayCountTitle(self, pArtist : str, pTitle : str):
        if pArtist in self.playedArtists:
            return pTitle in self.playedArtists.getPlayCountForTitle(pTitle)
        else:
            return 0
        
    def addSongSelection(self, pSongSelection):
        self.songSelections.append(pSongSelection)
        
    def getSongSelectionNames(self):
        result = list(map(lambda songSelection: songSelection.getName(), self.songSelections))
        return result
    
    def selectionWithNameExists(self,pSelectionName):
        selectionNames = list(map(lambda selection: selection.getName(), self.songSelections))
        return pSelectionName in selectionNames
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

