#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Allo stato attuale => da replicare nell'installer (ammesso che sia possibile) è necessario:
    - autorizzare gli script di bash: sudo chmod +x bash/blam_offline.sh
                                      sudo chmod +x bash/is_blam_running.sh
    - effettuare il sourcing di entrambi gli environments (backpack & BLAM!)
                    -    cd /home/teo/installer_SLAM/gui/_core/catkin_ws/devel_isolated &&   source setup.bash && cd -
                    -    cd /home/teo/installer_SLAM/gui/_core/blam/internal/devel && source setup.bash && cd -

    !! se verrà compilato il core dovrebbe essere possibile fare il sourcing di quelli interni !!

'''
### Librariries
# os dependencies
import os
import sys
import signal
import subprocess
import rviz
import roslib
import ConfigParser
import argparse
import time
import glob

from os import listdir
from os.path import isfile, join

# threading dependencies
from threading import Thread, Event, Lock

# Qt dependencies
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtCore import QThread , QProcess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# internal dependencies
from _lib.base_window import BaseWindow
from _lib.rviz_handler import RVizHandler
from _lib.rospath_handler import rospathSet
from _lib.icon_button import IconButton
from _lib.progress_bar_handler import progressBarHandler
from _lib.utility import replace_default_var, variablename, str2bool, select_file
from _lib.ros_thread import subprocessThread,checkWorker, rosWorker
from _lib.ros_collections import do_job
from _lib.progress_bar import QProgBar



###path fixing
home_path = os.path.dirname(os.path.abspath(__file__))


###load-ui
Ui_MainWindow, QtBaseClass                  = uic.loadUiType(home_path+'/_gui/post_processing_new.ui')

### Configurations-gui
# configuration-parser
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file-name', default="__configuration_files/post_processing.conf", dest='configuration_file_name')
parsed = parser.parse_args()
config = ConfigParser.ConfigParser()
config.readfp(open(home_path+"/"+parsed.configuration_file_name))
print config.options("paths")
#main-directories configuration
img_d_path          = replace_default_var(config.get("paths","img_d_path"))
log_dir             = replace_default_var(config.get("paths","log_dir"))
project_path        = replace_default_var(config.get("paths","project_path"))
output_bag_dir      = replace_default_var(config.get("paths","output_bag_dir"))
output_post_dir     = replace_default_var(config.get("paths","output_post_dir"))
output_idx_dir      = replace_default_var(config.get("paths","output_idx_dir"))


### Roscore management
#roscore-start
roscore_cmd = "roscore"
p1 = QProcess()
p1.start(roscore_cmd)

# source the environment: TO BE REMOVED IF INSIDE SNAP (HOPEFULLY)
#def source_backpack_env():
    #subprocess.call(['source',home_path+'/_core/catkin_ws/backpack/'])


#kill roscore
def kill_roscore():
    subprocess.call(['kill',str(p1.pid())])





load_rviz_module = True


class MyApp(BaseWindow, Ui_MainWindow):
    def __init__(self):
        print( "------------------------ INIT MyApp ----------------------------")
        BaseWindow.__init__(self, os.path.realpath(__file__), False)
        Ui_MainWindow.__init__(self)


        ### rviz
        if load_rviz_module:
            self.rviz_file  = home_path+"/_rviz/blam.rviz"
            self.form_widget_2 = RVizHandler(self.rviz_file, False)
            self.layout_rviz_2.setSpacing(0)
            self.layout_rviz_2.addWidget(self.form_widget_2)
            self.rviz_thread_2 = QtCore.QThread()
            self.rviz_thread_2.start()
            self.form_widget_2.moveToThread(self.rviz_thread_2)


        ### buttons & combo_bag
        # button-exit
        self.button_exit  = IconButton(img_d_path+"exit")
        self.buttons_layout_exit.addWidget(self.button_exit)
        self.button_exit.clicked.connect(self.close_program)

        # file-dialog box
        self.project_path = home_path
        #self.button_file_dialog = IconButton(img_d_path+"folder.png")
        self.button_file_dialog.clicked.connect(self.file_dialog)

        # status frame
        self.status_val.setText("Waiting...")
        self.status_val.setStyleSheet("color: orange;margin:2px;")

        # button_start
        self.button_start.clicked.connect(self.start_pp_cmd)
        self.button_start.setEnabled(False)

        # button_stop
        self.button_stop.clicked.connect(self.kill_pp)
        self.button_stop.setEnabled(False)



        ### logo & progress-bar
        image = QPixmap(home_path+"/_img/logo.png") #.scaled(QSize(400,300),  Qt.KeepAspectRatio);
        imageLabel = QLabel()
        imageLabel.setAlignment(Qt.AlignCenter)
        imageLabel.setPixmap(image.scaled(imageLabel.width(), imageLabel.height(), Qt.KeepAspectRatio))
        self.tdt_logo.setPixmap(image.scaled(imageLabel.width(), imageLabel.height(), Qt.KeepAspectRatio))

        self.buttons_layout.setSpacing(30)

        self.thread_stop = Event()
        self.thread_lock = Lock()

        self.progress_bar_slam.setValue(0)

        #self.timer_val = 0.0
        #self.timer_active = False
        #self.timer = [self.timer_active, self.timer_val]

    ### Gui functions
    # file-dialog
    def file_dialog(self):
        self.combo_bag.clear()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        project_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.project_path = project_path
        if project_path:
            print "chosen directory: " + project_path
            self.date       = str(time.strftime("%Y-%m-%d"))+"_"+str(time.strftime("%H-%M-%S"))
            print "looking for bags @ " + str(project_path)

            #bag_files = sorted(glob.glob(project_path+"*-*-*_*-*-*/bag/*"))
            bag_files = []
            bag_files_name = []

            dirs_walk= list(next(os.walk(project_path)))
            dirs = [ dirs_walk[0] +'/' + dir for dir in dirs_walk[1]]
            print dirs
            
            for dir in dirs:
                files = [f for f in listdir(dir) if isfile(join(dir, f))]
                for file in files:
                    filename, file_extension = os.path.splitext(file)
                    if file_extension == '.bag':
                        bag_files.append(dir+'/'+filename)
                        bag_files_name.append(filename)


            if len(bag_files_name):
                self.status_val.setText("Ready")
                self.status_val.setStyleSheet("color: green; margin:2px;")
                self.button_start.setEnabled(True)

                for bag_file in bag_files_name:
                    self.combo_bag.addItem(bag_file)
                    
                    

            else:
                self.bag_val.setText('no .bag found')
                self.status_val.setStyleSheet("color: red; margin:2px;")

    def close_program(self):
        try:
            self.thread_stop.set()
        except:
            print 'no event to be killed while exiting '

        #signal.signal(signal.SIGTERM, Event)
        sys.exit([ main(),kill_roscore(),])

    def reset(self):
        reset = CmdReset(log_dir+"init_reset", home_path+"/bash/reset.sh")

################################################################################
##      PostProcessing comands
################################################################################

    def refresh_cmd(self):
        cmd = home_path+"/bash/is_blam_running.sh"
        p = subprocess.Popen(cmd.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = p.communicate()
        if int(out) < 1:
            self.status_val.setText("Ready")
            self.status_val.setStyleSheet()
        else:
            self.status_val.setText("Running")
            self.status_val.setStyleSheet("color: red; margin:2px;")

    def set_start(self):
        if self.processs_pid != -1:
            print " 1 PID = ", self.processs_pid
            os.kill(self.processs_pid, signal.SIGTERM)
            self.reset_cmd        = home_path+"/bash/reset_pp.sh"
            processs = subprocess.Popen(self.reset_cmd.split(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            self.processs_pid = -1
            print " 2 PID = ", self.processs_pid
        # self.button_start.clicked.connect(self.start_pp_cmd)
    

# da incorporare necessariamente come metodo della classe della gui, modificare in qesta funzione attributo ready/starting/running/waiting
    global process_info 
    process_info = 'dunno'
    

    def start_pp_cmd(self):
        bag_file = self.combo_bag.currentText()+".bag"
        fake_path = '/home/teo/installer_SLAM/gui'
        rospathSet(fake_path)
        path = bag_file.replace("/"+output_bag_dir,"/"+output_post_dir)
        path = path.replace(".bag","")
        post_processing_dir     = path[0:path.rfind("/"+output_post_dir)]+ "/"+output_post_dir + "/"
        if not os.path.exists(post_processing_dir):
            os.makedirs(post_processing_dir)

        csv_file = path+".csv"

        print bag_file 
        print path
        print csv_file
       

        self.bag_val.setText(bag_file)
        self.status_val.setText('Initializing...')
        self.status_val.setStyleSheet("color: orange; margin:2px;")        
        # ros processes:
        print self.project_path + '/bag/'+bag_file
        self.ros_worker = rosWorker(self,self.project_path+'/bag/'+bag_file)
        self.ros_worker.start()

        #deactivate start-button:
        self.button_start.setEnabled(False)
        self.button_start.setStyleSheet("background-color: grey; margin:2px;")

        # check processess:
        self.check_worker = checkWorker(self,status_widget = self.status_val)
        self.check_worker.start()

        # progress bar
        self.progress_bar_handler = progressBarHandler(self,self.project_path + '/bag/'+bag_file,
                                             10, 
                                            self.progress_bar_slam)
        self.progress_bar_handler.start()
        
        #QThread list:
        self.thread_pp_list = [self.ros_worker,self.check_worker,self.progress_bar_handler]

        # activate stop button
        self.button_stop.setEnabled(True)

        #print " 3 PID = ", self.processs.pid
        #self.processs_pid = self.processs.pid
        #self.status_val.setText("Initializing..")
        #self.status_val.setStyleSheet("color: orange; margin:2px;")

        #self.refresh_cmd()

    def kill_pp(self):

        self.status_val.setText('Quitting..')
        self.status_val.setStyleSheet("color: orange; margin:2px;")


        for t in self.thread_pp_list:
            t.stop()

        self.status_valsetText('Waiting...')
        self.button_start.setStyleSheet("color: orange; margin:2px;")

        






def main():
    app = QApplication(sys.argv)
    window = MyApp()
    # window.showFullScreen()
    # window.setStyleSheet("QLineEdit { background-color: yellow }");
    window.setWindowTitle('SLAM-postprocessor')
    window.show()
    return app.exec_()


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    print("---start---")
    sys.exit([main(), kill_roscore() ])
