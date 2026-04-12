# Hardware Requirements

## AI-Based Queue Monitoring System

---

## Power Requirements

### Voltage & Current Specifications

| Component | Operating Voltage | Typical Current | Max Current |
|-----------|-------------------|-----------------|-------------|
| Raspberry Pi 4 | 5V DC | 0.5-2.5A | 3A |
| Camera Module 3 | 3.3V (from CSI) | 250mA | 300mA |
| Green LED | 2.0-2.5V | 15mA | 20mA |
| Red LED | 1.8-2.5V | 15mA | 20mA |
| Buzzer (active) | 5V | 30mA | 50mA |

### Power Supply Specifications

```
REQUIRED: 5V DC @ 3A minimum
Connector: USB-C (Raspberry Pi 4)
Input: 220V AC 50Hz (via adapter)

RECOMMENDED: Use official Raspberry Pi power adapter
- Ensures stable voltage under load
- Prevents brownouts during AI inference
- Protects from voltage fluctuations
```

### Power Consumption Summary

| Mode | Current | Duration | Battery Backup* |
|------|---------|----------|-----------------|
| Idle | 0.5A | Continuous | ~10 hours |
| Processing | 1.5A | Active | ~3 hours |
| Max (with peripherals) | 3.0A | Peak | ~1.5 hours |

*Battery backup with 15000mAh power bank

---

## System Requirements

### Minimum Hardware Requirements

#### Option A: Raspberry Pi Configuration
```
Processor:     ARM Cortex-A72 (Quad-core 1.5GHz)
RAM:           4GB minimum (8GB recommended)
Storage:       32GB SD Card (Class 10 or U3)
Camera:        Raspberry Pi Camera Module 3 or USB webcam
Connectivity:  Ethernet or WiFi (for dashboard access)
```

#### Option B: Laptop/Desktop Configuration
```
Processor:     Intel i5 8th gen or AMD Ryzen 5 equivalent
RAM:           8GB minimum
Storage:       256GB SSD
Camera:        Built-in webcam or USB webcam (720p+)
OS:            Windows 10/11, Linux (Ubuntu 20.04+), macOS
Connectivity:  WiFi/Ethernet (for dashboard access)
```

### Software Requirements

```
Python:          3.8 or higher
Operating System: 
  - Raspberry Pi OS (64-bit) Bullseye/Bookworm
  - Windows 10/11 with Python 3.8+
  - Ubuntu 20.04+ / Debian
  - macOS 11+ (Big Sur or later)

Additional:
  - OpenCV 4.5+
  - Ultralytics YOLOv8
  - Flask 2.0+
  - NumPy 1.20+
```

---

## Camera Requirements

### Resolution

| Resolution | Frames/sec | Detection Quality | Recommended Use |
|------------|------------|-------------------|-----------------|
| 640×480 | 30 | Good | Small queues, budget |
| 1280×720 (720p) | 30 | Better | Standard retail |
| 1920×1080 (1080p) | 30 | Best | Large queues |

**Recommendation:** 720p minimum, 1080p preferred

### Lens Specifications

```
Field of View:  60° - 120° (wider is better for close placement)
Focal Length:   2.8mm - 4mm (standard)
Aperture:       f/2.0 or lower (better low-light)
Auto-focus:     Recommended for varying distances
```

### Camera Placement

```
MAXIMUM DISTANCE FROM QUEUE: 3-5 meters
IDEAL HEIGHT: 2.5 - 3.5 meters (ceiling mount)
ANGLE: 15° - 30° downward tilt

┌─────────────────────────────────────────────────────────┐
│                                                         │
│                    CAMERA                               │
│                      │                                  │
│                      │ 2.5-3.5m                        │
│                      │                                 │
│                      ▼                                  │
│  ═══════════════════════════════════════════════════   │
│                                                         │
│                   QUEUE AREA                            │
│                   (detection zone)                     │
│                                                         │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│                                                         │
│     [Person] [Person] [Person]                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Environmental Considerations

### Lighting Requirements

| Condition | Lux Level | Quality | Action Required |
|-----------|-----------|---------|------------------|
| Bright daylight | 10,000+ | Excellent | Natural light sufficient |
| Indoor bright | 500-1,000 | Good | Standard indoor lighting |
| Overcast day | 1,000-2,000 | Good | Natural window light |
| Indoor dim | 100-500 | Acceptable | May need additional lighting |
| Indoor dark | <100 | Poor | Artificial lighting required |

```
MINIMUM LIGHTING: 200 Lux at queue level
RECOMMENDED: 300-500 Lux

