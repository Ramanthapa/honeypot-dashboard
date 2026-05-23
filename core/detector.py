from collections import defaultdict
from datetime import datetime, timedelta

attempt_tracker = defaultdict(list)

def classify_threat(ip):
    now = datetime.now()
    attempt_tracker[ip].append(now)
    attempt_tracker[ip] = [t for t in attempt_tracker[ip] if now - t < timedelta(seconds=60)]
    count = len(attempt_tracker[ip])
    if count >= 10:
        return 'CRITICAL'
    elif count >= 5:
        return 'HIGH'
    elif count >= 2:
        return 'MEDIUM'
    else:
        return 'LOW'

def is_brute_force(ip):
    return len(attempt_tracker.get(ip, [])) >= 10