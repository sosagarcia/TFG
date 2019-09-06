import datetime
# Rutas de LOG

hPath = "/var/log/iot/hum/"
tPath = "/var/log/iot/tem/"
irPath = "/var/log/iot/ir/"
disPath = "/var/log/iot/dis/"
aPath = "/var/log/iot/a/"
cpuTPath = "/var/log/iot/cpuT/"
cpuPath = "/var/log/iot/cpu/"
outPath = "/var/log/iot/out/"


dName = "_Distancia.log"
hName = "_Humedad.log"
tName = "_Temperatura.log"
irName = "_Movimientos.log"
aName = "_Alarmas.log"
cpuTName = "_TemperaturaCPU.log"
cpuName = "_UsoCPU.log"
outName = "_Out.log"


def write_log(text, path, name):
    log = open(path + datetime.datetime.now().strftime("%Y-%m-%d") + name, "a")
    line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
    log.write(line)
    log.close()
