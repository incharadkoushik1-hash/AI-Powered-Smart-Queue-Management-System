# Hardware Components List

## AI-Powered Smart Retail Store System

---

## 1. Vision Processing Unit

### Option A: Desktop/Laptop (Recommended for Development)

| Component | Quantity | Cost (INR) | Purpose |
|-----------|----------|------------|---------|
| USB Webcam (1080p) | 1 | ₹1,500 | Primary video capture device |
| Laptop/Desktop | 1 | - | Processing unit (already available) |

**Why This Option:**
- Faster processing with Intel i5/i7 or AMD Ryzen 5/7
- No additional hardware cost
- Easier debugging and development
- Suitable for demo and small-scale deployment

### Option B: Raspberry Pi 4 (Recommended for Production)

| Component | Quantity | Cost (INR) | Purpose |
|-----------|----------|------------|---------|
| Raspberry Pi 4 Model B (4GB) | 1 | ₹5,500 | Main processing unit running AI inference |
| 32GB SD Card (Class 10/U3) | 1 | ₹500 | Storage for OS and software |
| Raspberry Pi Camera Module 3 | 1 | ₹3,500 | High-quality video capture |
| Official Power Adapter (5V/3A USB-C) | 1 | ₹600 | Stable power supply |

**Why Raspberry Pi:**
- Low power consumption (5-15W)
- Compact form factor for retail deployment
- GPIO support for hardware alerts
- Cost-effective edge computing solution

### Option C: Industrial Edge Device (Large Deployments)

| Component | Quantity | Cost (INR) | Purpose |
|-----------|----------|------------|---------|
| NVIDIA Jetson Nano | 1 | ₹12,000 | GPU-accelerated AI inference |
| Raspberry Pi Camera Module 3 | 1 | ₹3,500 | Video capture |

---

## 2. Display & Output Components

### Alert Indicators

| Component | Quantity | Cost (INR) | Purpose |
|-----------|----------|------------|---------|
| Green LED (5mm) | 1 | ₹25 | System OK indicator |
| Red LED (5mm) | 1 | ₹25 | Alert indicator |
| Buzzer (5V Active) | 1 | ₹100 | Audio alert for critical events |
| Resistor (220Ω) | 2 | ₹10 | Current limiting for LEDs |
| Breadboard/PCB | 1 | ₹50 | Prototyping connection board |

**Why These Components:**
- LEDs provide instant visual feedback without looking at dashboard
- Buzzer alerts staff in noisy environments
- Low cost, reliable, easy to implement

### Optional: Local Display

| Component | Quantity | Cost (INR) | Purpose |
|-----------|----------|------------|---------|
| 7-inch HDMI Display | 1 | ₹3,000 | Local dashboard display |

---

## 3. Connectivity & Protection

| Component | Quantity | Cost (INR) | Purpose |
|-----------|----------|------------|---------|
| USB-C Cable | 1 | ₹200 | Power connection |
| USB Webcam Cable (3m) | 1 | ₹300 | Camera extension if needed |
| HDMI Cable | 1 | ₹300 | Video output (if using display) |
| ABS Plastic Enclosure | 1 | ₹800 | Housing for Raspberry Pi |
| Heat Sink Kit | 1 | ₹200 | Thermal management for Pi |
| Cable Ties (100pc) | 1 | ₹100 | Cable management |

---

## 4. Mounting & Installation

| Component | Quantity | Cost (INR) | Purpose |
|-----------|----------|------------|---------|
| Camera Tripod/Mount | 1 | ₹500 | Position camera at optimal angle |
| Adjustable Clamp | 2 | ₹150 | Secure camera position |
| Double-sided Tape | 1 | ₹50 | Temporary mounting |
| Cable Clips | 10 | ₹50 | Secure cable routing |

---

## 5. Complete Cost Breakdown

### Minimum Configuration (Using Existing Laptop/PC)

