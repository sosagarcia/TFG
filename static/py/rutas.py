import datetime
from os import remove, rename

# Rutas de LOG

hPath = "/var/log/iot/hum/"
tPath = "/var/log/iot/tem/"
irPath = "/var/log/iot/ir/"
disPath = "/var/log/iot/dis/"
aPath = "/var/log/iot/a/"
cpuTPath = "/var/log/iot/cpuT/"
cpuPath = "/var/log/iot/cpu/"
outPath = "/var/log/iot/out/"
config = "/var/log/iot/config/configuracion.conf"
confPath = "/var/log/iot/config/"
camara = "/var/log/iot/camera/"


dName = "_Distancia.log"
hName = "_Humedad.log"
tName = "_Temperatura.log"
irName = "_Movimientos.log"
aName = "_Alarmas.log"
cpuTName = "_TemperaturaCPU.log"
cpuName = "_UsoCPU.log"
outName = "_Out.log"
confName = "_Changes.log"


def write_log(text, path, name):
    try:
        with open(path + datetime.datetime.now().strftime("%Y-%m-%d") + name, "a") as f:
            line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
            f.write(line)

    finally:
        f.close()


def read_conf():
    try:
        with open(config, "r") as fconfig:
            configuraciones = fconfig.readlines()
            fconfig.close()
            result = list()
            max = len(configuraciones)
            for i in range(1, max - 1):
                linea = configuraciones[i]
                maxL = len(linea)
                result.append(linea[7: maxL - 1])
            return result

    finally:
        fconfig.close()


def save_conf(text):
    try:
        new = "/var/log/iot/config/configuracion" + "_Temp" + ".log"
        log = "Los ajustes cambiaran a la siguiente confirguación : " + '\n' + text
        write_log(log, confPath, confName)
        with open(new, "a") as f:

            f.write(text)
            remove(config)

    finally:
        rename(new, config)
        f.close()
