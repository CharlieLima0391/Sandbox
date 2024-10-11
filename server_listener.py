import socket

# Set up server details
SERVER_HOST = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 65432      # Port to listen on

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print(f"Listening on {SERVER_HOST}:{SERVER_PORT}...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established!")

# Receive data
try:
    while True:
        data = client_socket.recv(1024).decode()
        if data:
            print(f"Received telemetry: {data}")
except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    client_socket.close()
    server_socket.close()
