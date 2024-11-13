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
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())

            if message["type"] == "join":
                # Add new player or update existing one
                self.players[addr] = {"name": message["name"], "ready": False}
            elif message["type"] == "ready":
                # Update player ready state
                if addr in self.players:
                    self.players[addr]["ready"] = True

    def broadcast(self, message):
        for addr in self.players.keys():
            self.sock.sendto(json.dumps(message).encode(), addr)

    def stop(self):
        self.running = False
        self.sock.close()

    def all_ready(self):
        return len(self.players) >= 2 and all(player["ready"] for player in self.players.values())
