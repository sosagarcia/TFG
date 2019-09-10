#!/bin/bash
DIA=`date +"%d/%m/%Y"`
HORA=`date +"%H:%M"`
echo "Hoy es  $DIA y la hora actual es $HORA"

sudo python3 /var/www/html/TFG/status.py &
sudo python3 /var/www/html/TFG/worker.py &
 #as