#!/bin/bash


mkdir -p '/home/pi/camera/photos'
mkdir -p '/home/pi/camera/videos'

mkdir -p '/home/pi/camera/services/camera'
mkdir -p '/home/pi/camera/services/gallery'

cp -r 'services/camera' '/home/pi/camera/services/'
cp -r 'services/gallery' '/home/pi/camera/services/'

chown -R pi:pi '/home/pi/camera'

cp camera-pizero.service /etc/systemd/system/
cp gallery-pizero.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable camera-pizero.service
systemctl enable gallery-pizero.service

reboot
