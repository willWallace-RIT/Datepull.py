import os
import time
from datetime import datetime

def get_clean_timestamp(file_path):
    """Extracts and formats file modification time for a HUD overlay."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target file not found: {file_path}")
    
    # Retrieve system metadata (modification time)
    # For deep container metadata (like MP4/MKV creation time), ffmpeg-python can be swapped in here.
    mtime = os.path.getmtime(file_path)
    dt_obj = datetime.fromtimestamp(mtime)
    
    # Standardized format for HUD readability: [YYYY-MM-DD HH:MM:SS]
    formatted_timestamp = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "raw_epoch": mtime,
        "iso_format": dt_obj.isoformat(),
        "hud_string": f"TIMESTAMP: {formatted_timestamp}"
    }

def generate_vlc_marquee_command(file_path, text_position=4):
    """Generates the formatted string ready for a media player hook."""
    metadata = get_clean_timestamp(file_path)
    
    # Example structure for an external player hook or telemetry log
    hud_payload = {
        "source_file": os.path.basename(file_path),
        "overlay_text": metadata["hud_string"],
        "position": text_position, # 4 = bottom, etc.
        "update_interval": 1000
    }
    
    return hud_payload

if __name__ == "__main__":
    target_file = "sample_footage.mp4"
    # Create a dummy file for testing if it doesn't exist
    if not os.path.exists(target_file):
        with open(target_file, "w") as f:
            f.write("test data")
            
    payload = generate_vlc_marquee_command(target_file)
    print("HUD Payload Generated Successfully:")
    for key, value in payload.items( ):
        print(f"  {key}: {value}")
