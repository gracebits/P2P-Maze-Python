import socket
import threading
import json

class Network:
    def __init__(self, port):
        self.port = port
        self.players = {}  # {addr: {"name": str, "ready": bool}}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", self.port))
        self.running = True

    def start_listener(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode())
                print(f"Received message from {addr}: {message}")  # Debug log

                if message["type"] == "join":
                    if addr not in self.players:
                        print(f"New player joined: {message['name']} from {addr}")
                    self.players[addr] = {"name": message["name"], "ready": False}
                elif message["type"] == "ready":
                    if addr in self.players:
                        self.players[addr]["ready"] = True
                        print(f"Player {self.players[addr]['name']} is ready.")
            except Exception as e:
                print(f"Error in listening: {e}")

    def broadcast(self, message):
        print(f"Broadcasting message: {message}")  # Debug log
        for addr in self.players.keys():
            self.sock.sendto(json.dumps(message).encode(), addr)

    def stop(self):
        self.running = False
        self.sock.close()

    def all_ready(self):
        return len(self.players) >= 2 and all(player["ready"] for player in self.players.values())
