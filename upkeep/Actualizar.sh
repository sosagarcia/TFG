#!/bin/bash
echo"###########################################################################"
echo "Empieza la actualización"
sudo apt update -y
echo "Empieza la instalación"
sudo apt-get upgrade -y
sudo apt dist-upgrade -y
echo "Reiniciando"
sudo apt clean -y
echo"###########################################################################"
sudo reboot


