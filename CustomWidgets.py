from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QLabel, QFrame


class DropArea(QLabel):
    dropped = pyqtSignal(str)

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setMinimumSize(200, 100)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Dark)

    def dragEnterEvent(self, e):
        self.setBackgroundRole(QPalette.Light)
        e.accept()

    def dropEvent(self, e):
        mimeData = e.mimeData()
        self.setBackgroundRole(QPalette.Dark)
        self.dropped.emit(mimeData.text())

    def dragLeaveEvent(self, event):
        self.clear()
        event.accept()

    def clear(self):
        self.setText("<drop here>")
        self.setBackgroundRole(QPalette.Dark)
