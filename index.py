
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


def searchUser(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
    user = cur.fetchone()
    return user


def conn(texto):
    cur = mysql.get_db().cursor()
    cur.execute(texto)
    data = cur.fetchall()
    return data


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


@app.route('/')
def home():

    return render_template('index.html', mensaje=inicio)


@app.route('/ahora')
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
    estado = session['manual']
    return jsonify(result=hoy, estado=estado)

@app.route('/main')
def main():
    if session.get("name", None) is not None:
        agenda = conjunto(titulos())
        return render_template('main.html', agenda=agenda)
    else:
        flash("Sesión caducada",'dark')
        return redirect(url_for("login"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
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
                session['manual'] = "0"
                agenda = conjunto(titulos())
                return render_template("main.html", primer=1, agenda=agenda)
            else:
                return render_template("index.html", mensaje=contra)

    else:
        return render_template("index.html", mensaje=inicio)


@app.route('/perfil')
def perfil():
    
    if session.get("name", None) is not None:
        return render_template('perfil1.html')
    else:
        flash("Sesión caducada",'dark')
        return redirect(url_for("login"))


@app.route('/calendar')
def calendar():

    listado = users(usuarios())
    return render_template('calendar.html', mensaje=cal, lista=listado)


@app.route('/data')
def data():
    callist = list()
    data = conn('SELECT * FROM eventos')
    for row in data:
        callist.append(
            {'id': row[0], 'title': row[1], 'color': row[2], 'start': row[3], 'end': row[4], 'idUser': row[5], })

    return Response(json.dumps(callist),  mimetype='application/json')


@app.route('/data1')
def data1():
    labels = ['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge', 'New Bedford']
    data = [617594, 181045, 153060, 106519, 105162, 95072]
    title = "título"
    return jsonify(labels=labels, data=data, titulo=title)


# @app.route('/today')
# def today():
#    hoy = date.today()
#
#   return Response(json.dumps(hoy),  mimetype='application/json')

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
        if(not ( dif(start, end, mesEnMinutos))):
            return render_template('calendar.html', mensaje=unmes, lista=listado)
        # Comprobar si start o end esta entre el start o el end de algun otro evento
        
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
        flash("Sesión caducada",'dark')
        return redirect(url_for("login"))
        
        
        
@app.route('/deletEvent', methods=['POST'])
def deletEvent():

    id = request.form['canvas_data']
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM eventos WHERE id = {0}'.format(id))
    mysql.get_db().commit()



@app.route('/deletFull', methods=['POST'])
def deletAlgo():

    algo = request.form['canvas_data']
    algoInt = int(algo)
    if algoInt == 0:
        cur = mysql.get_db().cursor()
        cur.execute('TRUNCATE TABLE eventos ')
        mysql.get_db().commit()
    l


@app.route('/manual', methods=['POST'])
def manual():
    session['manual'] = "1"
    return render_template('calendar.html')

    
@app.route('/auto', methods=['POST'])
def auto():
    print("Auto")
    session['manual'] = "0"

    return redirect(url_for('calendar'))


@app.route('/manualdata')
def manualdata():
    print("el Manualmode actual es " , session['manual'])
    return jsonify(estado=session['manual'])


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
    


@app.route('/deletUser', methods=['POST'])
def deletUser():

    algo = request.form['canvas_data']
    cur = mysql.get_db().cursor()
    cur.execute(
        'DELETE FROM eventos where  idUser = {0}'.format(algo))
    mysql.get_db().commit()
    


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



@app.route('/state')
def state():

    humedad = statusNow(hPath,hName)
    temperatura = statusNow(tPath,tName)
    distancia = statusNow(disPath,dName)
    movimiento = statusNow(irPath,irName)
    alarma = statusNow(aPath,aName)
    temperaturaCPU = statusNow(cpuTPath,cpuTName)
    usoCPU = statusNow(cpuPath,cpuName)

    return jsonify ( humedad=humedad, temperatura=temperatura, distancia=distancia, movimiento=movimiento, alarma=alarma, temperaturaCPU=temperaturaCPU, usoCPU=usoCPU)
 




@app.route('/testa')
def chart():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = [ [11,14,15],
              [11,14,30],
              [11,14,45],
              [11,15,00],
              [11,15,15],
              [11,15,30],
              [11,15,45],
              [11,16,00],
              [11,16,15],
              [11,16,30],
              [11,16,45],
              [11,17,00],
              [11,17,15],
              [11,17,30],
              [11,17,45],
              [11,18,00],
              [11,18,15],
              [11,18,30]]
    print (times)
    return render_template('pruebaa.html', values=temperatures, labels=times, legend=legend)
 

@app.route('/testb')
def testb():
    legend = 'Temperaturas'
    fecha = "17-08-2019"
    fechas, valores  = getLogs(tPath,tName,fecha) 
    #tiempos = separa(fechas)
    return render_template('pruebaa.html', values=valores, labels=fechas, legend=legend)
    
@app.route('/testc')
def testc():
    fecha = "17-08-2019"
    fechas, valores  = getLogs(tPath,tName,fecha)
    return (fechas[11854] + fechas[11855]+ fechas[11856])
   


    

@app.route('/logout')
def logout():
    session.pop("name", None)
    return render_template('index.html', mensaje=adios)


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
        cur.execute('UPDATE contacts SET cambio_pass = %s WHERE email = %s', (codigo,email))
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
    flash('Se ha borrado el contacto correctamente', 'success')
    return redirect(url_for('lista'))


@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']
        cambia = request.form['bool']
        texto = """
 
        UPDATE contacts
        SET fullname=% s,
            phone=% s,
            email=% s,
            message=% s
        WHERE ID= % s
    """
        variables = (fullname, phone, email, message, id)
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
        SET fullname=% s,
            phone=% s,
            email=% s,
            message=% s,
            password=% s
        WHERE ID= % s
    """
                variables =(fullname, phone, email, message, hash_password, id)

        cur = mysql.get_db().cursor()
        cur.execute( texto, variables)
        mysql.get_db().commit()
        session['name'] = fullname
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
        if len(fullname and phone and email and password and repassword) == 0:
            return render_template('registro.html', title='Registro', mensaje=vacio)
        elif password != repassword:
            return render_template('registro.html', title='Registro', mensaje=coincide)
        else:

            cur = mysql.get_db().cursor()
            cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
            user = cur.fetchone()
            if user is not None:
                return render_template('registro.html', title='Registro', mensaje=usua)
            else:
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

                cur = mysql.get_db().cursor()
                cur.execute(
                    'INSERT INTO contacts (fullname, phone, email, password) VALUES(%s, %s, %s, %s)', (fullname, phone, email, hash_password))

                mysql.get_db().commit()

                flash('El contacto ha sido agregado correctamente ', 'success')
                return redirect(url_for('lista'))


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