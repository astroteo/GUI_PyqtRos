#!/usr/bin/env python
# -*- coding: utf-8 -*-

#standard python dependencies
import subprocess
from threading import Thread
import time

#ros packages
import rosnode


 

class subprocessThread(Thread):
    def __init__(self, cmd_subprocess):
        self.stdout = None
        self.stderr = None
        Thread.__init__(self)
        self.cmd_subprocess = cmd_subprocess

    def run(self):
        p = subprocess.Popen(self.cmd_subprocess,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = p.communicate()
        print(self.stdout)
        print(self.stdout)

global process_info
process_info = 'dunno'

class checkThread(Thread):
    def __init__(self,check_info, check_interval = 10):
        Thread.__init__(self)
        self.check_interval = check_interval
        self.check_info = check_info

    def run(self):

        active_nodes =['dunno']
        while True:
            time.sleep(self.check_interval)
        
            try:
                active_nodes = rosnode.get_node_names()
                #print active_nodes
                #time.sleep(5)
            except:
                active_nodes[0] = "nomaster"

            if (len(active_nodes) > 1 and active_nodes[0] != 'dunno'):
                process_info = "active"
                self.check_info = "active"
            elif (len(active_nodes) > 1 and active_nodes[0] == 'dunno'):
                process_info = "dunno"
                self.global_info="dunno"
            else:
                process_info = "inactive"
                self.check_info = "inactive" 
            time.sleep(10)




def do_job():
    print "hello..."
    print "SE non sei in uno snap \n \t !! assicurati di avr fatto sourcee che le variabili d'ambiente siano correttamente sovrapposte \n "
    print "environment-blam: :\n \t source /home/teo/installer_SLAM/gui/blam/internal/devel/setup.bash --extend \n\n"
    print "environment-backpack:\n \t source /home/teo/installer_SLAM/gui/_core/catkin_ws/devel/setup.bash \n\n"
   
    print "E.g. path: " + '/home/teo/Documents/test_cleanBlam/2017-10-24_11-47-19/bag/bagfile_2017-10-24-11-48-44.bag'
    bag_file = raw_input(" pregasi di inserire il path (assoluto) al file .bag = >")
    ## settings
    output_bag_dir = 'bag/'
    output_post_dir = 'post_processing_test3/'
    path = bag_file.replace("/"+output_bag_dir,"/"+output_post_dir)
    prefix = path.replace(".bag",'')
    path = path.replace(".bag","")
    csv_file = path+".csv"
    print 'csv-file: ' +csv_file
    print 'prefix: ' + prefix

    #blam_run_test = 'roslaunch blam_example test_offline.launch'
    std_buf = False
    roslaunch_backpack_test =  'roslaunch bagpack 3dt_slam_offline.launch bagfile:=' + str(bag_file).strip()+' index_name:=' + str(csv_file).strip() + ' trajectory:=true'
    if not std_buf:
        pass
    else:
        roslaunch_backpack_test = 'stdbuf -oL' + roslaunch_backpack_test


    print "\n \n test backpack roslaunch only ?? \n => run : " + roslaunch_backpack_test + '\n \n'
    
    
    rosrun_pcl_test = 'rosrun pcl_ros pointcloud_to_pcd input:=/blam/blam_slam/octree_map _prefix:='+prefix

    

    backpack_run_in_thread = True# questa è la condizione che funziona, nello snap finale
    if backpack_run_in_thread:

    	backpack_thread = subprocessThread(roslaunch_backpack_test)
        rosrun_pcl_thread = subprocessThread(rosrun_pcl_test)

        threads = [backpack_thread,rosrun_pcl_thread]#roscore_thread => self called by roslaunch !!
    	for t in threads:
    		t.start()

# da incorporare necessariamente come metodo della classe della gui, modificare in qesta funzione attributo ready/starting/running/waiting
def check():

    check_run_in_thread = True
    if check_run_in_thread:
        check_thread = checkThread(process_info)
        check_thread.start()
        #check_thread.join()

    while True:
        time.sleep(10)
        #print process_info
        #print check_thread.check_info
        time.sleep(10)

    






if __name__ == '__main__':

    do_job()
    #check()

    

    
    
    



