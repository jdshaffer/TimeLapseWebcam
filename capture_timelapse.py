##################################################
# Take time-lapse pictures with the WebCam
# Jeffrey D. Shaffer
# 2024-10-16
#
# Requires this python module:
#    pip install opencv-python
#
# CAMERA INDEX (My own notes)
#    MBA Camera is value 1
#    iPhone as wireless camera is value 2
#    MiniPC Camera is 0
#
# EXPOSURE VALUE (My own notes)
#    -11 works for MiniPC on cloudy day
#
# SUGGESTED TIMINGS
#    Fast Cloud Movement
#    Interval: 15s
#
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
output_dir = "timelapse_images"

# Helper function to create the output directory
def create_output_directory(directory):
    # Create the directory to store captured images if it doesn't exist.
    if not os.path.exists(directory):
        os.makedirs(directory)

# Helper function to let the camera drop a few frames, helps with autofocus and autoexposure on some cameras
def warmup_camera(cap):
    # Capture and discard initial frames to let the webcam adjust.
    for _ in range(2):    # Set to drop the first 2 frames, you can adjust this as you need
        ret, _ = cap.read()
        if not ret:
            print("Error during warm-up.")
            break
        time.sleep(0.1)  # Small delay between each frame

# Helper fuction to ask user for desired capture resolution
def get_resolution(option):
    if option == 1:
        return 640, 480
    elif option == 2:
        return 1280, 960
    elif option == 3:
        return 1920, 1080  # Full HD
    elif option == 4:
        return 3840, 2160  # 4K
    else:
        print("Invalid option. Defaulting to 640x480.")
        return 640, 480

# Main function to capture images
def capture_timelapse_images(camera_index=0, capture_interval=15, exposure_value=-11, resolution=(640, 480), total_duration=60):
    # Set the output directory
    create_output_directory(output_dir)
    
    # Open the webcam (run helper program "list_cameras.py" or "show_live_camera.py" to discover the correct index)
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Set the camera resolution (the user is prompted below)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])   # Set width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])  # Set height

    # Turn on Autofocus (manual focus didn't work for me)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    # Set the exposure (the user is prompted below)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
    
    # "Warm up" the camera by discarding initial frames
    print("Warming up the camera...")
    warmup_camera(cap)

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
    # Get camera index from the user
    camera_index = int(input(" Enter camera index to record: "))

    # Get exposure value from the user    
    exposure_value = float(input(" Enter exposure value: "))

    # Get resolution choice from the user
    print(" Select resolution:")
    print(" (1)  640x480")
    print(" (2) 1280x960")
    print(" (3) 1920x1080 (Full HD)")
    print(" (4) 3840x2160 (4K)")

    resolution_option = int(input(" Enter your choice (0-3): "))
    resolution = get_resolution(resolution_option)

    # Get capture interval (in seconds) from the user
    capture_interval = float(input(" Enter how over to capture images (every X seconds): "))

    # Get total capture duration (in seconds) from the user
    total_duration = float(input(" Enter the capture duration (capture for X seconds in total): "))

    # Start the camera capture with selected settings
    capture_timelapse_images(camera_index, capture_interval, exposure_value, resolution, total_duration)
