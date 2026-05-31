import socket
import threading
from datetime import datetime
from core.database import log_attack
from core.detector import classify_threat

TELNET_BANNER = "Ubuntu 20.04 LTS\r\nlogin: "
TELNET_PASS = "Password: "
TELNET_FAIL = "\r\nLogin incorrect\r\n"

def handle_telnet(conn, addr):
    ip = addr[0]
    port = addr[1]
    username = ''
    password = ''
    try:
        conn.send(TELNET_BANNER.encode())
        username = conn.recv(1024).decode(errors='ignore').strip()
        conn.send(TELNET_PASS.encode())
        password = conn.recv(1024).decode(errors='ignore').strip()
        threat = classify_threat(ip)
        log_attack(ip, port, 'TELNET_LOGIN', username=username, password=password, threat_level=threat)
        print("[TELNET] LOGIN ATTEMPT from " + ip)
        print("[TELNET] Username: " + username)
        print("[TELNET] Password: " + password)
        print("[TELNET] Threat: " + threat)
        print("-" * 40)
        conn.send(TELNET_FAIL.encode())
        conn.close()
    except:
        pass

def start_telnet_trap(port=2323):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(100)
    print("[TELNET TRAP] Listening on port " + str(port) + "...")
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_telnet, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    start_telnet_trap()