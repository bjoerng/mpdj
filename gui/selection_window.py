# -*- coding: UTF-8 -*-
'''
Created on 12.09.2020

@author: Bjoern Graebe
'''
from enum import Enum
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QLabel,QMessageBox
from PyQt5.Qt import QLineEdit, QHBoxLayout, Qt, QTableWidgetItem
from model.song_selection import SongSelection
from control.global_properties import GlobalProperties

PLUSBUTTONWITH = 50

class WindowMode(Enum):
    """This Enum represents the Mode of the selection window.
        New and edit are supported by now."""
    new = 1
    edit = 2

def add_empty_row_to_table(p_in_out_table : QTableWidget):
    """Adds an empty row to the table given in p_in_out_table"""
    row_count = p_in_out_table.rowCount()
    p_in_out_table.insertRow(row_count)

def clear_table(p_in_out_table : QTableWidget):
    """Clears the given table."""
    p_in_out_table.set_row_count(0)
    p_in_out_table.set_row_count(1)

def fill_criteria_table_with_data(p_table : QTableWidget, p_criteria_list):
    """Fills the given table in p_table with the criterias given
        in p_criteria_list."""
    criteria_count = len(p_criteria_list)
    p_table.set_row_count(criteria_count)
    row = 0
    for criteria in p_criteria_list:
        for i in range(0,p_table.columnCount()):
            header = p_table.horizontal_header_item(i).text()
            if header in criteria:
                if p_table.item(row,i) is None:
                    p_table.setItem(row,i,QTableWidgetItem())
                p_table.item(row,i).setText(criteria[header])
        row += 1

def create_selection_criteria_from_row_in_table(p_table : QTableWidget ,p_row):
    """Creates a selections criteria of the p_row of p_table
        and return the new criteria as a dict."""
    table_column_count = p_table.columnCount()
    selection_criteria = dict()
    for i in range(table_column_count):
        tag_value_item = p_table.item(p_row, i)
        if tag_value_item and tag_value_item.text() != '':
            tag_type = p_table.horizontal_header_item(i).text().lower()
            # TODO Fehlerfall, leere Überschrift abfangen
            selection_criteria[tag_type] = tag_value_item.text()
    return selection_criteria

def create_selection_from_table( p_table : QTableWidget):
    """Take p_table and creates a list of song selection
        criterias which is returned."""
    table_row_count = p_table.rowCount()
    criteria_list = []
    for i in range(table_row_count):
        new_criteria = create_selection_criteria_from_row_in_table(p_table, i)
        if new_criteria:
            criteria_list.append(new_criteria)
    return criteria_list

def prepare_table_from_tags(p_table : QTableWidget, p_tags):
    """Prepares the p_table with the tags given by p_tags."""
    p_table.set_row_count(1)
    p_table.set_column_count(len(p_tags))
    p_table.set_horizontal_header_labels(p_tags)

