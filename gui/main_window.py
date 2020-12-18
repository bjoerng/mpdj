'''
Created on 10.10.2020

@author: Bjoern Graebe
'''
import sys
from PyQt5.Qt import QMainWindow, QFileDialog, QMessageBox, QDockWidget,\
    QCheckBox,QFormLayout,QLabel,QWidget, QLineEdit,QIntValidator, QComboBox
from PyQt5.QtCore import Qt
from gui.selection_window import SelectionWindow
from gui.connection_table import ConnectionTableWidget
from control.global_properties import GlobalProperties, new_mpdj_data
from model.constants import FILE_SUFFIX
from model.mpdj_data import UnitPerBodeTouch

class MainWindowMPDJ(QMainWindow):
    """Display the main window of the application where the connections
        and other stuff is edited by the user."""

    def open_selection_window(self):
        """Creates and display a window to create or modify a selection."""
        self.opened_selection_window = SelectionWindow()
        self.opened_selection_window.show()

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
        self.limit_artist_play_chk_box.setChecked(
            global_properties.mpdj_data.limit_artists_in_node_touch)
        self.chk_box_graph_is_directed.setChecked(global_properties.edit_both_directions)
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

    def write_unit_per_node_touchto_mpdj(self):
        """Writes the selected unit for min and max per touch to the mpdj.
            This does not do anything at the moment. Has to be
            implemented properly"""
        global_properties = GlobalProperties.get_instance()
        selection_text = self.combo_box_minutes_or_titles.currentText()
        global_properties.mpdj_data.unit_per_node_touch = UnitPerBodeTouch[selection_text.upper()]

    def write_limit_artists_played_to_mpdj(self):#
        """Write to the current mpdj if the artist are limited per
            node touch."""
        global_properties = GlobalProperties.get_instance()
        state = self.limit_artist_play_chk_box.isChecked()
        global_properties.mpdj_data.limit_artists_in_node_touch = state

    def write_graph_is_directedo_mpdj(self):
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
        file_save_dialog.exec_()
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
            message_box.setWindowTitle('Song selection will not be added.')
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.setIcon(QMessageBox.Warning)
            message_box.exec_()

    def file_save(self):
        """Saves the current mpdj data to the current file."""
        global_properties = GlobalProperties.get_instance()
        self.save_mpdj_data_to_file(global_properties.path_of_current_file)

    def file_load(self):
        """Loads mpdj data from a file. Opens a file dialog which
            asks for the file to load."""
        global_properties = GlobalProperties.get_instance()
        file_name = self.file_dialog(load_save_type = QFileDialog.AcceptOpen)
        global_properties.load_mpdjdata_from_file(file_name)

    def __init__(self):
        """Constructor"""
        QMainWindow.__init__(self)
        global_properties = GlobalProperties.get_instance()
        self.connection_table = ConnectionTableWidget()
        global_properties.add_listener(self.connection_table)
        self.setCentralWidget(self.connection_table)

        self.menu_bar = self.menuBar()
        self.menu_file = self.menu_bar.addMenu('File')
        self.menu_file.addAction('New',new_mpdj_data)
        self.menu_file.addAction('Open', self.file_load)
        self.menu_file.addSeparator()
        self.menu_file.addAction('Save', self.file_save)
        self.menu_file.addAction('Save as', self.file_save_as)
        self.menu_file.addSeparator()
        self.menu_file.addAction('Exit',sys.exit)

        self.menu_selection =self.menu_bar.addMenu('Selections')
        self.action_add_selection = self.menu_selection.addAction('Add Selection')
        self.action_add_selection.triggered.connect(self.open_selection_window)
        self.setMenuBar(self.menu_bar)
        self.statusBar().showMessage('Welcome to mpdj!', 5000)

        self.mpdj_options_dock = QDockWidget("MPDJ Options Panel", self)
        self.mpdj_options_dock_layout = QFormLayout()
        self.mpdj_docked_widget = QWidget()

        self.tf_min_per_selection = QLineEdit()
        self.tf_min_per_selection.setValidator(QIntValidator())
        self.mpdj_options_dock_layout.addRow('Min per Node touch:', self.tf_min_per_selection)
        self.tf_min_per_selection.editingFinished.connect(self.write_min_per_note_to_mpdj)

        self.tf_max_per_selection = QLineEdit()
        self.tf_max_per_selection.setValidator(QIntValidator())
        self.mpdj_options_dock_layout.addRow('Max per Node touch:', self.tf_max_per_selection)
        self.tf_max_per_selection.editingFinished.connect(self.write_max_per_note_to_mpdj)

        self.combo_box_minutes_or_titles = QComboBox()
        for str_rept in UnitPerBodeTouch:
            self.combo_box_minutes_or_titles.addItem(str_rept.gui_representation())
        self.mpdj_options_dock_layout.addRow('Unit:', self.combo_box_minutes_or_titles)
        self.combo_box_minutes_or_titles.currentTextChanged.connect(
            self.write_unit_per_node_touchto_mpdj)

        self.mpdj_docked_widget.setLayout(self.mpdj_options_dock_layout)
        self.mpdj_options_dock.setWidget(self.mpdj_docked_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.mpdj_options_dock)

        self.limit_artist_play_chk_box = QCheckBox()
        self.limit_artist_play_chk_box.stateChanged.connect(self.write_limit_artists_played_to_mpdj)
        self.mpdj_options_dock_layout.addRow(
            QLabel('Artist only once per node crossing'), self.limit_artist_play_chk_box)

        self.chk_box_graph_is_directed = QCheckBox()
        self.chk_box_graph_is_directed.stateChanged.connect(self.write_graph_is_directedo_mpdj)
        self.mpdj_options_dock_layout.addRow(
            QLabel('Graph is directed'), self.chk_box_graph_is_directed)
        self.opened_selection_window = None
        global_properties.add_listener(self)
        self.update()
