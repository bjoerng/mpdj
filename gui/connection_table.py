'''
Created on 11.10.2020

@author: Bjoern Graebe
'''
from copy import deepcopy
from PyQt5.Qt import QTableWidget, QComboBox, QMenu, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from control.global_properties import GlobalProperties
from gui.selection_window import WindowMode,open_selection_window

def copy_selection(p_selection,p_with_connections=True):
    """Copy p_selection into a new collection and adds this to
        the selection of """
    global_properties = GlobalProperties.get_instance()
    new_selection = deepcopy(p_selection)
    copy_selection_name = new_selection.name
    copy_selection_name = copy_selection_name + " ( copy )"
    if global_properties.mpdj_data.selection_with_name_exists(copy_selection_name):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Unable to create selection_copy, name exists.")
        msg.setInformativeText(
            "{} can't be created, a selection with this name exists.".format(copy_selection_name))
        msg.setWindowTitle("MessageBox ")
        msg.setDetailedText("The details are as follows:")
    new_selection.set_name(copy_selection_name)
    global_properties.mpdj_data.add_song_selection(new_selection)
    if p_with_connections:
        neighbours = global_properties.mpdj_data.get_neighbours_for_node_name(
            p_selection.get_name())
        for neighbour in neighbours:
            global_properties.mpdj_data.set_connected(copy_selection_name,neighbour,1,False)
        all_selections = global_properties.mpdj_data.get_song_selection_names()
        for selection in all_selections:
            if global_properties.mpdj_data.is_connected(selection,
                                                        p_selection.get_name()):
                global_properties.mpdj_data.set_connected(selection,copy_selection_name,1,False)
    global_properties.inform_update_listener()

