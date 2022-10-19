#!/bin/sh
nitrogen --restore &
udiskie -t &
volumeicon &
nm-applet &
cbatticon -u 5 &
picom &
dex $HOME/.config/autostart/arcolinux-welcome-app.desktop &
