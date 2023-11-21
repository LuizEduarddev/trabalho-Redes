import socket

# Configurações do servidor
host = '127.0.0.1'
porta = 55000

# Criação do socket do servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    # Associa o socket ao endereço e à porta
    servidor.bind((host, porta))

    # Fica ouvindo por até 1 conexão
    servidor.listen(1)

    print(f"Servidor aguardando conexão em {host}:{porta}")

    # Aceita a conexão
    conexao, endereco_cliente = servidor.accept()
    
    with conexao:
        print(f"Conexão estabelecida por {endereco_cliente}")

        # Recebe os dados do cliente
        data = conexao.recv(1024).decode('UTF-8')

        print(f'Mensagem do cliente: {data}')

        

       
