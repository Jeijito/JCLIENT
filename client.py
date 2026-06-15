import socket
import sys
import config

def main():
    # Target address configuration
    server_ip = config.SERVER_IP
    server_port = config.SERVER_PORT
    
    print(f"Initializing client socket layer...")
    
    try:
        # 1. Create a socket object
        # AF_INET = IPv4, SOCK_STREAM = TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"Attempting connection handshake with {server_ip}:{server_port}...")
        # 2. Connect to the remote server architecture
        client_socket.connect((server_ip, server_port))
        
        print(" Handshake successful! Connected to the C server backend.")
        
    except ConnectionRefusedError:
        print("Connection refused. Is the C server running and listening?")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # 3. Clean up the socket resource channel
        print("Closing client socket channel.")
        client_socket.close()

if __name__ == "__main__":
    main()