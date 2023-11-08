import socket

def retornaHost():
    HOST = 'localhost'
    return HOST

def retornaPorta():
    PORTA = 54494
    return PORTA

def defineServidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return servidor

def desfragmentaString(string):
    string = string.split(' ')
    if string[0] == 'REG':
        socketREG()

def conexaoEstabelecida(conn):
    while True:
        data = conn.recv(1024)




def main():
    HOST = retornaHost()
    PORTA = retornaPorta()
    servidor = defineServidor()

    servidor.bind((HOST, PORTA))
    servidor.listen()
    print('Aguardando conexao....')
    conn, ender = servidor.accept()
    conexaoEstabelecida(conn)

