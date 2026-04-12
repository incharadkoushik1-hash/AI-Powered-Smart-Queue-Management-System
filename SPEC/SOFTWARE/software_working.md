# Software Working Explanation

## AI-Based Queue Monitoring System

---

## System Overview

The software pipeline processes video frames through AI detection to count people in a queue region and provide real-time statistics and alerts.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SOFTWARE PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐              │
│   │   CAMERA    │────►│  DETECTION  │────►│   ANALYSIS  │              │
│   │   HANDLER   │     │   (YOLOv8)   │     │    (ROI)     │              │
│   └─────────────┘     └─────────────┘     └──────┬──────┘              │
│                                                   │                     │
│                                                   ▼                     │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐              │
│   │  DASHBOARD  │◄────│    API      │◄────│   ALERTS    │              │
│   │  (Browser)  │     │   SERVER    │     │  (LED/BUZZ) │              │
│   └─────────────┘     └─────────────┘     └─────────────┘              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Working

### Step 1: Video Capture

**File:** `camera_handler.py`

```python
camera = CameraHandler(config)
camera.open()

while running:
    frame = camera.read()  # Gets numpy array (H, W, 3)
```

**What happens:**
- Opens video capture device (webcam/camera)
- Reads frames at configured FPS (default 30)
- Returns BGR numpy array for OpenCV processing

**Frame format:**
```
Shape: (720, 1280, 3)  # Height, Width, Channels
Dtype: uint8 (0-255)
Color: BGR (Blue, Green, Red)
```

---

### Step 2: Person Detection

**File:** `detector.py`

```python
detector = PersonDetector(config)
detector.load_model()  # Loads YOLOv8

boxes = detector.detect(frame)
```

**What happens:**
1. Preprocess frame: Resize to 640×640, normalize pixels
2. Run YOLOv8 inference on neural network
3. Post-process: Filter by confidence, extract bounding boxes
4. Return list of person detections

**YOLOv8 Processing:**
```
Input Frame          Neural Network          Output
(1280×720)     ───►  [Conv Layers]    ───►  [person boxes]
                   [Attention]              
                   [NMS]
```

**Detection Result:**
```python
class BoundingBox:
    x1, y1 = top-left corner
    x2, y2 = bottom-right corner
    center = ( (x1+x2)/2, (y1+y2)/2 )
    confidence = 0.0-1.0
    cls = 0 (person in COCO)
```

---

### Step 3: Queue Analysis

**File:** `queue_analyzer.py`

```python
analyzer = QueueAnalyzer(config)
count = analyzer.count_in_roi(boxes)
stats = analyzer.calculate_stats()
```

**ROI (Region of Interest):**
```
         ┌────────────────────┐
         │    CAMERA VIEW    │
         │                    │
         │   ┌────────────┐  │
         │   │   ROI      │  │
         │   │ (Queue     │  │
         │   │  Region)   │  │
         │   │            │  │
         │   │  [P] [P]   │  │  ← People inside ROI
         │   │     [P]    │  │
         │   └────────────┘  │
         │                    │
         └────────────────────┘
```

**Counting Logic:**
```python
for box in detected_boxes:
    if is_point_in_polygon(box.center, roi_points):
        count += 1
```

**Statistics Calculated:**
- `current_count`: People currently in queue
- `wait_time_minutes`: Estimated wait based on count
- `status`: CRITICAL/HIGH/NORMAL/LOW
- `trend`: INCREASING/DECREASING/STABLE

---

### Step 4: Alert Management

**File:** `alert_manager.py`

```python
alert_manager = AlertManager(config)

if status == 'CRITICAL':
    alert_manager.alert_queue_critical()
elif status == 'HIGH':
    alert_manager.alert_queue_high()
else:
    alert_manager.alert_queue_normal()
```

**Alert Actions:**
| Status | Green LED | Red LED | Buzzer |
|--------|-----------|---------|--------|
| LOW | ON | OFF | Silent |
| NORMAL | ON | OFF | Silent |
| HIGH | OFF | ON | Short beeps |
| CRITICAL | OFF | ON | Long beeps |

---

### Step 5: Dashboard Server

**File:** `dashboard_server.py`

