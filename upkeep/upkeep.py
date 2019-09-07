
from datetime import date, datetime, timedelta
import datetime as dt
from os import remove
import threading
# Rutas de LOG

reduction = 0.1

hPath = "/var/log/iot/hum/"
tPath = "/var/log/iot/tem/"
irPath = "/var/log/iot/ir/"
disPath = "/var/log/iot/dis/"
aPath = "/var/log/iot/a/"
cpuTPath = "/var/log/iot/cpuT/"
cpuPath = "/var/log/iot/cpu/"
outPath = "/var/log/iot/out/"


dName = "_Distancia"
hName = "_Humedad"
tName = "_Temperatura"
irName = "_Movimientos"
aName = "_Alarmas"
cpuTName = "_TemperaturaCPU"
cpuName = "_UsoCPU"
outName = "_Out"


def media(dia, unit):
    subresult = list()
    muestras = len(dia)
    salto = 1 / reduction
    final = muestras - 1
    fin = int(salto - 1)
    print
    for i in range(0, final, int(salto)):
        conteo = 0
        valorMedia = 0
        if (i >= (final - int(salto))):
            restantes = final - i
            fin = restantes
        for j in range(0, fin):
            linea = dia[j + i]
            valor = linea[20:24]
            if not (valor == "Erro") and (linea[10:11] == " "):
                if conteo == 0:
                    fecha = linea[0:20]
                conteo += 1
                valorMedia += float(valor)
        result = "{0:.2f}".format(valorMedia / conteo)
        newLine = fecha + str(result) + " " + str(unit) + '\n'
        subresult.append(newLine)
    return subresult


def reWrite(text, path, name, fecha):
    try:
        with open(path + fecha + name + ".log", "a") as f:
            remove(path + fecha + name + ".log")
            f.writelines(text)

    finally:
        f.close()


def dameFecha():
    hoy = dt.datetime.now()
    fecha = hoy - timedelta(days=31)
    result = fecha.strftime("%Y-%m-%d")
    return result


def openFile(path, name):
    fecha = dameFecha()
    ruta = str(path) + str(fecha) + name + ".log"
    print(ruta)
    try:
        with open(ruta,  "r") as f:
            logLines = f.readlines()
            f.close()

    except:

        return (-1, -1)

    return logLines, fecha


def empieza(path, name):
    fichero, fecha = openFile(path, name)
    print(len(fichero))
    print(fecha)
    if not (fichero == -1):
        print("a calcular media ")
        newFile = media(fichero, "%")
        print("a reescribir")
        reWrite(newFile, cpuPath, cpuName, fecha)
    else:
        print("pochao")
        pass


if __name__ == '__main__':

    try:
        print("CPUT")
        empieza(cpuTPath, cpuTName)
        print("CPU")
        empieza(cpuPath, cpuName)
    except:
        print("Se ha pochao")
        raise
    finally:
        print("finito")
