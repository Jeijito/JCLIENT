import os
import struct

def handle_upload(client_socket, target_filename):
    # A. Extract and encode metadata parameters
    filename_bytes = target_filename.encode('utf-8')
    filename_len = len(filename_bytes)
    file_size = os.path.getsize(target_filename)
    
    print(f"[CLIENT UPLOAD] Packing: {target_filename} ({file_size} bytes)")
    
    # B. Push complete metadata protocol header
    client_socket.sendall(bytes([filename_len]))
    client_socket.sendall(filename_bytes)
    client_socket.sendall(struct.pack('>Q', file_size))
    
    # C. Open local storage tracking file in Read Binary mode
    with open(target_filename, "rb") as f:
        while True:
            # Extract data incrementally in stable 4KB workspace chunks
            chunk = f.read(4096)
            if not chunk:
                break # Reached the exact end of the file safely
            
            client_socket.sendall(chunk)
            
    print("[CLIENT SUCCESS] File data stream transmission complete.")