#!/usr/bin/python
import datetime
import cv2
import os

# Config
stream_url = 'http://192.168.1.2:4321/stream.mjpg'

# Determine save location
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H-%M-%S")
absolute_script_dir = os.path.dirname(os.path.realpath(__file__))
save_dir = absolute_script_dir + '/snapshots/' + date
save_path = save_dir + '/' + time + '.jpg'

# Capture frame from camera stream
cap = cv2.VideoCapture(stream_url)
ret, frame = cap.read()

# Save frame as image
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

cv2.imwrite(save_path, frame)
