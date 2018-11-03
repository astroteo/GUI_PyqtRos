from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QObject
import rviz
import time


def rviz_window(window, stop_event, lock):
    while True and not stop_event.is_set():
        time.sleep(1)
        # time.sleep(0.25)
        window[0].update()
        window[1].update()
        window[2].update()
        # window[3].update()
        window[4].update()
        window[5].update()
        window[6].update()
        # window[7].update()
        # QApplication.processEvents()

class RVizHandler(QWidget):
    def __init__(self, filename="", status_bar=False):
        QWidget.__init__(self)

        self.filename = filename

        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, self.filename )

        self.frame = rviz.VisualizationFrame()
        # self.frame.setSplashPaths( "" )
        self.frame.initialize()
        self.frame.setMenuBar( None )
        if not status_bar:
            self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )
        self.frame.load( config )

        self.manager = self.frame.getManager()
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )

        layout = QVBoxLayout()
        layout.addWidget( self.frame )
        self.setLayout( layout )
        self.frame.show()
