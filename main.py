# basic just testing if this works

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QFileSystemModel

from ui_py.main_window import Ui_MainWindow
from ui_py.about import Ui_About
from ui_py.replay_path_detection import Ui_ReplayPathDetection

from utilities import replay_dir_manager

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.listview_replays_model = QStandardItemModel()
        self.listview_replays.setModel(self.listview_replays_model)
        self.connectSignalSlots()

    def connectSignalSlots(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.listview_replays.selectionModel().currentChanged.connect(self.replay_selected)

    def open(self):
        new_path = QFileDialog.getExistingDirectory()
        if dir_manager.set_path(new_path):
            self.reloadMenu(dir_manager.list_replays())

    def about(self):
        about = About(self)
        about.exec()

    def replay_selected(self):
        index = self.listview_replays.selectionModel().currentIndex()
        selection = str(index.data())
        self.statusbar.showMessage(dir_manager.replay_path_str + "/" + selection)

    def reloadMenu(self, replays):
        self.listview_replays_model.clear()
        if replays != None:
            for i in replays:
                item = QStandardItem(i)
                self.listview_replays_model.appendRow(item)

class ReplayPathDetection(QDialog, Ui_ReplayPathDetection):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class About(QDialog, Ui_About):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

# Setup main window
app = QApplication(sys.argv)
win = Window()
win.show()

# get the path automatically (or try to)
dir_manager = replay_dir_manager()
dir_manager.path_detection()
# set status bar to current path
win.statusbar.showMessage(dir_manager.replay_path_str)

# Show the path popup
path_detection = ReplayPathDetection(win)
path_detection.replay_path.setText(dir_manager.replay_path_str)
path_detection.exec()

win.reloadMenu(dir_manager.list_replays())

# Exit?
sys.exit(app.exec())
