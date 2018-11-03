from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore
from PyQt5.QtCore import QSize

class IconButton(QPushButton):
    def __init__(self, icon_name="", icon_size=60):
        self.status = True
        self.icon_name = icon_name
        self.icon_size = icon_size
        QPushButton.__init__(self)
        if icon_name != "":
            icon = QIcon()
            icon.addPixmap(QPixmap(self.icon_name+"_on.png"))
            self.setIcon(icon)
            self.setIconSize(QSize(self.icon_size,self.icon_size))
        self.setMinimumWidth(self.icon_size)
        self.setMinimumHeight(self.icon_size)
        # self.setCheckable(True)
        self.setStyleSheet("QPushButton{ border: 0px;  background: none !important;}")

    def change_status(self, restore = False):
        if self.icon_name != "":
            if self.status:
                icon = QIcon()
                icon.addPixmap(QPixmap(self.icon_name+"_off.png"))
                self.setIcon(icon)
                self.setIconSize(QSize(self.icon_size,self.icon_size))
            else:
                icon = QIcon()
                icon.addPixmap(QPixmap(self.icon_name+"_on.png"))
                self.setIcon(icon)
                self.setIconSize(QSize(self.icon_size,self.icon_size))
            self.status = not self.status
