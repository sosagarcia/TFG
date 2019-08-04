from datetime import date, datetime, timedelta


def fecha():
    now = datetime.now()
    d = now.strftime("%d")
    M = now.strftime("%m")
    a = now.strftime("%Y")
    h = now.strftime("%H")
    m = now.strftime("%M")
    s = now.strftime("%S")
    M = int(M) - 1
    hoy = [a,M,d,h,m,s]

    # need to be (year, month, day, hours, minutes, seconds, milliseconds)
    return(hoy)




def conjunto(data):
    # result = '<select>'
    result = '<ul class="list-group align-self-start first shadow p-3 mb-5 bg-white rounded mx-auto">'
    max = len(data)

    for i in range(0, max, 2):
        result += '<li class="list-group-item">%s</li>' % (
            data[i])
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


