import socket
import threading
from datetime import datetime
from core.database import log_attack
from core.detector import classify_threat

FTP_BANNER = "220 FTP Server Ready\r\n"
FTP_USER = "331 Password required\r\n"
FTP_PASS = "530 Login incorrect\r\n"

def handle_ftp(conn, addr):
    ip = addr[0]
    port = addr[1]
    username = ''
    password = ''
    try:
        conn.send(FTP_BANNER.encode())
        while True:
            data = conn.recv(1024).decode(errors='ignore').strip()
            if not data:
                break
            if data.upper().startswith('USER'):
                username = data[5:].strip()
                conn.send(FTP_USER.encode())
            elif data.upper().startswith('PASS'):
                password = data[5:].strip()
                threat = classify_threat(ip)
                log_attack(ip, port, 'FTP_LOGIN', username=username, password=password, threat_level=threat)
                print("[FTP] LOGIN ATTEMPT from " + ip)
                print("[FTP] Username: " + username)
                print("[FTP] Password: " + password)
                print("[FTP] Threat: " + threat)
                print("-" * 40)
                conn.send(FTP_PASS.encode())
                break
            elif data.upper().startswith('QUIT'):
                break
        conn.close()
    except:
        pass

def start_ftp_trap(port=2121):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(100)
    print("[FTP TRAP] Listening on port " + str(port) + "...")
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_ftp, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    start_ftp_trap()