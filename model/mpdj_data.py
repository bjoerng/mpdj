'''
Created on 20.09.2020

@author: Bjoern Graebe
'''
from model.artist import Artist
from model.song_selection import SongSelection
#from gui.selection_window import SelectionWindow, WindowMode


class MPDJData(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.songSelections = dict()
        self.minSongsPerGenre = 1
        self.maxSongsPerGenre = 5
        self.playedArtists = dict()
        self.selectionConnections = dict()
        self.graphIsDirected = False
        
    def playTitle(self, pArtist : str, pTitle : str):
        if not pArtist in self.playedArtists:
            newArtist = Artist(pArtist)
            newArtist.playTitle(pTitle)
        self.playedArtists[pArtist] = newArtist

    def isConnected(self, pArstist1, pArtist2):
        if pArstist1 in self.selectionConnections:
            if pArtist2 in self.selectionConnections[pArstist1]:
                return self.selectionConnections[pArstist1][pArtist2]
        return 0
    
    def setConnected(self, pArtist1, pArtist2,pIsConnected,pMarkOppositDirection=True):
        if not pArtist1 in self.selectionConnections:
            self.selectionConnections[pArtist1] = dict()
        self.selectionConnections[pArtist1][pArtist2]=pIsConnected
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
        self.songSelections[pSongSelection.name]=pSongSelection
        
    def getSongSelectionNames(self):
        result = list(map(lambda songSelection: songSelection.getName(),
                          self.songSelections.values()))
        return result
    
    def selectionWithNameExists(self,pSelectionName):
        selectionNames = list(map(lambda selection: selection.getName(), self.songSelections.values()))
        return pSelectionName in selectionNames
    
    def removeSongSelectionByName(self, pSongSelectionName):
        del self.songSelections[pSongSelectionName]
        if pSongSelectionName in self.selectionConnections:
            del self.selectionConnections[pSongSelectionName]
        for selectionConnection in self.selectionConnections.values():
            if pSongSelectionName in selectionConnection:
                del selectionConnection[pSongSelectionName]

    def getSongSelectionByName(self,pSelectionName):
        if pSelectionName in self.songSelections:
            return self.songSelections[pSelectionName]
        else:
            return None

    def changeSongSelection(self, pOldName,pNewSelection : SongSelection):
        if pOldName in self.songSelections:
            del self.songSelections[pOldName]
        self.addSongSelection(pNewSelection)
        if pOldName in self.selectionConnections:
            self.selectionConnections[pNewSelection.getName()] = self.selectionConnections.pop(pOldName)
        for songSelectionName in self.selectionConnections:
            if pOldName in self.selectionConnections[songSelectionName]:
                self.selectionConnections[songSelectionName][pNewSelection.getName()] = self.selectionConnections[songSelectionName].pop(pOldName)
