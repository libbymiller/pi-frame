# pi-frame

A simple Raspberry Pi based photo frame. See the blog post for more info: https://planb.nicecupoftea.org/2016/12/23/a-simple-raspberry-pi-based-picture-frame-using-flickr/

# Instructions

## Gather hardware

Version 1: Pi3, official touchscreen (you'll need a 2.5A power supply to power them together), 8GB micro SD card, and a ModMyPi customisable Pi screen stand.

Version 2: Pi Zero, micro USB converter, USB wifi, mini HDMI converter, HDMI cable, 8GB micro SD card, data micro USB cable, maybe a case.

## Create a flickr account and get a developer key

https://www.flickr.com/signup
https://www.flickr.com/services/apps/create/noncommercial/

## Provision an SD card


## Log in to the pi

for the Zero, follow these instructions:

For Pi3, I usually use etheret and shared network to ssh in.

## Change hostname, password, add wifi

change password

    passwd

change hostname 

    sudo pico /etc/hosts
    sudo pico /etc/hostname

add wifi credentials

    sudo pico /etc/wpa_supplicant/wpa_supplicant.conf

    network={
      ssid="YOUR NETWORK SSID"
      psk="YOUR NETWORK PASSWORD"
    }

or if your network has no password

    network={
      ssid="YOUR NETWORK SSID"
      proto=RSN
      key_mgmt=NONE
    }

## Get this repo

    git clone git@github.com:libbymiller/pi-frame.git /home/pi/frame

## Install prerequisites

   pip install flickrapi

If using face detection

   pip install numpy
   sudo apt-get install python-opencv
   curl -O https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml

## Test (if connected to a screen

    export DISPLAY=:0.0
    bash /home/pi/frame/frame.sh
    
## Configure crontab and autostart

    pico ~/.config/lxsession/LXDE-pi/autostart

contents should be:

    @lxpanel --profile LXDE-pi
    @pcmanfm --desktop --profile LXDE-pi
    @xscreensaver -no-splash
    @xset s off
    @xset -dpms
    @xset s noblank

    @/bin/bash /home/pi/frame/frame.sh

Add crontab

    crontab -e

    0,15,30,45 * * * * cd /home/pi/frame && /usr/bin/python cacheimages.py > log.txt 2>&1

or for pi zero (no face detection)

    0,15,30,45 * * * * cd /home/pi/frame && /usr/bin/python cacheimages_zero.py > log.txt 2>&1

