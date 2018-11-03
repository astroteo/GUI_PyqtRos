import os
import compileall

directories = ["_test", "_driver", "bash", "output", "_core/catkin_ws/src/backpack", "_gui", "tmp", "__configuration_files", "_img", "utility", "_application", "_lib", "_conf", "_rviz", "_scripts"]

for d in directories:
    print "--------------------------------------------------------------------"
    print " DIRECTORY = "+d
    for root, dirs, files in os.walk("./"+d):
        for file in files:
            if file.endswith(".py"):
                filename=os.path.join(root, file)
                compileall.compile_file(filename, force=True)
                os.remove(filename)
print "--------------------------------------------------------------------"

files = ["./main.py", "./main_external.py"]
for f in files:
    print "--------------------------------------------------------------------"
    print " FILE = "+f
    filename=os.path.abspath(f)
    if filename.endswith(".py"):
        compileall.compile_file(filename, force=True)
        os.remove(filename)
print "--------------------------------------------------------------------"
