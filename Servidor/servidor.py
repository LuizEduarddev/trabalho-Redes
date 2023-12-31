import socket

def retornaHost():
    HOST = '127.0.0.1'
    return HOST

def retornaPorta():
    PORTA = 54494
    return PORTA

def defineServidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return servidor

def desfragmentaString(clientes: dict, data: str, address, servidor: socket.socket):
    try:
        teste = data.split(' ')
    except:
        servidor.sendto(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'), address)
        exit()

    if teste[0] == 'REG':
        socketREG(clientes, data, address, servidor)

    elif teste[0] == 'UPD':
        socketUPD(clientes, data, address, servidor)

    elif teste[0] == 'LST':
        socketLST(clientes, servidor, address)

    elif teste[0] == 'END':
        socketEND(clientes, servidor, address, data)

    else:
        servidor.sendto(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'), address)
        return 0

def requirementsEND(servidor: socket.socket, data: str, address):
    string = data.split(' ')
    if len(string) < 3:
        servidor.sendto(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'), address)
        exit()
    else:
        port = int(string[2])
        if port > 65535 or port < 0:
            servidor.sendto(('ERR PORT_INVALID_NUM').encode('UTF-8'), address)
            exit()
        else:
            return string

def socketEND(clientes:dict, servidor: socket.socket, address, data: str):
    data = requirementsEND(servidor, data, address) # Dudu do futuro, nao precisa mudar a logica do return, ta certo
    password = data[1]
    port = data[2]
    client_exclud_list = []
    for client, info in clientes.items():
        if info['password'] == password and info['port'] == port:
            client_exclud_list.append(client)

    if len(client_exclud_list) <= 0:
        servidor.sendto(('ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD').encode('UTF-8'), address)
    else:
        excludItens(clientes, client_exclud_list, servidor, address)

def excludItens(clientes:dict, lista: list, servidor: socket.socket, address):
    for client in lista:
        servidor.sendto(('OK CLIENT_FINISHED').encode('UTF-8'), address)
        del clientes[client]

def verificaTemp(string, number, tamanho):
    temp = number + 1
    if temp >= tamanho:
        return 
    else:
       string = string + ','
       return string

def socketLST(clientes: dict, servidor: socket.socket, address):
    number = int(0)
    string = str()
    tamanho = len(clientes)

    for chave, info in clientes.items():
        number += 1
        string = string + f'{info["data"]},ip{info["users_count"]}:{info["address"]}'
        string = verificaTemp(string, number, tamanho)
    
    servidor.sendto(string.encode('UTF-8'), address)

def requirementsREG(string: str, servidor: socket.socket, address):
    string = string.split(' ')
    if len(string) < 4:
        servidor.sendto(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'), address)
        exit()
    else:
        port = int(string[2])
        if port > 65535 or port < 0:
            servidor.sendto(('ERR PORT_INVALID_NUM').encode('UTF-8'), address)
            exit()
        else:
            data = string[3]
            data.split(';')
            tamanho = len(data)
            servidor.sendto((f'OK <1>_REGISTERED_FILES').encode('UTF-8'), address)
            return string

def requirementsUPD(string: str, servidor: socket.socket, address):
    string = string.split(' ')
    if len(string) < 4:
        servidor.sendto(('ERR INVALID_MESSAGE_FORMAT').encode('UTF-8'), address)
        exit()
    else:
        port = int(string[2])
        if port > 65535 or port < 1:
            servidor.sendto(('ERR PORT_INVALID_NUM').encode('UTF-8'), address)
            exit()
        else:
            return string

def searchInDB(clientes:dict, data:str, port:str, password: str, servidor: socket.socket, address):
    for temp, info in clientes.items():
        if "password" in info and info["password"] == password:
            info["data"] = data
            info['password'] = password
            info['port'] = port
            tamanho = data.split(';')
            servidor.sendto((f'OK <1>_REGISTERED_FILES').encode('UTF-8'), address)
            return 
    servidor.sendto(('ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD').encode('UTF-8'), address)
    return 
        
def socketUPD(clientes:dict, data:str, address, servidor: socket.socket):
    data = requirementsUPD(data, servidor, address)
    password = data[1]
    dados = data[3]
    port = data[2]
    searchInDB(clientes, dados, port, password, servidor, address)
    
def socketREG(clientes:dict, data: str, address, servidor: socket.socket):
    data = requirementsREG(data, servidor, address)
    clientes = updateClientes(clientes, data[3], address, data[2], data[1], servidor)

def updateClientes(clientes :dict, data, address, port, password, servidor: socket.socket):
    atualizaNumero = 0
    atualizaNumero += int(clientes['usuarios'])
    clientes.update({'users_count': atualizaNumero})
    chave = f'client{atualizaNumero}'
    clientes.update({chave:{'data':data, 'address': address, 'port': port, 'password': password}})
    register = data[3]
    if ';' in register:
        register = register.split(';')
        servidor.sendto((f'OK <{len(register)}>_REGISTERED_FILES').encode('UTF-8'), address)
    else:
        number = 1
        servidor.sendto((f'OK <{(number)}>_REGISTERED_FILES').encode('UTF-8'), address)
    return clientes


clientes = {'usuarios': 0}
HOST = retornaHost()
PORTA = retornaPorta()
servidor = defineServidor()

servidor.bind((HOST, PORTA))
print('Waiting for some information.........')

while True:
    data, address  = servidor.recvfrom(1024)
    data = data.decode('UTF-8')

    print(f'Data |{data}| get from: {address}')
    desfragmentaString(clientes, data, address, servidor)

