
#!/bin/bash
DIA=`date +"%d/%m/%Y"`
HORA=`date +"%H:%M"`

echo "Hoy es  $DIA y la hora actual es $HORA"

echo "Empieza el commit"
cd /var/log/iot/
sudo git add .
sudo git commit -m "Hoy es  $DIA y la hora actual es $HORA"
#sudo git remote add origin https://MonYCon:EmeyCe.123@github.com/MonYCon/logs.$
sudo git push -u origin master
