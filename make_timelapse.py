#!/usr/bin/python
from datetime import date, timedelta
import cv2
import os
import shutil
import sys
import cli_utils

# Check arguments for fps
output_fps = float(cli_utils.get_cli_arg_with_default("--fps", 5.0))

# Check arguments for custom date
custom_date = cli_utils.get_cli_arg("--date")
if custom_date is None and cli_utils.has_cli_arg("--today"):
    custom_date = date.today().strftime("%Y-%m-%d")

if custom_date is None:
    # Get yesterday's snapshots
    yesterday = date.today() - timedelta(1)
    source_date = yesterday.strftime("%Y-%m-%d")
else:
    # Get snapshots for specified date
    source_date = custom_date

# Determine source directory
absolute_script_dir = os.path.dirname(os.path.realpath(__file__))
source_dir = absolute_script_dir + '/snapshots/' + source_date

if not os.path.exists(source_dir):
    print("Error: Source directory does not exist: {}".format(source_dir))
    sys.exit(1)

# Determine save location for timelapse video
save_dir = absolute_script_dir + '/timelapses'
save_path = save_dir + '/' + source_date + '.avi'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Delete any empty image files that were created in error
for imageFile in os.listdir(source_dir):
    if os.path.getsize(source_dir + "/" + imageFile) == 0:
        os.remove(source_dir + "/" + imageFile)

# Create timelapse and save
images = [img for img in os.listdir(source_dir)]
images.sort()
frame = cv2.imread(os.path.join(source_dir, images[0]))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter(save_path, fourcc, output_fps, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(source_dir, image)))

video.release()

# Ensure timelapse was generated successfully
if not os.path.exists(save_path):
    print("Error: Failed to generate timelapse video file.")
    sys.exit(2)

# Delete source images if desired
if cli_utils.has_cli_arg("--cleanup"):
    shutil.rmtree(source_dir)
