import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QProgressBar
from PyQt5.QtCore import QThread
import time

class progressBarHandler(QThread):
    def __init__(self, parent = None, path_to_bag= None, check_interval = 10, progress_bar = None):
        QThread.__init__(self,parent)
        self.progress_bar = progress_bar
        self.path_to_bag = path_to_bag
        self.check_interval = check_interval
        self.output_bag_dir = 'bag/'
        self.output_post_dir = 'post_processing/'
        path = self.path_to_bag.replace("/"+self.output_bag_dir,"/"+self.output_post_dir)
        path = path.replace(".bag",".pcd")
        path_to_pcd     = path 

        print 'executing stat on bag-file ==> ' + path_to_bag
        print 'executing stat on pcd-file ==> ' + path_to_pcd

        self._flag = True


    def run(self):
        time.sleep(200)
        while self._flag:
            time.sleep(self.check_interval)


            try:
                
                path = self.bag_file.replace("/"+output_bag_dir,"/"+output_post_dir)
                value = self.progress_status(output_post_dir)
                self.progress_bar.setValue(value)
            except:
                pass
       

    def progress_status(self,output_post_dir,magic_ratio = 0.006788321, path_to_pcd = None):
        try:
            size_full = os.stat(self.path_to_bag)
            print size_full
            if path_to_pcd is not None:
                print "pcd file explictely told"

            else:
                path = self.path_to_bag.replace("/"+self.output_bag_dir,"/"+self.output_post_dir)
                path = path.replace(".bag",".pcd")
                path_to_pcd     = path 

            try:
                size_now =  os.stat(path_to_pcd)
                return size_now/(size_full*magic_ratio) * 100

            except:
                print "post-processing not started yet "
                return 0#probably, not started pp yet
        except:
            print "bag file not found"
            return 0

    def stop(self):
        self._flag = False


        