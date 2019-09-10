#!/bin/bash
DIA=`date +"%d/%m/%Y"`
HORA=`date +"%H:%M"`
echo "Hoy es  $DIA y la hora actual es $HORA"

sudo python3 /home/pi/Scripts/worker.py &
sudo python3 /home/pi/Scripts/status.py &
 #as