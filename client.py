import socket
import config  # Import the configuration file

def client_program():
    server_ip = config.SERVER_IP  # Use the configuration from config.py
    server_port = config.SERVER_PORT

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        message = client_socket.recv(1024).decode()
        print(message, end='')

        response = input()
        client_socket.sendall(response.encode())

        message = client_socket.recv(1024).decode()
        print(message, end='')

        if "ready" in message.lower():
            response = input("Ready to start the game? (yes/no): ").strip().lower()
            client_socket.sendall(response.encode())
            if response == "yes":
                break

    print("Game started!")

if __name__ == "__main__":
    client_program()
