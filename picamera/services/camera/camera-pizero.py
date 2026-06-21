from picamera import PiCamera
from gpiozero import Button
from PIL import Image

import time
import glob
import os
import subprocess

BSTATE_RELEASED = 0
BSTATE_PRESSED = 1
BSTATE_HELD = 2

bstate = BSTATE_RELEASED

# TO DO: handle all possible exceptions

button = Button(13, bounce_time=0.25)
camera = PiCamera()
video_filename = None

CAMERA_DIRECTORY = '/home/pi/camera'
PHOTOS_DIRECTORY = CAMERA_DIRECTORY + '/photos'
VIDEOS_DIRECTORY = CAMERA_DIRECTORY + '/videos'

def on_pressed(btn):
    print('button {} is pressed'.format(btn))
    global bstate
    bstate = BSTATE_PRESSED

def on_held(btn):
    print('button {} is held'.format(btn))
    global bstate
    bstate = BSTATE_HELD
    global video_filename
    video_filename = time.strftime("%Y%m%d-%H%M%S") + ".h264"
    global camera
    camera.start_recording(video_filename, format='h264')
    print("-- start recording {}".format(video_filename))

def on_released(btn):
    print('button {} is released'.format(btn))
    global bstate
    global camera
    if bstate == BSTATE_HELD:
        camera.stop_recording()
        print("-- stop recording")
        global video_filename
        if video_filename:
            os.rename(video_filename, os.path.join(VIDEOS_DIRECTORY, video_filename))
            video_filename = None
    elif bstate == BSTATE_PRESSED:
        filename = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
        filepath = os.path.join(PHOTOS_DIRECTORY, filename)
        camera.capture(filepath)
        print("-- capture image {}".format(filename))
        (path, extension) = os.path.splitext(filepath)
        small_img_path = path + '_small' + extension
        img = Image.open(filepath)
        small_img = img.resize((320, 180))
        small_img.save(small_img_path)

    bstate = BSTATE_RELEASED



def main():
    global camera
    camera.resolution = (1280, 720)
    camera.framerate = 25
    camera.rotation = 180
    camera.start_preview()

    global button
    button.when_held = on_held
    button.when_pressed = on_pressed
    button.when_released = on_released

    while True:
        total_time = 0.0
        h264_files = glob.glob(VIDEOS_DIRECTORY + '/*.h264')
        t0 = time.time()
        for file in h264_files:
            (prefix, _) = os.path.splitext(file)
            dst_file = prefix + '.mp4'
            subprocess.call(['/usr/bin/ffmpeg', '-r', '30', '-i', file, '-vcodec', 'copy', dst_file])
            # the duration of resizing is too long
            # dst_file = prefix + '_small.mp4'
            # subprocess.call(['/usr/bin/ffmpeg', '-i', file, '-vf', 'scale=320:180', '-c:v', 'libx264', '-c:a', 'copy', dst_file])
            os.remove(file)
        t1 = time.time()
        dt = t1 - t0
        if dt < 1.0:
            time.sleep(1.0)


if __name__ == '__main__':
    main()