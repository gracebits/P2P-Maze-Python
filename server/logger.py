# server/logger.py
import logging

# Set up logging configuration
logging.basicConfig(filename='server.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def log_player_activity(player_name, activity, ip_address):
    log_message = f"Player {player_name} ({ip_address}) {activity}."
    logging.info(log_message)

def log_server_event(event):
    logging.info(f"Server Event: {event}")

def log_error(error_message):
    logging.error(f"Error: {error_message}")

# Example usage for logging player activity
# log_player_activity("John", "joined lobby 1", "192.168.1.2")
# log_server_event("Lobby 1 created.")
