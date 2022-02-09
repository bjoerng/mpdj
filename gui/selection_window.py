'''
Created on 12.09.2020

@author: Bjoern Graebe
'''
from enum import Enum
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QLabel,QMessageBox
from PyQt5.Qt import QLineEdit, QHBoxLayout, Qt, QTableWidgetItem, QFormLayout, QIntValidator,\
    QCheckBox
from model.song_selection import SongSelection
from control.global_properties import GlobalProperties
from gui.criterias_table import CriteriaTable

PLUSBUTTONWITH = 50

class WindowMode(Enum):
    """This Enum represents the Mode of the selection window.
        New and edit are supported by now."""
    NEW = 1
    EDIT = 2

def open_selection_window(p_mode=WindowMode.NEW, p_selection_name=''):
    """Creates and display a window to create or modify a selection."""
    opened_selection_window = SelectionWindow(p_selection_name, p_mode)
    GlobalProperties.get_instance().opened_windows.append(opened_selection_window)
    opened_selection_window.show()

def add_empty_row_to_table(p_in_out_table : QTableWidget):
    """Adds an empty row to the table given in p_in_out_table"""
    row_count = p_in_out_table.rowCount()
    p_in_out_table.insertRow(row_count)

def clear_table(p_in_out_table : QTableWidget):
    """Clears the given table."""
    p_in_out_table.setRowCount(0)
    p_in_out_table.setRowCount(1)

def fill_criteria_table_with_data(p_table : QTableWidget, p_criteria_list):
    """Fills the given table in p_table with the criterias given
        in p_criteria_list."""
    criteria_count = len(p_criteria_list)
    p_table.setRowCount(criteria_count)
    row = 0
    for criteria in p_criteria_list:
        for i in range(0,p_table.columnCount()):
            header = p_table.horizontalHeaderItem(i).text()
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
            tag_type = p_table.horizontalHeaderItem(i).text().lower()
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
    p_table.setRowCount(1)
    p_table.setColumnCount(len(p_tags))
    p_table.setHorizontalHeaderLabels(p_tags)

class SelectionWindow(QWidget):
    """Displays a window to create a selection of music-title."""


    def apply_mode(self):
        """"Changes window texts according to WindowMode."""
        bt_add_save_text = ''
        if self.window_mode == WindowMode.NEW:
            bt_add_save_text = 'Add'
        elif self.window_mode == WindowMode.EDIT:
            bt_add_save_text = 'Save'
        self.bt_add_save.setText(bt_add_save_text)
        if self.window_mode == WindowMode.NEW:
            self.setWindowTitle('Create selection')
        else:
            self.setWindowTitle('Change selection')

    def __init__(self, p_song_selection_name=None,p_mode=WindowMode.NEW):

        QWidget.__init__(self)

        self.window_mode = p_mode
        if p_song_selection_name:
            self.song_selection_name_to_edit = p_song_selection_name
        else:
            self.song_selection_name_to_edit = ''
        self.possible_tags\
            = list(map(lambda tagType: tagType.lower(),
                    GlobalProperties.get_instance().mpd_connection.get_possible_tags()))
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
        self.selection_white_list_table = CriteriaTable()
        prepare_table_from_tags(self.selection_white_list_table, self.possible_tags)
        self.main_layout.addWidget(self.selection_white_list_table)

        self.bt_add_line_to_white_list_table_layout = QHBoxLayout()
        self.bt_add_line_to_white_list_table_layout.setAlignment(Qt.AlignRight)

