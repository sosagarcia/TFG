
from datetime import date, datetime, timedelta
from flask.json import JSONEncoder
import datetime as dt
from flask import Flask, render_template, request, url_for, redirect, flash, session, Response
import os

import random
from flaskext.mysql import MySQL
import bcrypt
from flask import jsonify, json
from static.py.mensajes import *
from static.py.rutas import *
from static.py.funciones import *
from static.py.correo import *


# from flask.ext.session import Session
# import mysql
# import mysql.connector

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def titulos():

    hoy = dt.datetime.now()

    ayer = hoy - timedelta(days=1)
    mañana = hoy + timedelta(days=1)
    ayer = str(ayer)
    mañana = str(mañana)
    cur = mysql.get_db().cursor()
    cur.execute(
        'SELECT title, start, end FROM eventos where (%s < start) and ( start <  %s) ORDER BY start ASC', (ayer, mañana))
    data = cur.fetchall()
    data = [i for sub in data for i in sub]

    return data


def entre(fechaI, fechaF):
    fechaI = pasaFecha(fechaI)
    fechaF = pasaFecha(fechaF)

    data = conn('SELECT start, end FROM eventos')
    data = [i for sub in data for i in sub]
    max = len(data)
    for i in range(0, max, 2):
        if (data[i] <= fechaI < data[i+1]):
            return 1
        if (data[i] < fechaF <= data[i+1]):
            return 1
    for i in range(0, max):
        if (fechaI < data[i] < fechaF):
            return 1
    return 0


def usuarios():

    data = conn('SELECT fullname, id FROM contacts')
    data = [i for sub in data for i in sub]
    return data


def conn(texto):
    cur = mysql.get_db().cursor()
    cur.execute(texto)
    data = cur.fetchall()
    return data


def ajustes():
    datos = read_conf()
    session['nameD'] = datos[0]
    session['emailA'] = datos[1]
    session['tam'] = datos[2]
    session['disB'] = datos[3]
    session['disA'] = datos[4]
    session['tem'] = datos[5]
    session['hum'] = datos[6]
    session['humTem'] = datos[7]
    session['disT'] = datos[8]
    session['cpusT'] = datos[9]


mysql = MySQL()
app = Flask(__name__)

# MYSQL connection
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'renato'
app.config['MYSQL_DATABASE_PASSWORD'] = 'renato12'
app.config['MYSQL_DATABASE_DB'] = 'flaskcontacts'
mysql.init_app(app)


# Settings
app.json_encoder = CustomJSONEncoder
app.secret_key = os.urandom(16)
# app.config['JSON_AS_ASCII'] = True  # default


@app.route('/')
def home():

    return render_template('index.html', mensaje=inicio)


@app.route('/ahora',methods=["GET", "POST"])
def ahora():
    now = datetime.now()
    d = now.strftime("%d")
    M = now.strftime("%m")
    a = now.strftime("%Y")
    h = now.strftime("%H")
    m = now.strftime("%M")
    s = now.strftime("%S")
    M = int(M) - 1
    hoy = [a, M, d, h, m, s]

    # need to be (year, month, day, hours, minutes, seconds, milliseconds)
    return jsonify(hoy)


