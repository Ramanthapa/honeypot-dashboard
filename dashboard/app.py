from flask import Flask, render_template, jsonify
from core.database import get_all_attacks, get_stats, init_db

app = Flask(__name__)

@app.route('/')
def index():
    init_db()
    stats = get_stats()
    recent_attacks = get_all_attacks()[:10]
    return render_template('index.html', stats=stats, attacks=recent_attacks)

@app.route('/logs')
def logs():
    all_attacks = get_all_attacks()
    return render_template('logs.html', attacks=all_attacks)

@app.route('/api/stats')
def api_stats():
    stats = get_stats()
    recent = get_all_attacks()[:5]
    return jsonify({
        'total': stats['total'],
        'by_type': stats['by_type'],
        'recent': [list(a) for a in recent]
    })

def start_dashboard():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    start_dashboard()