from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import time
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.alarm import (
    set_alarm, stop_alarm, snooze_alarm, get_status, 
    get_adaptive_alarm_time, run_scheduler
)
from src.data import load_data

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Global scheduler thread
scheduler_thread = None
scheduler_running = False


def start_scheduler():
    """Start the alarm scheduler in a separate thread"""
    global scheduler_thread, scheduler_running
    
    if not scheduler_running:
        scheduler_running = True
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()


@app.route('/')
def index():
    """Main dashboard page"""
    df = load_data()
    
    # Calculate stats
    total_days = len(df)
    avg_snoozes = df['snoozes'].mean() if total_days > 0 else 0
    recent_data = df.tail(7) if total_days > 0 else df
    
    # Calculate points (simplified)
    total_points = 0
    if total_days > 0:
        for _, row in df.iterrows():
            if row['snoozes'] == 0:
                total_points += 10
            elif row['snoozes'] <= 2:
                total_points += 5
            else:
                total_points -= 5
    
    return render_template('index.html', 
                         total_days=total_days,
                         avg_snoozes=round(avg_snoozes, 1),
                         total_points=total_points,
                         recent_data=recent_data.to_dict('records') if total_days > 0 else [])


@app.route('/api/status')
def api_status():
    """API endpoint to get current alarm status"""
    return jsonify(get_status())


@app.route('/api/set_alarm', methods=['POST'])
def api_set_alarm():
    """API endpoint to set alarm time"""
    data = request.get_json()
    alarm_time = data.get('alarm_time', '07:00')
    
    set_alarm(alarm_time)
    start_scheduler()
    
    return jsonify({'success': True, 'alarm_time': alarm_time})


@app.route('/api/stop_alarm', methods=['POST'])
def api_stop_alarm():
    """API endpoint to stop the alarm"""
    success = stop_alarm()
    return jsonify({'success': success})


@app.route('/api/snooze_alarm', methods=['POST'])
def api_snooze_alarm():
    """API endpoint to snooze the alarm"""
    snooze_time = snooze_alarm()
    return jsonify({'success': True, 'snooze_time': snooze_time.strftime('%H:%M:%S')})


@app.route('/api/get_adaptive_time', methods=['POST'])
def api_get_adaptive_time():
    """API endpoint to get adaptive alarm time"""
    data = request.get_json()
    default_time = data.get('default_time', '07:00')
    
    adaptive_time = get_adaptive_alarm_time(default_time)
    return jsonify({'adaptive_time': adaptive_time})


if __name__ == '__main__':
    print("Starting WakeUp Alarm App...")
    print("Open your browser to http://localhost:4000")
    app.run(debug=True, host='0.0.0.0', port=4000)