@app.route('/main')
def main():
    if session.get("name", None) is not None:
        alarmas = logs(aPath)
        movimientos = logs(irPath)
        salidas = logs(outPath)
        agenda = conjunto(titulos())
        return render_template('main.html', agenda=agenda, alarma=alarmas, movimiento=movimientos, salida=salidas)
    else:
        flash("Sesión caducada", 'dark')
        return redirect(url_for("login"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session.clear()
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
        user = cur.fetchone()

        cur.close()

        if user is None:

            return render_template("index.html", mensaje=usu)
        else:
            if bcrypt.checkpw(password, user[4].encode('utf-8')):
                
                session['id'] = user[0]
                session['name'] = user[1]
                session['phone'] = user[2]
                session['email'] = user[3]
                session['message'] = user[5]
                session['root'] = user[8]
                
                ajustes()
                alarmas = logs(aPath)
                movimientos = logs(irPath)
                salidas = logs(outPath)
                agenda = conjunto(titulos())

                return render_template('main.html', agenda=agenda, primer=1, alarma=str(alarmas), movimiento=movimientos, salida=salidas)
            else:
                return render_template("index.html", mensaje=contra)

    else:
        return render_template("index.html", mensaje=inicio)


@app.route('/perfil')
def perfil():

    if session.get("name", None) is not None:
        data = conn('SELECT * FROM contacts')
        tap = conn('SELECT * FROM tap')
        datos = tabla(data,tap)
        return render_template('perfil.html', mensaje=reg, ajustes=1, contactos=data, taps=datos)
    else:
        flash("Sesión caducada", 'dark')
        return redirect(url_for("login"))


@app.route('/calendar')
def calendar():
    #if session.get("name", None) is not None:
    if session.get("root", None) == 0:
        return render_template('calendarMortal.html')
    else:
        listado = users(usuarios())
        return render_template('calendar.html', mensaje=cal, lista=listado)
    """else:
        flash("Sesión caducada", 'dark')
        return redirect(url_for("login"))"""


@app.route('/data')
def data():
    callist = list()
    data = conn('SELECT * FROM eventos')
    for row in data:
        callist.append(
            {'id': row[0], 'title': row[1], 'color': row[2], 'start': row[3], 'end': row[4], 'idUser': row[5], })

    return Response(json.dumps(callist),  mimetype='application/json')


@app.route('/add_event', methods=['POST'])
def add_event():
    if request.method == 'POST':
        idUser = request.form['title']
        color = request.form['color']
        start = request.form['start']
        cur = mysql.get_db().cursor()
        cur.execute("SELECT fullname FROM contacts WHERE id = %s", (idUser,))
        title = cur.fetchone()
        horas = request.form['horas']
        minutos = request.form['minutos']
        if len(minutos or horas) == 0:
            end = request.form['end']       
        else:
            end = pasaFecha(start)
            if (horas == ''):
                horas = 0
            else:
                horas = int(horas)
            if (minutos == ''):
                minutos = 0
            else:
                minutos = int(minutos)                
            end = end + timedelta(hours=horas)
            end = end + timedelta(minutes=minutos)
            end = str(end)

            temp = len(end)
            end = end.replace(" ", "T")
            end = end[:temp - 3]

        listado = users(usuarios())
        if len(idUser and start and end) == 0:
            return render_template('calendar.html', mensaje=vacioE, lista=listado)
        if (end < start):
            return render_template('calendar.html', mensaje=menor, lista=listado)
        if(dif(start, end, 3)):
            return render_template('calendar.html', mensaje=dosmin, lista=listado)
        mesEnMinutos = 44640
        if(not (dif(start, end, mesEnMinutos))):
            return render_template('calendar.html', mensaje=unmes, lista=listado)
        # Comprobar si start o end esta entre el start o el end de algun otro evento (comprobación explusiva del modo Auto.)
        if (entre(start, end)):
            return render_template('calendar.html', mensaje=fechae, lista=listado)

        cur = mysql.get_db().cursor()
        cur.execute(
            'INSERT INTO eventos (title, color, start, end, idUser) VALUES(%s, %s, %s, %s, %s)', (title, color, start, end, idUser))
        mysql.get_db().commit()
        return render_template('calendar.html', mensaje=event, lista=listado)

    if session.get("name", None) is not None:
        return render_template('index.html')
    else:
        flash("Sesión caducada", 'dark')
        return redirect(url_for("login"))


@app.route('/deletEvent', methods=['POST'])
def deletEvent():

    id = request.form['canvas_data']
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM eventos WHERE id = {0}'.format(id))
    mysql.get_db().commit()
    return Response("Done")



@app.route('/deletFull', methods=['POST'])
def deletAlgo():

    algo = request.form['canvas_data']
    algoInt = int(algo)
    if algoInt == 0:
        cur = mysql.get_db().cursor()
        cur.execute('TRUNCATE TABLE eventos ')
        mysql.get_db().commit()
        return Response("Done")



@app.route('/reinicio')
def reinicio():
    output = reiniciar()
    return jsonify(output)

@app.route('/actualiza')
def actualiza():
   algo =  actualizacion()
   return jsonify(algo)


@app.route('/deletDay', methods=['POST'])
def deletDay():
    algo = request.form['canvas_data']
    algo = pasaFecha1(algo)
    finDay = algo + timedelta(days=1)
    algo = str(algo)
    finDate = str(finDay)
    cur = mysql.get_db().cursor()
    cur.execute(
        'DELETE FROM eventos where (%s < start) and ( start <  %s) ', (algo, finDate))
    mysql.get_db().commit()
    return Response("Done")


@app.route('/deletUser', methods=['POST'])
def deletUser():

    algo = request.form['canvas_data']
    cur = mysql.get_db().cursor()
    cur.execute(
        'DELETE FROM eventos where  idUser = {0}'.format(algo))
    mysql.get_db().commit()
    return Response("Done")


@app.route('/delet2', methods=['POST'])
def delet2():

    obj = request.form['canvas_data']
    date = request.form['canvas_data_date']
    date = pasaFecha1(date)
    finDay = date + timedelta(days=1)
    date = str(date)
    finDay = str(finDay)
    cur = mysql.get_db().cursor()
    cur.execute(
        'DELETE FROM eventos where (%s < start) and ( start <  %s) and idUser = {0}'.format(obj), (date, finDay))
    mysql.get_db().commit()
    return Response("Done")


@app.route('/state')
def state():

    humedad = statusNow(hPath, hName)
    temperatura = statusNow(tPath, tName)
    distancia = statusNow(disPath, dName)
    movimiento = statusNow(irPath, irName)
    alarma = statusNow(aPath, aName)
    temperaturaCPU = statusNow(cpuTPath, cpuTName)
    usoCPU = statusNow(cpuPath, cpuName)

    return jsonify(humedad=humedad, temperatura=temperatura, distancia=distancia, movimiento=movimiento, alarma=alarma, temperaturaCPU=temperaturaCPU, usoCPU=usoCPU)


@app.route('/testa')
def chart():
        
        imagenes = list()
        return render_template('galery.html', rutas=imagenes)
        
@app.route('/asigna', methods=['POST'])
def asigna():
    datos = request.form.getlist('data[]')
    pins= list()
    users = list()
    mensaje = ""
    max = len(datos)
    for i in range (0,max,2):
        pin = datos[i]
        user = datos[i + 1]
        if not user == "":
            pins.append(pin)
            users.append(user)
    sublist = list()
    for i in users:
        if i not in sublist:
            sublist.append(i)
    if not users == sublist:
        mensaje = "Hay usuarios repetidos / Hay mas de una salida sin asignar"
        return jsonify(result= -1, msj=mensaje)
    fin = len(pins)
    for i in range (0,fin):
        pin = int(pins[i])
        user = int(users[i])
        cur = mysql.get_db().cursor()
        cur.execute('UPDATE contacts SET pin = %s WHERE id = %s', (pin, user))
        mysql.get_db().commit()
        cur = mysql.get_db().cursor()
        cur.execute('UPDATE tap SET idPropietario = %s WHERE pin = %s', (user, pin))
        mysql.get_db().commit()
    mensaje = "Salidas actualizadas correctamente"
    data = conn('SELECT * FROM contacts')
    tap = conn('SELECT * FROM tap')
    datos = minitabla(data,tap)
    return jsonify(result= 1, msj=mensaje, tap= datos)

   


@app.route('/updateStatistics', methods=['POST'])
def updateStatistics():
    tipo = request.form.getlist('tipo[]')
    fecha = request.form.get('fecha')
    muestra = request.form.get('muestras')
    labels, datos, color, title, unit = giveDatasets(giveTypes(tipo), fecha, muestra)

    return jsonify(fechas=labels, data=datos, unidad=unit, colour=color, titulo=title)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html', mensaje=adios)


@app.route('/pictures')
def pictures():
    imagenes = sorted(ls(images))
    imagenes.pop(0)
    #imagenes = list()
    return render_template('galery.html', rutas=imagenes)


@app.route('/registro')
def registro():
    return render_template('registro.html', mensaje=reg)


@app.route('/forgot')
def forgot():
    return render_template('forgot.html', mensaje=fgt)


@app.route('/pass_email', methods=['POST'])
def pass_email():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.get_db().cursor()
        cur.execute("SELECT fullname, id FROM contacts WHERE email = %s", (email,))
        user = cur.fetchone()
        if user is None:
            return render_template('forgot.html', mensaje=usuF)
        codigo = random.randrange(100000, 999999)
        text = cambio_pass + str(codigo)
        asunto = "Recuperación de contraseña - " + user[0]
        feedback = sendEmail(str(text), email, str(asunto))
        cur = mysql.get_db().cursor()
        cur.execute('UPDATE contacts SET cambio_pass = %s WHERE email = %s', (codigo, email))
        mysql.get_db().commit()
        id = user[1]
        return render_template('insert_code.html', mensaje=code, user=str(id))


@app.route('/verify/<string:id>', methods=['POST'])
def verify(id):
    if request.method == 'POST':
        code = request.form['code']
        cur = mysql.get_db().cursor()
        cur.execute("SELECT cambio_pass FROM contacts WHERE id = %s", (id,))
        codigo = cur.fetchone()
        if not (code == str(codigo[0])) :
            return render_template('insert_code.html', mensaje=codeI, user=id)
        now = dt.datetime.now()
        cur = mysql.get_db().cursor()
        cur.execute('UPDATE contacts SET pass_allow = %s WHERE id = %s', (str(now),id))
        mysql.get_db().commit()
        return render_template('change_pass.html', mensaje=cambio, user=id)


@app.route('/update_pass/<string:id>', methods=['POST'])
def update_pass(id):
    if request.method == 'POST':
        print (id)
        cur = mysql.get_db().cursor()
        cur.execute("SELECT pass_allow FROM contacts WHERE id = %s", (id,))
        check = cur.fetchone()
        if not(check == 0):
            password = request.form['pass'].encode('utf-8')
            repassword = request.form['repass'].encode('utf-8')
            if password != repassword:             
                return render_template('change_pass.html', mensaje=coincideC, user=id)
            if len(password and repassword) == 0:               
                return render_template('change_pass.html', mensaje=vacioC, user=id)
            else:
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur = mysql.get_db().cursor()
                cur.execute('UPDATE contacts SET password = %s, pass_allow = 0, cambio_pass = 0  WHERE id = %s', (hash_password,id))  
                mysql.get_db().commit()  
                return render_template('index.html', mensaje=cambioS)
        return render_template('forgot.html', mensaje=fgt)
        
               
        

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.get_db().commit()
    tap = conn('SELECT * FROM tap')
    data = conn('SELECT * FROM contacts')
    datos = tabla(data,tap)
    flash('Se ha borrado el contacto correctamente', 'success')
    return render_template('perfil.html', mensaje=reg, lista=1, contactos=data, taps=datos)


@app.route('/rol/<id>')
def edit_contact(id):
    if session.get("root", None) == 1:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT root FROM contacts WHERE id = %s', [id])
        data = cur.fetchall()
        rol= data[0][0]
        if rol == 0:
            rol = 1
        else:
            rol = 0
        texto = """
    
            UPDATE contacts
            SET root=% s
            WHERE ID= % s
        """
        variables = (rol, int(id))
        cur = mysql.get_db().cursor()
        cur.execute( texto, variables)
        mysql.get_db().commit()
        data = conn('SELECT * FROM contacts')
        tap = conn('SELECT * FROM tap')
        datos = tabla(data,tap)
        flash('Se ha modificado el Rol del contacto correctamente', 'warning')
        return render_template('perfil.html', mensaje=reg, lista=1, contactos=data, taps=datos)
    else:
        flash("Sesión caducada",'dark')
        return redirect(url_for("login"))



@app.route('/updateDevice', methods=['POST'])
def update_device():
    if request.method == 'POST':
        nameD = request.form['nameD']
        emailR = request.form['emailR']
        tam =request.form['tam']
        disB = request.form['disB']
        disA = request.form['disA']
        tem = request.form['tem']
        hum = request.form['hum']
        humTem = request.form['humTem']
        disT = request.form['disT']
        cpusT = request.form['cpusT']
        log = confText.format(nameD, emailR,tam, disB, disA, tem, hum, humTem, disT,cpusT)
        save_conf(log)
        session['nameD'] = nameD
        session['emailR'] = emailR
        session['tam'] = tam
        session['disB'] = disB
        session['disA'] = disA
        session['tem'] = tem
        session['hum'] = hum
        session['humTem'] = humTem
        session['disT'] = disT
        session['cpusT'] = cpusT
        data = conn('SELECT * FROM contacts')
        tap = conn('SELECT * FROM tap')
        datos = tabla(data,tap)
        flash('Configuración actualizada correctamente. Recuerde que algunos ajustes como los de Intervalo de muetsreo o "Altura de estanque" no serán actualizados hasta que se reinicie el sistemanivel', 'success')    
        return render_template('perfil.html',dispositivo=1,contactos=data, mensaje=reg, taps=datos)


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']
        cambia = request.form['bool']
        texto = """
 
        UPDATE contacts
        SET phone=% s,
            email=% s,
            message=% s
        WHERE ID= % s
    """
        variables = (phone, email, message, id)
        if cambia == "1":
            password = request.form['newpass'].encode('utf-8')
            repassword = request.form['repass'].encode('utf-8')
            if password != repassword:             
                flash('Las contraseñas no coinciden', 'danger')
                return redirect(url_for('perfil'))
            if len(password and repassword) == 0:               
                flash('Las contraseñas no pueden estar vacías', 'danger')
                return redirect(url_for('perfil'))
            else:
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                texto = """

        UPDATE contacts
        SET phone=% s,
            email=% s,
            message=% s,
            password=% s
        WHERE ID= % s
    """
                variables =(phone, email, message, hash_password, id)

        cur = mysql.get_db().cursor()
        cur.execute( texto, variables)
        mysql.get_db().commit()
        session['phone'] = phone
        session['email'] = email
        session['message'] = message
        flash('El contacto ha sido actualizado correctamente ', 'success')    
        return redirect(url_for('perfil'))


@app.route('/estadisticas')
def estadisticas():
   
    if session.get("name", None) is not None:
        listado = users(usuarios())
        return render_template('estadisticas.html', mensaje=esta, listado=listado)
    else:
        flash("Sesión caducada",'dark')
        return redirect(url_for("login"))



@app.route('/lista')
def lista():

    data = conn('SELECT * FROM contacts')
    return render_template('lista.html', contactos=data, title='Lista')


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['pass'].encode('utf-8')
        repassword = request.form['repass'].encode('utf-8')
        data = conn('SELECT * FROM contacts')
        tap = conn('SELECT * FROM tap')
        datos = tabla(data,tap)
        if len(fullname and phone and email and password and repassword) == 0:
            return render_template('perfil.html', title='Registro', mensaje=vacio,registro=1, contactos=data, taps=datos)
        elif password != repassword:
            return render_template('perfil.html', title='Registro', mensaje=coincide ,registro=1, contactos=data, taps=datos)
        else:

            cur = mysql.get_db().cursor()
            cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
            user = cur.fetchone()
            if user is not None:
                return render_template('perfil.html', title='Registro', mensaje=usua ,registro=1, contactos=data, taps=datos)
            else:
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

                cur = mysql.get_db().cursor()
                cur.execute(
                    'INSERT INTO contacts (fullname, phone, email, password) VALUES(%s, %s, %s, %s)', (fullname, phone, email, hash_password))

                mysql.get_db().commit()
                data = conn('SELECT * FROM contacts')
                tap = conn('SELECT * FROM tap')
                datos = tabla(data,tap)
                flash('El contacto ha sido agregado correctamente ', 'success')
                return render_template('perfil.html', lista=1, contactos=data, mensaje=reg, taps=datos)


if __name__ == '__main__':
   
    app.run(debug=True)
    # app.run()

# https://bootswatch.com/
# https://uigradients.com
# https://www.youtube.com/watch?v=tZTpKF2pkQo
# https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2
# alertas : https://www.youtube.com/watch?v=raqN7Il3Tr0
# login : https://www.youtube.com/watch?v=fOj16SIa02U
# Camera : https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/5
# Configuracion apache2 para el py : /etc/apache2/sites-available/TFT.conf (cambiar ip correspondiente)
# mysql en rapi https://www.youtube.com/watch?v=axceWuN0en0 / https://stackoverflow.com/questions/45628814/how-do-you-install-mysql-for-flask

# https://stackoverflow.com/questions/45628814/how-do-you-install-mysql-for-flask

# https://fullcalendar.io/docs/event-source
# Full calendar edit events https://www.youtube.com/watch?v=8OOddEiM55A&list=PLSuKjujFoGJ3xqSJHnZUR-INEO71t1znq&index=11

# https://vsn4ik.github.io/bootstrap-checkbox/

# Flas Session :https://pythonise.com/feed/flask/flask-session-object

#python hilos https://python-para-impacientes.blogspot.com/2016/12/threading-programacion-con-hilos-i.html

# mantenimiento : http://akirasan.net/lanzar-aplicacion-python-tras-iniciar-raspberrypi/ https://docs.oracle.com/cd/E24842_01/html/E23086/sysrescron-1.html