#!/bin/bash
DIA=`date +"%d/%m/%Y"`
HORA=`date +"%H:%M:%S"`
echo "###########################################################################"
echo "Hoy es  $DIA y la hora actual es $HORA"
echo "iniciando Status.py en segundo plano"
sudo python3 /var/www/html/TFG/status.py &
statusPID=$!
echo "Pid actual de status.py:  $statusPID"
echo "iniciando worker.py en segundo plano"
sudo python3 /var/www/html/TFG/worker.py &
workerPID=$!
echo "Pid actual de worker.py:  $workerPID"
 echo "###########################################################################"