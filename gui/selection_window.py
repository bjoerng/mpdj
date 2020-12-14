# -*- coding: UTF-8 -*-
'''
Created on 12.09.2020

@author: Bjoern Graebe
'''
from enum import Enum
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QLabel,QMessageBox
from model.song_selection import SongSelection
from PyQt5.Qt import QLineEdit, QHBoxLayout, Qt, QTableWidgetItem
from control.global_properties import GlobalProperties

PLUSBUTTONWITH = 50

class WindowMode(Enum):
    new = 1
    edit = 2

def addEmptyRowToTable(pInOutTable : QTableWidget):
    rowCount = pInOutTable.rowCount()
    pInOutTable.insertRow(rowCount)
    
def clearTable(pINOutTable : QTableWidget):
    pINOutTable.setRowCount(0)
    pINOutTable.setRowCount(1)
    
def fillCriteriaTableWithData(pTable : QTableWidget, pCriteriaList):
    criteriaCount = len(pCriteriaList)
    pTable.setRowCount(criteriaCount)
    row = 0
    for criteria in pCriteriaList:
        for i in range(0,pTable.columnCount()):
            header = pTable.horizontalHeaderItem(i).text()
            if header in criteria:
                if pTable.item(row,i) == None:
                    pTable.setItem(row,i,QTableWidgetItem())
                pTable.item(row,i).setText(criteria[header])
        row += 1

class SelectionWindow(QWidget):
    '''
    Display a window to create a selection of music-title.
    '''

    def __init__(self, pSongSelectionName='',pMode=WindowMode.new,
                 ):
        
        QWidget.__init__(self)
        
        self.windowMode = pMode
        self.songSelectionNameToEdit = pSongSelectionName
        self.possibleTags = list(map(lambda tagType: tagType.lower(),
                                     GlobalProperties.getInstance().mpdConnection.getPossibleTags()))
        self.window = QWidget()
        if pMode == WindowMode.new:
            self.window.setWindowTitle('Create selection')
        else:
            self.window.setWindowTitle('Change selection')
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
        self.prepareTableFromTags(self.selectionWhiteListTable, self.possibleTags)
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
        self.prepareTableFromTags(self.selectionBlackListTable, self.possibleTags)
        self.mainLayout.addWidget(self.selectionBlackListTable)
        
        if(self.windowMode == WindowMode.edit):
            self.fillFromExistingSongSelection(self.songSelectionNameToEdit)
        
        self.btAddLineToBlackListTableLayout=QHBoxLayout()
        self.btAddLineToBlackListTableLayout.setAlignment(Qt.AlignRight)
        self.btAddLineToBlackListTable = QPushButton('\N{heavy plus sign}')
        self.btAddLineToBlackListTable.clicked.connect(lambda:self.addRowToBlackListTable())
        self.btAddLineToBlackListTable.setMaximumWidth(PLUSBUTTONWITH)
        self.btAddLineToBlackListTableLayout.addWidget(self.btAddLineToBlackListTable)
        self.mainLayout.addLayout(self.btAddLineToBlackListTableLayout)
        
        self.buttonBottomLayout=QHBoxLayout()
        self.buttonBottomLayout.setAlignment(Qt.AlignRight)
        self.btClose = QPushButton('Close')
        self.btClose.clicked.connect(lambda: self.close())
        btAddSaveText = ''
        if self.windowMode == WindowMode.new:
            btAddSaveText = 'Add'
        elif self.windowMode == WindowMode.edit:
            btAddSaveText = 'Save'
        self.btAddSave = QPushButton(btAddSaveText)
        self.btAddSave.clicked.connect(lambda: self.addSaveButtonClicked())
        self.buttonBottomLayout.addWidget(self.btClose)
        self.buttonBottomLayout.addWidget(self.btAddSave)
        self.mainLayout.addLayout(self.buttonBottomLayout)
        
        self.window.setLayout(self.mainLayout)
        
    def createSelectionFromTable(self, pTable : QTableWidget):
        tableRowCount = pTable.rowCount()
        criteriaList = []
        for i in range(tableRowCount):
            newCriteria = self.createSelectionCriteriaFromRowInTable(pTable, i)
            if newCriteria:
                criteriaList.append(newCriteria)
        return criteriaList
            
            
    def createSelectionCriteriaFromRowInTable(self, pTable : QTableWidget ,pRow): 
        tableColumnCount = pTable.columnCount()
        selectionCriteria = dict()
        for i in range(tableColumnCount):
            tagValueItem = pTable.item(pRow, i)
            if tagValueItem and tagValueItem.text() != '':
                tagType = pTable.horizontalHeaderItem(i).text().lower() # TODO Fehlerfall, leere Überschrift abfangen
                selectionCriteria[tagType] = tagValueItem.text()
        return selectionCriteria
   
    def prepareTableFromTags(self, pTable : QTableWidget, pTags):
        pTable.setRowCount(1)
        pTable.setColumnCount(len(pTags))
        pTable.setHorizontalHeaderLabels(pTags)
        
    def addSaveButtonClicked(self):
        gp = GlobalProperties.getInstance()
        selectionName = self.tfSelectionName.text()
        if ( self.windowMode == WindowMode.new
        or WindowMode == WindowMode.edit
        and self.songSelectionNameToEdit != selectionName ):
            if gp.mpdjData.selectionWithNameExists(selectionName):
                messageBox = QMessageBox()
                messageBox.setText('A Selection with the name {} already exists.'.format(selectionName))
                messageBox.setWindowTitle('Song selection will not be added.')
                messageBox.setStandardButtons(QMessageBox.Ok)
                messageBox.setIcon(QMessageBox.Information)
                messageBox.exec_()
                return
        songSelection = SongSelection(selectionName)
        whiteListCriterias = self.createSelectionFromTable(self.selectionWhiteListTable)
        songSelection.setWhiteListCriterias(whiteListCriterias)
        blackListCriterias = self.createSelectionFromTable(self.selectionBlackListTable)
        songSelection.setBlackListCriterias(blackListCriterias)
        
        if self.windowMode == WindowMode.new:
            gp.mpdjData.addSongSelection(songSelection)
        if self.windowMode == WindowMode.edit:
            gp.mpdjData.changeSongSelection(self.songSelectionNameToEdit,songSelection)
        gp.informUpdateListener()
        clearTable(self.selectionWhiteListTable)
        clearTable(self.selectionBlackListTable)
        self.tfSelectionName.setText('')
        

    def addRowToWhiteListTable(self):
        addEmptyRowToTable(self.selectionWhiteListTable)

    def addRowToBlackListTable(self):
        addEmptyRowToTable(self.selectionBlackListTable)
        
    def fillFromExistingSongSelection(self, pSongSelectionName):
        self.tfSelectionName.setText(pSongSelectionName)
        gp = GlobalProperties.getInstance()
        songSelection = gp.mpdjData.getSongSelectionByName(pSongSelectionName)
        whiteListCriterias = songSelection.listOfWhiteListCriterias
        blackListCriterias = songSelection.listOfBlackListCriterias
        fillCriteriaTableWithData(self.selectionWhiteListTable,whiteListCriterias)
        fillCriteriaTableWithData(self.selectionBlackListTable, blackListCriterias)
        
    def show(self):
        #self.window.show()
        self.window.showMaximized()
        
    def close(self):
        print ("Closing")
        print (super().close())
