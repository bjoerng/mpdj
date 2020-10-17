# -*- coding: UTF-8 -*-
'''
Created on 12.09.2020

@author: hiroaki
'''

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QPushButton, QLabel
from model.song_selection import SongSelection
from PyQt5.Qt import QLineEdit, QHBoxLayout, Qt
from control.global_properties import GlobalProperties

PLUSBUTTONWITH = 50

def addEmptyRowToTable(pInOutTable : QTableWidget):
    rowCount = pInOutTable.rowCount()
    pInOutTable.insertRow(rowCount)
    
def clearTable(pINOutTable : QTableWidget):
    pINOutTable.setRowCount(0)
    pINOutTable.setRowCount(1)

class SelectionWindow(QWidget):
    '''
    Display a window to create a selection of music-title.
    '''

    def __init__(self):
        
        QWidget.__init__(self)
        
        self.possibleTags = list(map(lambda tagType: tagType.lower(),
                                     GlobalProperties.getInstance().connection.getPossibleTags()))
        self.window = QWidget()
        self.window.setWindowTitle('Create selection')
        self.mainLayout = QVBoxLayout()
        
        self.inputNameLayout = QHBoxLayout()
        self.labelNameDisplay = QLabel()
        self.labelNameDisplay.setText('Name:')
        self.labelNameDisplay.setAlignment(Qt.AlignRight)
        self.inputNameLayout.addWidget(self.labelNameDisplay)
        self.tfSelectionName = QLineEdit()
        self.inputNameLayout.addWidget(self.tfSelectionName)
        self.mainLayout.addLayout(self.inputNameLayout)
        
        self.labelWhiteListCriterias = QLabel()
        self.labelWhiteListCriterias.setText('White list criterias:')
        self.mainLayout.addWidget(self.labelWhiteListCriterias)
        self.selectionWhiteListTable = QTableWidget()
        self.prepateTableFromTags(self.selectionWhiteListTable, self.possibleTags)
        self.mainLayout.addWidget(self.selectionWhiteListTable)
        
        self.btAddLineToWhiteListTableLayout=QHBoxLayout()
        self.btAddLineToWhiteListTableLayout.setAlignment(Qt.AlignRight)
        
        self.btDelLineWhiteListTable = QPushButton('\N{heavy minus sign}')
        self.btDelLineWhiteListTable.clicked.connect(lambda:self.addRowToWhiteListTable())
        self.btDelLineWhiteListTable.setMaximumWidth(PLUSBUTTONWITH)
        self.btAddLineToWhiteListTableLayout.addWidget(self.btDelLineWhiteListTable)
        
        self.btAddLineToWhiteListTable = QPushButton('\N{heavy plus sign}')
        self.btAddLineToWhiteListTable.clicked.connect(lambda:self.addRowToWhiteListTable())
        self.btAddLineToWhiteListTable.setMaximumWidth(PLUSBUTTONWITH)
        self.btAddLineToWhiteListTableLayout.addWidget(self.btAddLineToWhiteListTable)
        self.mainLayout.addLayout(self.btAddLineToWhiteListTableLayout)
        
        self.labelBlackListCriterias = QLabel()
        self.labelBlackListCriterias.setText('Black list criterias:')
        self.mainLayout.addWidget(self.labelBlackListCriterias)
        self.selectionBlackListTable = QTableWidget()
        self.prepateTableFromTags(self.selectionBlackListTable, self.possibleTags)
        self.mainLayout.addWidget(self.selectionBlackListTable)
        
        self.btAddLineToBlackListTableLayout=QHBoxLayout()
        self.btAddLineToBlackListTableLayout.setAlignment(Qt.AlignRight)
        self.btAddLineToBlackListTable = QPushButton('\N{heavy plus sign}')
        self.btAddLineToBlackListTable.clicked.connect(lambda:self.addRowToBlackListTable())
        self.btAddLineToBlackListTable.setMaximumWidth(PLUSBUTTONWITH)
        self.btAddLineToBlackListTableLayout.addWidget(self.btAddLineToBlackListTable)
        self.mainLayout.addLayout(self.btAddLineToBlackListTableLayout)
        
        self.buttonBottomLayout=QHBoxLayout()
        self.buttonBottomLayout.setAlignment(Qt.AlignRight)
        self.btCancel =QPushButton('Cancel')
        self.btAdd = QPushButton('Add')
        self.btAdd.clicked.connect(lambda:self.createSongSelection())
        self.buttonBottomLayout.addWidget(self.btCancel)
        self.buttonBottomLayout.addWidget(self.btAdd)
        self.mainLayout.addLayout(self.buttonBottomLayout)
        
        self.window.setLayout(self.mainLayout)
        
    def createSelectionFromTable(self, pTable : QTableWidget):
        tableRowCount = pTable.rowCount()
        criteriaList = []
        for i in range(tableRowCount):
            newCriteria = self.createSelectionCreteriaFromRowInTable(pTable, i)
            criteriaList.append(newCriteria)
        return criteriaList
            
            
    def createSelectionCreteriaFromRowInTable(self, pTable : QTableWidget ,pRow): 
        tableColumnCount = pTable.columnCount()
        selectionCriteria = dict()
        for i in range(tableColumnCount):
            tagValueItem = pTable.item(pRow, i)
            if tagValueItem and tagValueItem.text() != '':
                tagType = pTable.horizontalHeaderItem(i).text().lower() # TODO Fehlerfall, leere Überschrift abfangen
                selectionCriteria[tagType] = tagValueItem.text()
        return selectionCriteria
   
    def prepateTableFromTags(self, pTable : QTableWidget, pTags):
        pTable.setRowCount(1)     
        pTable.setColumnCount(len(pTags))
        pTable.setHorizontalHeaderLabels(pTags)
        
    def createSongSelection(self):
        print('createSongSelection')
        selectionName = self.tfSelectionName.text()
        songSelection = SongSelection(selectionName)
        whiteListCriterias = self.createSelectionFromTable(self.selectionWhiteListTable)
        songSelection.setWhiteListCriterias(whiteListCriterias)
        blackListCriterias = self.createSelectionFromTable(self.selectionBlackListTable)
        songSelection.setBlackListCriterias(blackListCriterias)
        gp = GlobalProperties.getInstance()
        gp.mpdjData.addSongSelection(songSelection)
        clearTable(self.selectionWhiteListTable)
        clearTable(self.selectionBlackListTable)
        
    def addRowToWhiteListTable(self):
        addEmptyRowToTable(self.selectionWhiteListTable)

    def addRowToBlackListTable(self):
        addEmptyRowToTable(self.selectionBlackListTable)

    def show(self):
        #self.window.show()
        self.window.showMaximized()
        
