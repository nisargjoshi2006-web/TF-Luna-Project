@echo off
title TF-Luna LiDAR 3D Simulation
echo ==============================================================
echo       Starting TF-Luna 3D LiDAR Dashboard ^& Simulation...
echo ==============================================================
cd /d "%~dp0"
python run_dashboard.py
pause
