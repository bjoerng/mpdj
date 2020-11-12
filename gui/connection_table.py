'''
Created on 11.10.2020

@author: Bjoern Graebe
'''
from PyQt5.Qt import QTableWidget, QComboBox, QMenu
from PyQt5.QtCore import Qt
from control.global_properties import GlobalProperties
from gui.selection_window import SelectionWindow,WindowMode

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
        songSelectionNames.sort()
        numberOfSelection = len(songSelectionNames)
        self.setRowCount(numberOfSelection)
        self.setColumnCount(numberOfSelection)
        self.setHorizontalHeaderLabels(songSelectionNames)
        self.setVerticalHeaderLabels(songSelectionNames)
        self.initiateComboBoxes()
        
    def initiateComboBoxes(self):
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
        gp.informUpdateListener()
        
    
    def showHeaderRightClickMenu(self, position):
        menu = QMenu()
        removeSelection = menu.addAction('Remove song selection')
        changeSelection = menu.addAction('Change song selection')
        action = menu.exec_(self.mapToGlobal(position))
        print (position)
        logicalIndexX = self.horizontalHeaders.logicalIndexAt(position.x())
        logicalIndexY = self.verticalHeaders.logicalIndexAt(position.y())
        print ( str(logicalIndexX) + ',' + str(logicalIndexY))
        nameOfSelection = ''
        if logicalIndexX > logicalIndexY:
            nameOfSelection = self.verticalHeaderItem(logicalIndexX).text()
        else:
            nameOfSelection = self.horizontalHeaderItem(logicalIndexY).text()
        gp = GlobalProperties.getInstance()
        if action == removeSelection:
            gp.mpdjData.removeSongSelectionByName(nameOfSelection)
            gp.informUpdateListener()
        if action == changeSelection:
            selectionWindow = SelectionWindow(nameOfSelection, WindowMode.edit)
            selectionWindow.show()
            

    def __init__(self):
        '''
        Constructor
        '''
        QTableWidget.__init__(self)
        self.initiateComboBoxes()
        self.horizontalHeaders = self.horizontalHeader()
        self.horizontalHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeaders.customContextMenuRequested.connect(self.showHeaderRightClickMenu)
        self.verticalHeaders = self.verticalHeader()
        self.verticalHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeaders.customContextMenuRequested.connect(self.showHeaderRightClickMenu)
        #headers.setSelectionMode(QAbstractItemView.SingleSelection)