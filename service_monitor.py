import psutil
import time

# Initialize a set to track running services
running_services = set()

# Function to update service status
def update_services():
    global running_services
    current_services = {service.name() for service in psutil.win_service_iter() if service.status() == 'running'}
    started_services = current_services - running_services
    stopped_services = running_services - current_services
    running_services = current_services
    return started_services, stopped_services

# Main loop to monitor services
while True:
    started, stopped = update_services()
    if started:
        print(f"Started services: {', '.join(started)}")
    if stopped:
        print(f"Stopped services: {', '.join(stopped)}")
    # Wait for 5 seconds before checking again
    time.sleep(5)
