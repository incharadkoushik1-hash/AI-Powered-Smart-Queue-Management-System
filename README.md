# AI-Powered Smart Queue Management System

Real-time queue monitoring system using AI (YOLOv8), OpenCV, and Flask for retail and service environments.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)

---

## Overview

This system uses computer vision and AI to:
- Detect and count people in queues
- Estimate customer wait times
- Provide real-time alerts
- Generate staffing recommendations

---

## Features

- Real-time person detection using YOLOv8
- Configurable Region of Interest (ROI)
- LED/Buzzer alerts for queue thresholds
- Web dashboard with live statistics
- Staffing recommendations
- Wait time estimation
- Trend analysis

---

## Quick Start

### Prerequisites
- Python 3.8+
- Webcam or Raspberry Pi Camera Module 3

### Installation

```bash
# Navigate to SOFTWARE folder
cd SPEC/SOFTWARE

# Create virtual environment
python -m venv queue_env

# Activate environment
queue_env\Scripts\activate      # Windows
source queue_env/bin/activate   # Linux/Mac

# Install dependencies
pip install -r queue_monitor/requirements.txt

# Run the system
cd queue_monitor
python run.py
```

### Access Dashboard
Open browser: `http://localhost:5000`

---

## Project Structure

```
AI-Based Queue Monitoring System/
├── HARDWARE/              # Hardware documentation
│   ├── components_list.md
│   ├── circuit_connections.md
│   ├── circuit_diagram.md
│   ├── hardware_working.md
│   └── hardware_requirements.md
│
├── SOFTWARE/              # Source code
│   └── queue_monitor/
│       ├── camera_handler.py    # Video capture
│       ├── detector.py          # YOLOv8 detection
│       ├── queue_analyzer.py    # ROI & counting
│       ├── alert_manager.py     # LED/Buzzer alerts
│       ├── recommender.py       # Staffing suggestions
│       ├── dashboard_server.py  # Flask web server
│       ├── config.yaml          # Configuration
│       └── requirements.txt
│
└── WORKING/              # Documentation
    ├── system_working.md
    ├── execution_guide.md
    └── limitations_and_future_scope.md
```

---

## Hardware Requirements

| Option | Cost (INR) | Components |
|--------|------------|------------|
| Minimum | ₹2,150 | USB webcam + Laptop/PC |
| Recommended | ₹11,650 | Raspberry Pi 4 + Camera Module 3 |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats` | GET | Current queue statistics |
| `/api/stats/history` | GET | Historical count data |
| `/api/frame` | GET | Live video frame |
| `/api/frame/annotated` | GET | Frame with detection overlay |
| `/api/health` | GET | System health status |
| `/api/config` | GET | Current configuration |
| `/api/reset` | POST | Reset statistics |

---

## Configuration

Edit `SOFTWARE/queue_monitor/config.yaml`:

```yaml
camera:
  source: 0                    # Camera index
  width: 1280
  height: 720

detection:
  confidence: 0.5

queue:
  max_threshold: 10            # Alert threshold
  min_threshold: 3

server:
  port: 5000
```

---

## Tech Stack

- **Detection:** YOLOv8 (Ultralytics)
- **Image Processing:** OpenCV 4.5+
- **Web Server:** Flask 2.0+
- **Hardware:** Raspberry Pi 4 / Laptop/PC

---

## License

MIT License - See LICENSE file