Avoid:
- Direct sunlight on camera (causes washout)
- Strong backlighting (causes silhouettes)
- Flickering lights (causes detection issues)
```

### Recommended Lighting Setup

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Ceiling Lights (evenly distributed)                   │
│                                                         │
│    💡        💡        💡        💡                    │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│                   CAMERA                                │
│                      │                                  │
│                      ▼                                  │
│                                                         │
│                   QUEUE AREA                            │
│                                                         │
└─────────────────────────────────────────────────────────┘

LIGHTING GUIDELINES:
✓ Use diffused lighting (avoid harsh shadows)
✓ Position lights to avoid glare on camera lens
✓ Maintain consistent lighting (avoid flickering)
✓ Consider automatic lighting in 24/7 environments
```

### Environmental Factors

#### Temperature
```
Operating Range:
  Minimum: 0°C (32°F)
  Maximum: 45°C (113°F)
  
Storage Range:
  Minimum: -20°C (-4°F)  
  Maximum: 60°C (140°F)

Humidity: 10% - 90% (non-condensing)
```

#### Physical Placement

| Factor | Requirement | Notes |
|--------|-------------|-------|
| Height | 2.5-4 meters | Ceiling or wall mount |
| Distance | 1-5 meters from queue | Based on camera FOV |
| Angle | 0-30° downward tilt | Point toward queue |
| Vibration | Avoid vibrating surfaces | Prevents blurry images |
| Cleanliness | Keep lens dust-free | Clean monthly |

### Indoor vs Outdoor

| Aspect | Indoor | Outdoor |
|--------|--------|---------|
| Lighting | Controlled | Variable |
| Weather | Not applicable | IP rating needed |
| Temperature | Climate controlled | Extended range needed |
| Mounting | Standard | Weatherproof housing |

---

## Network Requirements

### Dashboard Access

```
Local Network (LAN):
  - Preferred method
  - Low latency (<50ms)
  - No internet required
  
WiFi Specifications:
  - 802.11n minimum (2.4GHz or 5GHz)
  - Signal strength: -70dBm minimum at camera location
```

### Bandwidth Requirements

| Function | Bandwidth | Frequency |
|----------|-----------|-----------|
| Video streaming | 2-5 Mbps | Continuous |
| Dashboard updates | <100 Kbps | Every 2 seconds |
| Initial model download | 50-100 MB | One-time |

---

## Physical Dimensions

### Raspberry Pi 4 Board
```
Length:    88mm (3.4 inches)
Width:     58mm (2.3 inches)
Height:    19.5mm (0.8 inches)
Weight:    46g
```

### Camera Module 3
```
Length:    25mm (1 inch)
Width:     24mm (0.9 inches)  
Height:    11.5mm (0.45 inches)
```

### Enclosure Recommendations
```
Size:      120mm × 90mm × 40mm minimum
Material:  ABS plastic or aluminum
Mounting:  DIN rail or wall mount compatible
Venting:   Ventilation holes for heat dissipation
```

---

## Reliability Requirements

### Uptime Expectations

| Deployment | Target Uptime | Max Downtime/day |
|------------|---------------|------------------|
| Business hours | 99% | 36 minutes |
| 24/7 operation | 99.9% | 8.6 minutes |

### MTBF (Mean Time Between Failures)

| Component | MTBF (hours) | MTBF (years) |
|-----------|-------------|--------------|
| Raspberry Pi 4 | 50,000 | 5.7 |
| USB Webcam | 30,000 | 3.4 |
| Power Supply | 50,000 | 5.7 |
| SD Card | 10,000 | 1.1 |

### Maintenance Schedule

| Task | Frequency |
|------|-----------|
| Lens cleaning | Weekly |
| SD card health check | Monthly |
| Software updates | Monthly |
| Hardware inspection | Quarterly |
| Full system backup | Weekly |

---

## Summary Checklist

Before deployment, verify:

```
[ ] Power supply: 5V/3A USB-C adapter ready
[ ] Camera: Proper focus and angle set
[ ] Lighting: 300+ Lux at queue level
[ ] Network: WiFi/Ethernet connected
[ ] Storage: SD card 50% free space minimum
[ ] Environment: Temperature within 0-45°C
[ ] Mounting: Camera stable and secure
[ ] Test: Detection working correctly
```
