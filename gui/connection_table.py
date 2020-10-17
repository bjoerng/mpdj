'''
Created on 11.10.2020

@author: hiroaki
'''
from PyQt5.Qt import QTableWidget
from control.global_properties import GlobalProperties

class ConnectionTableWidget(QTableWidget):
    '''
    classdocs
    '''
    def update(self):
        gp = GlobalProperties.getInstance()
        selectionCount = len(gp.mpdjData.songSelections)
        self.setColumnCount(selectionCount)
        self.setRowCount(selectionCount)
        for selection in gp.mpdjData.songSelections:
            

    def __init__(self):
        '''
        Constructor
        '''
        QTableWidget.__init__(self)