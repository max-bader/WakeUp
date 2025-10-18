# WakeUp - Smart Alarm Clock

A self-tuning alarm clock that adjusts alarm time based on reinforcement learning. The app learns from your wake-up patterns and rewards early wake-ups with points while making alarms earlier if you tend to snooze too much.

## Features

- 🧠 **AI-Powered**: Uses Q-learning to adapt alarm times based on your behavior
- 🎯 **Point System**: Earn points for waking up early, lose points for excessive snoozing
- 📊 **Sleep Analytics**: Track your sleep patterns and progress over time
- 🔔 **Smart Alarms**: Automatically adjusts alarm times to help you wake up better
- 💻 **Modern Web UI**: Sleek, responsive interface that works on any device
- 🔊 **Cross-Platform**: Works on macOS, Linux, and Windows

## How It Works

1. **Set Your Alarm**: Choose your preferred wake-up time
2. **AI Suggestion**: Get smart recommendations based on your sleep patterns
3. **Wake Up Tracking**: The app tracks when you actually wake up vs. when the alarm goes off
4. **Adaptive Learning**: The AI learns from your behavior and adjusts future alarm times
5. **Point System**: 
   - Wake up within 5 minutes: +10 points
   - Wake up within 15 minutes: +5 points
   - Wake up late: -5 points
   - Each snooze: -2 points

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd WakeUp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python src/main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### Setting an Alarm

1. Open the web interface at `http://localhost:5000`
2. Set your desired alarm time using the time picker
3. Click "Set Alarm" or use the "Get Smart Time" button for AI recommendations
4. The alarm will be scheduled and you'll see the status update

### When the Alarm Goes Off

1. The alarm will ring at the scheduled time
2. You'll see alarm controls appear in the web interface
3. Click "Stop Alarm" when you're fully awake
4. Use "Snooze" if you need 5 more minutes (but this affects your points!)

### Viewing Your Progress

- **Dashboard**: See your total points, days tracked, and average snoozes
- **History**: View your recent wake-up patterns and scores
- **Analytics**: The AI learns from your patterns to suggest better alarm times

## File Structure

```
WakeUp/
├── src/
│   ├── main.py          # Flask web application
│   ├── alarm.py         # Alarm scheduling and Q-learning logic
│   ├── agent.py         # Q-learning agent implementation
│   └── data.py          # Data storage and management
├── templates/
│   └── index.html       # Main web interface
├── static/
│   ├── css/
│   │   └── style.css    # Modern styling
│   └── js/
│       └── app.js       # Interactive functionality
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technical Details

### Q-Learning Agent

The app uses a Q-learning reinforcement learning algorithm to optimize alarm times:

- **States**: Based on recent snooze patterns and wake-up delays
- **Actions**: Adjust alarm time by -5, 0, or +5 minutes
- **Rewards**: Based on wake-up punctuality and snooze behavior
- **Learning**: Continuously improves recommendations based on your behavior

### Data Storage

- Sleep data is stored in `sleep_data.csv`
- Q-learning model is saved in `qtable.pkl`
- All data persists between sessions

### Web Interface

- Built with Flask for the backend
- Modern CSS with gradient backgrounds and smooth animations
- Responsive design that works on desktop and mobile
- Real-time status updates via JavaScript

## Customization

### Adjusting the Point System

Edit the reward calculation in `src/alarm.py`:

```python
# Reward calculation:
# - Early wake-up (within 5 minutes): +10 points
# - On time (5-15 minutes): +5 points  
# - Late (15+ minutes): -5 points
# - Each snooze: -2 points
```

### Changing Alarm Sounds

Modify the `play_alarm_sound()` function in `src/alarm.py` to use different sounds or add custom audio files.

### Styling

Customize the appearance by editing `static/css/style.css`. The design uses CSS custom properties for easy color scheme changes.

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `src/main.py` (line 101)
2. **Alarm sound not working**: Check your system's audio settings
3. **Data not saving**: Ensure the app has write permissions in the directory

### Browser Compatibility

The web interface works best with modern browsers:
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the app!

## License

This project is open source and available under the MIT License.
