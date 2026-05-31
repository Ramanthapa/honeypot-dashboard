# Honeypot Attack Dashboard

So I was curious about what actually happens when attackers find an open server.
Like what do they try first? What passwords do they use? How fast do they move?

Built this to find out. Started with just a fake SSH server, then kept adding 
stuff — HTTP trap, FTP trap, a database, and finally a live dashboard. Took me 
around 15 days to get it working properly.

<img width="1365" height="601" alt="screenshot" src="https://github.com/user-attachments/assets/1e1d9422-5cfd-4369-950d-acbed918b49a" />
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.0-lightgrey)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## What it does

Runs fake servers that look real to attackers. When someone tries to connect 
or login, everything gets logged silently — their IP, what credentials they 
tried, and the threat level based on how aggressive they are.

- SSH trap on port 2222 — catches brute force attempts
- HTTP trap on port 8080 — fake admin login page that logs credentials
- FTP trap on port 2121 — catches FTP login attempts
- Threat classifier — detects brute force based on attempt frequency
- Live dashboard — shows all attacks in real time with charts

## Tech Stack

Python, Socket, Threading, Flask, SQLite, Chart.js, HTML/CSS

## How to run

pip install flask

python -m main

Then open http://localhost:5000 in your browser.

## Project Structure

honeypot-dashboard/
├── honeypot/
│   ├── ssh_trap.py       
│   ├── http_trap.py      
│   └── ftp_trap.py       
├── core/
│   ├── database.py       
│   └── detector.py       
├── dashboard/
│   ├── app.py            
│   └── templates/        
├── logs/
│   └── attacks.db        
└── main.py               

## Threat Levels

| Level | What it means |
|---|---|
| LOW | Single probe — probably a scanner |
| MEDIUM | 2-4 attempts — someone is interested |
| HIGH | 5-9 attempts — getting aggressive |
| CRITICAL | 10+ attempts in 60 seconds — brute force |

## What I learned

Honestly the biggest thing was realizing how fast brute force attacks happen.
I expected maybe one attempt every few seconds. Nope — automated tools 
hammer hundreds of attempts per minute.

Also figured out why threading matters. Without it the whole server would 
freeze waiting for one connection while others pile up.

Understanding sockets at this level made HTTP, SSH and FTP way less 
mysterious. It's all just bytes going back and forth.

## Known Issues

- Runs locally only for now, haven't deployed it yet
- FTP trap occasionally misses very fast connections
- Dashboard gets a bit slow if logs cross 1000 entries

## TODO

- [ ] GeoIP lookup to show where attacks are coming from on a map
- [ ] Email alert when a CRITICAL threat is detected
- [ ] Deploy on a cloud VM so real internet traffic hits it

## Disclaimer

This is for learning purposes only. I tested everything on my own machine.
Don't run this on networks you don't own or have permission to monitor.

## Author

Raman Thapa — BCA 3rd Year  
github.com/Ramanthapa
