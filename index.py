
from datetime import date, datetime, timedelta

from flask.json import JSONEncoder
import datetime as dt
from flask import Flask, render_template, request, url_for, redirect, flash, session, Response
from flaskext.mysql import MySQL
import bcrypt
from flask import jsonify, json
from static.py.mensajes import *
from static.py.funciones import *

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

    data = conn('SELECT title, start FROM eventos')
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
    print("hol")
    cur = mysql.get_db().cursor()
    cur.execute(texto)
    data = cur.fetchall()
    return data


mysql = MySQL()
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder


# MYSQL connection
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'renato'
app.config['MYSQL_DATABASE_PASSWORD'] = 'renato12'
app.config['MYSQL_DATABASE_DB'] = 'flaskcontacts'
mysql.init_app(app)


# Settings
app.secret_key = 'mysecretkey'





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
    hoy = [a,M,d,h,m,s]

    # need to be (year, month, day, hours, minutes, seconds, milliseconds)

    return jsonify(result=hoy)

@app.route('/main')
def main():

    agenda = conjunto(titulos())
    return render_template('main.html', agenda=agenda)


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
                session['name'] = user[1]
                session['email'] = user[3]
                agenda = conjunto(titulos())
                return render_template("main.html", primer=1, agenda=agenda)
            else:
                return render_template("index.html", mensaje=contra)

    else:
        return render_template("index.html", mensaje=inicio)


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


# @app.route('/today')
# def today():
#    hoy = date.today()
#
#   return Response(json.dumps(hoy),  mimetype='application/json')


@app.route('/evento')
def evento():
    return render_template('evento.html', mensaje=cal)


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
        if(dosMin(start, end)):
            return render_template('calendar.html', mensaje=dosmin, lista=listado)
        # Comprobar si start o end esta entre el start o el end de algun otro evento
        if (entre(start, end)):
            return render_template('calendar.html', mensaje=fechae, lista=listado)

        cur = mysql.get_db().cursor()
        cur.execute(
            'INSERT INTO eventos (title, color, start, end, idUser) VALUES(%s, %s, %s, %s, %s)', (title, color, start, end, idUser))
        mysql.get_db().commit()
        return render_template('calendar.html', mensaje=event, lista=listado)


@app.route('/deletEvent', methods=['POST'])
def deletEvent():

    id = request.form['canvas_data']
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM eventos WHERE id = {0}'.format(id))
    mysql.get_db().commit()
    listado = users(usuarios())


@app.route('/deletFull', methods=['POST'])
def deletAlgo():

    algo = request.form['canvas_data']
    algoInt = int(algo)
    if algoInt == 0:
        cur = mysql.get_db().cursor()
        cur.execute('TRUNCATE TABLE eventos ')
        mysql.get_db().commit()


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


@app.route('/test')
def test():

    return render_template('test.html')

@app.route('/testa')
def testa():
    hoy = fecha()
    return jsonify(result=hoy)


@app.route('/logout')
def logout():
    session['name'] = "none"
    return render_template('index.html', mensaje=adios)
    


@app.route('/registro')
def registro():
    return render_template('registro.html', title='Registro', mensaje=reg)


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.get_db().commit()
    flash('Se ha borrado el contacto correctamente')
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
        cur = mysql.get_db().cursor()
        cur.execute("""

            UPDATE contacts
            SET fullname=% s,
                phone=% s,
                email=% s
            WHERE ID= % s
        """, (fullname, phone, email, id))
        mysql.get_db().commit()
        flash('El contacto ha sido actualizado correctamente ')
        return redirect(url_for('lista'))


@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')


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

                flash('El contacto ha sido agregado correctamente ')
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
