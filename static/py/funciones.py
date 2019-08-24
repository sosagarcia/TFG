from datetime import date, datetime, timedelta
import datetime as dt
import glob
import errno


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


def dif(start, end, intervalo):
    start = pasaFecha(start)
    end = pasaFecha(end)
    diferencia = intervalo * 60
    resta = end - start
    resta = resta.total_seconds()
    if (resta < diferencia):
        return 1
    return 0


def getLogs(path, name, fecha, muestras):
    fechas = list()
    valores = list()
    subresult = list()
    log = open(str(path) + str(fecha) + str(name), "r")
    logLines = log.readlines()
    log.close()
    saltos = len(logLines) / muestras
    if (saltos <= 1):
        saltos = 1
    for i in range(0, len(logLines), int(saltos)):
        linea = logLines[i]
        valor = linea[20:24]
        if not (valor == "Erro") and (linea[10:11] == " "):
            valores.append(valor)
            subresult = [linea[11:13], linea[14:16], linea[17:19]]
            fechas.append(subresult)

    return (fechas, valores)


def separa(fechas):
    result = list()
    subresult = list()
    for fecha in fechas:
        subresult = [fecha[0:1], fecha[3:4], fecha[6:9]]
        result.append(subresult)
    return result
