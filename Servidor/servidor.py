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

def desfragmentaString(string: str):
    try:
        string = string.split(' ')
    except:
        print('ERR INVALID_MESSAGE_FORMAT')

    if string[0] == 'REG':
        socketREG(string)
    elif string[0] == 'UPD':
        socketUPD(string)
    elif string[0] == 'LST':
        socketLST(string)
    elif string[0] == 'END':
        socketEND(string)
    else:
        print('ERR INVALID_MESSAGE_FORMAT')
        return 0


def socketREG(string: str):
    string = string.split(' ')

def updateClientes(clientes :dict, data, address):
    atualizaNumero = 0
    atualizaNumero += int(clientes['usuarios'])
    clientes.update({'usuarios': atualizaNumero})
    chave = f'cliente{atualizaNumero}'
    clientes.update({chave, {'data':data, 'address': address}})
    return clientes

def main():
    clientes = {'usuarios': 0}
    HOST = retornaHost()
    PORTA = retornaPorta()
    servidor = defineServidor()

    servidor.bind((HOST, PORTA))
    servidor.listen()
    print('Aguardando conexao....')
    conn, ender = servidor.accept()
    
    while True:
        data, address = servidor.recv(1024)

        print(f'Connection ready with IP: {address}')

        clientes = updateClientes(clientes, data, address)
        
        desfragmentaString()

        
    
    c1 = clientes[0]
    c1_addr, c1_port = c1

    c2 = clientes[1]
    c2_addr, c2_port = c2

    servidor.sendto(f'{c1_addr}, {c1_port} {PORTA}', c2)
    servidor.sendto(f'{c2_addr}, {c2_port} {PORTA}', c1)
    
if __name__ == '__main__':
    main()

