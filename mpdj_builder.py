#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 12.09.2020

@author: Bjoern Graebe
'''

from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindowMPDJ


if __name__ == '__main__':
    # Simply start the MPDJ builder
    qtApp = QApplication([])
    mw = MainWindowMPDJ()
    mw.show()
    qtApp.exec_()
