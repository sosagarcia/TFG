#!/usr/bin/python
import time
import datetime
import Adafruit_DHT

# Log file
log_path = "/var/log/iot/ht/"

# Configuracion del tipo de sensor DHT
sensor = Adafruit_DHT.DHT11

# Configuracion del puerto GPIO al cual esta conectado (GPIO 23)
pin = 4

# Escribe un archivo log en log_path con el nombre en el formato yyyy-mm-dd_dht.log
def write_log(text):
	log = open(log_path + datetime.datetime.now().strftime("%d-%m-%Y") + "_HumTemp.log","a")
	line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()


try:

	while True:
 
		humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)

		# Si obtiene una lectura del sensor la registra en el archivo log
		if humedad is not None and temperatura is not None:
			write_log("Temperatura: %s" % str(temperatura))
			write_log("Humedad:  %s" % str(humedad))
		else:
			write_log('Error al obtener la lectura del sensor')

		# Duerme 10 segundos
		time.sleep(10)


except Exception,e:
	# Registra el error en el archivo log y termina la ejecucion
	write_log(str(e))