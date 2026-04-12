# Hardware Working Explanation

## AI-Based Queue Monitoring System

---

## Overview

This document explains how each hardware component works together to form the complete queue monitoring system. The explanation is designed for beginners with basic electronics knowledge.

---

## System Block Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CAMERA    │────►│  PROCESSOR  │────►│   ALERTS    │────►│  DASHBOARD  │
│  (Capture)  │     │   (AI)      │     │ (Visual/Audio)│   │   (Display) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Component-by-Component Explanation

### 1. Camera Module (Image Capture Device)

**What it is:**
- A digital camera that captures video frames continuously
- For Raspberry Pi: Camera Module 3 with 12MP sensor
- For Laptop/PC: USB webcam (720p or 1080p)

**How it works:**
```
Light from scene
       │
       ▼
┌──────────────┐
│    LENS      │  ← Focuses light onto sensor
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    CMOS      │  ← Converts light to electrical signals
│    SENSOR    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   ADC        │  ← Converts analog to digital
│ (Converter)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    OUTPUT     │  ← Digital image/video data
│   (CSI/USB)  │
└──────────────┘
```

**Role in system:**
- Captures 15-30 frames per second
- Sends frames to processor via CSI ribbon or USB
- Field of view should cover entire queue area

**Beginner note:** Think of it like your phone camera - it captures pictures and converts them into data the computer can understand.

---

### 2. Raspberry Pi 4 / Computer (Processing Unit)

**What it is:**
- The "brain" of the system
- Runs Python code for AI detection
- Processes video frames and makes decisions

**How it works:**
```
┌─────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI 4                           │
│                                                             │
│  ┌─────────────┐                                            │
│  │  ARM Cortex │    ← Performs calculations                 │
│  │  A72 CPU    │      like a mini computer                  │
│  │  (1.5GHz)   │                                            │
│  └──────┬──────┘                                            │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │   4GB DDR4   │    ← Temporary memory                     │
│  │    RAM       │      stores active data                   │
│  └──────┬──────┘                                            │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │  VideoCore  │    ← Handles camera input                  │
│  │    VI       │      and image processing                  │
│  └─────────────┘                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Role in system:**
- Receives video frames from camera
- Runs YOLOv8 AI model for person detection
- Counts people in defined queue region
- Calculates queue statistics
- Sends alerts when threshold exceeded
- Hosts Flask web server for dashboard

**Power consumption:** ~5V/3A (15W maximum)

---

### 3. LED Indicators (Visual Alerts)

**What it is:**
- Two small light-emitting diodes
- Green = System OK / Normal queue
- Red = Alert / Long queue detected

**How it works (Basic Electronics):**
```
    ┌──────────────────────────────────────┐
    │                                      │
    │   GPIO Pin (3.3V)                    │
    │        │                             │
    │        ├────────┐                    │
    │        │        │                    │
    │        │    ┌───▼───┐                │
    │        │    │ 220Ω  │ Resistor      │
    │        │    └───┬───┘ limits current │
    │        │        │                    │
    │        │    ┌───▼───┐                │
    │        │    │  LED   │  Light        │
    │        │    │   ◐    │  Emission    │
    │        │    └───┬───┘                │
    │        │        │                    │
    │        │        │                    │
    │        │    ┌───▼───┐                │
    │        └────►│  GND   │              │
    │             └───┬───┘                │
    │                 │                    │
    └─────────────────▼────────────────────┘
    
    Current flows: GPIO → Resistor → LED → GND
    LED lights up when GPIO is HIGH (3.3V)
```

**Role in system:**
- Provides immediate visual feedback
- No screen required to see system status
- Can be seen from distance in retail environment

**Ohm's Law:** V = I × R
- Voltage: 3.3V (from GPIO)
- Current needed for LED: ~15mA
- Resistor: (3.3V - 2V LED drop) / 0.015A = 87Ω ≈ 220Ω (standard value)

---

### 4. Buzzer (Audio Alert)

**What it is:**
- A small audio transducer
- Converts electrical signal to sound
- Used when queue exceeds maximum threshold

**Why transistor is needed:**
```
    GPIO Pin cannot provide enough current for buzzer
    
    GPIO Output: 3.3V @ ~20mA (max)
    Buzzer requires: 5V @ ~50mA (or more)
    
    SOLUTION: Use transistor as switch
    
    ┌─────────┐      ┌─────────────┐
    │   GPIO  │──────│  Transistor │──────► Buzzer ──► GND
    │  3.3V   │      │  (2N2222)   │        5V
    └─────────┘      │   acts as   │
                     │   switch    │
                     └─────────────┘
