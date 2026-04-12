# AI-Based Queue Monitoring System

Real-time queue monitoring using AI (YOLOv8), OpenCV, and Flask.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)

---

## Features

- Real-time person detection using YOLOv8
- Queue counting with configurable ROI
- LED/Buzzer alerts for queue thresholds
- Web dashboard with live stats
- Staffing recommendations
- Wait time estimation

---

## Quick Start

### Prerequisites
- Python 3.8+
- Webcam or Raspberry Pi Camera

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-Queue-Monitoring-System.git
cd AI-Queue-Monitoring-System/SPEC/SOFTWARE

# Create virtual environment
python -m venv queue_env
source queue_env/bin/activate  # Linux/Mac
queue_env\Scripts\activate     # Windows

# Install dependencies
pip install -r queue_monitor/requirements.txt

# Run the system
cd queue_monitor
python run.py
```

### Access Dashboard
Open browser: `http://localhost:5000`

---

## Hardware Options

| Option | Cost (INR) | Components |
|--------|------------|------------|
| Minimum | ₹2,150 | USB webcam + Laptop/PC |
| Recommended | ₹11,650 | Raspberry Pi 4 + Camera Module 3 |

---

## Project Structure

```
SPEC/
├── HARDWARE/           # Hardware documentation
├── SOFTWARE/           # Source code and implementation
│   └── queue_monitor/ # Python application
└── WORKING/           # System working and execution guides
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats` | GET | Current queue statistics |
| `/api/frame` | GET | Live video frame |
| `/api/health` | GET | System health status |
| `/api/reset` | POST | Reset statistics |

---

## Configuration

Edit `queue_monitor/config.yaml` to customize:
- Camera source and resolution
- Detection confidence threshold
- Queue ROI points
- Alert thresholds
- Server port

---

## Tech Stack

- **Detection:** YOLOv8 (Ultralytics)
- **Image Processing:** OpenCV
- **Web Server:** Flask
- **Hardware:** Raspberry Pi 4 / Laptop/PC

---

## License

This project is for educational purposes.

---

## Author

Your Name - Final Year Project
