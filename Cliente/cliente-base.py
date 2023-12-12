import socket
import threading
import os
import random
import string
import hashlib

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

def tcp_server(client_socket, shared_directory):
    while True:
        command = client_socket.recv(1024).decode()
        if command == "LIST":
            files = os.listdir(shared_directory)
            files_list = "\n".join(files)
            client_socket.send(files_list.encode())
        elif command.startswith("DOWNLOAD"):
            _, filename = command.split()
            filepath = os.path.join(shared_directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    file_data = file.read()
                    client_socket.send(file_data)
            except FileNotFoundError:
                client_socket.send(b"File not found.")
        elif command == "DISCONNECT":
            break
    client_socket.close()

def handle_client(server_socket, shared_directory):
    client, _ = server_socket.accept()
    threading.Thread(target=tcp_server, args=(client, shared_directory)).start()

def generate_random_password():
    
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(8))

    return password

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

def main():
    print('\n\nWARNING: O DIRETORIO PRECISA SER ENVIADO ENTRE ASPAS\nEX: "/meu/diretorio"\n\n')
    if len(os.sys.argv) != 3:
        print("Usage: python3 cliente.py <IP> <DIRETORIO>")
        return

    server_ip = os.sys.argv[1]
    shared_directory = os.sys.argv[2]
    print(shared_directory)
    tcp_port = find_available_tcp_port()
    password = generate_random_password()

    directory = listar_arquivos_e_calcular_hash(shared_directory)
    register_to_server(server_ip, tcp_port, directory, password)

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('localhost', tcp_port))
    tcp_server_socket.listen(5)

    print(f"Cliente registrado com sucesso na porta TCP {tcp_port}")

    threading.Thread(target=handle_client, args=(tcp_server_socket, shared_directory)).start()

    while True:
        print("Comandos disponíveis:\n")
        print("1. LIST - Listar arquivos disponíveis")
        print("2. DOWNLOAD <filename> - Baixar um arquivo")
        print("3. UPD - Atualizar registro existente")
        print("4. DISCONNECT - Desconectar do servidor")
        command = int(input("\n\nOBS: DIGITE O NUMERO DA OPCAO\nDigite o comando desejado: "))

        if command == 1:
            command = "LST"
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (server_ip, 54494)
            client_socket.sendto(command.encode(), server_address)
            response, _ = client_socket.recvfrom(1024)
            print("Arquivos disponíveis:")
            print(response.decode())
            client_socket.close()

        elif command == 2:
            _, filename = command.split()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', tcp_port))
            client_socket.send(command.encode())
            file_data = client_socket.recv(1024)
            if file_data == b"File not found.":
                print("Arquivo não encontrado.")
            else:
                with open(os.path.join(shared_directory, filename), 'wb') as file:
                    file.write(file_data)
                print(f"Arquivo '{filename}' baixado com sucesso.")
            client_socket.close()

        elif command == 3:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', tcp_port))
            files = input("Por favor, insira o diretorio: ")
            command = f'UPD {password} {tcp_port} {files}'
            client_socket.send(command.encode())
            file_data = client_socket.recv(1024)
            print(file_data)
            client_socket.close()

        elif command == 4:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = (server_ip, 54494) 
            disconnect_message = f'END {password} {server_ip}'
            client_socket.sendto(disconnect_message.encode(), server_address)
            file_data = client_socket.recv(1024)
            print(file_data)
            break
        else:
            print("Comando inválido. Tente novamente.")

if __name__ == "__main__":
    main()