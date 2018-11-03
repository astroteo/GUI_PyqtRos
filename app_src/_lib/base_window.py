from PyQt5.QtWidgets import  QMainWindow, QShortcut, QWidget
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore

import sys

class BaseWindow(QMainWindow):
    def __init__(self, cmd_path="./", close_shortcut=True):
        self.x = 0
        self.y = 0

        self.cmd_path = cmd_path

        QMainWindow.__init__(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)

        if close_shortcut:
            self.shortcut_close = QShortcut(QKeySequence("Ctrl+Q"), self)
            self.shortcut_close.activated.connect(self.close)

    # def close(self):
    #     self.hide()

    def exit(self):
        reset = QtCore.QProcess()
        reset.setProcessChannelMode(QtCore.QProcess.MergedChannels);
        reset.start(self.cmd_path+"/bash/reset.sh")
        reset.write ("exit\n\r")
        reset.waitForFinished()
        QtCore.QCoreApplication.instance().quit()
        self.hide()
        sys.exit(0)

    def mouseMoveEvent(self, event):
        super(BaseWindow, self).mouseMoveEvent(event)
        # if self.leftClick == True:
        self.move(event.globalPos().x()-self.x,event.globalPos().y()-self.y)

    def mousePressEvent(self, event):
        super(BaseWindow, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick = True
            self.x=event.pos().x()
            self.y=event.pos().y()

    def mouseReleaseEvent(self, event):
        super(BaseWindow, self).mouseReleaseEvent(event)
        self.leftClick = False


class BaseWidget(QWidget):
    def __init__(self, cmd_path="./", close_shortcut=True):
        self.x = 0
        self.y = 0

        self.cmd_path = cmd_path

        QWidget.__init__(self)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)

        if close_shortcut:
            self.shortcut_close = QShortcut(QKeySequence("Ctrl+Q"), self)
            self.shortcut_close.activated.connect(self.close)

    def close(self):
        self.hide()

    def exit(self):
        reset = QtCore.QProcess()
        reset.setProcessChannelMode(QtCore.QProcess.MergedChannels);
        reset.start(self.cmd_path+"/bash/reset.sh")
        reset.write ("exit\n\r")
        reset.waitForFinished()
        QtCore.QCoreApplication.instance().quit()
        self.hide()
        sys.exit(0)

    def mouseMoveEvent(self, event):
        super(BaseWidget, self).mouseMoveEvent(event)
        # if self.leftClick == True:
        self.move(event.globalPos().x()-self.x,event.globalPos().y()-self.y)

    def mousePressEvent(self, event):
        super(BaseWidget, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick = True
            self.x=event.pos().x()
            self.y=event.pos().y()

    def mouseReleaseEvent(self, event):
        super(BaseWidget, self).mouseReleaseEvent(event)
        self.leftClick = False
