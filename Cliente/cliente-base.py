#!/usr/bin/python

import time
import socket
from _thread import *

porta_tcp = None

def configurar_ambiente():
    pass


def descobre_porta_disponivel():
    return 54494

def find_port():

    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('localhost', 0)) 
    _, port = temp_socket.getsockname()
    temp_socket.close()

    return port

def get_host():
    return 'localhost'

def define_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return client_socket

def get_port_server():
    return 54494

def controle_udp():
    PORT = get_port_server()
    HOST = get_host()
    server_address = (HOST, PORT)
    message = ''
    try:
        CLIENT = define_client()
    except:
        print('ERROR: THERE WAS A FAILURE TRYING TO CONNECT TO SERVER...')
        print('TRY AGAIN LATER')
        exit()
        
    while message != 'finish':
        message = input(str(b'SEND A MESSAGE TO SERVER: '))
        CLIENT.sendto(message, server_address)

        try:
            data, server = CLIENT.recvfrom(1024)
            data = str(data)
            data = data.encode().decode()
            print(data)
        except socket.timeout:
            print('REQUESTED TIME OUT')

    CLIENT.close()
    


def servico_tcp(client):
    # Codigo do servico TCP
    print('Nova conexao TCP')
    client.send(b'OI')
    client.close()


def controle_tcp():
    global porta_tcp
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _socket.bind(('', porta_tcp))
    _socket.listen(4096)
    while True:
        client, addr = _socket.accept()
        start_new_thread(servico_tcp, (client, ))


def inicia_controle_tcp():
    controle_tcp()


def inicia_controle_udp():
    controle_udp()


def main():
    global porta_tcp
    porta_tcp = descobre_porta_disponivel()

    configurar_ambiente()


    choice = input('FOR CONNECT TO THE SERVER, TYPE server OR ELSE TYPE client\n: ')

    if choice == 'server':
        start_new_thread(inicia_controle_udp, ())
    elif choice == 'client':
        start_new_thread(inicia_controle_tcp, ())


if __name__ == '__main__':
    main()