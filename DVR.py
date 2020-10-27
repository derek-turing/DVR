#!/usr/bin/env python
#! --*-- coding:utf-8 --*--
import cv2
import time
from datetime import datetime
import sys
import os, os.path
import logging

# ip = first para
IP = ' '.join(sys.argv[1:2])

# path = second para
PATH = ' '.join(sys.argv[2:])

# motion threshold (percent)
motion_threshold = 0.0001
record_time = 1200 # (secs)

# display debug frames
DEBUG = True

# max number of videos
max_nof_videos = 800

FPS = 15

def drawFrame (frame,text):
    cv2.putText(frame, text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

def captureVideo():

    # everfocus
    cap = cv2.VideoCapture("rtsp://admin:admin@"+ IP +":554/ch01/0") 
    

    if (cap.isOpened()== False):
        print("Error opening video stream or file")        
        return False
   
    imgSaveCount = 0
    numofdig = 4
    
    h_small = 0
    w_small = 0
    
    if (cap.isOpened()== True):
        # first cap
        ret, frame = cap.read()
        # get imagesize
        h, w, c = frame.shape
        print (cap.get(cv2.CAP_PROP_FPS))
        
    # record video setup  
    encode = cv2.VideoWriter_fourcc(*'MJPG')    
    out = None
    
    time_start = 0
    time_now = 0
    time_end = 0

    # Initializing motion = 0(no motion) 
    motion = 0
     
    # simple version for working with CWD
    count_file = len([name for name in os.listdir('.') if os.path.isfile(name)])
    
    # if too many videos than break all
    if (count_file >= max_nof_videos):                   
        print ("too many video , please remove some videos.")                    
        return False
    
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    out = cv2.VideoWriter( PATH + '/' + date_time + '.avi', encode, FPS, (w, h), True)                
    time_start = time.time()
    str_start_recording = "start recording : " + date_time
    print (str_start_recording)

    while(cap.isOpened()):
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == True:
            # Display the resulting frame

            if DEBUG :
                cv2.imshow('Frame',frame)   
            # wirten video
            out.write(frame)

            if DEBUG:
                # listance the keyboard
                k = cv2.waitKey(1)  

                if k == ord('s'):
                    fileNo = str(imgSaveCount).zfill(int(numofdig))
                    cv2.imwrite('saveImg/' + fileNo + '.png',frame)
                    imgSaveCount = imgSaveCount +1

                if k == 27:# wait for ESC key to exit 
                    out.release
                    print ("recording finishd !!! ")
                    break
            
            # get time
            time_now = time.time() 

        # save the video
            if time_now - time_start >= record_time :               
                time_end = time.time()
                out.release
                print ("recording finishd !!! ")

                # recording again
                now = datetime.now() # current date and time
                date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
                out = cv2.VideoWriter( PATH + '/' + date_time + '.avi', encode, FPS, (w, h), True)                
                time_start = time.time()
                str_start_recording = "start recording : " + date_time
                print (str_start_recording)

        # Break the loop
        else:
            print ("ret is false , can't get frame.")
            break

    
    # When everything done, release the video capture object
    if out:
        out.release
    
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


# real main start
def main():  
  
    print ("start open camera ...")
    captureVideo()
             

if __name__ == "__main__":
    main()


