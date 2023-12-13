#!/usr/bin/python

import secrets
import string
import sys
import time
import socket
from _thread import *
import os
from hashlib import md5
import random
import hashlib

client = {}

encerra_tcp = False

def generate_random_password():
    
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(8))

    return password

def string_arquivos():
    lista = []
    diretorio = client['shared_directory']

    for arquivo_nome in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, arquivo_nome)

        if os.path.isfile(caminho_arquivo):  # Certifica-se de que é um arquivo, não um diretório
            with open(caminho_arquivo, 'rb') as arquivo:
                md5_arquivo = md5(arquivo.read()).hexdigest()
                elemento_lista = f"{md5_arquivo},{arquivo_nome}"
                lista.append(elemento_lista)

    # Junte os elementos da lista em uma única string
    str_lista = ';'.join(lista)
    return str_lista


def find_port():
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('localhost', 0))
    _, port = temp_socket.getsockname()
    temp_socket.close()
    return port

def calcular_hash_do_arquivo(caminho_arquivo, algoritmo='sha256', buffer_size=65536):
    try:
        hash_obj = hashlib.new(algoritmo)

        with open(caminho_arquivo, 'rb') as arquivo:
            for bloco in iter(lambda: arquivo.read(buffer_size), b''):
                hash_obj.update(bloco)

        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Erro ao calcular hash: {e}")
        return None

