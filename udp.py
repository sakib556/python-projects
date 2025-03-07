import socket
import json
import os

# Set up UDP client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(5)  # Set timeout to 5 seconds


broadcast_ip = os.getenv("SERVER_IP", "")
server_port = int(os.getenv("SERVER_PORT", ""))

print(f"Connecting to server at {broadcast_ip}:{server_port}")

message = b"DISCOVER_SERVER"

# Send UDP broadcast
sock.sendto(message, (broadcast_ip, server_port))
print(f"Sent: {message.decode()} to {broadcast_ip}:{server_port}")

# List to store discovered servers
discovered_servers = []

# Receive multiple responses until timeout
try:
    while True:
        data, addr = sock.recvfrom(1024)
        response = data.decode()

        try:
            server_info = json.loads(response)
            server_info["source_ip"] = addr[0]  # Add the source IP

            # Avoid duplicates
            if server_info not in discovered_servers:
                discovered_servers.append(server_info)
                print(f"Discovered: {server_info}")
        
        except json.JSONDecodeError:
            print(f"Invalid JSON response from {addr}: {response}")

except socket.timeout:
    print("Finished listening for responses.")

sock.close()

# Print final list of discovered servers
print("\nFinal list of discovered servers:")
for server in discovered_servers:
    print(server)
