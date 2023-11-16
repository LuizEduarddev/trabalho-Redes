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

def desfragmentaString(clientes, data: str, address):
    try:
        data = data.split(' ')
    except:
        print('ERR INVALID_MESSAGE_FORMAT')

    if data[0] == 'REG':
        socketREG(clientes, data, address)
    elif data[0] == 'UPD':
        socketUPD(clientes, data, address)
    elif data[0] == 'LST':
        socketLST(clientes, data, address)
    elif data[0] == 'END':
        socketEND(clientes, data, address)
    else:
        print('ERR INVALID_MESSAGE_FORMAT')
        return 0

def requirementsREG(string: str):
    string = string.split(' ')
    if len(string) < 4:
        print('ERR INVALID_MESSAGE_FORMAT')
        exit()
    else:
        port = int(string[2])
        if port > 65535:
            print('ERR PORT_INVALID_NUM')
            exit()
        else:
            data = string[4]
            data.split(',')
            tamanho = len(data)
            print(f'OK <{tamanho}>_REGISTERED_FILES')
            return string


def socketREG(clientes:dict, data: str, address):
    data = requirementsREG(data)
    updateClientes(clientes, data[3], address, data[2], data[1])

def updateClientes(clientes :dict, data, address, port, password):
    atualizaNumero = 0
    atualizaNumero += int(clientes['usuarios'])
    clientes.update({'users_count': atualizaNumero})
    chave = f'client{atualizaNumero}'
    clientes.update({chave, {'data':data, 'address': address, 'port': port, 'password': password}})
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
        desfragmentaString(clientes, data, address)

        
    
    c1 = clientes[0]
    c1_addr, c1_port = c1

    c2 = clientes[1]
    c2_addr, c2_port = c2

    servidor.sendto(f'{c1_addr}, {c1_port} {PORTA}', c2)
    servidor.sendto(f'{c2_addr}, {c2_port} {PORTA}', c1)
    
if __name__ == '__main__':
    main()

