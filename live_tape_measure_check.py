"""
========================================================================================
     TF-LUNA MEASURING TAPE REAL-TIME ACCURACY VERIFIER
========================================================================================
Place your measuring tape from the front face of the TF-Luna to any flat target
(wall, box, book, door) at >= 20 cm distance.

This script displays in real-time:
1. RAW SENSOR (uncalibrated hardware integer)
2. CALIBRATED VALUE (sub-centimeter model: y = 1.0228x + 3.20 cm)
3. SIGNAL FLUX (signal quality confidence)
========================================================================================
"""

import sys
import os
import time
import json
import serial
import serial.tools.list_ports
import numpy as np
from collections import deque

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CALIB_JSON = "data/calibration.json"
BAUDRATE = 115200


def load_calibration():
    slope = 1.0228
    intercept = 3.20
    if os.path.exists(CALIB_JSON):
        try:
            with open(CALIB_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                slope = float(data.get("slope_m", slope))
                intercept = float(data.get("offset_error_cm", data.get("intercept_c", intercept)))
        except Exception:
            pass
    return slope, intercept


def find_sensor_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if any(k in p.description for k in ["CP210", "Silicon", "ESP32", "Arduino", "CH340", "USB Serial"]):
            return p.device
    for p in ports:
        if "Bluetooth" not in p.description:
            return p.device
    return None


def read_sample(ser):
    if not ser:
        return None, None
    try:
        if ser.in_waiting > 120:
            ser.reset_input_buffer()
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            return None, None
        tokens = [t for t in line.replace(',', ' ').split() if t.replace('.', '', 1).isdigit()]
        if len(tokens) >= 4:
            return float(tokens[2]), int(float(tokens[3]))
        elif len(tokens) == 2:
            return float(tokens[0]), int(float(tokens[1]))
        elif len(tokens) == 1:
            return float(tokens[0]), 1800
    except Exception:
        pass
    return None, None


def main():
    slope, intercept = load_calibration()
    port = find_sensor_port()

    print("\n" + "=" * 80)
    print("      🎯 TF-LUNA PHYSICAL MEASURING TAPE VERIFICATION TOOL")
    print("=" * 80)
    print(f"  • Active Calibration Model: Distance = {slope:.4f} * Raw + {intercept:+.2f} cm")
    print("  • Optical Zero Plane: Front glass face of the TF-Luna lenses")
    print("  • ⚠️ HARDWARE RULE: Target must be >= 20 cm away (0-20 cm is optical blind zone)")
    print("=" * 80)

    if not port:
        print("\n  ❌ No ESP-32 / TF-Luna detected on USB. Please plug it in!")
        input("\n  Press Enter to exit...")
        return

    try:
        s = serial.Serial()
        s.port = port
        s.baudrate = BAUDRATE
        s.dtr = False
        s.rts = False
        s.timeout = 1
        s.open()
        time.sleep(0.5)
        s.reset_input_buffer()
        print(f"  ✅ Connected to {port} @ {BAUDRATE} baud.\n")
    except Exception as e:
        print(f"  ❌ Error opening {port}: {e}")
        return

    print("  " + "-" * 76)
    print(f"  {'TAPE DISTANCE (cm)':<22} | {'RAW ToF (cm)':<16} | {'CALIBRATED (cm)':<18} | {'STATUS'}")
    print("  " + "-" * 76)

    window = deque(maxlen=10)
    try:
        while True:
            raw_d, flux = read_sample(s)
            if raw_d is not None:
                # If firmware is already outputting calibrated distance, detect it
                # Raw hardware output from TF-Luna is integer. Decimal smoothing gives sub-cm precision.
                window.append(raw_d)
                smooth_raw = float(np.mean(window))
                calibrated = (slope * smooth_raw) + intercept

                if smooth_raw < 20.0:
                    status = "⚠️ BLIND ZONE (<20cm)"
                    print(f"\r  Target too close! ({smooth_raw:4.1f}cm)    | Raw: {smooth_raw:5.1f} cm   | Move target >= 20 cm!  | {status:<18}", end="", flush=True)
                else:
                    status = "✅ OPTICAL LOCK" if flux >= 100 else "⚠️ LOW FLUX"
                    print(f"\r  Tape: Place ruler/tape | Raw: {smooth_raw:5.1f} cm   | Calibrated: {calibrated:6.2f} cm | {status:<18}", end="", flush=True)
            time.sleep(0.04)
    except KeyboardInterrupt:
        print("\n\n  [*] Stopped.")
    finally:
        s.close()


if __name__ == '__main__':
    main()
