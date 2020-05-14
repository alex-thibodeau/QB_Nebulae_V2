#!/bin/bash

mount /dev/sda1 /mnt/memory
rm /home/alarm/wifi.log
if [ -f /mnt/memory/wlan0-wifi ]
then
  echo starting wlan0-wifi> /home/alarm/wifi.log
  cp /mnt/memory/wlan0-wifi /etc/netctl
  ( sleep 10; systemctl start systemd-resolved; netctl start wlan0-wifi; iwconfig >> /home/alarm/wifi.log 2>&1 ) & 
else
  echo starting access point > /home/alarm/wifi.log
  ( sleep 10; systemctl start systemd-resolved; sh /home/alarm/QB_Nebulae_V2/Code/scripts/create_ap.sh --no-virt -n wlan0 Nebulae eurorack >> /home/alarm/wifi.log 2>&1 ) & 
fi

umount /dev/sda1
( sleep 10; systemctl start NebFile ) &
