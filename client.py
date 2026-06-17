import socket
import sys
import os
import struct
import config
import upload

def main():
    server_ip = config.SERVER_IP
    server_port = config.SERVER_PORT
    
    target_filename = "test.txt"
    
    if not os.path.exists(target_filename):
        with open(target_filename, "w") as f:
            f.write("Hello Cloud Server backend! This is a chunked stream experiment.")

    print(f"Initializing client socket layer...")
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print("Connected to the C server backend.")
        
        command_opcode = b'\x01'
        
        if command_opcode == b'\x01':
            # --- UPLOAD MODE REGISTERED ---
            client_socket.sendall(command_opcode)
            
            # Pass execution off to our dedicated module function!
            upload.handle_upload(client_socket, target_filename)
            
        elif command_opcode == b'\x02':
            # --- DOWNLOAD MODE REGISTERED ---
            print("[CLIENT DOWNLOAD] Download sequence requested (Placeholder).")
            # Future implementation...


    except ConnectionRefusedError:
        print("Connection refused. Is the C server running and listening?")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        print("Closing client socket channel.")
        client_socket.close()

if __name__ == "__main__":
    main()