#         self.bt_del_line_white_list_table = QPushButton('\N{heavy minus sign}')
#         self.bt_del_line_white_list_table.clicked.connect(self.add_row_to_white_list_table)
#         self.bt_del_line_white_list_table.setMaximumWidth(PLUSBUTTONWITH)
#         self.bt_add_line_to_white_list_table_layout.addWidget(self.bt_del_line_white_list_table)

        self.bt_add_line_to_white_list_table = QPushButton('\N{heavy plus sign}')
        self.bt_add_line_to_white_list_table.clicked.connect(self.add_row_to_white_list_table)
        self.bt_add_line_to_white_list_table.setMaximumWidth(PLUSBUTTONWITH)
        self.bt_add_line_to_white_list_table_layout.addWidget(self.bt_add_line_to_white_list_table)
        self.main_layout.addLayout(self.bt_add_line_to_white_list_table_layout)

        self.label_black_list_criterias = QLabel()
        self.label_black_list_criterias.setText('Black list criterias:')
        self.main_layout.addWidget(self.label_black_list_criterias)
        self.selection_black_list_table = CriteriaTable()
        prepare_table_from_tags(self.selection_black_list_table, self.possible_tags)
        self.main_layout.addWidget(self.selection_black_list_table)
        self.bt_add_line_to_black_list_table_layout = QHBoxLayout()
        self.bt_add_line_to_black_list_table_layout.setAlignment(Qt.AlignRight)
        self.bt_add_line_to_black_list_table = QPushButton('\N{heavy plus sign}')
        self.bt_add_line_to_black_list_table.clicked.connect(self.add_row_to_black_list_table)
        self.bt_add_line_to_black_list_table.setMaximumWidth(PLUSBUTTONWITH)
        self.bt_add_line_to_black_list_table_layout.addWidget(self.bt_add_line_to_black_list_table)
        self.main_layout.addLayout(self.bt_add_line_to_black_list_table_layout)

        self.duration_heading_layout = QHBoxLayout()
        self.label_duration_display = QLabel()
        self.label_duration_display.setText('Duration (in seconds) 0 means no limit:')
        self.main_layout.addWidget(self.label_duration_display, 0, Qt.AlignLeft)
        self.label_duration_display.setAlignment(Qt.AlignRight)
        self.duration_layout_min_max = QFormLayout()
        self.tf_duration_min = QLineEdit()
        self.tf_duration_min.setValidator(QIntValidator(0,2147483647))
        self.duration_layout_min_max.addRow('min:', self.tf_duration_min)
        self.tf_duration_max = QLineEdit()
        self.tf_duration_min.setValidator(QIntValidator(0,2147483647))
        self.duration_layout_min_max.addRow('max:', self.tf_duration_max)
        self.main_layout.addLayout(self.duration_layout_min_max)

        self.tf_node_min_minutes = QLineEdit()
        self.tf_node_min_minutes.setValidator(QIntValidator(0,2147483647))
        self.duration_layout_min_max.addRow('Node min. minutes:',
                                            self.tf_node_min_minutes)

        self.tf_node_max_minutes = QLineEdit()
        self.tf_node_max_minutes.setValidator(QIntValidator(0,2147483647))
        self.duration_layout_min_max.addRow('Node max. minutes:',
                                            self.tf_node_max_minutes)

        self.tf_node_max_overspill_minutes = QLineEdit()
        self.tf_node_max_overspill_minutes.setValidator(QIntValidator(0,2147483647))
        self.cb_limit_overflow = QCheckBox()
        self.cb_limit_overflow.stateChanged.connect(
            lambda: self.tf_node_max_overspill_minutes.setDisabled(
                not self.cb_limit_overflow.isChecked()))
        self.overflow_layoout = QHBoxLayout()
        self.overflow_layoout.addWidget(self.cb_limit_overflow)
        self.overflow_layoout.addWidget(self.tf_node_max_overspill_minutes)
        self.duration_layout_min_max.addRow("Limit overspill:",
                                           self.overflow_layoout)

        if self.window_mode == WindowMode.EDIT:
            self.fill_from_existing_song_selection(self.song_selection_name_to_edit)

        self.button_bottom_layout = QHBoxLayout()
        self.button_bottom_layout.setAlignment(Qt.AlignRight)
        self.bt_close = QPushButton('Close')
        self.bt_close.clicked.connect(self.close)
        self.bt_add_save = QPushButton()
        self.apply_mode()
        self.bt_add_save.clicked.connect(self.add_save_button_clicked)
        self.button_bottom_layout.addWidget(self.bt_close)
        self.button_bottom_layout.addWidget(self.bt_add_save)
        self.main_layout.addLayout(self.button_bottom_layout)
        self.setLayout(self.main_layout)


    def write_simple_fields_to_song_selection(self, song_selection):
        """Write simple fields to song_selection. The tables are handled separately."""
        if self.tf_duration_min.text():
            song_selection.min_duration = int(self.tf_duration_min.text())
        else:
            song_selection.min_duration = 0
        if self.tf_duration_max.text():
            song_selection.max_duration = int(self.tf_duration_max.text())
        else:
            song_selection.max_duration = 0
        if self.tf_node_min_minutes.text():
            song_selection.min_song_units_per_node_touch = int(
                self.tf_node_min_minutes.text())
        else:
            song_selection.min_song_units_per_node_touch = -1
        if self.tf_node_max_minutes.text():
            song_selection.max_song_units_per_node_touch = int(
                self.tf_node_max_minutes.text())
        else:
            song_selection.max_song_units_per_node_touch = -1
        song_selection.limit_overspill = self.cb_limit_overflow.isChecked()
        if self.tf_node_max_overspill_minutes.text():
            song_selection.overspill_limit = int(
                self.tf_node_max_overspill_minutes.text())
        else:
            song_selection.overspill_limit= -1

    def add_save_button_clicked(self):
        """Is executed when the save button is clicked. Creates
            a new song selection and writes it to the mpdj.
            Clears the window afterwards."""
        global_properties = GlobalProperties.get_instance()
        selection_name = self.tf_selection_name.text()
        if ( self.window_mode == WindowMode.NEW
             or self.window_mode == WindowMode.EDIT
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
        self.write_simple_fields_to_song_selection(song_selection)

        white_list_criterias = create_selection_from_table(self.selection_white_list_table)
        song_selection.set_white_list_criterias(white_list_criterias)
        black_list_criterias = create_selection_from_table(self.selection_black_list_table)
        song_selection.set_black_list_criterias(black_list_criterias)

        if self.window_mode == WindowMode.NEW:
            global_properties.mpdj_data.add_song_selection(song_selection)
        if self.window_mode == WindowMode.EDIT:
            global_properties.mpdj_data.change_song_selection(
                self.song_selection_name_to_edit,song_selection)
        global_properties.inform_update_listener()
        clear_table(self.selection_white_list_table)
        clear_table(self.selection_black_list_table)
        self.tf_selection_name.setText('')
        self.tf_duration_max.setText('0')
        self.tf_duration_min.setText('0')
        self.tf_node_max_minutes.setText('-1')
        self.tf_node_min_minutes.setText('-1')
        self.cb_limit_overflow.setChecked(True)
        self.tf_node_max_overspill_minutes.setText('0')
        self.window_mode = WindowMode.NEW
        self.apply_mode()

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
        if hasattr(song_selection, 'min_duration'):
            self.tf_duration_min.setText(str(song_selection.min_duration))
        else:
            self.tf_duration_min.setText('0')
        if hasattr(song_selection, 'max_duration'):
            self.tf_duration_max.setText(str(song_selection.max_duration))
        else:
            self.tf_duration_max.setText('0')
        if hasattr(song_selection, 'min_song_units_per_node_touch'):
            self.tf_node_min_minutes.setText(str(
                song_selection.min_song_units_per_node_touch))
        if hasattr(song_selection, 'max_song_units_per_node_touch'):
            self.tf_node_max_minutes.setText(str(
                song_selection.max_song_units_per_node_touch))
        if hasattr(song_selection, 'limit_overspill'):
            self.cb_limit_overflow.setChecked(
                song_selection.limit_overspill)
        if hasattr(song_selection, 'overspill_limit'):
            self.tf_node_max_overspill_minutes.setText(str(
                song_selection.overspill_limit))

    def closeEvent(self, *args, **kwargs):
        """Will be executed, when window is closed."""
        global_properties = GlobalProperties.get_instance()
        if self in global_properties.opened_windows:
            global_properties.opened_windows.remove(self)
