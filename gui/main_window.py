'''
Created on 10.10.2020

@author: hiroaki
'''
from PyQt5.Qt import QMainWindow
from gui.selection_window import SelectionWindow
from gui.connection_table import ConnectionTableWidget
class MainWindowMPDJ(QMainWindow):
    '''
    classdocs
    '''
    def openSelectionWindow(self):
        self.openedSelectionWindow = SelectionWindow()
        self.openedSelectionWindow.show()
        
    def show(self):
        QMainWindow.showMaximized(self)
        
        
    def __init__(self):
        '''
        Constructor
        '''
        QMainWindow.__init__(self)
        self.setWindowTitle('MPDJ')
        
        self.connectionTable = ConnectionTableWidget()
        self.setCentralWidget(self.connectionTable)
        
        self.menuBar = self.menuBar()
        self.menuFile = self.menuBar.addMenu('File')
        self.menuSelection =self.menuBar.addMenu('Selections')
        self.actionAddSelection = self.menuSelection.addAction('Add Selection')
        self.actionAddSelection.triggered.connect(self.openSelectionWindow)
                self.setMenuBar(self.menuBar)
        

        