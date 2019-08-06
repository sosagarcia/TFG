from datetime import date, datetime, timedelta
import datetime as dt


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


def dosMin(start, end):
    start = pasaFecha(start)
    end = pasaFecha(end)
    dosM = 3 * 60
    dif = end - start
    dif = dif.total_seconds()
    if (dif < dosM):
        return 1
    return 0
