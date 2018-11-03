'''
creates the correct rosparam nel backpack ros-node
'''
from xml.dom import minidom

def rospathSet(base_path):
    backpack_set_path = base_path+ '/_core/catkin_ws/src/backpack/launch/'
    tdt_slam_offline_launch_path = backpack_set_path + '3dt_slam_offline.launch'
    tdt_offline_launch_doc = minidom.parse(tdt_slam_offline_launch_path)
    tdt_offline_launch_params = tdt_offline_launch_doc.getElementsByTagName('rosparam')
    print tdt_offline_launch_doc.toxml()

    for i in range(1,len(tdt_offline_launch_params)):
        #print tdt_offline_launch_params[i].attributes['file'].value
        curr_val = tdt_offline_launch_params[i].attributes['file'].value
        end_val = curr_val.split('/')[-1]
        good_val = base_path + '/bash/blam_slam/' + end_val
        print good_val
        tdt_offline_launch_params[i].attributes['file'].value = good_val
        #print tdt_offline_launch_params[i].attributes['file'].value
    print tdt_offline_launch_doc.toxml()
    tdt_offline_launch_doc.writexml(open(tdt_slam_offline_launch_path,'w'))
