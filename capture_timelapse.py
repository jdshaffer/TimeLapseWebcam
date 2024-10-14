##################################################
# Take time-lapse pictures with the webcam
# Created by ChatGPT, corrected by Jds
# 2024-10-13
#
# Requires this python module:
#    pip install opencv-python
#
# CAMERA INDEX
#    MBA Camera is value 1
#    iPhone as wireless camera is value 2
#
# SUGGESTED TIMINGS
#    Cloud Movement and Weather Changes:
#    Interval: 5 to 15 minutes
#
#    Sunrise and Sunset:
#    Interval: 1 to 3 minutes
#
#    Seasonal Changes:
#    Interval: 1 hour to 1 day
#
##################################################


import cv2
import time
import os

# Configuration
camera_index = 1         # Which camera to use (can test with show_live_camera.py)
capture_interval = 5     # Interval in seconds between captures
total_duration = 60      # Total time to run the script (seconds)
warmup_frames = 2        # Number of frames to discard to allow webcam to adjust
brightness_value = 0.6   # Adjust the brightness (0.0 to 1.0)
exposure_value = -4      # Adjust the exposure (-1 for auto, negative for darker, positive for brighter)
output_dir = "timelapse_images"

def create_output_directory(directory):
    """Creates the directory to store captured images if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def warmup_camera(cap, warmup_frames):
    """Capture and discard initial frames to let the webcam adjust."""
    for _ in range(warmup_frames):
        ret, _ = cap.read()
        if not ret:
            print("Error during warm-up.")
            break
        time.sleep(0.1)  # Small delay between each frame

def capture_timelapse_images():
    """Capture time-lapse images from the webcam."""
    create_output_directory(output_dir)
    
    # Open the webcam (try different indices if needed)
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Adjust camera properties (brightness, exposure)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness_value)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
    
    # Warm up the camera by discarding initial frames
    print("Warming up the camera...")
    warmup_camera(cap, warmup_frames)

    start_time = time.time()
    image_count = 0
    
    while (time.time() - start_time) < total_duration:
        ret, frame = cap.read()  # Capture a frame
        
        if not ret:
            print("Failed to grab frame.")
            break
        
        # Save the captured frame as an image file
        img_name = os.path.join(output_dir, f"image_{image_count:04d}.jpg")
        cv2.imwrite(img_name, frame)
        print(f"Captured {img_name}")
        
        image_count += 1
        
        # Wait for the specified interval before capturing the next image
        time.sleep(capture_interval)
    
    # Release the webcam and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_timelapse_images()
