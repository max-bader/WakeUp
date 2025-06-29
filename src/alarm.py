import schedule
import time
from datetime import datetime
from src.agent import QAgent
from src.data import load_data, save_entry


# load agent
AGENT = QAgent(actions=[-5,0,+5])
try:
    AGENT.load()
except FileNotFoundError:
    pass


def ring():
    """
    This will be called when the alarm goes off.
    - Play a sound / print a notification
    - Prompt the user for wakeup details
    - Compute reward & update the agent
    - Save both new data entry and updated Q-table
    """
    # TODO


def set_alarm(alarm_time_str: str):
    """
    Schedule the `ring` function to fire at alarm_time_str (e.g. "07:00").
    """
    schedule.every().day.at(alarm_time_str).do(ring)


def run_scheduler(default_alarm="07:00"):
    """
    Decide today’s alarm via the agent, schedule it, then loop.
    """
    # 1) Load yesterday’s data & compute state
    # 2) action = AGENT.choose_action(state)
    # 3) alarm_time = adjust default_alarm by action
    # 4) set_alarm(alarm_time)
    # 5) while True: schedule.run_pending(); time.sleep(...)
    pass