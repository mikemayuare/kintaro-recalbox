# Kintaro for Recalbox v9.0

Version 1.6.EB
Tested on Super Kuma 9000
tested on Raspberry Pi3 B

Creator: Kintaro
Author: Michael Kirsch & Eduardo Betancourt
This is the official Kintaro script for Recalbox.

Changelog: 
v1.6.EB | 08/08/2023 
I make an uodate on some script mainly on .sh file to make it work with recalbox 9.0
it works flawless from first install and reboot.
remember maintain the power button 'ON" on the first reboot o power supply connect.

Issues:
Some minor actions with the reset buttons

To install this script you do the following steps:

1. Connect with SSH
2. Remount partition on read-write with the command: ```mount -o remount,rw /```
3. Then copy the ```S100kintaro.sh``` into ```/etc/init.d```
4. Copy the ```kintaro``` folder into ```/opt/``` 
5. reboot
