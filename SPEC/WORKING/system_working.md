# System Working Explanation

## AI-Based Queue Monitoring System

---

## Overview

This document explains how the complete system works - integrating both hardware and software components to form a functioning AI-based queue monitoring solution.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            COMPLETE SYSTEM                                  │
│                                                                              │
│  ┌─────────────────────────── HARDWARE ───────────────────────────┐         │
│  │                                                               │         │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │         │
│  │   │   CAMERA    │───►│  RASPBERRY  │───►│   ALERTS    │    │         │
│  │   │ (Capture)   │    │    PI 4     │    │(LED/Buzzer) │    │         │
│  │   │             │    │  (Process)  │    │             │    │         │
│  │   └─────────────┘    └──────┬──────┘    └─────────────┘    │         │
│  │                              │                               │         │
│  │                    ┌─────────┴─────────┐                   │         │
│  │                    │      DISPLAY       │                   │         │
│  │                    │   (Dashboard)      │                   │         │
│  │                    └───────────────────┘                   │         │
│  └────────────────────────────────────────────────────────────┘         │
│                                    │                                      │
│                                    │                                      │
│  ┌─────────────────────────── SOFTWARE ───────────────────────────┐      │
│  │                                                               │      │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │      │
│  │   │  Video   │─►│   YOLO   │─►│   Queue  │─►│ Dashboard│     │      │
│  │   │ Capture  │  │Detection │  │ Analysis │  │  Server  │     │      │
│  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘     │      │
│  │                                                               │      │
│  └───────────────────────────────────────────────────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Hardware + Software Integration

### Data Flow

```
REAL WORLD                           SYSTEM                              OUTPUT
──────────                           ──────                              ──────

    │                                   │                                   │
    │   Light from queue               │                                   │
    │        ▼                          │                                   │
    │ ┌───────────┐                    │                                   │
    │ │  Camera   │  Video Signal      │                                   │
    │ │  Lens     │────────────────────│                                   │
    │ └───────────┘                    │                                   │
    │                                   │                                   │
    │                                   │  ┌───────────────────────────┐   │
    │                                   │  │  Python + OpenCV          │   │
    │                                   │  │  - Read frame             │   │
    │                                   │  │  - Preprocess             │   │
    │                                   │  │  - YOLO inference         │   │
    │                                   │  └─────────────┬─────────────┘   │
    │                                   │                │                 │
    │                                   │                ▼                 │
    │                                   │  ┌───────────────────────────┐   │
    │                                   │  │  Bounding Boxes           │   │
    │                                   │  │  [Person, 0.95]          │   │
    │                                   │  │  [Person, 0.87]          │   │
    │                                   │  └─────────────┬─────────────┘   │
    │                                   │                │                 │
    │                                   │                ▼                 │
    │                                   │  ┌───────────────────────────┐   │
    │                                   │  │  ROI Filter               │   │
    │                                   │  │  - Check centers in zone  │   │
    │                                   │  │  - Count: 5              │   │
    │                                   │  └─────────────┬─────────────┘   │
    │                                   │                │                 │
    │              ┌────────────────────┼────────────────┼──────┐          │
    │              │                    │                │      │          │
    │              ▼                    ▼                ▼      ▼          │
    │        ┌──────────┐        ┌──────────┐     ┌────────┐  ┌──────┐ │
    │        │  GPIO    │        │  Flask   │     │  JSON  │  │ Image│ │
    │        │  Alerts  │        │  Server  │     │  Stats │  │ Frame│ │
    │        └──────────┘        └──────────┘     └────────┘  └──────┘ │
    │              │                    │              │          │       │
    │              ▼                    ▼              ▼          ▼       │
    │        ┌──────────┐        ┌──────────┐     ┌────────┐  ┌──────┐ │
    │        │LED/BUZZER│        │  Web     │     │Browser │  │Browser│ │
    │        │ Hardware │        │  Server  │     │Dashboard│ │  img  │ │
    │        └──────────┘        └──────────┘     └────────┘  └──────┘ │
    │                                                                              │
    └──────────────────────────────────────────────────────────────────────────────
```

---

## End-to-End Workflow

### Phase 1: Initialization

```
1. System Startup
   │
   ├── Load configuration (config.yaml)
   ├── Initialize camera
   ├── Load YOLOv8 model
   ├── Setup GPIO pins (if available)
   └── Start Flask server

2. Camera Ready
   └── Green LED ON (system ready)

3. Dashboard Available
   └── http://localhost:5000
```

### Phase 2: Continuous Processing

```
┌─────────────────────────────────────────────────────────┐
│                     MAIN LOOP                           │
│  (Runs continuously while system is active)             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 1: Capture Frame                                   │
│         camera.read() → 1280×720 BGR image              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: Detection (every 5th frame)                     │
│         - Resize to 640×640                              │
│         - Run YOLOv8 inference                           │
│         - Filter by confidence > 0.5                     │
│         - Extract person bounding boxes                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: Queue Analysis                                   │
│         - For each detection:                           │
│           - Calculate center point                       │
│           - Check if in ROI polygon                      │
│         - Count total people in queue                    │
│         - Update statistics                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: Alert Decision                                   │
│         - Compare count to thresholds                    │
│         - Set LED states                                 │
│         - Trigger buzzer if needed                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: Dashboard Update                                │
│         - Update shared variables                        │
│         - Annotate frame with boxes                      │
│         - Serve via Flask API                            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                    (Loop continues)
```

### Phase 3: User Interaction

