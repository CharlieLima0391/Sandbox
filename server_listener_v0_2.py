import socket
from colorama import init, Fore, Style

# Initialize colorama
init()

# Set up server details
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 65432

# Define colors using colorama
COLORS = {
    'service': Fore.GREEN,
    'file': Fore.YELLOW,
    'registry': Fore.RED,
    'reset': Style.RESET_ALL
}

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print(f"Listening on {SERVER_HOST}:{SERVER_PORT}...")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established!")

def get_color(message):
    if "service" in message.lower():
        return COLORS['service']
    elif "file" in message.lower():
        return COLORS['file']
    elif "registry" in message.lower():
        return COLORS['registry']
    return COLORS['reset']

try:
    while True:
        data = client_socket.recv(1024).decode()
        if data:
            color = get_color(data)
            print(f"{color}Received telemetry: {data}{COLORS['reset']}")
except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    client_socket.close()
    server_socket.close()
