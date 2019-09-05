from datetime import date, datetime, timedelta
import datetime as dt
import glob
import errno
import os

switcher = {
    "_Distancia": "/var/log/iot/dis/",
    "_Humedad": "/var/log/iot/hum/",
    "_Temperatura": "/var/log/iot/tem/",
    "_Movimientos": "/var/log/iot/ir/",
    "_Alarmas": "/var/log/iot/a/",
    "_TemperaturaCPU": "/var/log/iot/cpuT/",
    "_UsoCPU": "/var/log/iot/cpu/"
}

unidades = {
    "_Distancia": "cm.",
    "_Humedad": "%",
    "_Temperatura": "ºC",
    "_TemperaturaCPU": "ºC",
    "_UsoCPU": "%"
}


def statusNow(path, name):
    hoy = dt.datetime.now()
    i = 0
    limite = 100
    while i <= limite:
        try:
            fecha = hoy.strftime("%d-%m-%Y")
            log = open(path + fecha + name, "r")
            logLines = log.readlines()
            log.close()
            actual = logLines[len(logLines) - 1]
            return actual
        except:
            ayer = hoy - timedelta(days=1)
            hoy = ayer
            i += 1
    return (-1)


def logs(path):
    data = ""
    blanco = '\n' + '\n'
    ruta = path + '*.log'
    files = sorted(glob.glob(ruta))
    for name in files:
        try:
            with open(name) as f:
                data += f.read() + blanco
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return data


def conjunto(data):
    # result = '<select>'

    result = '<ul class="list-group align-self-start first shadow p-3 mb-5 bg-white rounded mx-auto " >'
    result += '<label class="bg-warning rounded">Listado de eventos recientes y próximos</label>'
    max = len(data)

    if max == 0:

        result += '<span class=" mt-1 d-inline-block" tabindex="0" data-toggle="tooltip" data-placement="right" title="No hay eventos programados para las próximas 24Hs.">'
        result += '<li class = "list-group-item bg-light pointer" > No hay ningún evento para hoy </li>'
        result += '</span>'

    else:
        style = ""
        for i in range(0, max, 3):

            if (data[i+1] <= dt.datetime.now() < data[i+2]):
                style = "primary"
            else:
                style = "light"
            strDesde = data[i+1].strftime('%d/%m/%y a las %H:%M')
            strHasta = data[i+2].strftime('%d/%m/%y a las %H:%M')
            result += '<span class=" mt-1 d-inline-block" tabindex="0" data-toggle="tooltip" data-placement="right" title="Desde el %s hasta el %s">' % (
                strDesde, strHasta)
            result += '<li class="pointer list-group-item bg-%s">%s </li>' % (
                style, data[i])
            result += '</span>'
        result += '</ul>'

    return (result)


def users(data):
    # result = '<select>'
    result = '<option value="" selected hidden>Seleccione un usuario</option>'
    max = len(data)

    for i in range(0, max, 2):
        result += '<option value="%s">%s</option>' % (
            data[i + 1], data[i])
    result += '</select>'

    return (result)


def pasaFecha(fecha):
    fecha = datetime.strptime(fecha, '%Y-%m-%dT%H:%M')
    return fecha


def pasaFecha1(fecha):
    fecha = datetime.strptime(fecha, '"%Y-%m-%d"')
    return fecha

def divideFechas(fecha):
    dia1 = fecha[8:10]
    mes1 = fecha[5:7]
    año1 = fecha[0:4]
    hora1 = fecha[11:13]
    minuto1 = fecha[14:16]
    dia2 = fecha[24:26]
    mes2 = fecha[21:23]
    año2 = fecha[16:20]
    hora2 = fecha[27:29]
    minuto2 = fecha[30:32]
    
    inicio = datetime(year = int(año1), month = int(mes1), day = int(dia1), hour= int(hora1), minute = int(minuto1))
    fin = datetime(year = int(año2), month =int( mes2), day = int(dia2), hour= int(hora2), minute = int(minuto2))

    return (inicio, fin)


def dif(start, end, intervalo):
    start = pasaFecha(start)
    end = pasaFecha(end)
    diferencia = intervalo * 60
    resta = end - start
    resta = resta.total_seconds()
    if (resta < diferencia):
        return 1
    return 0


def openAll(path):
    logLines = list()
    ruta = path + '*.log'
    files = sorted(glob.glob(ruta), key=os.path.getmtime)
    for name in files:
        try:
            with open(name) as f:
                logLines += f.readlines()
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return logLines


def getLogs(path, name, fecha, muestras):


    if (str(fecha) == "*"):
       logLines = openAll(path)
    else :
        log = open(str(path) + str(fecha) + str(name), "r")
        logLines = log.readlines()
        log.close()
    
    fechas, valores = determina(logLines,muestras)

    return (fechas, valores)

def determina(logLines, muestras):
    subresult = list()
    fechas = list()
    valores = list()
    saltos = len(logLines) / (int(muestras) - 1)
    if (saltos <= 1):
        saltos = 1
    for i in range(0, len(logLines), int(saltos)):
        linea = logLines[i]
        valor = linea[20:24]
        if not (valor == "Erro") and (linea[10:11] == " "):
            valores.append(valor)
            subresult = [linea[11:13], linea[14:16], linea[17:19],linea[0:2],linea[3:5],linea[6:10]]
            fechas.append(subresult)
    return (fechas,valores)

def getLogsD(path, name, fecha, muestras):
    subresult = list()
    inicio,fin = divideFechas (fecha)
    logLines = openAllBig(path, inicio, fin )
    return (logLines, logLines)
    max =len(logLines)
    #Realizar barrido de array de array
    for i in range(0, max):
        linea = logLines[i]
        fechaTemp = datetime(year = int(linea[6:10]), month = int(linea[3:5]), day = int(linea[0:2]), hour = int(linea[11:13]), minute = int(linea[14:16]), second = int(linea[17:19]))
        if (inicio < fechaTemp < fin):
            subresult.append(linea)
            

    return ("0","subresult")      
    fechas, valores = determina(subresult, muestras)
    return (fechas, valores)



def openAllBig(path, inicio, fin):
    logLines = list()
    lenPath =  len (path)
    ruta = path + '*.log'
    files = sorted(glob.glob(ruta), key=os.path.getmtime)
    antes = inicio - timedelta(days=1)
    despues = fin - timedelta(days=1)
    for name in files:
        try:
            with open(name) as f:
                lenName = len(name)
                nombre = name [lenPath : lenName]
                fechaTemp = datetime(year = int(nombre[6:10]), month = int(nombre[3:5]), day = int(nombre[0:2])) 
                if (antes < fechaTemp < fin):
                    logLines.append(f.readlines())
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    return logLines

def damePath(tipo):
    path = switcher.get(str(tipo))
    return path


def dameUnit(tipo):
    unit = unidades.get(str(tipo))
    return unit


def separa(fechas):
    result = list()
    subresult = list()
    for fecha in fechas:
        subresult = [fecha[0:1], fecha[3:4], fecha[6:9]]
        result.append(subresult)
    return result
