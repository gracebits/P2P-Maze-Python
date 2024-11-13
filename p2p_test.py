import socket
import threading
import json
import time

# Configuration
PORT = 5000  # Port for communication
BROADCAST_IP = "255.255.255.255"  # Broadcast address
BUFFER_SIZE = 1024  # Maximum data size

class P2PNetwork:
    def __init__(self, player_name):
        self.player_name = player_name
        self.players = {}  # Dictionary of discovered players
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", PORT))
        self.running = True

    def broadcast_presence(self):
        """Broadcast player presence to the network."""
        while self.running:
            message = {
                "type": "presence",
                "name": self.player_name,
                "timestamp": time.time(),
            }
            self.sock.sendto(json.dumps(message).encode(), (BROADCAST_IP, PORT))
            print(f"[DEBUG] Broadcasted presence: {message}")
            time.sleep(2)  # Broadcast every 2 seconds

    def listen_for_messages(self):
        """Listen for messages from other players."""
        while self.running:
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                message = json.loads(data.decode())
                if message["type"] == "presence":
                    if addr not in self.players:
                        print(f"[LOG] New player joined: {message['name']} from {addr}")
                    self.players[addr] = message["name"]
                    print(f"[DEBUG] Current players: {self.players}")
            except Exception as e:
                print(f"[ERROR] Error receiving message: {e}")

    def start(self):
        """Start the network operations."""
        threading.Thread(target=self.broadcast_presence, daemon=True).start()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def stop(self):
        """Stop the network operations."""
        self.running = False
        self.sock.close()


# Main function
if __name__ == "__main__":
    player_name = input("Enter your player name: ")
    network = P2PNetwork(player_name)

    try:
        print(f"[INFO] Starting P2P network for player: {player_name}")
        network.start()
        print("[INFO] Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Stopping network...")
        network.stop()
