<?php
# MYSQL connection
define('HOST', 'localhost');
define('USER', 'renato');
define('PASS', 'jOTA.1584');
define('DBNAME', 'flaskcontacts');

$conn = new PDO('mysql:host=' . HOST . ';dbname=' . DBNAME . ';', USER, PASS;