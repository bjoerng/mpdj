'''
Created on 11.10.2020

@author: Bjoern Graebe
'''
from PyQt5.Qt import QTableWidget, QComboBox
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
        songSelectionNames = gp.mpdjData.getSongSelectionNames()
        numberOfSelection = len(songSelectionNames)
        self.setRowCount(numberOfSelection)
        self.setColumnCount(numberOfSelection)
        self.setHorizontalHeaderLabels(songSelectionNames)
        self.setVerticalHeaderLabels(songSelectionNames)
        self.initiateComboxBoxes()
        
    def initiateComboxBoxes(self):
        columnCount = self.columnCount()
        rowCount = self.rowCount()
        self.blockSignals(True)
        gp = GlobalProperties.getInstance()
        for c in range(0,columnCount):
            for r in range(0,rowCount):
                rowHeading = self.horizontalHeaderItem(r).text()
                columnHeading = self.verticalHeaderItem(c).text()
                isConnected = gp.mpdjData.isConnected(rowHeading,columnHeading)
                newComboBox = QComboBox()
                newComboBox.addItems(['0','1'])
                isConnectedStr = str(isConnected)
                itemIndex = newComboBox.findText(isConnectedStr)
                if itemIndex != -1:
                    newComboBox.setCurrentIndex(itemIndex)
                newComboBox.setProperty('row', r)
                newComboBox.setProperty('column',c)
                newComboBox.currentIndexChanged.connect(self.ArtistConnectionComboBoxChanged_indexchanged)
                self.setCellWidget(r,c, newComboBox)
        self.blockSignals(False)
        
    def ArtistConnectionComboBoxChanged_indexchanged(self):
        comboBox = self.sender()
        row = comboBox.property('row')
        column = comboBox.property('column')
        artistConnectionValue = int(comboBox.currentText())
        artistRow = self.horizontalHeaderItem(column).text()
        artistcolumn = self.verticalHeaderItem(row).text()
        gp = GlobalProperties.getInstance()
        gp.mpdjData.setConnected(artistcolumn,artistRow,artistConnectionValue)
        
    def __init__(self):
        '''
        Constructor
        '''
        QTableWidget.__init__(self)
        self.initiateComboxBoxes()