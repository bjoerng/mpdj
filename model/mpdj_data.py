'''
Created on 20.09.2020

@author: hiroaki
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
        
        def playTitle(pArtist : str, pTitle : str):
            if not pArtist in self.playedArtists:
                newArtist = Artist(pArtist)
                newArtist.playTitle(pTitle)
            self.playedArtists[pArtist] = newArtist

        def getPlayCountArtist(pArtist : str):
            if pArtist in self.playedArtists:
                return self.playedArtists.__getitem__()
            else:
                return 0

        def getPlayCountTitle(pArtist : str, pTitle : str):
            if pArtist in self.playedArtists:
                return pTitle in self.playedArtists.getPlayCountForTitle(pTitle)
            else:
                return 0
            
        def addSongSelection(self, pSongSelection):
            self.songSelections.append(pSongSelection)
