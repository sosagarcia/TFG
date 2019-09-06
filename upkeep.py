import socket


def giveIp():
    ip1 = socket.gethostbyname(socket.gethostname())
    ip2 = socket.gethostbyname_ex(socket.gethostname())
    return (ip1, ip2)
