#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ros_thread import subprocessThread
import subprocess

def do_job(bag_file):
        
        print "processing bag-file => path = "+ bag_file
        ## settings
        output_bag_dir = 'bag/'
        output_post_dir = 'post_processing/'
        path = bag_file.replace("/"+output_bag_dir,"/"+output_post_dir)
        prefix = path.replace(".bag",'')
        path = path.replace(".bag","")
        csv_file = path+".csv"
        print 'csv-file: ' +csv_file
        print 'prefix: ' + prefix
        print "processing bag-file => path = "+ bag_file
        #blam_run_test = 'roslaunch blam_example test_offline.launch'
        std_buf = False
        roslaunch_backpack_test =  'roslaunch bagpack 3dt_slam_offline.launch bagfile:=' + str(bag_file).strip()+' index_name:=' + str(csv_file).strip() + ' trajectory:=true'
        if not std_buf:
            pass
        else:
            roslaunch_backpack_test = 'stdbuf -oL' + roslaunch_backpack_test
        
        rosrun_pcl_test = 'rosrun pcl_ros pointcloud_to_pcd input:=/blam/blam_slam/octree_map _prefix:='+prefix

        

        backpack_run_in_thread = True# questa è la condizione che funziona, nello snap finale
        if backpack_run_in_thread:

            backpack_thread = subprocessThread(roslaunch_backpack_test)
            rosrun_pcl_thread = subprocessThread(rosrun_pcl_test)

            threads = [backpack_thread,rosrun_pcl_thread]#roscore_thread => self called by roslaunch !!
            for t in threads:
                t.start()