# Execution Guide

## AI-Based Queue Monitoring System

---

## Quick Start

### Prerequisites
- Python 3.8+ installed
- Webcam or camera connected
- Internet connection (for first-time model download)

### Run in 5 Steps

```bash
# 1. Navigate to project
cd "E:/6sem/ai workshop/AI_Queue_Management_Spec/AI-Based Queue Monitoring System/SPEC/SOFTWARE"

# 2. Create virtual environment
python -m venv queue_env

# 3. Activate environment
queue_env\Scripts\activate  # Windows
source queue_env/bin/activate  # Linux/Mac

# 4. Install dependencies
pip install -r queue_monitor/requirements.txt

# 5. Run the system
cd queue_monitor
python run.py
```

**Access Dashboard:** Open browser → `http://localhost:5000`

---

## Detailed Execution Steps

### Step 1: Environment Setup

**Windows:**
```cmd
cd "E:\6sem\ai workshop\AI_Queue_Management_Spec\AI-Based Queue Monitoring System\SPEC\SOFTWARE"

python -m venv queue_env

queue_env\Scripts\activate
```

**Linux/Mac:**
```bash
cd "E:/6sem/ai workshop/AI_Queue_Management_Spec/AI-Based Queue Monitoring System/SPEC/SOFTWARE"

python3 -m venv queue_env
source queue_env/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r queue_monitor/requirements.txt
```

**Expected output:**
```
Installing collected packages: opencv-python, ultralytics, flask, etc.
Successfully installed opencv-python-4.x.x
Successfully installed ultralytics-8.x.x
...
```

### Step 3: Download YOLO Model (First Run Only)

The model downloads automatically on first run:
```
Downloading yolov8n.pt...
100%|██████████| 6.3MB/6.3MB
```

If download fails, manually download from:
https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt

### Step 4: Configure System

Edit `queue_monitor/config.yaml`:

**For webcam (default):**
```yaml
camera:
  source: 0
```

**For video file testing:**
```yaml
camera:
  source: "path/to/test_video.mp4"
```

**Adjust ROI for your camera view:**
```yaml
queue:
  roi_points:
    - [100, 100]    # Top-left
    - [600, 100]    # Top-right
    - [600, 400]    # Bottom-right
    - [100, 400]    # Bottom-left
```

### Step 5: Run the System

```bash
cd queue_monitor
python run.py
```

**Expected startup output:**
```
INFO:ai_queue:==================================================
INFO:ai_queue:AI Queue Monitoring System
INFO:ai_queue:==================================================
INFO:ai_queue:Initializing camera...
INFO:ai_queue:Camera opened: 1280x720 @ 30fps
INFO:ai_queue:Loading YOLOv8 model...
INFO:ai_queue:YOLO model loaded successfully
INFO:ai_queue:Initializing queue analyzer...
INFO:ai_queue:Initializing alert manager...
INFO:ai_queue:Starting dashboard server...
INFO:ai_queue:Dashboard available at http://localhost:5000
INFO:ai_queue:Starting main processing loop...
```

---

## Running Options

### Option 1: Default (With Alerts)

```bash
python run.py
```

### Option 2: Disable Hardware Alerts

Use this when running on laptop without GPIO:
```bash
python run.py --no-alerts
```

### Option 3: Custom Configuration

```bash
python run.py --config custom_config.yaml
```

### Option 4: Debug Mode

```bash
cd queue_monitor
export FLASK_DEBUG=1
python run.py
```

---

## Verifying System is Working

### Check 1: Terminal Output

Look for continuous processing messages:
```
INFO:ai_queue:Processed 100 frames - Current queue: 5
INFO:ai_queue:Processed 200 frames - Current queue: 7
```

### Check 2: Dashboard Access

1. Open browser
2. Go to `http://localhost:5000`
3. You should see:
   - Live video feed
   - Queue count updating
   - Status badge (NORMAL/HIGH/CRITICAL)

### Check 3: API Response

```bash
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{"status": "healthy", "camera_connected": true, "timestamp": "..."}
```

### Check 4: Statistics API

```bash
curl http://localhost:5000/api/stats
```

