@echo off
title TF-Luna LiDAR & ESP-32 Live Telemetry Stream
cd /d "%~dp0"
python live_telemetry_stream.py
pause
