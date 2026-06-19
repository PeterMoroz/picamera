#!/bin/bash

systemctl stop camera-pizero.service
systemctl disable camera-pizero.service

systemctl stop gallery-pizero.service
systemctl disable gallery-pizero.service

rm /etc/systemd/system/camera-pizero.service
rm /etc/systemd/system/gallery-pizero.service

systemctl daemon-reload

rm -rf '/home/pi/camera'

reboot
