import socket


def giveIp():
    ip_address = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


if __name__ == '__main__':
    path = "/etc/apache2/sites-available/"
    ip = giveIp()
    text = """<VirtualHost *:80>
     # Add machine's IP address (use ifconfig command)
     ServerName 192.168.137.117
     # Give an alias to to start your website url with
     WSGIScriptAlias / /var/www/html/TFG/iniciar.wsgi
     <Directory /var/www/html/TFG/>
                # set permissions as per apache2.conf file
            Options FollowSymLinks
            AllowOverride None
            Require all granted
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost> """

    try:
        with open(name) as f:
            lenName = len(name)
            nombre = name[lenPath: lenName]
            fechaTemp = datetime(year=int(nombre[0:4]), month=int(
                nombre[5:7]), day=int(nombre[8:10]))
            if (antes < fechaTemp < fin):
                logLines.append(f.readlines())
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
    finally:
