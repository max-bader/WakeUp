// WakeUp Alarm App JavaScript
class WakeUpApp {
    constructor() {
        this.alarmStatus = null;
        this.statusCheckInterval = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.startStatusCheck();
        this.loadCurrentStatus();
    }

    bindEvents() {
        // Set alarm button
        document.getElementById('set-alarm-btn').addEventListener('click', () => {
            this.setAlarm();
        });

        // Stop alarm button
        document.getElementById('stop-alarm-btn').addEventListener('click', () => {
            this.stopAlarm();
        });

        // Snooze alarm button
        document.getElementById('snooze-alarm-btn').addEventListener('click', () => {
            this.snoozeAlarm();
        });

        // Get adaptive time button
        document.getElementById('get-adaptive-btn').addEventListener('click', () => {
            this.getAdaptiveTime();
        });

        // Enter key on time input
        document.getElementById('alarm-time').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.setAlarm();
            }
        });
    }

    async setAlarm() {
        const alarmTime = document.getElementById('alarm-time').value;
        const button = document.getElementById('set-alarm-btn');
        
        if (!alarmTime) {
            this.showMessage('Please select a time for your alarm', 'error');
            return;
        }

        button.innerHTML = '<div class="loading"></div> Setting...';
        button.disabled = true;

        try {
            const response = await fetch('/api/set_alarm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ alarm_time: alarmTime })
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage(`Alarm set for ${alarmTime}`, 'success');
                this.updateAlarmStatus(true, alarmTime);
            } else {
                this.showMessage('Failed to set alarm', 'error');
            }
        } catch (error) {
            console.error('Error setting alarm:', error);
            this.showMessage('Error setting alarm', 'error');
        } finally {
            button.innerHTML = '<i class="fas fa-play"></i> Set Alarm';
            button.disabled = false;
        }
    }

    async stopAlarm() {
        const button = document.getElementById('stop-alarm-btn');
        button.innerHTML = '<div class="loading"></div> Stopping...';
        button.disabled = true;

        try {
            const response = await fetch('/api/stop_alarm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage('Alarm stopped successfully!', 'success');
                this.updateAlarmStatus(false);
            } else {
                this.showMessage('No active alarm to stop', 'error');
            }
        } catch (error) {
            console.error('Error stopping alarm:', error);
            this.showMessage('Error stopping alarm', 'error');
        } finally {
            button.innerHTML = '<i class="fas fa-stop"></i> Stop Alarm';
            button.disabled = false;
        }
    }

    async snoozeAlarm() {
        const button = document.getElementById('snooze-alarm-btn');
        button.innerHTML = '<div class="loading"></div> Snoozing...';
        button.disabled = true;

        try {
            const response = await fetch('/api/snooze_alarm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage(`Alarm snoozed! Next alarm at ${data.snooze_time}`, 'success');
            } else {
                this.showMessage('Failed to snooze alarm', 'error');
            }
        } catch (error) {
            console.error('Error snoozing alarm:', error);
            this.showMessage('Error snoozing alarm', 'error');
        } finally {
            button.innerHTML = '<i class="fas fa-bed"></i> Snooze (5 min)';
            button.disabled = false;
        }
    }

    async getAdaptiveTime() {
        const defaultTime = document.getElementById('alarm-time').value || '07:00';
        const button = document.getElementById('get-adaptive-btn');
        const display = document.getElementById('adaptive-time-display');
        
        button.innerHTML = '<div class="loading"></div> Thinking...';
        button.disabled = true;

        try {
            const response = await fetch('/api/get_adaptive_time', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ default_time: defaultTime })
            });

            const data = await response.json();

            if (data.adaptive_time) {
                display.textContent = `Smart suggestion: ${data.adaptive_time}`;
                display.style.display = 'block';
                
                // Auto-fill the time input with the adaptive time
                document.getElementById('alarm-time').value = data.adaptive_time;
                
                this.showMessage(`AI suggests ${data.adaptive_time} based on your sleep patterns`, 'success');
            }
        } catch (error) {
            console.error('Error getting adaptive time:', error);
            this.showMessage('Error getting smart suggestion', 'error');
        } finally {
            button.innerHTML = '<i class="fas fa-brain"></i> Get Smart Time';
            button.disabled = false;
        }
    }

    async loadCurrentStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            this.updateAlarmStatus(status.alarm_active, status.current_alarm_time);
        } catch (error) {
            console.error('Error loading status:', error);
        }
    }

    startStatusCheck() {
        // Check alarm status every 5 seconds
        this.statusCheckInterval = setInterval(async () => {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();
                
                if (JSON.stringify(status) !== JSON.stringify(this.alarmStatus)) {
                    this.alarmStatus = status;
                    this.updateAlarmStatus(status.alarm_active, status.current_alarm_time);
                }
            } catch (error) {
                console.error('Error checking status:', error);
            }
        }, 5000);
    }

    updateAlarmStatus(isActive, alarmTime = null) {
        const statusLight = document.getElementById('status-light');
        const statusText = document.getElementById('status-text');
        const alarmInfo = document.getElementById('alarm-info');
        const alarmActions = document.getElementById('alarm-actions');

        if (isActive) {
            statusLight.classList.add('active');
            statusText.textContent = 'Alarm Active';
            alarmInfo.textContent = `Alarm time: ${alarmTime || 'Unknown'}`;
            alarmActions.style.display = 'flex';
            
            // Add pulsing animation to the entire alarm panel
            document.querySelector('.alarm-panel').style.animation = 'pulse 2s infinite';
        } else {
            statusLight.classList.remove('active');
            statusText.textContent = alarmTime ? `Alarm Set for ${alarmTime}` : 'Alarm Not Set';
            alarmInfo.textContent = '';
            alarmActions.style.display = 'none';
            
            // Remove pulsing animation
            document.querySelector('.alarm-panel').style.animation = 'none';
        }
    }

    showMessage(text, type = 'success') {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());

        // Create new message
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;

        // Insert message at the top of the alarm panel
        const alarmPanel = document.querySelector('.alarm-panel');
        alarmPanel.insertBefore(message, alarmPanel.firstChild);

        // Auto-remove message after 5 seconds
        setTimeout(() => {
            message.remove();
        }, 5000);
    }

    // Cleanup when page unloads
    destroy() {
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.wakeUpApp = new WakeUpApp();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.wakeUpApp) {
        window.wakeUpApp.destroy();
    }
});

// Add some visual feedback for interactions
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn')) {
        e.target.style.transform = 'scale(0.95)';
        setTimeout(() => {
            e.target.style.transform = '';
        }, 150);
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Space bar to toggle alarm actions when alarm is active
    if (e.code === 'Space' && !e.target.matches('input, textarea')) {
        e.preventDefault();
        const alarmActions = document.getElementById('alarm-actions');
        if (alarmActions.style.display === 'flex') {
            const stopBtn = document.getElementById('stop-alarm-btn');
            if (stopBtn) {
                stopBtn.click();
            }
        }
    }
    
    // Escape key to snooze when alarm is active
    if (e.code === 'Escape' && !e.target.matches('input, textarea')) {
        e.preventDefault();
        const alarmActions = document.getElementById('alarm-actions');
        if (alarmActions.style.display === 'flex') {
            const snoozeBtn = document.getElementById('snooze-alarm-btn');
            if (snoozeBtn) {
                snoozeBtn.click();
            }
        }
    }
});
