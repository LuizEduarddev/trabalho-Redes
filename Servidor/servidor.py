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

def desfragmentaString(clientes, data: str, address, servidor: socket.socket):
    try:
        data = data.split(' ')
    except:
        servidor.send('ERR INVALID_MESSAGE_FORMAT')

    if data[0] == 'REG':
        socketREG(clientes, data, address, servidor)

    elif data[0] == 'UPD':
        socketUPD(clientes, data, address, servidor)

    elif data[0] == 'LST':
        socketLST(clientes, data, address, servidor)

    elif data[0] == 'END':
        socketEND(clientes, data, address, servidor)

    else:
        servidor.send('ERR INVALID_MESSAGE_FORMAT')
        return 0

def verificaTemp(string, number, tamanho):
    temp = number + 1
    if temp >= tamanho:
        return 
    else:
        string = string + ','

def socketLST(clientes: dict, servidor: socket.socket):
    number = int(0)
    string = str()
    tamanho = len(clientes)

    for chave, info in clientes.items():
        number += 1
        string = string + f'{info["data"]},ip{info["users_count"]}:{info["address"]}'
        verificaTemp(string, number, tamanho)
    
    servidor.send(string)

def requirementsREG(string: str, servidor: socket.socket):
    string = string.split(' ')
    if len(string) < 4:
        servidor.send('ERR INVALID_MESSAGE_FORMAT')
        exit()
    else:
        port = int(string[2])
        if port > 65535:
            servidor.send('ERR PORT_INVALID_NUM')
            exit()
        else:
            data = string[4]
            data.split(';')
            tamanho = len(data)
            servidor.send(f'OK <{tamanho}>_REGISTERED_FILES')
            return string

def requirementsUPD(string: str, servidor: socket.socket):
    string = string.split(' ')
    if len(string) < 4:
        servidor.send('ERR INVALID_MESSAGE_FORMAT')
        exit()
    else:
        port = int(string[2])
        if port > 65535:
            servidor.send('ERR PORT_INVALID_NUM')
            exit()
        else:
            data = string[3]
            data.split(',')
            return string

def searchInDB(clientes:dict, data:str, password: str, servidor: socket.socket):
    for temp, info in clientes.items():
        if "password" in info and info["password"] == password:
            info["data"] = data
            data = data.split(';')
            servidor.send(f'OK <{len(data)}>_REGISTERED_FILES')
            return 
        
    servidor.send('ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD')
    return 
        
def socketUPD(clientes:dict, data:str, address, servidor: socket.socket):
    data = requirementsUPD(data)
    password = data[1]
    searchInDB(clientes, data, password, servidor)
    
def socketREG(clientes:dict, data: str, address, servidor: socket.socket):
    data = requirementsREG(data, servidor)
    clientes = updateClientes(clientes, data[3], address, data[2], data[1], servidor)

def updateClientes(clientes :dict, data, address, port, password, servidor: socket.socket):
    atualizaNumero = 0
    atualizaNumero += int(clientes['usuarios'])
    clientes.update({'users_count': atualizaNumero})
    chave = f'client{atualizaNumero}'
    clientes.update({chave:{'data':data, 'address': address, 'port': port, 'password': password}})
    register = data[3]
    register = register.split(';')
    servidor.send(f'OK <{len(register)}>_REGISTERED_FILES')
    return clientes

def main():
    clientes = {'usuarios': 0}
    HOST = retornaHost()
    PORTA = retornaPorta()
    servidor = defineServidor()

    servidor.bind((HOST, PORTA))
    servidor.listen()
    print('Aguardando conexao....')
    conn, address = servidor.accept() 
    
    while True:
        data  = servidor.recv(1024) 

        print(f'Connection ready with IP: {address}')
        desfragmentaString(clientes, data, address, servidor)

        
    
    c1 = clientes[0]
    c1_addr, c1_port = c1

    c2 = clientes[1]
    c2_addr, c2_port = c2

    servidor.sendto(f'{c1_addr}, {c1_port} {PORTA}', c2)
    servidor.sendto(f'{c2_addr}, {c2_port} {PORTA}', c1)
    
if __name__ == '__main__':
    main()