class ConnectionTableWidget(QTableWidget):
    '''
    classdocs
    '''
    def update(self):
        """Updates the view of with the current connection status of the model."""
        global_properties = GlobalProperties.get_instance()
        selection_count = len(global_properties.mpdj_data.song_selections)
        self.setColumnCount(selection_count + 1)
        self.setRowCount(selection_count + 1)
        header_names = global_properties.mpdj_data.get_song_selection_names()
        header_names.sort()
        header_names.append('neighbours')
        self.setRowCount(len(header_names))
        self.setColumnCount(len(header_names))
        self.setHorizontalHeaderLabels(header_names)
        self.setVerticalHeaderLabels(header_names)
        self.initiate_combo_boxes()
        self.update_neighbour_count()


    def initiate_combo_boxes(self):
        """Sets the horizontal and vertical headers, initiates the comboboxes
            sets the comboboxes to the right values, found in the model."""
        column_count = self.columnCount()
        row_count = self.rowCount()
        self.blockSignals(True)
        global_properrties = GlobalProperties.get_instance()
        for column in range(0,column_count - 1):
            for row in range(0,row_count - 1):
                row_heading = self.horizontalHeaderItem(row).text()
                column_heading = self.verticalHeaderItem(column).text()
                is_connected = global_properrties.mpdj_data.is_connected(row_heading,column_heading)
                new_combo_box = QComboBox()
                new_combo_box.addItems(['0','1'])
                is_connected_str = str(is_connected)
                item_index = new_combo_box.findText(is_connected_str)
                if item_index != -1:
                    new_combo_box.setCurrentIndex(item_index)
                new_combo_box.setProperty('row', row)
                new_combo_box.setProperty('column',column)
                new_combo_box.currentIndexChanged.connect(
                    self.artist_connection_combo_box_changed_indexchanged)
                self.setCellWidget(row,column, new_combo_box)
        self.blockSignals(False)

    def artist_connection_combo_box_changed_indexchanged(self):
        """This method is called when a new value is selected in one
            of the comboboxes which represent the connections."""
        combo_box = self.sender()
        row = combo_box.property('row')
        column = combo_box.property('column')
        artist_connection_value = int(combo_box.currentText())
        artist_row = self.horizontalHeaderItem(column).text()
        artist_column = self.verticalHeaderItem(row).text()
        global_properties = GlobalProperties.get_instance()
        mark_opposit_direction = not global_properties.mpdj_data.graph_is_directed
        global_properties.mpdj_data.set_connected(artist_column,artist_row,
                                                  artist_connection_value,
                                                  mark_opposit_direction)

    def update_neighbour_count_row(self):
        """This method updates the neighbour count for each row."""
        column_count = self.columnCount()
        for column in range(0,column_count-1):
            neighbour_count = 0
            row_count = self.rowCount()
            for row in range(0,  row_count - 1):
                neighbour_count += int(self.cellWidget(column,row).currentText())
            if not isinstance(self.cellWidget(column, row_count), QLabel):
                self.setCellWidget(column, row_count - 1, QLabel())
            self.cellWidget(column, column_count - 1).setText(str(neighbour_count))

    def update_neighbour_count_column(self):
        """The method updates the neighbor count for each column"""
        row_count = self.rowCount()
        for row in range(0,row_count - 1):
            neighbour_count = 0
            column_count = self.columnCount()
            for column in range(0, column_count - 1):
                neighbour_count += int(self.cellWidget(column,row).currentText())
            if not isinstance(self.cellWidget(row_count - 1, row), QLabel):
                self.setCellWidget(row_count - 1, row, QLabel())
            self.cellWidget(row_count - 1, row).setText(str(neighbour_count))

    def update_neighbour_count(self):
        """Updates the neighbour count for rows and columns."""
        self.update_neighbour_count_column()
        self.update_neighbour_count_row()
        if not isinstance(self.cellWidget(self.rowCount() - 1, self.columnCount() - 1),QLabel):
            self.setCellWidget(self.rowCount() - 1, self.columnCount() - 1,QLabel())
        self.cellWidget(self.rowCount() - 1, self.columnCount() - 1).setText('')

    def show_header_right_click_menu(self, position):
        """Display the menu for header actions."""
        menu = QMenu()

        add_selection = menu.addAction('Add selection')
        change_selection = menu.addAction('Change song selection')
        copy_selected_selection = menu.addAction('Copy song selection')
        copy_selected_selection_with_connections = menu.addAction(
            'Copy song selection with connection')
        remove_selection = menu.addAction('Remove song selection')
        action = menu.exec_(self.mapToGlobal(position))
        logical_index_x = self.horizontal_headers.logicalIndexAt(position.x())
        logical_index_y = self.vertical_headers.logicalIndexAt(position.y())
        name_of_selection = ''
        if logical_index_x > logical_index_y:
            name_of_selection = self.verticalHeaderItem(logical_index_x).text()
        else:
            name_of_selection = self.horizontalHeaderItem(logical_index_y).text()
        global_properties = GlobalProperties.get_instance()
        if action == remove_selection:
            global_properties.mpdj_data.remove_song_selection_by_name(name_of_selection)
            global_properties.inform_update_listener()
            return
        if action == change_selection:
            open_selection_window(WindowMode.EDIT, name_of_selection)
            return
        selection = global_properties.mpdj_data.get_song_selection_by_name(name_of_selection)
        if action == copy_selected_selection:
            copy_selection(selection, False)
            return
        if action == copy_selected_selection_with_connections:
            copy_selection(selection,True)
            return
        if action == add_selection:
            open_selection_window(WindowMode.NEW)

    def __init__(self):
        """Constructor"""
        QTableWidget.__init__(self)
        self.initiate_combo_boxes()
        self.horizontal_headers = self.horizontalHeader()
        self.horizontal_headers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontal_headers.customContextMenuRequested.connect(
            self.show_header_right_click_menu)
        self.vertical_headers = self.verticalHeader()
        self.vertical_headers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.vertical_headers.customContextMenuRequested.connect(self.show_header_right_click_menu)
