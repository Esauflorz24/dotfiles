#!/bin/sh
nitrogen --restore &
udiskie -t &
volumeicon &
nm-applet &
cbatticon -u 5 &
picom &
#picom --config=$HOME/.config/picom/picom.conf &

