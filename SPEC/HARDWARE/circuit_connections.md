# Circuit Connections Guide

## AI-Based Queue Monitoring System

---

## Connection Overview

This guide provides detailed pin-to-pin connections for setting up the hardware components.

---

## Option 1: Raspberry Pi 4 with Camera Module 3

### Camera Connection

```
Raspberry Pi 40-Pin GPIO                          Camera Module 3
┌─────────────────────┐                          ┌─────────────────┐
│                     │                          │                 │
│    CSI Port         │◄─────────────────────────│ Camera Ribbon   │
│    (15-pin FPC)     │    Ribbon Cable          │ Connector       │
│                     │                          │                 │
└─────────────────────┘                          └─────────────────┘
```

**Steps to Connect Camera:**
1. Locate the CSI port between HDMI and 3.5mm jack
2. Pull up the plastic clip on the CSI port
3. Insert ribbon cable with metal contacts facing HDMI port
4. Push clip back down to secure
5. Ensure cable is firmly seated

### Power Supply Connection

```
┌──────────────────────┐         ┌──────────────────────┐
│  Power Adapter       │         │   Raspberry Pi 4     │
│  (5V/3A USB-C)       │         │   USB-C Port         │
│                      │         │                      │
│  Input: 220V AC     │─────────►│  Output: 5V DC       │
│  Output: 5V/3A DC   │         │  Max: 3A            │
└──────────────────────┘         └──────────────────────┘
```

### LED Indicator Connections

```
┌──────────────────────┐
│  Raspberry Pi GPIO   │
│                      │
│  GPIO 17 ──────┬────►│──► LED 1 (Green - System OK)
│  GPIO 27 ──────┤
│                │     └──► LED 2 (Red - Alert)
│  GND ──────────┴──────► Common Ground
│                      │
└──────────────────────┘

Connection Table:
┌─────────────┬──────────┬────────────┬──────────────────┐
│ Component   │ Pin      │ Connected To│ Purpose         │
├─────────────┼──────────┼────────────┼──────────────────┤
│ LED Green   │ GPIO 17  │ 220Ω Resistor │ Status LED   │
│ LED Red     │ GPIO 27  │ 220Ω Resistor │ Alert LED    │
│ LED Anode   │ +3.3V    │ Via Resistor  │ Power Source │
│ LED Cathode │ GND      │ Pin 39         │ Ground       │
└─────────────┴──────────┴────────────┴──────────────────┘
```

### Buzzer Connection

```
┌──────────────────────┐
│  Raspberry Pi GPIO   │
│                      │
│  GPIO 22 ──────┐     │
│                │     ├──► Transistor Base (2N2222)
│  5V ───────────┤     │
│                │     │
│  GND ──────────┴────►│──► Buzzer (+) Terminal
│                      │
└──────────────────────┘

Connection Table:
┌─────────────┬──────────┬────────────┬──────────────────┐
│ Component   │ Pin      │ Connected To│ Purpose         │
├─────────────┼──────────┼────────────┼──────────────────┤
│ Buzzer +    │ GPIO 22  │ Transistor  │ Signal Control │
│ Buzzer -    │ GND      │ Ground       │ Ground        │
│ Transistor C│ Buzzer + │ Via Resistor  │ Switch       │
│ Transistor E│ GND      │ Ground       │ Emitter       │
└─────────────┴──────────┴────────────┴──────────────────┘
```

---

## Option 2: USB Webcam (Laptop/Desktop)

### Simple Connection

```
┌──────────────────────┐         ┌──────────────────────┐
│  Laptop/Desktop      │         │   USB Webcam         │
│                      │         │                      │
│  USB Port ◄──────────┼─────────│ USB Connector        │
│                      │         │                      │
└──────────────────────┘         └──────────────────────┘

Connection Table:
┌─────────────┬──────────┬────────────┬──────────────────┐
│ Component   │ Port     │ Connected To│ Purpose         │
├─────────────┼──────────┼────────────┼──────────────────┤
│ Webcam      │ USB 2.0+ │ Computer    │ Video + Power    │
│ USB Cable   │ Type-A   │ Any USB Port│ Data + Power     │
└─────────────┴──────────┴────────────┴──────────────────┘
```

---

## Complete GPIO Pin Mapping (Raspberry Pi)

```
┌────────────────────────────┐
│     Raspberry Pi 4        │
│        Top View           │
├────────────────────────────┤
│  3.3V  │  1  │  2  │  5V  │  Power Rails
│  GPIO  │  3  │  4  │  5V  │  
│  SDA   │  5  │  6  │  GND │  I2C / Ground
│  SCL   │  7  │  8  │  14  │  I2C / UART
│  GND   │  9  │ 10  │  15  │  Ground / GPIO
│  17    │ 11  │ 12  │  18  │  LED Green
│  27    │ 13  │ 14  │  GND │  LED Red / Ground
│  22    │ 15  │ 16  │  23  │  Buzzer / GPIO
│  3.3V  │ 17  │ 18  │  24  │  Power / GPIO
│  10    │ 19  │ 20  │  GND │  SPI / Ground
│  9     │ 21  │ 22  │  25  │  SPI / GPIO
│  11    │ 23  │ 24  │  8   │  SPI
│  GND   │ 25  │ 26  │  7   │  Ground / GPIO
│  ID_SD │ 27  │ 28  │  ID_SC│  I2C EEPROM
│  5V    │ 29  │ 30  │  GND │  Power / Ground
│  21    │ 31  │ 32  │  33  │  GPIO
│  GND   │ 35  │ 36  │  37  │  Ground / GPIO
│  26    │ 37  │ 38  │  40  │  GPIO / GPIO
└────────────────────────────┘
```

### Final Connection Summary

| Component | GPIO Pin | Function | Resistor |
|-----------|----------|----------|----------|
| Green LED | GPIO 17 | Status indicator | 220Ω |
| Red LED | GPIO 27 | Alert indicator | 220Ω |
| Buzzer | GPIO 22 | Audio alert | 1kΩ (base) |
| Camera | CSI Port | Video capture | N/A |
| Power | USB-C | System power | N/A |

---

## Safety Precautions

1. **Power Off**: Always disconnect power before wiring
2. **Polarity**: Check LED polarity (longer leg = anode/+)
3. **Resistors**: Always use resistors with LEDs to prevent burnout
4. **Voltage**: Never connect 5V to 3.3V GPIO directly
5. **Static Discharge**: Handle components carefully to avoid ESD damage

---

## Testing Connections

```python
# Test GPIO connections on Raspberry Pi
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # Green LED
GPIO.setup(27, GPIO.OUT)  # Red LED
GPIO.setup(22, GPIO.OUT)  # Buzzer

# Blink LEDs to verify connections
for i in range(3):
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.5)

GPIO.cleanup()
```
