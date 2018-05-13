# IPCam Timelapse Generator
This project contains a collection of Python scripts for generating timelapse
videos from streaming IP cameras. This project works by taking single-frame
snapshots of a running IP camera stream, storing and organizing the snapshots
by date, then generating a timelapse video from the snapshots for a particular
day.

## Requirements
- Python 2.7
- OpenCV for Python

## Usage
To begin using the scripts, clone or download the Git repository to the system
on which you would like to run the timelapse generator. Then, be sure to follow
the steps outlined in the [**Setup**](#setup) section of this README.

The project consists of two runnable scripts, `take_snapshot.py` and
`make_timelapse.py`.

### `take_snapshot.py`
The `take_snapshot.py` script takes no parameters. When run, it simply consumes
the configured camera stream and saves a single frame as a JPEG image. It saves
the image to the `snapshots/<date>` directory within the same directory in
which the script is located (`<date>` is the current date in `YYYY-MM-DD`
format). Even if the script is run in a different directory, the image will
always be saved in the same directory relative to the script's location. The
snapshot file will be named `HH-MM-SS.jpg`, where `HH`, `MM`, and `SS` are the
hour, minute, and second, respectively, at which the snapshot was taken. If no
`snapshots` directory exists, it is automatically created at runtime.

You may run the script as follows:

```
./take_snapshot.py
```

### `make_timelapse.py`
The `make_timelapse.py` script compiles all snapshots for a given date into a
single `.avi` video file, which is saved to the `timelapses` directory within
the same directory in which the script is located. If this directory does not
exist, it is automatically created at runtime. The file will be named as
`YYYY-MM-DD.avi`, where `YYYY-MM-DD` is the date on which the snapshots were
taken (which will not necessarily be today's date). When run with no
parameters, the script will use yesterday's date as the date for which to
generate a timelapse.

This script takes the following optional parameters:
- `--today` : make a timelapse using snapshots taken on today's date
- `--date <YYYY-MM-DD>` : make a timelapse using snapshots taken on the
  specified date, provided in `YYYY-MM-DD` format
- `--fps <float>` : output the timelapse video with the specified number of
  frames (i.e., snapshots) per second. Defaults to `5.0` frames per second
- `--cleanup` : flag which instructs the script to delete all snapshot images
  from disk for the given date, after the timelapse video has been generated.
  Does not delete snapshots if timelapse video file could not be generated

You may run the script as follows:

```
./make_timelapse.py
```

## Setup
### 1. Install Python 2.7
If you're running a Linux distribution or macOS, chances are you already have
Python 2.7 installed by default.

If you're running Windows, you can install Python 2.7 by visiting
https://www.python.org/downloads and downloading the appropriate installer for
your platform.

### 2. Install OpenCV
Installing OpenCV for Python can be challenging depending on your platform, but
if you're running a Debian-based distribution of Linux (such as Ubuntu or
Mint), then you should be able to easily install OpenCV by running:

```
sudo apt-get install python-opencv
```

Otherwise, if you have [`pip`](https://pypi.org/project/pip/) installed, you
can try the following:

```
pip install opencv-contrib-python
```

### 3. Configure URL to camera stream
In order for the `take_snapshot.py` script to be able to save a frame from a
camera stream, you must configure the URL to your IP camera's video stream.
Edit `take_snapshot.py` and look for the `stream_url` variable definition:

```
stream_url = 'http://192.168.1.2:4321/stream.mjpg'
```

Change the value of the `stream_url` variable to the correct URL for the video
stream you wish to consume. A dummy URL is supplied in the code and will likely
not work with your setup.

### 4. Setup cron job (optional)
Optionally, you may choose to run the snapshot and timelapse generator scripts
automatically at certain intervals by setting up a cron job on your system.
This is preferred, as it takes the manual work out of capturing snapshots
throughout the day and compiling the final timelapse.

To setup a cron job, you could edit your `/etc/crontab` file and add the
following lines to the bottom:

```
*/5 * * * * user /home/user/ipcam-timelapse/take_snapshot.py
02 00 * * * user /home/user/ipcam-timelapse/make_timelapse.py
```

Replace `user` above with the name of the user you wish to run the scripts.
Also, change the absolute paths to each script to point to their actual
locations on your system.

In the above example, the first line configures the `take_snapshot.py` script
to run every 5 minutes (`*/5`), which means a new snapshot will be taken from
the camera stream and saved to disk every 5 minutes throughout each day. The
second line configures the `make_timelapse.py` script to run every day at 12:02
AM, which will group together all snapshots generated for the previous day and
combine them into a video file. In real life usage, it may also be a good idea
to pass the `--cleanup` flag to `make_timelapse.py`, in order to prevent
excessive disk space usage due to keeping unneeded snapshots around.

