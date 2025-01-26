'''
Created on 15.02.2022

@author: Bjoern Graebe
'''

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QPushButton, QFormLayout, QSpinBox, QSizePolicy
from control.global_properties import GlobalProperties
from PyQt5.Qt import QLineEdit
from PyQt5 import QtGui
from gui.gui_constants import *
#from PyQt5.QtGui import QFont

class MPDConnectionWindow(QWidget):
    '''
    Display a window to represent and edit connections to MPD-Server.
    '''

    def closeEvent(self, *args, **kwargs):
        """Will be executed, when window is closed."""
        global_properties = GlobalProperties.get_instance()
        global_properties.opened_windows.remove(self)

    def __init__(self):
        '''
        Constructor
        '''
        QWidget.__init__(self)
        self.main_layout = QVBoxLayout()
        self.label_headline = QLabel()
        self.label_headline.setText('MPD Connections:')
        font = self.label_headline.font()
        font.setPointSize(14)
        font.setBold(True)
        self.main_layout.addWidget(self.label_headline)
        self.select_connection_layout = QHBoxLayout()
        self.label_connection = QLabel()
        self.label_connection.setText('Connection:')
        self.select_connection_layout.addWidget(self.label_connection)
        self.combo_connection_selection = QComboBox()
        self.combo_connection_selection.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred))
        self.select_connection_layout.addWidget(self.combo_connection_selection)
        self.bt_add_mpd_connection = QPushButton('\N{heavy plus sign}')
        self.bt_add_mpd_connection.setMaximumWidth(PLUSBUTTONWIDTH)
        self.select_connection_layout.addWidget(self.bt_add_mpd_connection)
        self.bt_remove_mpd_connection = QPushButton('\N{heavy minus sign}')
        self.bt_remove_mpd_connection.setMaximumWidth(PLUSBUTTONWIDTH)
        self.select_connection_layout.addWidget(self.bt_remove_mpd_connection)
        self.main_layout.addLayout(self.select_connection_layout)
        self.layout_connection_table = QFormLayout()
        self.tf_connection_name_input = QLineEdit()
        self.layout_connection_table.addRow("Name:", self.tf_connection_name_input)
        self.host_layout = QHBoxLayout()
        self.tf_hostname = QLineEdit()
        self.tf_port = QSpinBox()
        self.tf_port.setRange(0, 65535)
        self.host_layout.addWidget(self.tf_hostname)
        self.host_layout.addWidget(self.tf_port)
        self.layout_connection_table.addRow('Host:', self.host_layout)
        self.tf_password = QLineEdit()
        self.tf_password.setEchoMode(QLineEdit.Password)
        self.tf_password.setToolTip('Please note that the password is stored in clear text.')
        self.layout_connection_table.addRow('Password:',self.tf_password)
        self.main_layout.addLayout(self.layout_connection_table)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)
        