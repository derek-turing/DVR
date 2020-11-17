#!/bin/bash -i
run_dir="."
video_dir=vid_0

nowday="$(date +'%Y_%m_%d')"
oldday="$(date -d '14 day ago' +'%Y_%m_%d')"

cam_ip=192.168.10.168


echo "To day is:" $nowday
echo "Remove the file of day:" $oldday

# remove 14 days video
rm $oldday*.avi

# move to target dir
cd $run_dir 
python3 DVR.py $cam_ip $video_dir
