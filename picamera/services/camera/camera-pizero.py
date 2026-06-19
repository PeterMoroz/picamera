from picamera import PiCamera
from gpiozero import Button

import time
import os
import subprocess

BSTATE_RELEASED = 0
BSTATE_PRESSED = 1
BSTATE_HELD = 2

bstate = BSTATE_RELEASED

# TO DO: handle all possible exceptions

button = Button(13, hold_time=2)
camera = PiCamera()
video_filename = None

CAMERA_DIRECTORY = '/home/pi/camera'
PHOTOS_DIRECTORY = CAMERA_DIRECTORY + '/photos'
VIDEOS_DIRECTORY = CAMERA_DIRECTORY + '/videos'

def on_pressed(btn):
    print("button {btn} is pressed")
    global bstate
    bstate = BSTATE_PRESSED

def on_held(btn):
    print("button {btn} is held")
    global bstate
    bstate = BSTATE_HELD
    global video_filename
    video_filename = time.strftime("%Y%m%d-%H%M%S") + ".h264"
    global camera
    camera.start_recording(video_filename, format='h264')
    print("-- start recording {}".format(video_filename))

def on_released(btn):
    print("button {btn} is released")
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
    bstate = BSTATE_RELEASED



def main():
    #button = Button(13)
    #camera = PiCamera()
    global camera
    camera.resolution = (1280, 720)
    camera.framerate = 25
    camera.start_preview()

    global button
    button.when_held = on_held
    button.when_pressed = on_pressed
    button.when_released = on_released

    while True:
        # time.sleep(1)

        #button.wait_for_press()
        #filename = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
        #camera.capture(filename)

        total_time = 0.0
        for root, _, files in os.walk(VIDEOS_DIRECTORY):
            for filename in files:
                if filename.endswith('h264'):
                    fullpath = os.path.join(root, filename)
                    name, _ = os.path.splitext(filename)
                    t0 = time.time()
                    subprocess.call(['/usr/bin/ffmpeg', '-r', '30', '-i', fullpath, '-vcodec', 'copy', os.path.join(root, '{}.mp4'.format(name))])
                    t1 = time.time()
                    os.remove(fullpath)
                    total_time += (t1 - t0)
        if total_time < 1.0:
            time.sleep(1.0)


    #camera.start_recording('video.mp4', format='h264')
    #time.sleep(30)
    #camera.stop_recording()
        
if __name__ == '__main__':
    main()