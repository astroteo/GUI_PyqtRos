from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QProgressBar

class QProgBar(QProgressBar):
 
    value = 0
 
    @pyqtSlot()
    def increaseValue(progressBar):
        progressBar.setValue(progressBar.value)
        progressBar.value = progressBar.value+1
