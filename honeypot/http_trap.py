import socket
import threading
from datetime import datetime

HTTP_HEADER = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0f0f0f;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .box {
            background: #1a1a2e;
            padding: 40px 35px;
            border-radius: 12px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 0 40px rgba(0,255,245,0.15);
            border: 1px solid #0f3460;
        }
        .logo { text-align: center; margin-bottom: 25px; }
        .logo span { font-size: 40px; }
        h2 {
            color: #00fff5;
            text-align: center;
            font-size: 20px;
            margin-bottom: 6px;
        }
        .subtitle {
            color: #555;
            text-align: center;
            font-size: 12px;
            margin-bottom: 28px;
        }
        .input-group { margin-bottom: 16px; }
        .input-group label {
            display: block;
            color: #aaa;
            font-size: 12px;
            margin-bottom: 6px;
            letter-spacing: 1px;
        }
        .input-group input {
            width: 100%;
            padding: 12px 14px;
            background: #0f0f1a;
            border: 1px solid #0f3460;
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
            outline: none;
            transition: border 0.3s;
        }
        .input-group input:focus { border-color: #00fff5; }
        .input-group input::placeholder { color: #444; }
        button {
            width: 100%;
            padding: 13px;
            background: #00fff5;
            color: #0f0f0f;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 8px;
            transition: opacity 0.3s;
        }
        button:hover { opacity: 0.85; }
        button:active { opacity: 0.7; }
        .error {
            color: #ff6b6b;
            font-size: 12px;
            text-align: center;
            margin-top: 16px;
            padding: 10px;
            background: rgba(255,107,107,0.1);
            border-radius: 6px;
            border: 1px solid rgba(255,107,107,0.2);
        }
        .footer {
            text-align: center;
            margin-top: 24px;
            color: #333;
            font-size: 11px;
        }
        @media (max-width: 480px) {
            .box { padding: 30px 20px; }
            h2 { font-size: 18px; }
            .input-group input { font-size: 16px; padding: 14px; }
            button { padding: 15px; font-size: 16px; }
        }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo"><span>&#128272;</span></div>
        <h2>Admin Panel</h2>
        <p class="subtitle">Restricted Access Only</p>
        <form method="POST">
            <div class="input-group">
                <label>USERNAME</label>
                <input type="text" name="username" placeholder="Enter username" required/>
            </div>
            <div class="input-group">
                <label>PASSWORD</label>
                <input type="password" name="password" placeholder="Enter password" required/>
            </div>
            <button type="submit">Login</button>
        </form>
        <div class="error">Invalid credentials. Please try again.</div>
        <div class="footer">Protected System - Unauthorized access is prohibited</div>
    </div>
</body>
</html>"""

def parse_credentials(data):
    username = ''
    password = ''
    try:
        if 'username=' in data and 'password=' in data:
            body = data.split('\r\n\r\n')[-1]
            parts = body.split('&')
            for part in parts:
                if 'username=' in part:
                    username = part.split('=')[1]
                if 'password=' in part:
                    password = part.split('=')[1]
    except:
        pass
    return username, password

def handle_http(conn, addr):
    ip = addr[0]
    try:
        data = conn.recv(4096).decode(errors='ignore')
        if not data:
            conn.close()
            return
        first_line = data.split('\n')[0].strip()
        if 'POST' in data:
            username, password = parse_credentials(data)
            print("[HTTP] LOGIN ATTEMPT from " + ip)
            print("[HTTP] Username: " + username)
            print("[HTTP] Password: " + password)
            print("[HTTP] Time: " + str(datetime.now()))
            print("-" * 40)
        else:
            print("[HTTP] Visit from " + ip + " -> " + first_line)
        response = HTTP_HEADER + HTML_PAGE
        conn.send(response.encode('utf-8'))
        conn.close()
    except:
        pass

def start_http_trap(port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(100)
    print("[HTTP TRAP] Listening on port " + str(port) + "...")
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_http, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    start_http_trap()