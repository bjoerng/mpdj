'''
Created on 07.02.2021

@author: Bjoern Graebe
'''
from PyQt5.Qt import QMenu, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class CriteriaTable(QTableWidget):
    '''
    Displays criterias and offers capabilities to add, change and
    delete criterias.
    '''

    def copy_row(self, p_source_row : int, p_destination_row : int):
        """Copy content from row p_source_row to row p_destination_row"""
        for column in range(0,self.columnCount()):
            if self.item(p_source_row, column) is None:
                continue
            copy_value = self.item(p_source_row, column).text()
            if self.item(p_destination_row, column) is None:
                self.setItem(p_destination_row, column, QTableWidgetItem())
            self.item(p_destination_row,column).setText(copy_value)

    def show_header_right_click_menu(self, position):
        """Displays menu for actions on criterias."""
        menu = QMenu()
        action_remove_criteria = menu.addAction('Remove criteria')
        action_copy_criteria = menu.addAction('Copy criteria')
        action = menu.exec_(self.mapToGlobal(position))
        logical_index_y = self.vertical_headers.logicalIndexAt(position.y())
        if action == action_remove_criteria:
            self.removeRow(logical_index_y)
        if action == action_copy_criteria:
            self.insertRow(logical_index_y + 1)
            self.copy_row(logical_index_y, logical_index_y + 1)

    def __init__(self):
        '''
        Constructor
        '''
        QTableWidget.__init__(self)
        self.horizontal_headers = self.horizontalHeader()
        self.vertical_headers = self.verticalHeader()
        self.vertical_headers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.vertical_headers.customContextMenuRequested.connect(
            self.show_header_right_click_menu)