class SelectionWindow(QWidget):
    """Displays a window to create a selection of music-title."""

    def __init__(self, p_song_selection_name='',p_mode=WindowMode.new):

        QWidget.__init__(self)

        self.window_mode = p_mode
        self.song_selection_name_to_edit = p_song_selection_name
        self.possible_tags\
            = list(map(lambda tagType: tagType.lower(),
                    GlobalProperties.get_instance().mpd_connection.get_possible_tags()))
        if p_mode == WindowMode.new:
            self.setWindowTitle('Create selection')
        else:
            self.setWindowTitle('Change selection')
        self.main_layout = QVBoxLayout()

        self.input_name_layout = QHBoxLayout()
        self.label_name_display = QLabel()
        self.label_name_display.setText('Name:')
        self.label_name_display.setAlignment(Qt.AlignRight)
        self.input_name_layout.addWidget(self.label_name_display)
        self.tf_selection_name = QLineEdit()
        self.input_name_layout.addWidget(self.tf_selection_name)
        self.main_layout.addLayout(self.input_name_layout)

        self.label_white_list_criterias = QLabel()
        self.label_white_list_criterias.setText('White list criterias:')
        self.main_layout.addWidget(self.label_white_list_criterias)
        self.selection_white_list_table = QTableWidget()
        self.prepare_table_from_tags(self.selection_white_list_table, self.possible_tags)
        self.main_layout.addWidget(self.selection_white_list_table)

        self.bt_add_line_to_white_list_table_layout = QHBoxLayout()
        self.bt_add_line_to_white_list_table_layout.setAlignment(Qt.AlignRight)

        self.bt_del_line_white_list_table = QPushButton('\N{heavy minus sign}')
        self.bt_del_line_white_list_table.clicked.connect(self.add_row_to_white_list_table)
        self.bt_del_line_white_list_table.setMaximumWidth(PLUSBUTTONWITH)
        self.bt_add_line_to_white_list_table_layout.addWidget(self.bt_del_line_white_list_table)

        self.bt_add_line_to_whitef_list_table = QPushButton('\N{heavy plus sign}')
        self.btAddLineToWhiteListTable.clicked.connect(self.add_row_to_white_list_table)
        self.btAddLineToWhiteListTable.setMaximumWidth(PLUSBUTTONWITH)
        self.bt_add_line_to_white_list_table_layout.addWidget(self.btAddLineToWhiteListTable)
        self.main_layout.addLayout(self.bt_add_line_to_white_list_table_layout)

        self.label_black_list_criterias = QLabel()
        self.label_black_list_criterias.setText('Black list criterias:')
        self.main_layout.addWidget(self.label_black_list_criterias)
        self.selection_black_list_table = QTableWidget()
        self.prepare_table_from_tags(self.selection_black_list_table, self.possible_tags)
        self.main_layout.addWidget(self.selection_black_list_table)

        if self.window_mode == WindowMode.edit:
            self.fill_from_existing_song_selection(self.song_selection_name_to_edit)

        self.bt_add_line_to_black_list_table_layout = QHBoxLayout()
        self.bt_add_line_to_black_list_table_layout.setAlignment(Qt.AlignRight)
        self.bt_add_line_to_black_list_table = QPushButton('\N{heavy plus sign}')
        self.bt_add_line_to_black_list_table.clicked.connect(self.add_row_to_black_list_table)
        self.bt_add_line_to_black_list_table.setMaximumWidth(PLUSBUTTONWITH)
        self.bt_add_line_to_black_list_table_layout.addWidget(self.bt_add_line_to_black_list_table)
        self.main_layout.addLayout(self.bt_add_line_to_black_list_table_layout)

        self.button_bottom_layout = QHBoxLayout()
        self.button_bottom_layout.setAlignment(Qt.AlignRight)
        self.bt_close = QPushButton('Close')
        self.bt_close.clicked.connect(self.close)
        bt_add_save_text = ''
        if self.window_mode == WindowMode.new:
            bt_add_save_text = 'Add'
        elif self.window_mode == WindowMode.edit:
            bt_add_save_text = 'Save'
        self.bt_add_save = QPushButton(bt_add_save_text)
        self.bt_add_save.clicked.connect(self.add_save_button_clicked)
        self.button_bottom_layout.addWidget(self.bt_close)
        self.button_bottom_layout.addWidget(self.bt_add_save)
        self.main_layout.addLayout(self.button_bottom_layout)

        self.setLayout(self.main_layout)

    def add_save_button_clicked(self):
        """Is executed when the save button is clicked. Creates
            a new song selection and writes it to the mpdj.
            Clears the window afterwards."""
        global_properties = GlobalProperties.get_instance()
        selection_name = self.tf_selection_name.text()
        if ( self.window_mode == WindowMode.new
             or self.window_mode == WindowMode.edit
             and self.song_selection_name_to_edit != selection_name ):
            if global_properties.mpdj_data.selection_with_name_exists(selection_name):
                message_box = QMessageBox()
                message_box.setText(
                    'A Selection with the name {} already exists.'.format(selection_name))
                message_box.setWindowTitle('Song selection will not be added.')
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.setIcon(QMessageBox.Information)
                message_box.exec_()
                return
        song_selection = SongSelection(selection_name)
        white_list_criterias = self.create_selection_from_table(self.selection_white_list_table)
        song_selection.set_white_list_criterias(white_list_criterias)
        black_list_criterias = self.create_selection_from_table(self.selection_black_list_table)
        song_selection.set_black_list_criterias(black_list_criterias)

        if self.window_mode == WindowMode.new:
            global_properties.mpdj_data.add_song_selection(song_selection)
        if self.window_mode == WindowMode.edit:
            global_properties.mpdj_data.change_song_selection(
                self.song_selection_name_to_edit,song_selection)
        global_properties.inform_update_listener()
        clear_table(self.selection_white_list_table)
        clear_table(self.selection_black_list_table)
        self.tf_selection_name.setText('')

    def add_row_to_white_list_table(self):
        """Adds a row to the whitelist table."""
        add_empty_row_to_table(self.selection_white_list_table)

    def add_row_to_black_list_table(self):
        """Adds a row to the blacklist table."""
        add_empty_row_to_table(self.selection_black_list_table)

    def fill_from_existing_song_selection(self, p_song_selection_name):
        """Fill the white- and blacklist table from the SongSelection,
        with the name p_song_selection."""
        self.tf_selection_name.setText(p_song_selection_name)
        global_properties = GlobalProperties.get_instance()
        song_selection = global_properties.mpdj_data.get_song_selection_by_name(
            p_song_selection_name)
        white_list_criterias = song_selection.list_of_white_list_criterias
        black_list_criterias = song_selection.list_of_black_list_criterias
        fill_criteria_table_with_data(self.selection_white_list_table,white_list_criterias)
        fill_criteria_table_with_data(self.selection_black_list_table, black_list_criterias)

    def show(self):
        """Shows the window maximized."""
        #self.window.show()
        self.showMaximized()
