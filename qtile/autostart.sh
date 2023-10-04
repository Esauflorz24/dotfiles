#!/bin/sh
# usb application
udiskie -t &

# network manager applet
nm-applet &

# volume icon
volumeicon &

# wallpapper
nitrogen --restore &

# composer
picom &

setxkbmap -layout us -variant altgr-intl -option nodeadkeys &
