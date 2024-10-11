I started this project as I couldn't get Cuckoo to work as at the time of writing, Cuckoo was (apparantly) in the process of being updated for windows ll and more presisngly,
the latest versions of Python. It doesnt support anything after version 2.x of python.





The following Python modules need to be installed for this to work (as at 11/10/2024)

psutil - For monitoring system services.

watchdog - For monitoring file system changes.

pywin32 - For accessing Windows-specific APIs, which allows us to monitor registry changes.

colorama - For managing terminal colors and making ANSI escape codes compatible with Windows.




Copy service_monitor.py to the node to be monitored. 
You will then need to edit the IP address where to send the telemetry.

Copy server_listener.py to the recieveing node, and run in powershell.
Its designed to run in powershell.
If you run it in Python IDLE, you wont get the colour coding.

If you are using this to monitor the exectution of a malicious file, please ensure:

- You configure your networking appropriatly to prevet "leakage"
- Here’s a revised version with a bit more clarity and some additional security considerations:

To prevent malware from tampering with the service_monitor.py script, it’s crucial to set up appropriate file permissions. 
Ensure that the account used to log into the detonation host—such as "labadmin"—has only the necessary permissions to run the script, without modify rights. 
This will (hopefully) prevent unauthorized changes to the script during execution.

For example, if you log in as "labadmin," configure the permissions so that "labadmin" can only 
read and execute the service_monitor.py script, without any write or modify privileges.

Consider using a separate, higher-privileged account for initial script setup, allowing you to further restrict 
permissions on the detonation host. Additionally, you may want to use access control measures, such as AppLocker or 
similar application whitelisting tools, to prevent any unauthorized applications or users from 
modifying critical monitoring scripts.
