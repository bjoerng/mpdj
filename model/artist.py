'''
Created on 27.09.2020

@author: hiroaki
'''

class Artist(object):
    '''
    classdocs
    '''


    def __init__(self, pName):
        '''
        Constructor
        '''
        self.name = pName
        self.playCount = 0
        self.songPlayCount = dict()
        
        def __getitem__(self, pKey):
            self.songPlayCount.get(pKey, 0)
            
        def __setitem__(self, key, value):
            self.songPlayCount.__setitem__(key, value)
            
        def playTitle(self, title):
            if title in self.songPlayCount:
                self.songPlayCount[title] += 1
            else:
                self.songPlayCount[title] = 1
            self.playCount += 1

        def getPlayCountForTitle(pTitle : str):
            self.__getItem__(pTitle, 0)