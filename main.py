import threading
from core.database import init_db
from honeypot.ssh_trap import start_ssh_trap
from honeypot.http_trap import start_http_trap
from honeypot.ftp_trap import start_ftp_trap
from core.logger import start_telnet_trap
from dashboard.app import start_dashboard

def main():
    print("""
    ██╗  ██╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ ████████╗
    ██║  ██║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
    ███████║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝ ██████╔╝██║   ██║   ██║
    ██╔══██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝  ██╔═══╝ ██║   ██║   ██║
    ██║  ██║╚██████╔╝██║ ╚████║███████╗   ██║   ██║     ╚██████╔╝   ██║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝      ╚═════╝    ╚═╝
    """)
    print("[*] Initializing database...")
    init_db()

    print("[*] Starting honeypot traps...")

    ssh_thread = threading.Thread(target=start_ssh_trap, args=(2222,))
    ssh_thread.daemon = True
    ssh_thread.start()

    http_thread = threading.Thread(target=start_http_trap, args=(8080,))
    http_thread.daemon = True
    http_thread.start()

    ftp_thread = threading.Thread(target=start_ftp_trap, args=(2121,))
    ftp_thread.daemon = True
    ftp_thread.start()

    telnet_thread = threading.Thread(target=start_telnet_trap, args=(2323,))
    telnet_thread.daemon = True
    telnet_thread.start()

    print("[*] All traps active:")
    print("    SSH     → port 2222")
    print("    HTTP    → port 8080")
    print("    FTP     → port 2121")
    print("    TELNET  → port 2323")
    print("[*] Dashboard → http://localhost:5000")
    print("[*] Press CTRL+C to stop\n")

    start_dashboard()

if __name__ == '__main__':
    main()