**Expected response:**
```json
{
    "current_count": 5,
    "peak_count": 12,
    "status": "NORMAL",
    ...
}
```

---

## Debug Steps If Not Working

### Problem: "Camera not detected"

**Solutions:**
1. Check camera is connected and not used by another app
2. Try different camera index:
   ```yaml
   camera:
     source: 1  # Try 0, 1, 2
   ```
3. On Linux, check permissions:
   ```bash
   ls -la /dev/video*
   sudo chmod 666 /dev/video0
   ```

### Problem: "YOLO model failed to load"

**Solutions:**
1. Manually download model:
   ```bash
   wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt
   mv yolov8n.pt queue_monitor/models/
   ```
2. Update model path in config.yaml:
   ```yaml
   detection:
     model_path: "yolov8n.pt"
   ```

### Problem: "Port 5000 already in use"

**Solutions:**
1. Find and kill the process:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <process_id> /F
   
   # Linux
   lsof -i :5000
   kill <process_id>
   ```
2. Or change port in config.yaml:
   ```yaml
   server:
     port: 5001
   ```

### Problem: "Module not found"

**Solutions:**
```bash
pip install -r queue_monitor/requirements.txt
```

### Problem: Green LED not working (Raspberry Pi)

**Solutions:**
1. Run in simulation mode:
   ```bash
   python run.py --no-alerts
   ```
2. Check GPIO wiring (see circuit_connections.md)
3. Test GPIO manually:
   ```python
   import RPi.GPIO as GPIO
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(17, GPIO.OUT)
   GPIO.output(17, GPIO.HIGH)
   ```

### Problem: Detection not accurate

**Solutions:**
1. Adjust confidence threshold:
   ```yaml
   detection:
     confidence: 0.6  # Increase to reduce false positives
   ```
2. Adjust ROI to exclude non-queue areas
3. Improve lighting
4. Position camera at better angle

---

## Running on Raspberry Pi

### Full Steps:

```bash
# 1. SSH into Raspberry Pi
ssh pi@192.168.1.100

# 2. Navigate to project
cd ~/AI-Queue-Monitoring-System/SPEC/SOFTWARE

# 3. Create and activate environment
python3 -m venv queue_env
source queue_env/bin/activate

# 4. Install dependencies
pip install -r queue_monitor/requirements.txt

# 5. Enable camera (if using CSI camera)
sudo raspi-config
# Interface Options → Camera → Enable → Reboot

# 6. Run
cd queue_monitor
python run.py
```

### Check GPIO (Raspberry Pi):
```bash
python3 -c "import RPi.GPIO as GPIO; print('GPIO OK')"
```

---

## Stopping the System

**Graceful shutdown:**
```
Press: Ctrl+C
```

**Force kill (if needed):**
```bash
# Windows
taskkill /F /IM python.exe

# Linux
pkill -f "python run.py"
```

---

## Testing Without Real Camera

Use a video file:
```yaml
camera:
  source: "test_data/sample_queue.mp4"
```

Or use OpenCV's test pattern:
```python
# Modify camera_handler.py to return test frame:
import numpy as np
frame = np.zeros((720, 1280, 3), dtype=np.uint8)
cv2.putText(frame, "Test Frame", (500, 360), ...)
return frame
```

---

## System Startup Checklist

```
Before running, verify:
[ ] Python 3.8+ installed
[ ] Virtual environment created and activated
[ ] Dependencies installed (pip list)
[ ] Webcam/camera connected and working
[ ] YOLO model downloaded
[ ] config.yaml edited for your setup
[ ] No other process using port 5000
```

---

## Expected Performance

| Metric | Laptop | Raspberry Pi 4 |
|--------|--------|----------------|
| FPS | 25-30 | 10-15 |
| Detection latency | 20ms | 80ms |
| Memory usage | 500MB | 300MB |
| CPU usage | 30-50% | 70-90% |

---

## Next Steps After Successful Run

1. **Adjust ROI** - Define exact queue area in config.yaml
2. **Set thresholds** - Adjust based on expected queue size
3. **Configure alerts** - Set LED/buzzer thresholds
4. **Network access** - Access dashboard from other devices
5. **Test with real queue** - Validate in actual environment