def listar_arquivos_e_calcular_hash(diretorio):
    try:
        lista_arquivos = os.listdir(diretorio)
        if not lista_arquivos:
            print("O diretório está vazio.")
            return None

        print("Arquivos disponíveis:")
        for i, arquivo in enumerate(lista_arquivos, start=1):
            print(f"{i}. {arquivo}")

        escolha = int(input("Escolha o número do arquivo: "))
        if 1 <= escolha <= len(lista_arquivos):
            arquivo_escolhido = lista_arquivos[escolha - 1]

            caminho_arquivo = os.path.abspath(os.path.join(diretorio, arquivo_escolhido))

            hash_do_arquivo = calcular_hash_do_arquivo(caminho_arquivo)

            return f"{hash_do_arquivo},{arquivo_escolhido}"
        else:
            print("Escolha inválida.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def envia_recebe_udp(mensagem, endereco_servidor, socket_cliente):
    try:
        socket_cliente.sendto(mensagem.encode('utf-8'), endereco_servidor)
        print(f'\nMensagem enviada: {mensagem}\n')
        data, _ = socket_cliente.recvfrom(4096)
        resposta = data.decode('utf-8')
        print(f'\nMensagem recebida: {resposta}\n')
        return resposta
    except:
        print(f'Erro ao tentar se comunicar com o servidor\n')

def menu_selecionar_arquivo(str_arquivos):
    while True:
        if not str_arquivos:
            print('Não há arquivos disponíveis para download.\n')
            return None

        # Transforma a string em uma lista de arquivos
        arquivos_lista = str_arquivos.split(';')

        # Verifica se há arquivos disponíveis para download
        arquivos_disponiveis = False
        for arquivo_info in arquivos_lista:
            # Adiciona uma verificação para garantir que há pelo menos dois valores após o split(',')
            if ',' not in arquivo_info:
                continue

            md5, nome, *hosts = arquivo_info.split(',')
            
            # Verifica se o IP e a porta do cliente estão na lista de hosts do arquivo
            if (str(client['server_ip']) + ':' + str((client['port']))) not in hosts:
                arquivos_disponiveis = True
                break

        if not arquivos_disponiveis:
            print('Não há arquivos disponíveis para download.\n')
            return None

        print('Selecione um arquivo que deseja baixar:')
        for i, arquivo_info in enumerate(arquivos_lista):
            # Adiciona novamente a verificação para garantir que há pelo menos dois valores após o split(',')
            if ',' not in arquivo_info:
                continue

            md5, nome, *hosts = arquivo_info.split(',')
            
            # Verifica se o IP e a porta do cliente estão na lista de hosts do arquivo
            if (str(client['server_ip']) + ':' + str((client['port']))) not in hosts:
                print(f'{i + 1} - Nome: {nome}, Hash: {md5}')

        print('0 - Sair')
        opcao = int(input('\nOpção: '))

        # Verifica se a opção selecionada está dentro do índice da arquivos_lista
        if 0 <= opcao <= len(arquivos_lista):
            if opcao == 0:
                print('Saindo do menu de seleção de arquivo.')
                return None
            else:
                arquivo_selecionado = arquivos_lista[opcao - 1]
                return arquivo_selecionado
        else:
            print('Opção inválida. Tente novamente.')


def menu_selecionar_host(arquivo_selecionado):
    md5 , nome, *hosts = arquivo_selecionado.split(',')
    print(f'\nSelecione um host para baixar o arquivo "{nome}":')
    for i, host_info in enumerate(hosts):
        ip, porta = host_info.split(':')
        print(f'{i+1} - IP: {ip}, Porta: {porta}')

    opcao = int(input('\nOpção: '))

    if 1<= opcao <= len(hosts):
        host_selecionado = hosts[opcao - 1]
        print(f'\nVocê selecionou o arquivo "{nome}" do host "{host_selecionado}" para download.')
        ip, porta = host_selecionado.split(':')
        return ip, porta, md5, nome
    else:
        print('Opção inválida.')

def requisita_arquivo(ip, porta, hash, nome):
    try:
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_cliente.connect((ip, int(porta)))
        mensagem = f"GET {hash}"
        socket_cliente.send(mensagem.encode('utf-8'))
        print(f'\nMensagem enviada: {mensagem}\n')

        with open(os.path.join(client['shared_directory'], nome), 'wb') as arquivo:
            while True:
                data = socket_cliente.recv(4096)
                print(f'\nMensagem recebida: {data}\n')
                if not data:
                    break
                arquivo.write(data)
    except Exception as e:
        print(f"\nErro ao requisitar o arquivo: {nome}")
    finally:
        socket_cliente.close()

def envia_recebe_udp(mensagem, endereco_servidor, socket_cliente):
    try:
        socket_cliente.sendto(mensagem.encode('utf-8'), endereco_servidor)
        print(f'\nMensagem enviada: {mensagem}\n')
        data, _ = socket_cliente.recvfrom(4096)
        resposta = data.decode('utf-8')
        print(f'\nMensagem recebida: {resposta}\n')
        return resposta
    except:
        print(f'Erro ao tentar se comunicar com o servidor\n')

def controle_udp():
    
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    directory = client['shared_directory']
    directory = listar_arquivos_e_calcular_hash(client['shared_directory'])
    register_to_server(client['server_ip'], client['port'], directory, client['password'])
    endereco_servidor = ('localhost', 54494)
    
    while True:
        #cria interfaçe para o usúario poder selecionar se ele quer listar arquivos disponíveis, baixar um arquivo ou sair do programa
        print("Comandos disponíveis:\n")
        print("1. LIST - Listar arquivos disponíveis")
        print("2. DOWNLOAD <filename> - Baixar um arquivo")
        print("3. UPD - Atualizar registro existente")
        print("4. DISCONNECT - Desconectar do servidor")
        command = int(input("\n\nOBS: DIGITE O NUMERO DA OPCAO\nDigite o comando desejado: "))
        if command == 1:
            command = "LST"
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('localhost', 54494)
            client_socket.sendto(command.encode(), server_address)
            response, _ = client_socket.recvfrom(1024)
            print("Arquivos disponíveis:")
            print(response.decode())
        
        elif command == 2:
            mensagem = "LST"
            resposta = envia_recebe_udp(mensagem, endereco_servidor, udp_client)
            info_arquivo = menu_selecionar_arquivo(resposta)
            if info_arquivo is None:
                continue
            ip, porta, hash, nome = menu_selecionar_host(info_arquivo)
            requisita_arquivo(ip, porta, hash, nome)
            str_arquivos = string_arquivos()
            mensagem = f"UPD {client['password']} {client['port']} {str_arquivos}"
            envia_recebe_udp(mensagem, endereco_servidor, udp_client)
        
        elif command == 3:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('localhost', 54494)
            shared_directory = input('digite o diretorio\n: ')
            files = listar_arquivos_e_calcular_hash(shared_directory)
            password = client['password']
            tcp_port = client['port']
            command = f'UPD {password} {tcp_port} {files}'
            client_socket.sendto(command.encode(), server_address)
            response, _ = client_socket.recvfrom(1024)
            print(response.decode())
        
        elif command == 4:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('localhost', 54494)
            disconnect_message = f"END {password} {'localhost'}"
            client_socket.sendto(disconnect_message.encode(), server_address)
            response, _ = client_socket.recvfrom(1024)
            print(response.decode())
            client_socket.close()
            exit(0)
        else:
            print("Comando inválido. Tente novamente.")

def servico_tcp(client):
    try:
        mensagem = client.recv(4096).decode('utf-8')
        print(f'\nMensagem recebida: {mensagem}\n')
        
        if mensagem.startswith("GET "):
            _, hash_arquivo = mensagem.split(" ")
            diretorio = client['shared_directory']

            for arquivo_nome in os.listdir(diretorio):
                caminho_arquivo = os.path.join(diretorio, arquivo_nome)

                if os.path.isfile(caminho_arquivo):
                    with open(caminho_arquivo, 'rb') as arquivo:
                        md5_arquivo = md5(arquivo.read()).hexdigest()

                        if md5_arquivo == hash_arquivo:
                            # Envia o arquivo para o cliente
                            with open(caminho_arquivo, 'rb') as arquivo_enviar:
                                dados = arquivo_enviar.read()
                                client.sendall(dados)
                            break
            else:
                client.sendall('Arquivo não encontrado')
        else:
            client.sendall('Mensagem inválida')

    except Exception as e:
        return

    finally:
        client.close()

def controle_tcp(client):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _socket.bind((client['server_ip'], client['port']))
    _socket.listen(4096)
    while True:
        client, addr = _socket.accept()
        start_new_thread(servico_tcp, (client, ))
        if encerra_tcp:
            _socket.close()
        
def inicia_controle_tcp():
    controle_tcp()

def inicia_controle_udp():
    controle_udp()

def find_available_tcp_port():
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('localhost', 0))
    _, port = temp_socket.getsockname()
    temp_socket.close()
    return port

def register_to_server(server_ip, tcp_port, shared_directory, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, 54494)

    registration_message = f"REG {password} {tcp_port} {shared_directory}"
    client_socket.sendto(registration_message.encode(), server_address)
    response, _ = client_socket.recvfrom(1024)
    print(response.decode())
    client_socket.close()

def configurar_ambiente():
    tcp_port = find_available_tcp_port()
    password = generate_random_password()

    client['port'] = tcp_port
    client['password'] = password

def main():   
    
    configurar_ambiente()

    print(f"SUA PORTA: {client['port']}")
    print(f"SUA SENHA: {client['password']}")
    
    start_new_thread(controle_tcp, (client,))
    start_new_thread(inicia_controle_udp, ())

    while True:
        time.sleep(60)
        print('\nCliente em execução')

if __name__ == '__main__':
    if len(os.sys.argv) != 3:
        print("Usage: python3 cliente.py <IP> <DIRETORIO>")
        sys.exit(-1)
    else:
        client['server_ip'] = os.sys.argv[1]
        client['shared_directory'] = os.sys.argv[2]
        main()