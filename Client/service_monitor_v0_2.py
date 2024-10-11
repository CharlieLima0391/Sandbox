import psutil
import socket
import time

# Server IP and Port
SERVER_IP = '192.168.3.12'  # Replace with your server's IP address
SERVER_PORT = 65432

# Initialize a set to track running services
running_services = set()

# Set up the socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Function to update service status
def update_services():
    global running_services
    current_services = {service.name() for service in psutil.win_service_iter() if service.status() == 'running'}
    started_services = current_services - running_services
    stopped_services = running_services - current_services
    running_services = current_services
    return started_services, stopped_services

# Main loop to monitor services and send updates
try:
    while True:
        started, stopped = update_services()
        if started:
            message = f"Started services: {', '.join(started)}"
            client_socket.send(message.encode())
        if stopped:
            message = f"Stopped services: {', '.join(stopped)}"
            client_socket.send(message.encode())
        # Wait for 5 seconds before checking again
        time.sleep(1)
except KeyboardInterrupt:
    print("Client shutting down...")
finally:
    client_socket.close()
