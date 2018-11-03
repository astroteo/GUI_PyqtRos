#!/bin/bash
echo " blam_offline fucking invoked"
################################################################################
TITLE_NAME="BLAM OFFLINE"
BLAM_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../_core/blam/"
BAG_FILE="$1"
CSV_FILE="$2"
PREFIX="$3"
DATE=`date +%Y-%m-%d_%H-%M-%S-`
################################################################################
echo "checking variables: "
echo "========================================================================="
echo "BLAM_PATH == "
echo $BLAM_PATH

echo "BAG_FILE == "
echo $BAG_FILE

echo "CSV_FILE == "
echo $CSV_FILE

echo "PREFIX == "
echo $PREFIX

echo "========================================================================="


UTILITY_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_utility/"
source "${UTILITY_PATH}/title.sh"

#: << END
title " BEGIN ${TITLE_NAME}"

mv /tmp/blam.check_out /tmp/blam.check_out_bkp
mv /tmp/blam.cmd.check /tmp/blam.cmd.check_bkp
rm -rf /tmp/blam.check_out /tmp/blam.cmd.check

################################################################################
CMD="stdbuf -oL roslaunch bagpack 3dt_slam_offline.launch bagfile:=\"${BAG_FILE}\" index_name:=\"${CSV_FILE}\" trajectory:=true"
echo $CMD > /tmp/blam.cmd.check &
stdbuf -oL roslaunch bagpack 3dt_slam_offline.launch \
  bagfile:="${BAG_FILE}" \
  index_name:="${CSV_FILE}" \
  trajectory:=true > /tmp/blam.check_out &

echo "RECORD"
rosrun pcl_ros pointcloud_to_pcd input:=/blam/blam_slam/octree_map _prefix:=${PREFIX}
################################################################################

title " END   ${TITLE_NAME}"
#END
#echo " temporarily locked BLAM for debugging  "
