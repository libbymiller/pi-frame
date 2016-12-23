#!/bin/bash

# random is just to stop it caching
myrandom=$RANDOM

# start a tiny server
cd /home/pi/frame/public && /usr/bin/python -m SimpleHTTPServer 3000 &

# again to stop it caching
rm -rf /home/pi/.config/chromium/
/usr/bin/chromium-browser --disable-infobars --disable-session-crashed-bubble --disable-application-cache --no-first-run http://localhost:3000/index.html#$myrandom




