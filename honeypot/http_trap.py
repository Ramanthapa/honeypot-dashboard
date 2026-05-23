import socket
import threading
from datetime import datetime
from core.database import log_attack
from core.detector import classify_threat

HTTP_HEADER = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #060612;
            font-family: 'Inter', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 16px;
            background-image: radial-gradient(ellipse at top, #0d1b2a 0%, #060612 70%);
        }
        .card {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(20px);
            padding: 48px 40px;
            border-radius: 20px;
            width: 100%;
            max-width: 420px;
            border: 1px solid rgba(0,255,245,0.1);
            box-shadow: 0 0 60px rgba(0,255,245,0.05), 0 20px 60px rgba(0,0,0,0.5);
        }
        .top { text-align: center; margin-bottom: 32px; }
        .icon-wrap {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #00fff5, #0070ff);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 28px;
            box-shadow: 0 0 30px rgba(0,255,245,0.3);
        }
        h2 {
            color: #ffffff;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .subtitle { color: #4a5568; font-size: 13px; }
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0,255,245,0.15), transparent);
            margin: 24px 0;
        }
        .input-group { margin-bottom: 18px; }
        .input-group label {
            display: block;
            color: #718096;
            font-size: 11px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        }
        .input-wrap { position: relative; }
        .input-wrap .icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 15px;
            opacity: 0.4;
        }
        .input-group input {
            width: 100%;
            padding: 13px 14px 13px 42px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            color: #fff;
            font-size: 14px;
            font-family: inherit;
            outline: none;
            transition: all 0.25s ease;
        }
        .input-group input:focus {
            border-color: rgba(0,255,245,0.4);
            background: rgba(0,255,245,0.04);
            box-shadow: 0 0 0 3px rgba(0,255,245,0.08);
        }
        .input-group input::placeholder { color: #2d3748; }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #00fff5, #0070ff);
            color: #060612;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 700;
            font-family: inherit;
            cursor: pointer;
            margin-top: 6px;
            transition: all 0.25s ease;
            box-shadow: 0 4px 20px rgba(0,255,245,0.25);
        }
        button:hover { transform: translateY(-1px); box-shadow: 0 8px 25px rgba(0,255,245,0.35); }
        button:active { transform: translateY(0px); opacity: 0.9; }
        .error-box {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #fc8181;
            font-size: 12px;
            margin-top: 18px;
            padding: 12px 14px;
            background: rgba(252,129,129,0.08);
            border-radius: 8px;
            border: 1px solid rgba(252,129,129,0.15);
        }
        .error-box span { font-size: 16px; }
        .footer {
            text-align: center;
            margin-top: 28px;
            color: #2d3748;
            font-size: 11px;
            letter-spacing: 0.3px;
        }
        .footer strong { color: #3d4a5c; }
        @media (max-width: 480px) {
            body { padding: 12px; align-items: flex-start; padding-top: 40px; }
            .card { padding: 36px 24px; border-radius: 16px; }
            h2 { font-size: 20px; }
            .icon-wrap { width: 56px; height: 56px; font-size: 24px; }
            .input-group input { font-size: 16px; padding: 14px 14px 14px 42px; }
            button { padding: 15px; font-size: 16px; }
        }
        @media (max-width: 360px) {
            .card { padding: 28px 18px; }
            h2 { font-size: 18px; }
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="top">
            <div class="icon-wrap">&#128272;</div>
            <h2>Admin Panel</h2>
            <p class="subtitle">Authorized Personnel Only</p>
        </div>
        <div class="divider"></div>
        <form method="POST">
            <div class="input-group">
                <label>Username</label>
                <div class="input-wrap">
                    <span class="icon">&#128100;</span>
                    <input type="text" name="username" placeholder="Enter your username" required/>
                </div>
            </div>
            <div class="input-group">
                <label>Password</label>
                <div class="input-wrap">
                    <span class="icon">&#128274;</span>
                    <input type="password" name="password" placeholder="Enter your password" required/>
                </div>
            </div>
            <button type="submit">Sign In</button>
        </form>
        <div class="error-box">
            <span>&#9888;</span>
            Invalid credentials. Access denied.
        </div>
        <div class="footer">
            <strong>PROTECTED SYSTEM</strong> — Unauthorized access is strictly prohibited
        </div>
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
        threat = classify_threat(ip)
        if 'POST' in data:
            username, password = parse_credentials(data)
            log_attack(ip, 8080, 'LOGIN_ATTEMPT', username=username, password=password, threat_level=threat)
            print("[HTTP] LOGIN ATTEMPT from " + ip)
            print("[HTTP] Username: " + username)
            print("[HTTP] Password: " + password)
            print("[HTTP] Threat: " + threat)
            print("-" * 40)
        else:
            log_attack(ip, 8080, 'HTTP_PROBE', raw_data=first_line, threat_level=threat)
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