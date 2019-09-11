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
config = "/var/log/iot/config/configuracion.conf"


dName = "_Distancia.log"
hName = "_Humedad.log"
tName = "_Temperatura.log"
irName = "_Movimientos.log"
aName = "_Alarmas.log"
cpuTName = "_TemperaturaCPU.log"
cpuName = "_UsoCPU.log"
outName = "_Out.log"


def write_log(text, path, name):
    try:
        with open(path + datetime.datetime.now().strftime("%Y-%m-%d") + name, "a") as f:
            line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
            f.write(line)

    finally:
        f.close()

def read_conf():
    try:
        with open(config, "r") as f:
            configuraciones = f.readlines()
            f.close()
            result = list ()
            max = len(configuraciones)
            for i in range (0, max):
                linea = configuraciones [i]
                maxL = len(linea)
                result [i] = linea[7:maxL]
            return result


    finally:
        f.close()
