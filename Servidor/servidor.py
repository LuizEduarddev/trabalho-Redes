import socket
import hashlib

def calculate_md5(file_content):
    md5 = hashlib.md5()
    md5.update(file_content)
    return md5.hexdigest()

def handle_reg(message, clients, client_address):
    _, password, port, files = message.split(" ", 3)
    ip, _ = client_address

    clients[port] = {"password": password, "files": files, "ip":ip}
    num_files = len(files.split(";"))

    response = f"OK {num_files}_REGISTERED_FILES"

    return response

def handle_upd(message, clients, client_address):
    _, password, port, files = message.split(" ", 3)
    ip, _ = client_address

    for client_info in clients.values():
        if client_info["ip"] == ip and client_info["password"] == password:
            client_info["port"] = port
            client_info["files"] = files

            num_files = len(files.split(";"))
            response = f"OK {num_files}_REGISTERED_FILES"
            
            return response

    return "ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD"

def handle_lst(clients):
    response = ""
    for porta, client_info in clients.items():
        for file_info in client_info["files"].split(";"):
            if ',' in file_info:
                md5, file_name = file_info.split(",", 1)
                response += f"{md5},{file_name},{porta}:{client_info['ip']};"
            else:
                md5, file_name = file_info, "NULL"
                response += f"{md5},{file_name},{porta}:{client_info['ip']};"

    return response

def handle_end(message, clients, client_address):
    _, password, port = message.split(" ", 2)
    ip, _ = client_address

    if ip in clients and clients[ip]["password"] == password:
        del clients[ip]
        response = "OK CLIENT_FINISHED"
    else:
        response = "ERR IP_REGISTERED_WITH_DIFFERENT_PASSWORD"

    return response

def main():
    clients = {}

    server_ip = "127.0.0.1"
    server_port = 54494

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print("Server is listening on {}:{}".format(server_ip, server_port))

    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode("utf-8")
        print(f'received message {message}')
        message_type = message.split(" ")[0]

        if message_type == "REG":
            response = handle_reg(message, clients, client_address)
        elif message_type == "UPD":
            response = handle_upd(message, clients, client_address)
        elif message_type == "LST":
            response = handle_lst(clients)
        elif message_type == "END":
            response = handle_end(message, clients, client_address)
        else:
            response = "ERR INVALID_MESSAGE_FORMAT"

        server_socket.sendto(response.encode("utf-8"), client_address)
        print(clients)

if __name__ == "__main__":
    main()