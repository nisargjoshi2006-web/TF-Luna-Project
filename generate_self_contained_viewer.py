import os
import json
from continuous_multi_point_scanner import generate_clean_web_viewer

ply_path = "reports/continuous_scan.ply"
if not os.path.exists(ply_path):
    ply_path = "data/room_scan.ply"

meta = {
    'D_N': 2.4, 'D_E': 2.4, 'D_S': 2.4, 'D_W': 2.4,
    'width_x': 4.8, 'length_z': 4.8,
    'objects': [
        {
            'name': 'Almari',
            'label': 'Almari: 65 cm Bahar (Inward Bulge)',
            'dist_cm': 65,
            'x': -0.703, 'y': 2.65, 'z': 1.75,
            'target_y': 1.9,
            'color': '#FF8C00',
            'border': '#FFA726'
        },
        {
            'name': 'Gate',
            'label': 'Gate: 60 cm Andar (Outward Recess)',
            'dist_cm': 60,
            'x': 3.0, 'y': 2.65, 'z': -0.752,
            'target_y': 2.15,
            'color': '#00E676',
            'border': '#69F0AE'
        }
    ]
}

out_html = generate_clean_web_viewer(ply_path, meta)
print(f"Generated self-contained {out_html} successfully!")