```

**Role in system:**
- Audio alert for staff attention
- Different beep patterns for different alerts
- Can alert staff in back office

---

### 5. Power Supply

**What it is:**
- Converts AC (220V) to DC (5V)
- Provides stable power to all components

**Power budget:**
```
Component           Current    Power (5V)
─────────────────────────────────────────
Raspberry Pi 4      2.5A       12.5W
Camera Module 3     0.25A      1.25W
Buzzer (peak)       0.05A      0.25W
LEDs (both)         0.03A      0.15W
─────────────────────────────────────────
Total (max)         2.83A      14.15W

Recommended: 5V/3A adapter = 15W (provides margin)
```

---

## Data Flow Through System

### Step 1: Image Capture
```
Real World Scene
       │
       │ Light reflects from people in queue
       │
       ▼
Camera Sensor (captures frame)
       │
       │ Digital image data (1920×1080 @ 30fps)
       │
       ▼
CSI/USB Interface
       │
       │ ~33MB/s data transfer
       │
       ▼
```

### Step 2: Processing
```
Frame received by CPU
       │
       │ Frame stored in RAM
       │
       ▼
Image Preprocessing
       │
       │ Resize to 640×640 (YOLO input)
       │ Normalize pixel values (0-1)
       │
       ▼
Neural Network (YOLOv8)
       │
       │ Forward pass through CNN layers
       │ ~3-5ms on Raspberry Pi 4
       │
       ▼
Detection Output
       │
       │ [class, confidence, bounding_box] for each person
       │
       ▼
```

### Step 3: Analysis
```
Detection Results
       │
       │ Filter by confidence (>0.5)
       │ Filter by class (person only)
       │
       ▼
ROI Check
       │
       │ Is person inside queue region?
       │ Check if center point is in polygon
       │
       ▼
Count Update
       │
       │ Increment/decrement counter
       │ Track entry/exit
       │
       ▼
```

### Step 4: Alert Decision
```
Queue Count
       │
       │ Compare with threshold
       │
       ▼
┌───────────────────────────────────────┐
│  count > MAX_THRESHOLD (10)?          │
│       │                                │
│       ├──YES──► RED LED ON + BUZZER   │
│       │                                │
│       └──NO───► GREEN LED ON          │
└───────────────────────────────────────┘
```

### Step 5: Dashboard Update
```
Current Stats
       │
       │ Create JSON response
       │ {
       │   "count": 8,
       │   "avg_wait_time": "12 minutes",
       │   "status": "NORMAL"
       │ }
       │
       ▼
Flask HTTP Server
       │
       │ Serve on local network
       │ http://localhost:5000/api/stats
       │
       ▼
Web Browser Display
       │
       │ Dashboard shows real-time data
       │ Auto-refresh every 2 seconds
       │
       ▼
```

---

## Timing Diagram

```
TIME ──►

Camera:     │▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│▓▓▓│
            ├────┴────┴────┴────┴────┴────┴────┴────┤
            │  30 FPS  = 1 frame every 33ms        │

Processing: │████│    │████│    │████│    │████│    │
            ├────┴────┴────┴────┴────┴────┴────┴────┤
            │  Processing takes ~30ms per frame    │

Detection:  │▓▓▓▓│    │▓▓▓▓│    │▓▓▓▓│    │▓▓▓▓│    │
            ├────┴────┴────┴────┴────┴────┴────┴────┤
            │  AI inference ~10-15ms               │

Dashboard:  │████│████│    │    │████│████│    │    │
            ├────┴────┴────┴────┴────┴────┴────┴────┤
            │  Updated every 2 seconds (browser)     │

LED:        │LOW │HIGH│HIGH│HIGH│HIGH│HIGH│LOW │LOW │
            ├────┴────┴────┴────┴────┴────┴────┴────┤
            │  Alert when queue > threshold          │
```

---

## Temperature Considerations

Raspberry Pi 4 generates heat during processing:

```
                    Temperature Zones
                    
    ┌─────────────────────────────────────────┐
    │                                         │
    │   0-50°C    ✓ NORMAL - Green LED       │
    │   50-80°C   ⚠ WARNING - Reduced perf   │
    │   80°C+     ✗ CRITICAL - Throttling    │
    │                                         │
    └─────────────────────────────────────────┘

Heat dissipation:
- CPU: ~1-2W during AI inference
- Metal housing helps dissipate heat
- Heat sinks recommended for continuous operation
```

---

## Troubleshooting Quick Reference

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Camera not detected | Ribbon cable loose | Re-seat cable |
| Green LED off | Software not running | Check Python script |
| Red LED always on | Threshold too low | Adjust in config.yaml |
| Buzzer silent | GPIO misconfigured | Check wiring |
| System slow | CPU overheating | Add heatsink/fan |
| No video feed | USB bandwidth issue | Try different USB port |