```
Browser User
      │
      ├── Opens http://localhost:5000
      │
      ├── Dashboard loads (HTML/CSS/JS)
      │
      ├── JS polls /api/stats every 2 seconds
      │
      ├── JS refreshes image every 5 seconds
      │
      └── User sees:
          - Live video feed
          - Queue count
          - Wait time
          - Staffing recommendation
```

---

## Component Interactions

### Camera ↔ Processor

```
Camera captures at 30 FPS
         │
         │ USB/CSI cable
         │ ~33ms per frame
         ▼
Processor receives raw video
         │
         │ OpenCV reads frame
         │ BGR format, 720p
         ▼
Stored in memory
         │
         │ Next frame arrives
         ▼
(Previous frame processed)
```

### YOLOv8 ↔ Queue Analyzer

```
YOLOv8 Output                          Queue Analyzer Input
──────────────                          ───────────────────
[BoundingBox(x1,y1,x2,y2)] ──────────► Check if center in ROI
[BoundingBox(x1,y1,x2,y2)]            Count +1 if inside
...                                    │
                                       ▼
                                  count = N
```

### Flask Server ↔ Browser

```
Server                          Browser
───────                         ───────
Holds latest frame  ◄─────────── GET /api/frame
Stores stats dict    ◄─────────── GET /api/stats
                    ─────────────► JSON response
                    ─────────────► JPEG image
```

### GPIO ↔ Alert Manager

```
Alert Manager                   Hardware
────────────                   ────────
set_led('red', True) ────────► GPIO 27 = HIGH → Red LED ON
set_led('green', False) ─────► GPIO 17 = LOW → Green LED OFF
beep(0.5) ───────────────────► GPIO 22 = HIGH for 0.5s → Buzzer sounds
```

---

## Real-World Scenario

### Morning Rush (8:00 AM)

```
1. First customers arrive
   └── Queue count: 1-2 (LOW status, green LED)

2. Queue builds up
   └── Queue count: 5-6 (NORMAL status, green LED)

3. Peak time
   └── Queue count: 10 (HIGH status, red LED + short beeps)
   └── Dashboard shows: "ADD_STAFF" recommendation

4. Additional counter opens
   └── Staff sends more people through
   └── Queue count decreases to 6

5. Rush ends
   └── Queue count: 2-3 (LOW status, green LED)
```

---

## System Timing

```
Time    Camera    Detection    Analysis    Dashboard
─────────────────────────────────────────────────────
0ms     Frame 1   Frame 1      Frame 1     Stats 1
33ms    Frame 2   (skip)       (skip)      (update)
66ms    Frame 3   Frame 2      Frame 2     Stats 2
100ms   Frame 4   (skip)       (skip)      (update)
133ms   Frame 5   Frame 3      Frame 3     Stats 3

Detection runs every 5th frame = 6 FPS detection
Dashboard updates = 0.5 FPS (every 2 seconds)
```

---

## Where and How to Run

### Development/Testing (Laptop)

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   ┌─────────────┐                                   │
│   │   LAPTOP    │                                   │
│   │             │                                   │
│   │  ┌───────┐  │    Camera: Built-in webcam       │
│   │  │ webcam│  │                                   │
│   │  └───┬───┘  │                                   │
│   │      │      │                                   │
│   │      ▼      │                                   │
│   │  ┌───────┐  │                                   │
│   │  │ Python │  │   Terminal: python run.py       │
│   │  │  code  │  │                                   │
│   │  └───────┘  │                                   │
│   │      │      │                                   │
│   │      ▼      │                                   │
│   │  ┌───────┐  │                                   │
│   │  │Browser │  │   Browser: http://localhost:5000 │
│   │  └───────┘  │                                   │
│   └─────────────┘                                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Production (Raspberry Pi)

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   ┌─────────────┐         ┌─────────────┐         │
│   │   RPi 4     │◄───────►│   CAMERA    │         │
│   │             │  CSI/USB │   Module    │         │
│   │  ┌───────┐  │         │      o      │         │
│   │  │ Python │  │         └─────────────┘         │
│   │  │  code  │  │                                │
│   │  └───────┘  │         ┌─────────────┐         │
│   │      │      │         │  LED/BUZZER │         │
│   │      │      │─────────►│   (GPIO)    │         │
│   │      │      │   GPIO   └─────────────┘         │
│   │      │      │                                │
│   │      ▼      │         ┌─────────────┐         │
│   │  ┌───────┐  │         │   DISPLAY   │         │
│   │  │ Flask │  │─────────►│   (HDMI)    │         │
│   │  │Server │  │ Network │             │         │
│   │  └───────┘  │         └─────────────┘         │
│   └─────────────┘                                │
│          │                                        │
│          │ Network                                │
│          ▼                                        │
│   ┌─────────────┐                                 │
│   │   BROWSER   │  (Phone/Tablet/PC)             │
│   │ http://IP   │                                 │
│   └─────────────┘                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## System Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                     SYSTEM BOUNDARY                          │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                   THIS PROJECT                         │ │
│  │                                                       │ │
│  │  INCLUDED:                                            │ │
│  │  - Camera capture and video processing                │ │
│  │  - AI person detection (YOLOv8)                       │ │
│  │  - Queue counting and analysis                        │ │
│  │  - Alert system (LED/Buzzer)                         │ │
│  │  - Web dashboard                                      │ │
│  │                                                       │ │
│  │  NOT INCLUDED:                                        │ │
│  │  - POS/retail system integration                      │ │
│  │  - Staff scheduling software                          │ │
│  │  - Customer tracking across cameras                   │ │
│  │  - Cloud storage/analytics                            │ │
│  │  - Mobile push notifications                          │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
