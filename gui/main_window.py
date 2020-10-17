'''
Created on 10.10.2020

@author: Bjoern Graebe
'''
from PyQt5.Qt import QMainWindow
from gui.selection_window import SelectionWindow
from gui.connection_table import ConnectionTableWidget
from control.global_properties import GlobalProperties
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
        self.menuSelection =self.menuBar.addMenu('Selections')
        self.actionAddSelection = self.menuSelection.addAction('Add Selection')
        self.actionAddSelection.triggered.connect(self.openSelectionWindow)
        self.setMenuBar(self.menuBar)
        

        gp.addListener(self)

        