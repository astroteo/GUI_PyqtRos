#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from threading import Thread
import rosnode
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtCore import QThread , QProcess

class subprocessThread(Thread):
    def __init__(self, cmd_subprocess):
        self.stdout = None
        self.stderr = None
        Thread.__init__(self)
        self.cmd_subprocess = cmd_subprocess

    def run(self):
        print 'started'
        self.p = subprocess.Popen(self.cmd_subprocess,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = self.p.communicate()
        print(self.stdout)
        print(self.stdout)
      

    def stop(self):
        subprocess.call(['kill',str(self.p.pid())])





global process_info
process_info = 'dunno'


class checkWorker(QThread):
    def __init__(self,parent= None,check_info = None, check_interval = 10, status_widget = None):
        QThread.__init__(self,parent)
        self.check_interval = check_interval
        self.check_info = check_info
        self.status_widget = status_widget
        self._flag = True

    def run(self):
        active_nodes =[0]
        while self._flag:
            time.sleep(self.check_interval)
        
            try:
                active_nodes = rosnode.get_node_names()
                #print active_nodes
                #time.sleep(5)
            except:
                active_nodes[0] = 0 #"nomaster"

            if (len(active_nodes) > 1 and active_nodes[0] != 0):
                #process_info = 1 "active"
                self.check_info =1# "active"
            elif (len(active_nodes) > 1 and active_nodes[0] == 0):
                #process_info = "dunno"
                self.check_info=2#"dunno"
            else:
                #process_info = "inactive"
                self.check_info =3# "inactive" 

            self.update()

    def update(self):
        if self.status_widget is not None:

            if self.check_info == 0:
                try:
                    self.status_widget.setText('Waiting')
                    self.status_widget.setStyleSheet("color: orange; margin:2px;")
                except:
                    pass

            elif self.check_info == 1:
                try:
                     self.status_widget.setText('Running...')
                     self.status_widget.setStyleSheet("color: red; margin:2px;")
                except:
                    pass
            else:
                self.status_widget.setText('Unknow... please wait')
                self.status_widget.setStyleSheet("color: red; margin:2px;")

    def stop(self):
        self._flag = False







class rosWorker(QThread):

  def __init__(self,parent= None, bag_file = None):
    QThread.__init__(self,parent)
    self.bag_file = bag_file
    self._flag = True



  def stop(self):
        for t in self.threads:
            t.stop()

        self._flag = False

  def run(self):
    if self._flag:
        output_bag_dir = 'bag/'
        output_post_dir = 'post_processing/'
        path = self.bag_file.replace("/"+output_bag_dir,"/"+output_post_dir)
        prefix = path.replace(".bag",'')
        path = path.replace(".bag","")
        csv_file = path+".csv"
        print 'csv-file: ' +csv_file
        print 'prefix: ' + prefix
        print "processing bag-file => path = "+ self.bag_file

        std_buf = False
        roslaunch_backpack_test =  'roslaunch bagpack 3dt_slam_offline.launch bagfile:=' + str(self.bag_file).strip()+' index_name:=' + str(csv_file).strip() + ' trajectory:=true'
        print "command not starting: " + roslaunch_backpack_test
        if not std_buf:
            pass
        else:
            roslaunch_backpack_test = 'stdbuf -oL' + roslaunch_backpack_test
            
        rosrun_pcl_test = 'rosrun pcl_ros pointcloud_to_pcd input:=/blam/blam_slam/octree_map _prefix:='+prefix


        backpack_run_in_thread = True# questa è la condizione che funziona, nello snap finale
        if backpack_run_in_thread:
            self.roslaunch_backpack_thread = subprocessThread(roslaunch_backpack_test)
            self.rosrun_pcl_thread = subprocessThread(rosrun_pcl_test)

            self.threads = [self.roslaunch_backpack_thread,self.rosrun_pcl_thread]#roscore_thread => self called by roslaunch !!
            for t in self.threads:
                print 'starting some threads...'
                t.start()
  



