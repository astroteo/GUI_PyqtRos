import subprocess
import time
from _lib.UDP_TCP_server import get_OxTS_msg, send_cmd_photo_server

def check_configuration_pane_vals(values, home_path, stop_event, lock):
    try:
        MESSAGE = 'S'
        data = send_cmd_photo_server(MESSAGE)
    except:
        data = "Error"

    if "OK" in data:
        values[1].setText("[OK]")
        values[1].setStyleSheet("color: green")
    else:
        values[1].setText("[Error]")
        values[1].setStyleSheet("color: red")
    while True and not stop_event.is_set():
        time.sleep(3);
        with lock:
            update_cam_num(values, home_path)
            imu_check(values, home_path)
            vel_pc(values, home_path)
            vel_ls(values, home_path)
            values[0].update()
            values[1].update()
            values[2].update()
            values[3].update()
            values[4].update()

def update_cam_num(values, home_path):
    cmd = home_path+"/_camera/build/camera_num"
    p = subprocess.Popen(cmd.split(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    values[0].setText(str(out))
    if int(out) < 4:
        values[0].setStyleSheet("color: red; margin:20px;")
    else:
        values[0].setStyleSheet("color: green; margin:20px;")

    # print " ---> ",values[1].text()
    if int(out) < 4 or values[1].text() == "[Error]":
        # print "=====>"
        cmd = home_path+"/_camera/_main/click.py S"
        p = subprocess.Popen(cmd.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = p.communicate()
        if "OK" in out:
            values[1].setText("[OK]")
            values[1].setStyleSheet("color: green")
            # print "=====> OK"
        else:
            values[1].setText("[Error]")
            values[1].setStyleSheet("color: red")
            # print "=====> NOOOO"

def imu_check(values, home_path):
    cmd = home_path+"/bash/check_imu.sh"
    p = subprocess.Popen(cmd.split(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    if int(out) < 1:
        values[2].setText("[FAIL]")
        values[2].setStyleSheet("color: red; margin:20px;")
    else:
        values[2].setText("[OK]")
        values[2].setStyleSheet("color: green; margin:20px;")

def vel_pc(values, home_path):
    cmd = home_path+"/bash/check_velodyne_point_cloud.sh"
    p = subprocess.Popen(cmd.split(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    if int(out) < 1:
        values[3].setText("[FAIL]")
        values[3].setStyleSheet("color: red; margin:20px;")
    else:
        values[3].setText("[OK]")
        values[3].setStyleSheet("color: green; margin:20px;")

def vel_ls(values, home_path):
    cmd = home_path+"/bash/check_velodyne_scan.sh"
    p = subprocess.Popen(cmd.split(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    if int(out) < 1:
        values[4].setText("[FAIL]")
        values[4].setStyleSheet("color: red; margin:20px;")
    else:
        values[4].setText("[OK]")
        values[4].setStyleSheet("color: green; margin:20px;")