| Item | Cost (INR) |
|------|------------|
| USB Webcam (720p minimum) | ₹1,500 |
| Buzzer (optional) | ₹100 |
| LED Indicators (optional) | ₹50 |
| **TOTAL** | **₹1,650** |

### Standard Configuration (Laptop + Alerts)

| Item | Cost (INR) |
|------|------------|
| USB Webcam (1080p) | ₹1,500 |
| Green LED | ₹25 |
| Red LED | ₹25 |
| Buzzer (5V) | ₹100 |
| Resistors (220Ω × 2) | ₹10 |
| Breadboard | ₹50 |
| **TOTAL** | **₹1,710** |

### Raspberry Pi Configuration (Production)

| Item | Cost (INR) |
|------|------------|
| Raspberry Pi 4 (4GB) | ₹5,500 |
| Camera Module 3 | ₹3,500 |
| SD Card 32GB | ₹500 |
| Power Adapter | ₹600 |
| Enclosure | ₹800 |
| LED + Buzzer Kit | ₹150 |
| Heat Sink | ₹200 |
| Misc (cables) | ₹400 |
| **TOTAL** | **₹11,650** |

### Enterprise Configuration (High-Volume)

| Item | Cost (INR) |
|------|------------|
| NVIDIA Jetson Nano | ₹12,000 |
| Camera Module 3 | ₹3,500 |
| Storage (SSD) | ₹1,500 |
| Enclosure + Cooling | ₹2,000 |
| **TOTAL** | **₹19,000** |

---

## 6. Component Selection Criteria

### Webcam Selection

| Specification | Minimum | Recommended | Best |
|---------------|---------|-------------|------|
| Resolution | 720p | 1080p | 1080p |
| Frame Rate | 30 fps | 30 fps | 60 fps |
| Field of View | 60° | 90° | 120° |
| Auto-focus | Yes | Yes | Yes |
| USB Interface | USB 2.0 | USB 3.0 | USB 3.0 |

**Recommended Webcams:**
1. Logitech C920 (720p/1080p) - ₹2,500
2. Logitech C270 (720p) - ₹1,500
3. Creative Senz3D (720p) - ₹2,000

### Camera Module Selection (Raspberry Pi)

| Specification | Camera Module 3 | HQ Camera |
|---------------|-----------------|-----------|
| Resolution | 12MP | 12.3MP |
| Video | 1080p30 / 720p60 | 1080p30 |
| Interface | CSI | CSI |
| Price | ₹3,500 | ₹3,500 |
| Best For | Standard retail | High detail |

---

## 7. Hardware Alternatives

| Component | Alternative 1 | Alternative 2 | Notes |
|-----------|---------------|---------------|-------|
| Webcam | IP Camera | Phone Camera (DroidCam) | Network-based |
| Processing | Orange Pi 4 | Rock Pi 4 | ARM alternatives |
| Storage | USB Flash Drive | Network Storage | For larger data |
| Power | Power Bank (15W) | PoE HAT | Battery backup |

---

## 8. Supplier Recommendations (India)

| Component | Supplier | Website |
|-----------|----------|---------|
| Raspberry Pi | Robu.in | robu.in |
| Camera Modules | Fab.to.Lab | fabtolab.com |
| Sensors/Kits | RoboMart | robomart.com |
| Webcams | Amazon India | amazon.in |
| General Electronics | LCSC | lcsc.com |

---

## 9. Notes

1. **Camera Resolution:** 720p minimum recommended; 1080p preferred for better detection accuracy at distance

2. **Raspberry Pi Alternatives:** NVIDIA Jetson Nano, Google Coral can be used for GPU-accelerated AI but increase cost

3. **Webcam Selection:** Choose cameras with auto-focus and wide-angle lens for better shelf coverage

4. **Power Supply:** Always use quality power adapters. Brownouts during AI inference can cause system instability

5. **LED Color Coding:**
   - Green: System OK / Normal operation
   - Yellow/Orange: Warning / Busy queue
   - Red: Critical / Action required
