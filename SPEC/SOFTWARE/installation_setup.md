# Installation & Setup Guide

## AI-Based Queue Monitoring System

---

## Prerequisites

### Hardware Options

**Option A: Laptop/Desktop (Recommended for beginners)**
- Any laptop/desktop with webcam
- Windows 10/11, Linux (Ubuntu 20.04+), or macOS
- 8GB RAM minimum
- 10GB free disk space

**Option B: Raspberry Pi 4**
- Raspberry Pi 4 Model B (4GB or 8GB)
- 32GB SD Card (Class 10 or U3)
- Raspberry Pi Camera Module 3 OR USB webcam
- 5V/3A Power Supply
- Optional: Heatsink, case

---

## Step 1: Install Python

### Windows

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### macOS

```bash
# Install using Homebrew
brew install python3
python3 --version
```

### Raspberry Pi OS

Python 3 is pre-installed. Verify:
```bash
python3 --version
```

---

## Step 2: Create Project Directory

```bash
# Navigate to your workspace
cd "E:/6sem/ai workshop/AI_Queue_Management_Spec/AI-Based Queue Monitoring System/SPEC"

# Create virtual environment
python -m venv queue_env

# Activate virtual environment
# Windows:
queue_env\Scripts\activate

# Linux/macOS:
source queue_env/bin/activate

# Raspberry Pi:
source queue_env/bin/activate
```

---

## Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r queue_monitor/requirements.txt
```

**Note:** If installing on Raspberry Pi, the YOLO inference will be slower but will work.

---

## Step 4: Download YOLOv8 Model

The model will download automatically on first run, or you can download it manually:

```bash
# Create models directory
mkdir -p queue_monitor/models

# Download YOLOv8 nano model (~6MB)
# The model file (yolov8n.pt) will be downloaded by ultralytics on first run
```

To download manually:
1. Visit [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
2. Download `yolov8n.pt` from releases
3. Place in `queue_monitor/models/` folder

---

## Step 5: Configure the System

Edit `queue_monitor/config.yaml`:

```yaml
camera:
  source: 0                    # 0 = default webcam
  width: 1280
  height: 720
  fps: 30

detection:
  model_path: "yolov8n.pt"
  confidence: 0.5
  classes:
    - 0                       # 0 = person in COCO dataset

queue:
  roi_points:                  # Define your queue region
    - [200, 150]
    - [1080, 150]
    - [1080, 570]
    - [200, 570]
  max_threshold: 10           # Alert when queue exceeds this
  min_threshold: 3
  history_size: 100
  avg_service_time: 120       # Seconds per customer

alerts:
  led_enabled: true            # Set false if no GPIO
  buzzer_enabled: true
  alert_duration: 2

server:
  host: "0.0.0.0"
  port: 5000
  debug: false

recommendations:
  staff_per_5_people: 1
  max_queue_per_staff: 5
  current_staff: 2
```

**Camera Source Options:**
- `0` - Default webcam
- `1` - Second webcam
- `/path/to/video.mp4` - Video file for testing

---

## Step 6: Test Camera Connection

```bash
# Activate environment
# Windows:
queue_env\Scripts\activate
# Linux/macOS:
source queue_env/bin/activate

# Test camera with Python
python
```

```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    print(f"Camera works! Frame shape: {frame.shape}")
else:
    print("Camera not detected")
cap.release()
```

---

## Step 7: Run the System

```bash
# From project root
cd queue_monitor
python run.py
```

**With custom config:**
```bash
python run.py --config path/to/config.yaml
```

**Disable alerts (for testing without GPIO):**
```bash
python run.py --no-alerts
```

---

## Step 8: Access Dashboard

1. Open web browser
2. Go to: `http://localhost:5000`
3. View real-time queue statistics

**For network access:**
- Find your computer's IP:
  - Windows: `ipconfig`
  - Linux: `hostname -I`
  - macOS: `ifconfig`
- Access from other devices: `http://<IP>:5000`

---

## Raspberry Pi Specific Setup

### Enable Camera Interface

```bash
sudo raspi-config
```

Navigate to:
- Interface Options → Camera → Enable
- Reboot: `sudo reboot`

### Install GPIO Libraries

```bash
sudo apt install python3-rpi.gpio
```

### Mount Camera

```
1. Locate CSI port between HDMI and 3.5mm jack
2. Pull up plastic clip
3. Insert ribbon cable (metal contacts toward HDMI)
4. Push clip down to secure
```

### Test Camera on Raspberry Pi

```bash
raspistill -o test.jpg
```

If image captured, camera is working.

---

## Troubleshooting Installation

### Common Issues

**1. OpenCV import error on Windows**
```bash
pip uninstall opencv-python
pip install opencv-python --no-cache-dir
```

**2. YOLO model download fails**
```bash
# Download manually
wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt
mv yolov8n.pt queue_monitor/models/
```

**3. Camera not found**
- Check if camera is connected
- Try different camera index (0, 1, 2)
- On Linux: `ls /dev/video*`

**4. Port 5000 already in use**
```yaml
# Change port in config.yaml
server:
  port: 5001
```

**5. Permission denied (Linux)**
```bash
# Add user to video group
sudo usermod -a -G video $USER
# Log out and log back in
```

---

## Running on Boot (Optional)

### Systemd Service (Linux/Raspberry Pi)

Create `/etc/systemd/system/queue-monitor.service`:

```ini
[Unit]
Description=AI Queue Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/AI-Queue-Monitoring-System/SPEC/SOFTWARE/queue_monitor
ExecStart=/home/pi/AI-Queue-Monitoring-System/SPEC/SOFTWARE/queue_env/bin/python run.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable queue-monitor
sudo systemctl start queue-monitor
```

---

## Quick Reference Commands

```bash
# Activate environment
source queue_env/bin/activate  # Linux/macOS
queue_env\Scripts\activate     # Windows

# Run system
python run.py

# Run with debug
python run.py --debug

# Stop system
# Ctrl+C in terminal, or:
pkill -f "python run.py"

# Check status
curl http://localhost:5000/api/health
```

---

## Next Steps

After installation:
1. Configure ROI points for your camera setup
2. Adjust thresholds based on expected queue size
3. Test detection accuracy
4. Mount camera at optimal position
5. Access dashboard from multiple devices
