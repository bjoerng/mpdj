'''
Created on 10.10.2020

@author: Bjoern Graebe
'''
import sys
from PyQt5.Qt import QMainWindow, QFileDialog, QMessageBox, QDockWidget,\
    QCheckBox,QFormLayout,QLabel,QWidget, QLineEdit, QIntValidator, QComboBox
from PyQt5.QtCore import Qt

from gui.connection_table import ConnectionTableWidget
from gui.selection_window import open_selection_window, WindowMode
from gui.merge_nodes_window import open_merge_node_window
from control.global_properties import GlobalProperties, new_mpdj_data
from model.constants import FILE_SUFFIX
from model.mpdj_data import UnitPerNodeTouch


def create_add_selection_window():
    """Opens a new selection window with an empty selection."""
    open_selection_window(p_mode=WindowMode.new, p_selection_name='')

def create_merge_selectoon_window():
    """Opens a new merge selection window."""
    open_merge_node_window()

def file_new_clicked():
    """This will be executed when menu item File/New is licked.
        Asks if unsaved changes should be discarded and clears data."""
    global_properties = GlobalProperties.get_instance()
    if global_properties.changes_happened_since_last_save:
        ok_or_cancel = show_discard_data_ok_cancel_message()
    if (not global_properties.changes_happened_since_last_save
                            or ok_or_cancel == QMessageBox.Ok):
        new_mpdj_data()

def make_bidirectional_or():
    """Transforms a directed graph into an undirected graph.
        With this function a connection will be established
        if on directions is established before. """
    global_properties = GlobalProperties.get_instance()
    global_properties.mpdj_data.make_bidirectional(any)

def make_bidirectional_and():
    """Transforms a directed graph into an undirected graph.
        With this function a connections will remain, if 
        both directions are established before. A
        connection will be deleted, when less than 
        both directions are established."""
    global_properties = GlobalProperties.get_instance()
    global_properties.mpdj_data.make_bidirectional(all)

