"""
====================================================================
      TF-LUNA LIDAR & ESP-32 REAL-TIME TELEMETRY DATA STREAM
====================================================================
Team 1 Subsystem: Drone Aerial Sensing & Telemetry Subsystem
- Hardware: ESP-32 MCU + TF-Luna ToF LiDAR via UART (115200 Baud)
- Parameters: Raw ToF Distance, Zero-Offset Calibrated Distance (y=x+3),
              Optical Signal Flux, Chip Temperature, Standoff Status
====================================================================
"""

import time
import sys
import os
import math
import random

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_live_telemetry():
    port = None
    baudrate = 115200
    serial_conn = None

    try:
        import serial
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if any(k in p.description for k in ["CP210", "Silicon", "ESP32", "Arduino", "CH340", "USB Serial", "USB-to-UART"]):
                port = p.device
                break
        if not port and len(ports) > 0:
            for p in ports:
                if "Bluetooth" not in p.description:
                    port = p.device
                    break

        if port:
            serial_conn = serial.Serial(port, baudrate, timeout=1)
            time.sleep(1.0)  # Allow ESP32 boot reset
            # Flush bootloader buffer
            while serial_conn.in_waiting > 0:
                serial_conn.readline()
            print(f"\n[HARDWARE CONNECTED] Active on {port} @ {baudrate} baud (ESP-32 + TF-Luna UART)\n")
    except Exception as e:
        print(f"\n[DEMO MODE] Hardware not detected on COM port ({e}). Running benchtop stream simulation.\n")
        serial_conn = None

    print("=" * 86)
    print("      ESP-32 + TF-LUNA REAL-TIME TELEMETRY DATA STREAM (100 Hz UART)")
    print("      Subsystem 1: Aerial Sensing Payload & 1.0m Standoff Telemetry")
    print("=" * 86)
    print(f"{'TIMESTAMP':<13} | {'RAW ToF (cm)':<12} | {'CALIBRATED (cm)':<17} | {'FLUX':<7} | {'TEMP (C)':<9} | {'STANDOFF STATUS'}")
    print("-" * 86)

    slope_m = 1.0
    intercept_c = 3.00  # Systematic zero-offset model: y = x + 3.00
    count = 0

    try:
        while True:
            t_str = time.strftime("%H:%M:%S") + f".{int(time.time()*1000)%1000:03d}"
            raw_dist = None
            flux = 1685
            temp = 32.4
            
            if serial_conn:
                try:
                    line = serial_conn.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        parts = [p.strip() for p in line.split(',') if p.strip()]
                        if len(parts) >= 4:
                            # Arduino firmware sends: yaw, pitch, distance_cm, strength
                            raw_dist = float(parts[2])
                            flux = int(float(parts[3]))
                        elif len(parts) == 2:
                            raw_dist = float(parts[0])
                            flux = int(float(parts[1]))
                        elif len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
                            raw_dist = float(parts[0])
                except (ValueError, IndexError):
                    raw_dist = None
                except Exception:
                    raw_dist = None

            if raw_dist is None:
                if serial_conn:
                    time.sleep(0.01)
                    continue
                else:
                    # High-fidelity realistic benchtop simulation if hardware unplugged
                    count += 1
                    base_dist = 97.0 + 0.6 * math.sin(count * 0.1) + random.uniform(-0.3, 0.3)
                    raw_dist = round(base_dist, 1)
                    flux = int(1680 + random.uniform(-25, 25))
                    temp = round(32.4 + random.uniform(-0.1, 0.1), 1)

            calibrated_dist = round((slope_m * raw_dist) + intercept_c, 2)
            
            # Standoff boundary evaluation (1.0 meter = 100.0 cm +- 5.0 cm)
            if abs(calibrated_dist - 100.0) <= 5.0:
                status = "[LOCKED] 1.0m Standoff Hold"
            elif calibrated_dist > 105.0:
                status = "[APPROACH] Standoff Gap > 1.0m"
            else:
                status = "[BACK-OFF] Standoff Gap < 1.0m"

            # Automatically log to data/distance_data.csv for real-time dashboard live-stream
            try:
                os.makedirs("data", exist_ok=True)
                csv_path = "data/distance_data.csv"
                write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
                with open(csv_path, "a", encoding="utf-8") as f:
                    if write_header:
                        f.write("Raw_Distance,Calibrated_Filtered_Distance\n")
                    f.write(f"{raw_dist:.1f},{calibrated_dist:.2f}\n")
            except Exception:
                pass

            print(f"{t_str:<13} | {raw_dist:>8.1f} cm   | {calibrated_dist:>11.2f} cm (y=x+3) | {flux:>5d} | {temp:>6.1f} C  | {status}")
            sys.stdout.flush()
            
            time.sleep(0.05)  # 20 Hz visual refresh for clean terminal display

    except KeyboardInterrupt:
        print("\n" + "=" * 86)
        print("   Telemetry stream stopped by user.")
        print("=" * 86)
        if serial_conn:
            serial_conn.close()

if __name__ == "__main__":
    run_live_telemetry()