```python
@app.route('/api/stats')
def get_stats():
    return jsonify(stats)

@app.route('/api/frame')
def get_frame():
    return send_file(frame_bytes, mimetype='image/jpeg')
```

**API Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard HTML page |
| `/api/stats` | GET | Current queue statistics |
| `/api/stats/history` | GET | Historical count data |
| `/api/frame` | GET | Latest video frame (raw) |
| `/api/frame/annotated` | GET | Frame with detection boxes |
| `/api/health` | GET | System health status |
| `/api/reset` | POST | Reset statistics |

---

## Wait Time Calculation

```python
def calculate_wait_time(count, min_threshold=3, avg_service_time=120):
    if count <= min_threshold:
        return 0  # No wait
    
    extra_people = count - min_threshold
    wait_minutes = extra_people * (avg_service_time / 60) / min_threshold
    return wait_minutes
```

**Example:**
- Average service time: 2 minutes
- Min threshold: 3 people
- Current count: 8 people

```
Wait = (8 - 3) * (2 min) / 3 = 3.3 minutes
```

---

## Dashboard Display

**Frontend Flow:**
```
1. Browser loads index.html
2. JS polls /api/stats every 2 seconds
3. Updates DOM elements with new data
4. Refreshes video feed every 5 seconds
5. Displays real-time queue count and alerts
```

**Dashboard Elements:**
- Live video feed (with ROI overlay)
- Current queue count
- Peak count
- Average count
- Wait time estimate
- Queue status badge
- Trend indicator
- Staffing recommendation

---

## Data Flow Diagram

```
                    CAMERA
                       │
                       ▼
               ┌───────────────┐
               │  Frame (BGR)  │
               │  1280×720    │
               └───────┬───────┘
                       │
                       ▼
               ┌───────────────┐
               │  YOLOv8       │
               │  Detection    │
               │  (GPU/CPU)    │
               └───────┬───────┘
                       │
                       ▼
               ┌───────────────┐
               │  0-N Boxes    │
               │  with centers │
               └───────┬───────┘
                       │
                       ▼
               ┌───────────────┐
               │  ROI Check    │
               │  Is center in │
               │  polygon?     │
               └───────┬───────┘
                       │
              ┌────────┴────────┐
              │                 │
         [YES]              [NO]
              │                 │
              ▼                 ▼
       ┌──────────┐        (ignore)
       │ COUNT++  │
       └────┬─────┘
            │
            ▼
    ┌───────────────┐
    │  Calculate   │
    │  Stats        │
    │  & Alerts     │
    └───────┬───────┘
            │
    ┌───────┼───────┐
    │       │       │
    ▼       ▼       ▼
 ┌────┐ ┌────┐ ┌────────┐
 │GPIO│ │API │ │Display │
 │    │ │    │ │Frames │
 └────┘ └────┘ └────────┘
```

---

## Thread Safety

The system uses threading for parallel operations:

```python
# Main thread: Video processing
while running:
    frame = camera.read()
    boxes = detector.detect(frame)
    count = analyzer.count_in_roi(boxes)

# Server thread: HTTP requests  
# Runs Flask server on port 5000
# Responds to browser requests
```

**Shared Resources (protected by locks):**
- `global_frame`: Latest processed frame
- `global_stats`: Current statistics

---

## Performance Considerations

| Operation | Time (RPi 4) | Time (Laptop) |
|-----------|-------------|---------------|
| Frame capture | 5ms | 3ms |
| YOLOv8 inference | 50-100ms | 10-20ms |
| ROI analysis | 1ms | <1ms |
| Dashboard update | <1ms | <1ms |
| **Total per frame** | **60ms** | **25ms** |

**FPS achievable:**
- Raspberry Pi 4: ~15 FPS
- Laptop/Desktop: ~30+ FPS

---

## Error Handling

```python
try:
    frame = camera.read()
    if frame is None:
        logger.warning("Frame read failed")
        continue
        
    boxes = detector.detect(frame)
    
except Exception as e:
    logger.error(f"Processing error: {e}")
    alert_manager.system_error()
```

**Graceful Degradation:**
- Camera disconnected → retry with delay
- Model load failure → exit with error
- Detection error → skip frame, continue
- Network error → show last known state
