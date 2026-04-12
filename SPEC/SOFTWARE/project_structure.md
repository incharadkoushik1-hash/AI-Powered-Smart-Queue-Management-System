# Software Project Structure

## AI-Based Queue Monitoring System

---

## Directory Structure

```
AI-Queue-Monitoring-System/
│
├── SOFTWARE/
│   │
│   ├── queue_monitor/
│   │   │   ├── __init__.py
│   │   │   ├── camera_handler.py      # Video capture module
│   │   │   ├── detector.py            # YOLOv8 detection
│   │   │   ├── queue_analyzer.py      # Queue counting & ROI
│   │   │   ├── alert_manager.py       # LED/Buzzer alerts
│   │   │   ├── recommender.py         # Staffing recommendations
│   │   │   └── dashboard_server.py    # Flask web server
│   │   │
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py            # Configuration loader
│   │   │
│   │   ├── models/                     # YOLO model storage
│   │   │   └── yolov8n.pt              # YOLOv8 nano model
│   │   │
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── dashboard.css       # Dashboard styling
│   │   │   │
│   │   │   └── js/
│   │   │       └── dashboard.js        # Frontend JavaScript
│   │   │
│   │   ├── templates/
│   │   │   └── index.html              # Dashboard HTML
│   │   │
│   │   ├── tests/
│   │   │   ├── test_camera.py
│   │   │   ├── test_detector.py
│   │   │   └── test_analyzer.py
│   │   │
│   │   ├── config.yaml                 # Main configuration
│   │   ├── requirements.txt            # Python dependencies
│   │   ├── run.py                      # Main entry point
│   │   └── README.md
│   │
│   └── (Documentation files)
│       ├── project_structure.md
│       ├── software_working.md
│       ├── api_documentation.md
│       └── installation_setup.md
│
├── HARDWARE/
│   ├── components_list.md
│   ├── circuit_connections.md
│   ├── circuit_diagram.md
│   ├── hardware_working.md
│   └── hardware_requirements.md
│
└── WORKING/
    ├── system_working.md
    ├── execution_guide.md
    └── limitations_and_future_scope.md
```

---

## File Descriptions

### Core Modules

| File | Purpose |
|------|---------|
| `camera_handler.py` | Handles video capture from webcam/Raspberry Pi camera |
| `detector.py` | Runs YOLOv8 inference for person detection |
| `queue_analyzer.py` | Defines ROI, counts people, calculates statistics |
| `alert_manager.py` | Controls GPIO pins for LED and buzzer alerts |
| `recommender.py` | Provides staffing recommendations based on queue data |
| `dashboard_server.py` | Flask server for web dashboard API |

### Configuration

| File | Purpose |
|------|---------|
| `config.yaml` | All system parameters (thresholds, camera settings, etc.) |
| `settings.py` | Python configuration loader and validator |

### Frontend

| File | Purpose |
|------|---------|
| `index.html` | Main dashboard page |
| `dashboard.css` | Styling for dashboard |
| `dashboard.js` | JavaScript for API polling and updates |

### Entry Points

| File | Purpose |
|------|---------|
| `run.py` | Main application entry point |
| `requirements.txt` | Python package dependencies |

---

## Data Flow Between Modules

```
┌──────────────┐
│   run.py     │  Main entry point
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   camera_    │────►│   detector    │
│   handler.py │     │   .py         │
└──────────────┘     └───────┬──────┘
                             │
                             ▼
                      ┌──────────────┐
                      │   queue_     │
                      │  analyzer.py │
                      └───────┬──────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │   alert_   │ │dashboard_ │ │ recommender│
       │  manager.py│ │ server.py  │ │    .py     │
       └────────────┘ └─────┬──────┘ └────────────┘
                            │
                            ▼
                     ┌────────────┐
                     │  Browser   │
                     │ Dashboard  │
                     └────────────┘
```

---

## Class/Function Overview

### camera_handler.py
```python
class CameraHandler:
    - __init__(config)
    - open() -> bool
    - read() -> frame
    - release()
    - isOpened() -> bool
```

### detector.py
```python
class PersonDetector:
    - __init__(model_path)
    - load_model()
    - detect(frame) -> List[BoundingBox]
    - draw_boxes(frame, boxes) -> frame
```

### queue_analyzer.py
```python
class QueueAnalyzer:
    - __init__(config, detector)
    - set_roi(points)
    - count_in_roi(boxes) -> int
    - calculate_stats() -> dict
    - get_trend() -> str
```

### alert_manager.py
```python
class AlertManager:
    - __init__(config)
    - set_led(color, state)
    - beep(duration)
    - alert_queue_high()
    - alert_queue_normal()
```

### recommender.py
```python
class StaffingRecommender:
    - __init__(config)
    - get_recommendation(queue_count) -> dict
    - calculate_optimal_staff(current_count, queue_count)
```

### dashboard_server.py
```python
app = Flask(__name__)

@app.route('/api/stats')
def get_stats():
    return jsonify(stats)

@app.route('/api/frame')
def get_frame():
    return send_file(frame_bytes, mimetype='image/jpeg')
```

---

## Configuration Structure (config.yaml)

```yaml
camera:
  source: 0                    # Camera index or video file path
  width: 1280
  height: 720
  fps: 30

detection:
  model_path: "models/yolov8n.pt"
  confidence: 0.5
  classes: [0]                  # Class 0 = person in COCO

queue:
  roi_points: [[100, 100], [500, 100], [500, 400], [100, 400]]
  max_threshold: 10
  min_threshold: 3
  history_size: 100

alerts:
  led_enabled: true
  buzzer_enabled: true
  alert_duration: 2

server:
  host: "0.0.0.0"
  port: 5000
  debug: false

recommendations:
  staff_per_5_people: 1
  max_queue_per_staff: 5
```

---

## Dependencies (requirements.txt)

```
opencv-python>=4.5.0
ultralytics>=8.0.0
flask>=2.0.0
numpy>=1.20.0
pyyaml>=5.4.0
pillow>=8.0.0
raspberry-gpio (optional, for Raspberry Pi)
```
