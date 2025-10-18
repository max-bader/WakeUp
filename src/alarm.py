import schedule
import time
import threading
import os
import platform
from datetime import datetime, timedelta
from src.agent import QAgent
from src.data import load_data, save_entry


# load agent
AGENT = QAgent(actions=[-5, 0, +5])
try:
    AGENT.load()
except FileNotFoundError:
    pass

# Global state
current_alarm_time = None
alarm_active = False
snooze_count = 0
wake_up_time = None


def play_alarm_sound():
    """Play alarm sound based on the operating system"""
    system = platform.system()
    if system == "Darwin":  # macOS
        os.system("afplay /System/Library/Sounds/Glass.aiff")
    elif system == "Linux":
        os.system("paplay /usr/share/sounds/alsa/Front_Left.wav")
    elif system == "Windows":
        os.system("powershell -c (New-Object Media.SoundPlayer 'C:\\Windows\\Media\\chimes.wav').PlaySync()")


def ring():
    """
    This will be called when the alarm goes off.
    - Play a sound / print a notification
    - Prompt the user for wakeup details
    - Compute reward & update the agent
    - Save both new data entry and updated Q-table
    """
    global alarm_active, snooze_count, wake_up_time
    
    alarm_active = True
    wake_up_time = datetime.now()
    
    print("\n" + "="*50)
    print("🔔 ALARM IS RINGING! 🔔")
    print("="*50)
    
    # Play sound
    play_alarm_sound()
    
    print(f"Wake up time: {wake_up_time.strftime('%H:%M:%S')}")
    print("Alarm is active - use the web interface to stop it!")


def snooze_alarm():
    """Handle snooze functionality"""
    global snooze_count, current_alarm_time
    
    snooze_count += 1
    snooze_time = datetime.now() + timedelta(minutes=5)
    
    print(f"\n😴 Snoozed! Next alarm in 5 minutes at {snooze_time.strftime('%H:%M:%S')}")
    
    # Schedule next alarm
    schedule.clear()
    schedule.every().day.at(snooze_time.strftime("%H:%M")).do(ring)
    
    return snooze_time


def stop_alarm():
    """Stop the alarm and process wake-up data"""
    global alarm_active, snooze_count, wake_up_time, current_alarm_time
    
    if not alarm_active:
        return False
    
    alarm_active = False
    actual_wake_time = datetime.now()
    
    # Calculate reward based on wake-up behavior
    if wake_up_time:
        time_diff = (actual_wake_time - wake_up_time).total_seconds() / 60  # minutes
        
        # Reward calculation:
        # - Early wake-up (within 5 minutes): +10 points
        # - On time (5-15 minutes): +5 points  
        # - Late (15+ minutes): -5 points
        # - Each snooze: -2 points
        
        if time_diff <= 5:
            reward = 10
        elif time_diff <= 15:
            reward = 5
        else:
            reward = -5
            
        reward -= snooze_count * 2
        
        # Get yesterday's data for state
        df = load_data()
        if len(df) > 0:
            last_entry = df.iloc[-1]
            state = (last_entry['snoozes'], int(time_diff))
        else:
            state = (0, 0)
        
        # Learn from this experience
        action = 0  # Default action for now
        next_state = (snooze_count, int(time_diff))
        AGENT.learn(state, action, reward, next_state)
        
        # Save data
        entry = {
            'date': wake_up_time.date(),
            'alarm_time': current_alarm_time,
            'wakeup_time': actual_wake_time.time(),
            'snoozes': snooze_count
        }
        save_entry(entry)
        
        # Save agent
        AGENT.save()
        
        print(f"\n✅ Alarm stopped!")
        print(f"Wake-up time: {actual_wake_time.strftime('%H:%M:%S')}")
        print(f"Snoozes: {snooze_count}")
        print(f"Reward: {reward} points")
        
        # Reset for next day
        snooze_count = 0
        wake_up_time = None
        
        return True
    
    return False


def set_alarm(alarm_time_str: str):
    """
    Schedule the `ring` function to fire at alarm_time_str (e.g. "07:00").
    """
    global current_alarm_time
    current_alarm_time = alarm_time_str
    
    schedule.clear()
    schedule.every().day.at(alarm_time_str).do(ring)
    print(f"Alarm set for {alarm_time_str}")


def get_adaptive_alarm_time(default_alarm="07:00"):
    """
    Use the agent to determine the optimal alarm time based on past behavior.
    """
    df = load_data()
    
    if len(df) == 0:
        return default_alarm
    
    # Get recent data (last 7 days)
    recent_data = df.tail(7)
    
    # Calculate average snoozes and wake-up patterns
    avg_snoozes = recent_data['snoozes'].mean()
    avg_wakeup_delay = 0  # Could calculate this from alarm_time vs wakeup_time
    
    # Create state based on recent behavior
    state = (int(avg_snoozes), int(avg_wakeup_delay))
    
    # Get action from agent
    action = AGENT.choose_action(state)
    
    # Adjust alarm time
    alarm_time = datetime.strptime(default_alarm, "%H:%M")
    adjusted_time = alarm_time + timedelta(minutes=action)
    
    return adjusted_time.strftime("%H:%M")


def run_scheduler(default_alarm="07:00"):
    """
    Decide today's alarm via the agent, schedule it, then loop.
    """
    global current_alarm_time
    
    # Get adaptive alarm time
    alarm_time = get_adaptive_alarm_time(default_alarm)
    current_alarm_time = alarm_time
    
    # Set the alarm
    set_alarm(alarm_time)
    
    print(f"Adaptive alarm set for {alarm_time}")
    print("Scheduler running... Press Ctrl+C to stop")
    
    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")


def get_status():
    """Get current alarm status for the web interface"""
    return {
        'alarm_active': alarm_active,
        'current_alarm_time': current_alarm_time,
        'snooze_count': snooze_count,
        'wake_up_time': wake_up_time.strftime('%H:%M:%S') if wake_up_time else None
    }