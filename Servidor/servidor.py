import socket

def retornaHost():
    HOST = 'localhost'
    return HOST

def retornaPorta():
    PORTA = 54494
    return PORTA

def defineServidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return servidor

def desfragmentaString(clientes, data: str, address, servidor: socket.socket):
    try:
        data = data.split(' ')
    except:
        servidor.send(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'))
        exit()

    if data[0] == 'REG':
        socketREG(clientes, data, address, servidor)

    elif data[0] == 'UPD':
        socketUPD(clientes, data, address, servidor)

    elif data[0] == 'LST':
        socketLST(clientes, data, address, servidor)

    elif data[0] == 'END':
        socketEND(clientes, data, address, servidor)

    else:
        servidor.send(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'))
        return 0

def socketEND(clientes:dict, password: str, port: str, servidor: socket.socket):
    client_exclud_list = []
    for client, info in clientes.items():
        if info['password'] == password and info['port'] == port:
            client_exclud_list.append(client)

    if len(client_exclud_list) <= 0:
        servidor.send(('ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD').encode('UTF-8'))
    else:
        excludItens(client_exclud_list)

def excludItens(clientes:dict, lista: list, servidor: socket.socket):
    for client in lista:
        servidor.send(('OK CLIENT_FINISHED').encode('UTF-8'))
        del clientes[client]

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
    
    servidor.send(string.encode('UTF-8'))

def requirementsREG(string: str, servidor: socket.socket):
    string = string.split(' ')
    if len(string) < 4:
        servidor.send(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'))
        exit()
    else:
        port = int(string[2])
        if port > 65535 or port < 0:
            servidor.send(('ERR PORT_INVALID_NUM').encode('UTF-8'))
            exit()
        else:
            data = string[3]
            data.split(';')
            tamanho = len(data)
            servidor.send((f'OK <{tamanho}>_REGISTERED_FILES').encode('UTF-8'))
            return string

def requirementsUPD(string: str, servidor: socket.socket):
    string = string.split(' ')
    if len(string) < 4:
        servidor.send(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'))
        exit()
    else:
        port = int(string[2])
        if port > 65535 or port < 1:
            servidor.send(('ERR PORT_INVALID_NUM').encode('UTF-8'))
            exit()
        else:
            return string

def searchInDB(clientes:dict, data:str, port:str, password: str, servidor: socket.socket):
    for temp, info in clientes.items():
        if "password" in info and info["password"] == password:
            info["data"] = data
            info['password'] = password
            info['port'] = port
            tamanho = data.split(';')
            servidor.send((f'OK <{len(tamanho)}>_REGISTERED_FILES').encode('UTF-8'))
            return 
    servidor.send(('ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD').encode('UTF-8'))
    return 
        
def socketUPD(clientes:dict, data:str, address, servidor: socket.socket):
    data = requirementsUPD(data)
    password = data[1]
    dados = data[3]
    port = data[2]
    searchInDB(clientes, dados, port, password, servidor)
    
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
    servidor.send((f'OK <{len(register)}>_REGISTERED_FILES').encode('UTF-8'))
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
        desfragmentaString(clientes, data, address, conn)
        
if __name__ == '__main__':
    main()

