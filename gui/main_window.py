'''
Created on 10.10.2020

@author: Bjoern Graebe
'''
from PyQt5.Qt import QMainWindow, QFileDialog, QMessageBox, QDockWidget,\
    QCheckBox,QFormLayout,QLabel,QWidget, QLineEdit,QIntValidator, QComboBox
from PyQt5.QtCore import Qt
from gui.selection_window import SelectionWindow
from gui.connection_table import ConnectionTableWidget
from control.global_properties import GlobalProperties
from model.constants import FILE_SUFFIX
from model.mpdj_data import UnitPerBodeTouch
import sys


class MainWindowMPDJ(QMainWindow):
    '''
    classdocs
    '''
    def openSelectionWindow(self):
        self.openedSelectionWindow = SelectionWindow()
        self.openedSelectionWindow.show()
        
    def show(self):
        QMainWindow.showMaximized(self)
        
        
    def update(self):
        gp = GlobalProperties.getInstance()
        self.tfMinPerSelection.setText(str(gp.mpdjData.minUnitsPerNodeTouch))
        self.tfMaxPerSelection.setText(str(gp.mpdjData.maxUnitsPerNodeTouch))
        textToFind = gp.mpdjData.unitPerNodeTouch.guiRepresentation()
        index = self.comboBoxMinutesOrTitles.findText(textToFind, Qt.MatchFixedString)
        self.comboBoxMinutesOrTitles.setCurrentIndex(index)
        self.limitArtistPlayChkBox.setChecked(gp.mpdjData.limitArtistinNodeTouch)
        self.chkBoxGraphIsDirected.setChecked(gp.mpdjData.graphIsDirected)
        self.setWindowTitle('MPDJ: {}'.format(gp.pathOfCurrentFile))
        
    
    def writeMinPerNoteToMPDJ(self):
        gp = GlobalProperties.getInstance()
        gp.mpdjData.minUnitsPerNodeTouch = int(self.tfMinPerSelection.text())

        
    def writeMaxPerNoteToMPDJ(self):
        gp = GlobalProperties.getInstance()
        gp.mpdjData.maxUnitsPerNodeTouch = int(self.tfMaxPerSelection.text())
        
    def writeUnitPerNodeTouchtoMPDJ(self):
        gp = GlobalProperties.getInstance()
        selectionText = self.comboBoxMinutesOrTitles.currentText()
        gp.mpdjData.unitPerNodeTouch = UnitPerBodeTouch[selectionText.upper()]
        
    def writeLimitArtistsPlayedToMPDJ(self):#
        gp = GlobalProperties.getInstance()
        state = self.limitArtistPlayChkBox.isChecked()
        gp.mpdjData.limitArtistinNodeTouch = state
        
    def writeGraphIsDirectedoMPDJ(self):
        gp = GlobalProperties.getInstance()
        state = self.chkBoxGraphIsDirected.isChecked()
        gp.mpdjData.graphIsDirected = state
        

    def file_dialog(self,loadSaveType=QFileDialog.AcceptSave):
        fileSaveDialog = QFileDialog(self)
        fileSaveDialog.setFileMode(QFileDialog.AnyFile)
        fileSaveDialog.setAcceptMode(loadSaveType)
        fileSaveDialog.setNameFilters(["MPDJ files (*.{})".format(FILE_SUFFIX)])
        fileSaveDialog.selectNameFilter("MPDJ files (*.{})".format(FILE_SUFFIX))
        fileSaveDialog.setDefaultSuffix((FILE_SUFFIX))
        fileSaveDialog.exec_()
        fileNames = fileSaveDialog.selectedFiles()
        if len (fileNames) != 1:
            messageBox = QMessageBox()
            messageBox.setText('Please select only one file!')
            messageBox.setWindowTitle('Save error.')
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIcon(QMessageBox.Information)
            messageBox.exec_()
            return
        return fileNames[0]
    
    def newMPDJData(self):
        gp = GlobalProperties.getInstance()
        gp.newMPDJ()

    def file_save_as(self):
        fileName = self.file_dialog(loadSaveType = QFileDialog.AcceptSave)
        self.saveMPDJDataToFile(fileName)


    def saveMPDJDataToFile(self, pFileName : str):
        try:
            gp = GlobalProperties.getInstance()
            gp.saveMPDJDataToFile(pFileName)
            self.statusBar().showMessage('Saved to {}'.format(pFileName), 5000)
        except (OSError, IOError) as e:
            messageBox = QMessageBox()
            messageBox.setText('Error saving the file: {}'.format(str(e)))
            messageBox.setWindowTitle('Song selection will not be added.')
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.exec_()
            
        
    def file_save(self):
        gp = GlobalProperties.getInstance()
        self.saveMPDJDataToFile(gp.pathOfCurrentFile)
        
    def file_load(self):
        gp = GlobalProperties.getInstance()
        fileName = self.file_dialog(loadSaveType = QFileDialog.AcceptOpen)
        gp.loadMPDJDataToFile(fileName)
        


    def __init__(self):
        '''
        Constructor
        '''
        QMainWindow.__init__(self)
        gp = GlobalProperties.getInstance()
        
        self.connectionTable = ConnectionTableWidget()
        gp.addListener(self.connectionTable)
        self.setCentralWidget(self.connectionTable)

        
        self.menuBar = self.menuBar()
        self.menuFile = self.menuBar.addMenu('File')
        self.menuFile.addAction('New',self.newMPDJData)
        self.menuFile.addAction('Open', self.file_load)
        self.menuFile.addSeparator()
        self.menuFile.addAction('Save', self.file_save)
        self.menuFile.addAction('Save as', self.file_save_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction('Exit',sys.exit)

        
        self.menuSelection =self.menuBar.addMenu('Selections')
        self.actionAddSelection = self.menuSelection.addAction('Add Selection')
        self.actionAddSelection.triggered.connect(self.openSelectionWindow)
        self.setMenuBar(self.menuBar)
        self.statusBar().showMessage('Welcome to mpdj!', 5000)
        
        self.mpdjOptionsDock = QDockWidget("MPDJ Options Panel", self)
        self.mpdjOptionsDockLayout = QFormLayout()
        self.mpdjDockedWidget = QWidget()

        self.tfMinPerSelection = QLineEdit()
        self.tfMinPerSelection.setValidator(QIntValidator())
        self.mpdjOptionsDockLayout.addRow('Min per Node touch:', self.tfMinPerSelection)
        self.tfMinPerSelection.editingFinished.connect(self.writeMinPerNoteToMPDJ)
        
        self.tfMaxPerSelection = QLineEdit()
        self.tfMaxPerSelection.setValidator(QIntValidator())
        self.mpdjOptionsDockLayout.addRow('Max per Node touch:', self.tfMaxPerSelection)
        self.tfMaxPerSelection.editingFinished.connect(self.writeMaxPerNoteToMPDJ)
        
        self.comboBoxMinutesOrTitles = QComboBox()
        for strRept in UnitPerBodeTouch:
            self.comboBoxMinutesOrTitles.addItem(strRept.guiRepresentation())
        self.mpdjOptionsDockLayout.addRow('Unit:', self.comboBoxMinutesOrTitles)
        self.comboBoxMinutesOrTitles.currentTextChanged.connect(self.writeUnitPerNodeTouchtoMPDJ)
        
        self.mpdjDockedWidget.setLayout(self.mpdjOptionsDockLayout)
        self.mpdjOptionsDock.setWidget(self.mpdjDockedWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.mpdjOptionsDock)

        self.limitArtistPlayChkBox = QCheckBox()
        self.limitArtistPlayChkBox.stateChanged.connect(self.writeLimitArtistsPlayedToMPDJ)
        self.mpdjOptionsDockLayout.addRow(QLabel('Artist only once per node crossing'), self.limitArtistPlayChkBox)

        self.chkBoxGraphIsDirected = QCheckBox()
        self.chkBoxGraphIsDirected.stateChanged.connect(self.writeGraphIsDirectedoMPDJ)
        self.mpdjOptionsDockLayout.addRow(QLabel('Graph is directed'), self.chkBoxGraphIsDirected)

        gp.addListener(self)
        self.update()

        