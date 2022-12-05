#!/bin/sh
nitrogen --restore &
udiskie -t &
volumeicon &
nm-applet &
cbatticon -u 5 &
setxkbmap -layout us -variant altgr-intl -option nodeadkeys
picom &
#picom --config=$HOME/.config/picom/picom.conf &

