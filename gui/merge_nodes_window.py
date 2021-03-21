'''
Created on 28.02.2021

@author: Bjoern Graebe
'''
from PyQt5.Qt import QWidget,QFormLayout,QComboBox,QPushButton,QLineEdit,QMessageBox
from control.global_properties import GlobalProperties
from model.mpdj_data import ConnectionMergeMode

def open_merge_node_window():
    """Creates and display a window to create or modify a selection."""
    merge_nodes_window = MergeNodeWindow()
    GlobalProperties.get_instance().opened_windows.append(merge_nodes_window)
    merge_nodes_window.show()

class MergeNodeWindow(QWidget):
    '''
    Class to display the merge nodes window.
    '''

    def ok_button_clicked(self):
        """Is executed when the OK button is clicked. Merges the two nodes."""
        node_name1 = self.combo_node1.currentText()
        node_name2 = self.combo_node2.currentText()
        if node_name1 == node_name2:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please select two different nodes")
            msg.setInformativeText("It makes to sense to merge a node with itself")
            msg.setWindowTitle("Cannot merge")
            msg.exec_()
            return
        new_name = self.tf_new_name.text()
        if new_name == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please provide the name for the resulting node.")
            msg.setInformativeText("The resulting node should have a name.")
            msg.setWindowTitle("No new name given")
            msg.exec_()
            return
        connection_mode = ConnectionMergeMode[
            self.combo_connection_transfer_mode.currentText().upper()]
        global_properties = GlobalProperties.get_instance()
        global_properties.mpdj_data.merge_two_nodes_into_one(node_name1, node_name2,
                                                             new_name, connection_mode)
        self.close()

    def __init__(self):
        '''
        Constructor
        '''
        QWidget.__init__(self)
        self.layout = QFormLayout()
        self.combo_node1 = QComboBox()
        self.layout.addRow('Node 1:', self.combo_node1)
        self.combo_node2 = QComboBox()
        self.layout.addRow('Node 2:', self.combo_node2)
        node_names = GlobalProperties.get_instance().mpdj_data.get_song_selection_names()
        self.combo_node1.addItems(node_names)
        self.combo_node2.addItems(node_names)

        self.combo_connection_transfer_mode = QComboBox()
        self.combo_connection_transfer_mode.addItems(
            [ mode.gui_representation() for mode in ConnectionMergeMode ])
        self.layout.addRow('Connection transfer mode', self.combo_connection_transfer_mode)

        self.tf_new_name = QLineEdit()
        self.layout.addRow('New name:',self.tf_new_name)

        self.button_ok = QPushButton('OK')
        self.button_ok.clicked.connect(self.ok_button_clicked)
        self.layout.addRow(self.button_ok)

        self.setWindowTitle('Merge selections')
        self.setLayout(self.layout)

    def closeEvent(self, *args, **kwargs):
        """Will be executed, when window is closed."""
        global_properties = GlobalProperties.get_instance()
        global_properties.opened_windows.remove(self)
