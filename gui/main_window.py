'''
Created on 10.10.2020

@author: Bjoern Graebe
'''
from PyQt5.Qt import QMainWindow, QFileDialog, QMessageBox
from gui.selection_window import SelectionWindow
from gui.connection_table import ConnectionTableWidget
from control.global_properties import GlobalProperties
from model.constants import FILE_SUFFIX



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
        pass

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

    def file_save(self):
        gp = GlobalProperties.getInstance()
        fileName = self.file_dialog(loadSaveType = QFileDialog.AcceptSave)
        gp.saveMPDJDataToFile(fileName)
        
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
        self.setWindowTitle('MPDJ')
        
        self.connectionTable = ConnectionTableWidget()
        gp.addListener(self.connectionTable)
        self.setCentralWidget(self.connectionTable)

        
        self.menuBar = self.menuBar()
        self.menuFile = self.menuBar.addMenu('File')
        self.menuFile.addAction('Open', self.file_load)
        self.menuFile.addAction('Save', self.file_save)

        
        self.menuSelection =self.menuBar.addMenu('Selections')
        self.actionAddSelection = self.menuSelection.addAction('Add Selection')
        self.actionAddSelection.triggered.connect(self.openSelectionWindow)
        self.setMenuBar(self.menuBar)
        self.statusBar().showMessage('Welcome to mpdj!', 2000)
        

        gp.addListener(self)

        