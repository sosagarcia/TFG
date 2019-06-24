from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

app = Flask(__name__)
# MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'


def searchUser(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE email = %s", (email,))
    user = cur.fetchone()
    return user
