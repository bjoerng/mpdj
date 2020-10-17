# -*- coding: UTF-8 -*-
'''
Created on 12.09.2020

@author: Bjoern Graebe
'''

from PyQt5.Qt import QApplication

from gui.main_window import MainWindowMPDJ

if __name__ == '__main__':
    qtApp = QApplication([])
    mw = MainWindowMPDJ()
    mw.show()
    qtApp.exec_()
