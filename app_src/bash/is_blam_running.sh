#!/bin/bash

RESULT1=`cat /tmp/blam.check_out 2>&1 | grep -oh "Finished processing bag file"`
RESULT2=`cat /tmp/blam.check_out 2>&1 | grep -oh "shutting down processing monitor complete"`
RESULT3=`cat /tmp/blam.check_out 2>&1 | grep -oh "No such file or directory"`
RESULT="$RESULT1$RESULT2$RESULT3"
if [ -z "$RESULT" ]; then
  echo 1
else
  echo 0
fi
