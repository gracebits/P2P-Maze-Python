import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 5000))  # Listen on port 5000
print("Listening for messages...")
while True:
    data, addr = sock.recvfrom(1024)
    print(f"Message received from {addr}: {data.decode()}")
