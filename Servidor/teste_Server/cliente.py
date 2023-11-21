import socket

host = '127.0.0.1'
porta = 55000

# Criação do socket do cliente
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    # Conecta ao servidor
    cliente.connect((host, porta))

    nome = f'Luiz Eduardo'.encode('UTF-8')
    cliente.send(nome)

    # Recebe a resposta do servidor
    dados = cliente.recv(1024)

print(f"Resposta do servidor: {dados.decode()}")