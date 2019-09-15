#!/bin/bash
DIA=`date +"%d/%m/%Y"`
HORA=`date +"%H:%M:%S"`
echo "###########################################################################"
echo "Hoy es  $DIA y la hora actual es $HORA"
sudo service apache2 stop &
cd
cd /var/www/html/
echo "Borrando"
sudo rm -R TFG/
echo "Empieza el Clonado"
sudo git clone https://sosagarcia:nuevacontraseña12@github.com/sosagarcia/TFG.git
echo "Permisos"
cd
sudo chmod -R 777 /var/www
echo "Reiniciando Apache"
sudo service apache2 start &
echo "Copiando scripts"
sudo cp -R /var/www/html/TFG/upkeep/* /home/pi/Scripts/
echo "Permisos Scripts"
sudo chmod -R 777 /home/pi/Scripts/
echo "copiando fotos"
sudo cp -R /var/log/iot/camera/* /var/www/html/TFG/static/img/camara
ra
echo "###########################################################################"