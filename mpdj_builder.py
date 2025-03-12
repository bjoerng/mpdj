#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 12.09.2020

@author: Bjoern Graebe
'''

from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindowMPDJ
import atexit
import jsonpickle

from control.global_properties import GlobalProperties

def exit_handler():
    gp = GlobalProperties.get_instance()
    gp.configuration
    
    print("Exiting")


if __name__ == '__main__':
    # Simply start the MPDJ builder
    atexit.register(exit_handler)
    qtApp = QApplication([])
    mw = MainWindowMPDJ()
    mw.show()
    qtApp.exec()
