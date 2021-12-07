# basic just testing if this works

import sys
import os
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QFileSystemModel

from ui_py.main_window import Ui_MainWindow
from ui_py.about import Ui_About
from ui_py.replay_path_detection import Ui_ReplayPathDetection

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
		print (new_path)

	def about(self):
		about = About(self)
		about.exec()

	def replay_selected(self):
		index = self.listview_replays.selectionModel().currentIndex()
		selection = str(index.data())
		self.statusbar.showMessage(replay_folder_path_str + "/" + selection + ".ini")

	def reloadMenu(self, replays):
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

# Attempt to detect the file path...
# There may or may not be more than one Steam UID here, if there's more than one then just don't?
# TODO: platform agnostic
replay_folder_path = Path.home().joinpath('.local','share','Skullgirls','Replays')
dir_list = os.listdir(replay_folder_path)
if len(dir_list) == 1:
	replay_folder_path = replay_folder_path.joinpath(dir_list[0])

replay_folder_path_str = str(replay_folder_path)
win.statusbar.showMessage(replay_folder_path_str)

# Show the path popup
path_detection = ReplayPathDetection(win)
path_detection.replay_path.setText(replay_folder_path_str)
path_detection.exec()

replays = os.listdir(replay_folder_path)
replays = [os.path.splitext(each)[0] for each in replays]
replays = list(dict.fromkeys(replays))

win.reloadMenu(replays)

# Exit?
sys.exit(app.exec())
