# basic just testing if this works

import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog

import replay_reader
from ui_py.main_window import Ui_MainWindow
from ui_py.about import Ui_About
from ui_py.replay_path_detection import Ui_ReplayPathDetection
from utilities import ReplayDirManager
from replay_reader import ReplayReader


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, dir_manager, replay_reader, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.dir_manager = dir_manager
        self.replay_reader = replay_reader
        self.listview_replays_model = QStandardItemModel()
        self.listview_replays.setModel(self.listview_replays_model)
        self.connect_signal_slots()

    def connect_signal_slots(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.listview_replays.selectionModel().currentChanged.connect(self.replay_selected)

    def open(self):
        if self.dir_manager.path_valid:
            new_path = QFileDialog.getExistingDirectory(self, "Open Directory", self.dir_manager.replay_path_str)
        else:
            new_path = QFileDialog.getExistingDirectory(self, "Open Directory")
        if new_path != "":
            if self.dir_manager.set_path(new_path):
                self.replay_reader.set_path_from_string(self.dir_manager.replay_path_str)
                self.reload_menu(self.dir_manager.list_replays())

    def about(self):
        about = About(self)
        about.exec()

    def replay_selected(self):
        index = self.listview_replays.selectionModel().currentIndex()
        selection = str(index.data())
        self.statusbar.showMessage(self.dir_manager.replay_path_str + "/" + selection)
        replay_json = self.replay_reader.read_replay(selection)
        self.text_replay.setText(replay_reader.format_replay(replay_json))

    def reload_menu(self, replays):
        self.listview_replays_model.clear()
        if replays is not None:
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


def main():
    dir_manager = ReplayDirManager()
    replay_reader = ReplayReader()

    # Setup main window
    app = QApplication(sys.argv)
    win = Window(dir_manager, replay_reader)
    win.show()

    # get the path automatically (or try to)
    dir_manager.path_detection()
    # set status bar to current path
    win.statusbar.showMessage(dir_manager.replay_path_str)

    # Show the path popup
    path_detection = ReplayPathDetection(win)
    path_detection.replay_path.setText(dir_manager.replay_path_str)
    path_detection.exec()

    win.reload_menu(dir_manager.list_replays())
    replay_reader.set_path_from_string(dir_manager.replay_path_str)

    # Exit?
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
