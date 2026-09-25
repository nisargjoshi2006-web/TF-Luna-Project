"""
====================================================================
           TF-LUNA LIDAR - 1-CLICK VS CODE LAUNCHER
====================================================================
How to use in VS Code without typing in the terminal:
1. Open this file (run_dashboard.py) in VS Code.
2. Click the Play button (▶) in the top-right corner of VS Code!
   (OR press F5 on your keyboard)
3. The dashboard and 3D simulation will launch automatically!
====================================================================
"""

import sys
import os
import subprocess
import webbrowser
import time
import threading

def open_browser_tab():
    time.sleep(1.8)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    print("=" * 65)
    print("   Starting TF-Luna 3D LiDAR Dashboard...")
    print("   Opening browser at: http://localhost:8501")
    print("=" * 65)

    # Ensure working directory is project root
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # Launch browser automatically
    threading.Thread(target=open_browser_tab, daemon=True).start()

    # Launch Streamlit process
    cmd = [sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.headless=true"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
