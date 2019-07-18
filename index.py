
from datetime import date, datetime
from flask.json import JSONEncoder
import datetime as dt
from flask import Flask, render_template, request, url_for, redirect, flash, session, Response
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from flask import jsonify, json
from static.py.mensajes import *



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


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder


# MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'renato'
app.config['MYSQL_PASSWORD'] = 'Jota.1584'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'


# Funciones
def conn(texto):
    cur = mysql.connection.cursor()
    cur.execute(texto)
    data = cur.fetchall()
    return data

def users(data):
    result = "<select name= 'title'> "
    for i in data:
        result += '<option value="%s"selected>%s</option>' % (i, i)
    result += '</select>'
    return (result)

def usuarios():


    
    data = conn ('SELECT fullname FROM contacts')
    data = [i for sub in data for i in sub]
    return data

def entre(fecha):
    fecha = datetime.strptime(fecha,'%Y-%m-%dT%H:%M')
    print (type (fecha))
    data = conn ('SELECT start, end FROM eventos')
    data = [i for sub in data for i in sub]
    max = len(data)
    for i in range(0,max,2):
        if (data[i] < fecha < data[i+1]):
            return 1
    return 0    


@app.route('/')
def home():

    return render_template('index.html', mensaje=inicio)


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
        user = cur.fetchone()

        cur.close()

        if user is None:

            return render_template("index.html", mensaje=usu)
        else:
            if bcrypt.checkpw(password, user[4].encode('utf-8')):
                session['name'] = user[1]
                session['email'] = user[3]
                return render_template("main.html", primer=1 )
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
    data = conn ('SELECT * FROM eventos')

    for row in data:
        callist.append(
            {'title': row[1], 'color': row[2], 'start': row[3], 'end': row[4]})

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
        title = request.form['title']
        color = request.form['color']
        start = request.form['start']
        end = request.form['end']
        listado = users(usuarios())
        if len(title and start and end) == 0:
            return render_template('calendar.html', mensaje=vacioE, lista=listado)
        if (end < start):
            return render_template('calendar.html', mensaje=menor, lista=listado)
        #Comprobar si start o end está entre el start o el end de algún otro evento
        if (entre (start) or entre (end)):
            return render_template('calendar.html', mensaje=fechae, lista=listado)
    
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO eventos (title, color, start, end) VALUES(%s, %s, %s, %s)', (title, color, start, end))
        mysql.connection.commit()
        return render_template('calendar.html', mensaje=event, lista=listado)


@app.route('/test')
def test():
    
    print(entre())

@app.route('/logout')
def logout():
    return render_template('index.html', mensaje=adios)
    session['name'] = none


@app.route('/registro')
def registro():
    return render_template('registro.html', title='Registro', mensaje=reg)


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Se ha borrado el contacto correctamente')
    return redirect(url_for('lista'))


@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""

            UPDATE contacts
            SET fullname=% s,
                phone=% s,
                email=% s
            WHERE ID= % s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
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
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
            user = cur.fetchone()
            if user is not None:
                return render_template('registro.html', title='Registro', mensaje=usua)
            else:
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur = mysql.connection.cursor()
                cur.execute(
                    'INSERT INTO contacts (fullname, phone, email, password) VALUES(%s, %s, %s, %s)', (fullname, phone, email, hash_password))
                mysql.connection.commit()
                flash('El contacto ha sido agregado correctamente ')
                return redirect(url_for('lista'))




if __name__ == '__main__':
    app.run(port=5000, debug=True)
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
# Full calendar edit events https://www.youtube.com/watch?v=k9b0GjdqAnA&list=PLSuKjujFoGJ3xqSJHnZUR-INEO71t1znq&index=4
