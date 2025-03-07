import socket
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
SERVER_IP = os.getenv("SERVER_IP", "")
SERVER_PORT = int(os.getenv("SERVER_PORT", ""))

print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}")

def send_tcp_message(ip, port):
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Set a timeout of 5 seconds

        # Connect to the server
        sock.connect((ip, port))
        print("Connected successfully to the server!")

        # Step 1: Send authentication message
        auth_message = json.dumps({"connection": {"pin": "1"}})
        sock.sendall(auth_message.encode())
        print(f"Sent authentication message: {auth_message}")

        # Step 2: Wait for the authentication response
        auth_response = sock.recv(1024).decode()
        print(f"Received authentication response: {auth_response}")

        # Check if authentication was successful
        try:
            auth_data = json.loads(auth_response)
            if auth_data.get("connection", {}).get("message") == "Authenticated":
                print("Authentication successful, sending further settings...")

                # Step 3: Send other messages only after successful authentication
                settings_message_1 = json.dumps({"settings": {"copyMode": "Append"}})
                #settings_message_1 = json.dumps({"settings": {"copyMode": "Overwrite"}})
            #   settings_message_2 = json.dumps({"settings": {"copyMode": "Append"}})

                sock.sendall(settings_message_1.encode())
                print(f"Sent settings message 1: {settings_message_1}")

                # sock.sendall(settings_message_2.encode())
                # print(f"Sent settings message 2: {settings_message_2}")
            else:
                print("Authentication failed. Terminating communication.")
                sock.close()
                return
        except json.JSONDecodeError:
            print("Failed to decode authentication response.")
            sock.close()
            return
        
        # Step 4: Receive and print the server's response
        response = sock.recv(1024)
        if response:
            print("Response from server:", response.decode())
        else:
            print("No response from the server.")

        # Close the socket connection
        sock.close()
        print("Connection closed.")

    except socket.timeout:
        print("Connection timed out.")
    except socket.error as e:
        print(f"Socket error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Call the function to send the messages based on authentication response
    send_tcp_message(server_ip, server_port)
