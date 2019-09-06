
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
    stop = int(muestras/salto)
    print(stop)
    print(fin)
    print(final)
    for i in range(0, final, int(salto)):
        conteo = 0

        valorMedia = 0
        if (i >= stop):
            restantes = final - i
            print(i)
            print(restantes)
            fin = restantes
        for j in range(0, fin):
            linea = dia[j + i]
            valor = linea[20:24]
            if not (valor == "Erro") and (linea[10:11] == " "):
                if conteo == 0:
                    fecha = linea[0:20]
                conteo += 1
                valorMedia += float(valor)
        result = valorMedia / conteo
        newLine = fecha + str(result) + " " + str(unit)
        subresult.append(newLine)
    return subresult


def reWrite(text, path, name, fecha):
    try:
        with open(path + fecha + name + "_old" + ".log", "a") as f:
            f.writelines(text)
            print("Eliminando archivo viejo")
            remove(path + fecha + name + ".log")

    finally:
        f.close()


def dameFecha():
    hoy = dt.datetime.now()
    fecha = hoy - timedelta(days=31)
    result = fecha.strftime("%Y-%m-%d")
    return result


def openFile(path, name):
    fecha = dameFecha()
    print(fecha)
    ruta = str(path) + str(fecha) + name + ".log"
    print(ruta)
    try:
        with open(ruta,  "r") as f:
            logLines = f.readlines()
            f.close()

    except:

        return (-1, -1)

    return logLines, fecha


def cpuH():
    fichero, fecha = openFile(cpuPath, cpuName)
    if not (fichero == -1):
        print("calculando Media")
        newFile = media(fichero, "%")
        reWrite(newFile, cpuPath, cpuName, fecha)
    else:
        print("Error 1")


if __name__ == '__main__':

    #t1 = threading.Thread(target=cpuH)

    # t1.setDaemon(True)

    print("iniciando")
    # t1.start()
    cpuH()
