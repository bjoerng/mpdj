'''
Created on 11.10.2020

@author: Bjoern Graebe
'''
from PyQt5.Qt import QTableWidget, QComboBox, QMenu, QLabel, QPushButton
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
        self.setColumnCount(selectionCount + 1)
        self.setRowCount(selectionCount + 1)
        headerNames = gp.mpdjData.getSongSelectionNames()
        headerNames.sort()
        headerNames.append('neighbours')
        self.setRowCount(len(headerNames))
        self.setColumnCount(len(headerNames))
        self.setHorizontalHeaderLabels(headerNames)
        self.setVerticalHeaderLabels(headerNames)
        self.initiateComboBoxes()
        self.updateNeighbourCount()
        
    def initiateComboBoxes(self):
        columnCount = self.columnCount()
        rowCount = self.rowCount()
        self.blockSignals(True)
        gp = GlobalProperties.getInstance()
        for c in range(0,columnCount - 1):
            for r in range(0,rowCount - 1):
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
                newComboBox.currentIndexChanged.connect(self.artistConnectionComboBoxChanged_indexchanged)
                self.setCellWidget(r,c, newComboBox)
        self.blockSignals(False)
        
    def artistConnectionComboBoxChanged_indexchanged(self):
        comboBox = self.sender()
        row = comboBox.property('row')
        column = comboBox.property('column')
        artistConnectionValue = int(comboBox.currentText())
        artistRow = self.horizontalHeaderItem(column).text()
        artistcolumn = self.verticalHeaderItem(row).text()
        gp = GlobalProperties.getInstance()
        gp.mpdjData.setConnected(artistcolumn,artistRow,artistConnectionValue)
        gp.informUpdateListener()
        
    
    def updateNeighbourCountRow(self):
        columnCount = self.columnCount()
        for column in range(0,columnCount-1):
            neighbourCount = 0
            rowCount = self.rowCount()
            for row in range(0,  rowCount - 1):
                neighbourCount += int(self.cellWidget(column,row).currentText())
            if not isinstance(self.cellWidget(column, rowCount), QLabel):
                self.setCellWidget(column, rowCount - 1, QLabel())
            self.cellWidget(column, columnCount - 1).setText(str(neighbourCount))
    
    def updateNeighbourCountColumn(self):
        rowCount = self.rowCount()
        for row in range(0,rowCount - 1):
            neighbourCount = 0
            columnCount = self.columnCount()
            for column in range(0, columnCount - 1):
                neighbourCount += int(self.cellWidget(column,row).currentText())
            if not isinstance(self.cellWidget(rowCount - 1, row), QLabel):
                self.setCellWidget(rowCount - 1, row, QLabel())
            self.cellWidget(rowCount - 1, row).setText(str(neighbourCount))
    
    def updateNeighbourCount(self):
        self.updateNeighbourCountColumn()
        self.updateNeighbourCountRow()
    
    def showHeaderRightClickMenu(self, position):
        menu = QMenu()
        removeSelection = menu.addAction('Remove song selection')
        changeSelection = menu.addAction('Change song selection')
        action = menu.exec_(self.mapToGlobal(position))
        logicalIndexX = self.horizontalHeaders.logicalIndexAt(position.x())
        logicalIndexY = self.verticalHeaders.logicalIndexAt(position.y())
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
        