import socket
import threading
from datetime import datetime

SSH_BANNER = "SSH-2.0-OpenSSH_7.4\r\n"

def handle_connection(conn, addr):
    ip = addr[0]
    port = addr[1]
    
    try:
        conn.send(SSH_BANNER.encode())
        data = conn.recv(1024).decode(errors='ignore')
        
        print(f"[SSH] Connection from {ip}:{port}")
        print(f"[SSH] Data: {data}")
        print(f"[SSH] Time: {datetime.now()}")
        print("-" * 40)
        
        conn.close()
        
    except Exception as e:
        pass

def start_ssh_trap(port=2222):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(100)
    
    print(f"[SSH TRAP] Listening on port {port}...")
    
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    start_ssh_trap()