def show_discard_data_ok_cancel_message():
    """Shows a QMessageBox to ask if the current mpdj data should be
        discarded. Contains an OK and an Cancel Button."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText("You have unsaved changes in your current Data. Discard\
                unsaved changes and proceed?")
    msg.setInformativeText("Unsaved changes will be lost.")
    msg.setWindowTitle("Unsaved changes")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()
    return retval

class MainWindowMPDJ(QMainWindow):
    """Display the main window of the application where the connections
        and other stuff is edited by the user."""

    def show(self):
        """Shows this window (maximized). I will work on a better solution."""
        QMainWindow.showMaximized(self)

    def update(self):
        """Updates the view."""
        global_properties = GlobalProperties.get_instance()
        self.tf_min_per_selection.setText(str(global_properties.mpdj_data.min_units_per_node_touch))
        self.tf_max_per_selection.setText(str(global_properties.mpdj_data.max_units_per_node_touch))
        text_to_find = global_properties.mpdj_data.unit_per_node_touch.gui_representation()
        index = self.combo_box_minutes_or_titles.findText(text_to_find, Qt.MatchFixedString)
        self.combo_box_minutes_or_titles.setCurrentIndex(index)
#        self.limit_artist_play_chk_box.setChecked(
#            global_properties.mpdj_data.limit_artist_in_node_touch)
        self.chk_box_graph_is_directed.setChecked(global_properties.mpdj_data.graph_is_directed)
        self.setWindowTitle('MPDJ: {}'.format(global_properties.path_of_current_file))

    def write_min_per_note_to_mpdj(self):
        """Write the selected min count per node touch to the mpdj which
            is currently worked on."""
        global_properties = GlobalProperties.get_instance()
        global_properties.mpdj_data.min_units_per_node_touch = int(self.tf_min_per_selection.text())

    def write_max_per_note_to_mpdj(self):
        """Writes the selected max count per node touch to the mpdj which is
            currently worked on."""
        global_properties = GlobalProperties.get_instance()
        global_properties.mpdj_data.max_units_per_node_touch = int(self.tf_max_per_selection.text())

    def write_unit_per_node_touch_to_mpdj(self):
        """Writes the selected unit for min and max per touch to the mpdj.
            This does not do anything at the moment. Has to be
            implemented properly"""
        global_properties = GlobalProperties.get_instance()
        selection_text = self.combo_box_minutes_or_titles.currentText()
        global_properties.mpdj_data.unit_per_node_touch = UnitPerNodeTouch[selection_text.upper()]

    def write_limit_artists_played_to_mpdj(self):#
        """Write to the current mpdj if the artist are limited per
            node touch."""
        global_properties = GlobalProperties.get_instance()
        state = self.limit_artist_play_chk_box.isChecked()
        global_properties.mpdj_data.limit_artists_in_node_touch = state

    def write_graph_is_directed_to_mpdj(self):
        """Write if the graph is directed to mpd, this should be
            changed somehow, since this does only concern the editing
            of the connections."""
        global_properties = GlobalProperties.get_instance()
        state = self.chk_box_graph_is_directed.isChecked()
        global_properties.mpdj_data.graph_is_directed = state

    def file_dialog(self,load_save_type=QFileDialog.AcceptSave):
        """Opens an file save dialog and returns the selected
            filename."""
        file_save_dialog = QFileDialog(self)
        file_save_dialog.setFileMode(QFileDialog.AnyFile)
        file_save_dialog.setAcceptMode(load_save_type)
        file_save_dialog.setNameFilters(["MPDJ files (*.{})".format(FILE_SUFFIX)])
        file_save_dialog.selectNameFilter("MPDJ files (*.{})".format(FILE_SUFFIX))
        file_save_dialog.setDefaultSuffix((FILE_SUFFIX))
        exec_value = file_save_dialog.exec()
        if exec_value == 0:
            return None
        file_names = file_save_dialog.selectedFiles()
        if len (file_names) != 1:
            message_box = QMessageBox()
            message_box.setText('Please select only one file!')
            message_box.setWindowTitle('Save error.')
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
            return None
        return file_names[0]

    def file_save_as(self):
        """Saves the file. opens a file_dialog which asks for the
            filename."""
        file_name = self.file_dialog(load_save_type = QFileDialog.AcceptSave)
        if file_name:
            self.save_mpdj_data_to_file(file_name)

    def save_mpdj_data_to_file(self, p_file_name : str):
        """Saves the current mpdj data to the file by the path given
            in p_file_name."""
        try:
            global_properties = GlobalProperties.get_instance()
            global_properties.save_mpdj_data_to_file(p_file_name)
            self.statusBar().showMessage('Saved to {}'.format(p_file_name), 5000)
        except (OSError, IOError) as exception:
            message_box = QMessageBox()
            message_box.setText('Error saving the file: {}'.format(str(exception)))
            message_box.setWindowTitle('Error saving the file.')
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.setIcon(QMessageBox.Warning)
            message_box.exec_()

    def file_save(self):
        """Saves the current mpdj data to the current file."""
        global_properties = GlobalProperties.get_instance()
        if len(global_properties.path_of_current_file) > 0:
            self.save_mpdj_data_to_file(global_properties.path_of_current_file)
        else:
            self.file_save_as()

    def file_load(self):
        """Loads mpdj data from a file. Opens a file dialog which
            asks for the file to load."""
        global_properties = GlobalProperties.get_instance()
        file_name = self.file_dialog(load_save_type = QFileDialog.AcceptOpen)
        if file_name:
            if global_properties.changes_happened_since_last_save:
                retval = show_discard_data_ok_cancel_message()
            if not global_properties.changes_happened_since_last_save or retval == QMessageBox.Ok:
                try:
                    global_properties.load_mpdjdata_from_file(file_name)
                except AttributeError as err:
                    message_box = QMessageBox()
                    message_box.setText('Error reading your MPDJ-File: {}'.format(err))
                    message_box.setWindowTitle('Load error.')
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.setIcon(QMessageBox.Warning)
                    message_box.exec_()

    def __init__(self):
        """Constructor"""
        QMainWindow.__init__(self)
        global_properties = GlobalProperties.get_instance()
        self.connection_table = ConnectionTableWidget()
        global_properties.add_listener(self.connection_table)
        self.setCentralWidget(self.connection_table)

        self.menu_bar = self.menuBar()
        self.menu_file = self.menu_bar.addMenu('File')
        self.menu_file.addAction('New',file_new_clicked)
        self.menu_file.addAction('Open', self.file_load)
        self.menu_file.addSeparator()
        self.menu_file.addAction('Save', self.file_save)
        self.menu_file.addAction('Save as', self.file_save_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction('Exit',sys.exit)

        self.menu_file = self.menu_bar.addMenu('Connections')
        self.make_birectional_menu = self.menu_file.addMenu('Make bidirectional')
        self.make_birectional_menu.addAction("with and", make_bidirectional_and)
        self.make_birectional_menu.addAction("with or", make_bidirectional_or)

        self.menu_selection =self.menu_bar.addMenu('Selections')
        self.action_add_selection = self.menu_selection.addAction('Add Selection')
        self.action_add_selection.triggered.connect(create_add_selection_window)
        self.action_merge_selections = self.menu_selection.addAction('Merge Selections')
        self.action_merge_selections.triggered.connect(create_merge_selectoon_window)
        self.setMenuBar(self.menu_bar)
        self.statusBar().showMessage('Welcome to mpdj!', 5000)

        self.mpdj_options_dock = QDockWidget("MPDJ Options Panel", self)
        self.mpdj_options_dock_layout = QFormLayout()
        self.mpdj_docked_widget = QWidget()

        self.tf_min_per_selection = QLineEdit()
        self.tf_min_per_selection.setValidator(QIntValidator(0,2147483647))
        self.mpdj_options_dock_layout.addRow('Min per Node touch:', self.tf_min_per_selection)
        self.tf_min_per_selection.editingFinished.connect(self.write_min_per_note_to_mpdj)

        self.tf_max_per_selection = QLineEdit()
        self.tf_max_per_selection.setValidator(QIntValidator(0,2147483647))
        self.mpdj_options_dock_layout.addRow('Max per Node touch:', self.tf_max_per_selection)
        self.tf_max_per_selection.editingFinished.connect(self.write_max_per_note_to_mpdj)

        self.combo_box_minutes_or_titles = QComboBox()
        self.combo_box_minutes_or_titles.addItems(
            [unit.gui_representation() for unit in UnitPerNodeTouch])
        self.mpdj_options_dock_layout.addRow('Unit:', self.combo_box_minutes_or_titles)
        self.combo_box_minutes_or_titles.currentTextChanged.connect(
            self.write_unit_per_node_touch_to_mpdj)

        self.mpdj_docked_widget.setLayout(self.mpdj_options_dock_layout)
        self.mpdj_options_dock.setWidget(self.mpdj_docked_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.mpdj_options_dock)

        self.chk_box_graph_is_directed = QCheckBox()
        self.chk_box_graph_is_directed.stateChanged.connect(self.write_graph_is_directed_to_mpdj)
        self.mpdj_options_dock_layout.addRow(
            QLabel('Graph is directed'), self.chk_box_graph_is_directed)
        self.opened_selection_window = None
        global_properties.add_listener(self)
        self.update()
