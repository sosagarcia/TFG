
from datetime import date, datetime, timedelta
import datetime as dt
from os import remove, rename
import threading
# Rutas de LOG

reduction = 0.1

hPath = "/var/log/iot/hum/"
tPath = "/var/log/iot/tem/"
disPath = "/var/log/iot/dis/"
cpuTPath = "/var/log/iot/cpuT/"
cpuPath = "/var/log/iot/cpu/"


dName = "_Distancia"
hName = "_Humedad"
tName = "_Temperatura"
cpuTName = "_TemperaturaCPU"
cpuName = "_UsoCPU"


unidades = {
    "_Distancia": "cm.",
    "_Humedad": "%",
    "_Temperatura": "ºC",
    "_TemperaturaCPU": "ºC",
    "_UsoCPU": "%"
}


def dameUnit(tipo):
    unit = unidades.get(str(tipo))
    return unit


def reduccion(dia, unit):
    subresult = list()
    muestras = len(dia)
    salto = 1 / reduction
    final = muestras - 1
    for i in range(0, final, int(salto)):
        linea = dia[i]
        valor = linea[20:24]
        if not (valor == "Erro") and (linea[10:11] == " "):
            fecha = linea[0:20]
            newLine = fecha + valor + " " + unit + '\n'
            subresult.append(newLine)
    return subresult


def media(dia, unit):
    subresult = list()
    muestras = len(dia)
    salto = 1 / reduction
    final = muestras - 1
    fin = int(salto - 1)
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
                if (j <= int(fin/2)):
                    fecha = linea[0:20]
                conteo += 1
                valorMedia += float(valor)
        result = "{0:.2f}".format(valorMedia / conteo)
        newLine = fecha + str(result) + " " + unit + '\n'
        subresult.append(newLine)
    return subresult


def reWrite(text, path, name, fecha):
    try:
        new = path + fecha + name + "_Temp" + ".log"
        old = path + fecha + name + ".log"

        with open(new, "a") as f:
            f.writelines(text)
            remove(old)

    finally:
        rename(new, old)
        f.close()
        print("Se ha reducido correctamente el contenido del archivo")


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
    if not (fichero == -1):
        unit = dameUnit(name)
        if (name == cpuName):
            newFile = reduccion(fichero, unit)
        else:
            newFile = media(fichero, unit)
        reWrite(newFile, path, name, fecha)
    else:
        print("Error")
        pass


if __name__ == '__main__':

    try:
        hoy = dt.datetime.now()

        print("Empieza tarea de mantenimiento, a fecha de : " +
              hoy.strftime("%d-%m-%Y %H:%M:%S"))
        empieza(disPath, dName)
        empieza(hPath, hName)
        empieza(tPath, tName)
        empieza(cpuTPath, cpuTName)
        empieza(cpuPath, cpuName)

    except:
        print("Error Fatal")
        raise
    finally:
        hoy = dt.datetime.now()
        print("Termina la tarea de mantenimiento, a fecha de : " +
              hoy.strftime("%d-%m-%Y %H:%M:%S") + '\n')
