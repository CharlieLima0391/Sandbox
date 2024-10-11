import psutil
import socket
import time
import win32api
import win32con
import win32event
import win32security
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread

# Server IP and Port
SERVER_IP = '192.168.3.12'  # Replace with your server's IP address
SERVER_PORT = 65432

# Directory to watch (root of the main drive)
DIRECTORY_TO_WATCH = "C:\\"

# Registry notification constants
REG_NOTIFY_CHANGE_NAME = 0x00000001
REG_NOTIFY_CHANGE_ATTRIBUTES = 0x00000002
REG_NOTIFY_CHANGE_LAST_SET = 0x00000004
REG_NOTIFY_CHANGE_SECURITY = 0x00000008

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

# Define the event handler for file system changes
class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        message = f"File created: {event.src_path}"
        client_socket.send(message.encode())
    def on_modified(self, event):
        message = f"File modified: {event.src_path}"
        client_socket.send(message.encode())
    def on_deleted(self, event):
        message = f"File deleted: {event.src_path}"
        client_socket.send(message.encode())
    def on_moved(self, event):
        message = f"File moved from {event.src_path} to {event.dest_path}"
        client_socket.send(message.encode())

# Registry monitoring function
# Registry monitoring function with full key path reporting
def monitor_registry_changes():
    registry_keys = [
        (win32con.HKEY_CURRENT_USER, "Software"),
        (win32con.HKEY_LOCAL_MACHINE, "SOFTWARE")
    ]
    reg_handles = []
    for hive, sub_key in registry_keys:
        handle = win32api.RegOpenKeyEx(hive, sub_key, 0, win32con.KEY_NOTIFY)
        reg_handles.append((hive, handle, sub_key))

    while True:
        for hive, handle, sub_key in reg_handles:
            win32api.RegNotifyChangeKeyValue(
                handle, True, REG_NOTIFY_CHANGE_NAME |
                REG_NOTIFY_CHANGE_ATTRIBUTES |
                REG_NOTIFY_CHANGE_LAST_SET |
                REG_NOTIFY_CHANGE_SECURITY, None, False
            )
            # Construct and send the full registry path
            full_path = get_registry_hive_name(hive) + "\\" + sub_key
            message = f"Registry change detected in {full_path}"
            client_socket.send(message.encode())

# Helper function to get the hive name
def get_registry_hive_name(hive):
    hive_names = {
        win32con.HKEY_CURRENT_USER: "HKEY_CURRENT_USER",
        win32con.HKEY_LOCAL_MACHINE: "HKEY_LOCAL_MACHINE"
    }
    return hive_names.get(hive, "UNKNOWN_HIVE")


# Set up file monitoring
observer = Observer()
observer.schedule(WatcherHandler(), DIRECTORY_TO_WATCH, recursive=True)
observer.start()

# Start registry monitoring in a separate thread
registry_thread = Thread(target=monitor_registry_changes)
registry_thread.start()

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
        time.sleep(1)
except KeyboardInterrupt:
    print("Client shutting down...")
finally:
    observer.stop()
    observer.join()
    client_socket.close()
