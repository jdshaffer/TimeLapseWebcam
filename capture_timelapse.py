##################################################
# Take time-lapse pictures using the WebCam
# Jeffrey D. Shaffer
# 2024-10-17
#
# Requires this python module:
#    pip install opencv-python
#
# TO DO
#    - double-check all is OK with changes
#    - make configuration easier to read / use
#
##################################################

import cv2
import time
import os
from datetime import datetime, timedelta


# Configuration
output_dir       = "timelapse_images"
camera_index     = 0    # find using helper programs "list_cameras.py" or "show_live_camera.py"
exposure_value   = -4   # -11 for outdoors, -4 for indoors seem good
capture_interval = 1    # in seconds -- 10 seems good for clouds
total_duration   = 10    # in seconds -- set to 0 to specify an end_time below
start_time = datetime.now()  # to start right away
#start_time = datetime(2024, 10, 18, 14, 4, 30)   # Set start time (yyyy, mm, dd, hh, mm, ss)
end_time = datetime(2024, 10, 18, 14, 31, 40)      # Set end   time (yyyy, mm, dd, hh, mm, ss)


# Helper program to calculate end time based on start time and duration
def calculate_end_time(start_time, duration_seconds):
    return start_time + timedelta(seconds=duration_seconds)


# Helper function to wait until a specified time to start
def wait_until(target_time):
    while True:
        now = datetime.now()
        if now >= target_time:
            break
        time.sleep(1)  # Check every second


# Helper function to create the output directory
def create_output_directory(directory):
    # Create the directory to store captured images if it doesn't exist.
    if not os.path.exists(directory):
        os.makedirs(directory)


# Helper function to let the camera drop a few frames, helps with autofocus and autoexposure on some cameras
def warmup_camera(cap):
    for _ in range(2):    # Set to drop the first 2 frames, adjust as needed
        ret, _ = cap.read()
        if not ret:
            print("Error during warm-up.")
            break
        time.sleep(0.1)  # Small delay between each drop frame


# Helper function to ask user for desired capture resolution
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
def capture_timelapse_images(camera_index=0, capture_interval=15, exposure_value=-11, resolution=(640, 480)):
    # Set the output directory
    create_output_directory(output_dir)
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Turn on Autofocus (manual focus didn't work for me)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    # Set the exposure (set in the "configuration" section above)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
    
    # "Warm up" the camera by discarding initial frames
    print("\nWarming up the camera...")
    warmup_camera(cap)

    image_count = 0
    
    while datetime.now() < end_time:
        ret, frame = cap.read()  # Capture a frame
        if not ret:
            print("Failed to grab frame.")
            break
            
        # Save the captured frame as an image file
        img_name = os.path.join(output_dir, f"image_{image_count:04d}.jpg")
        cv2.imwrite(img_name, frame)
        
        # Calculate and display remaining time
        time_remaining = end_time - datetime.now()
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Captured {img_name} (Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d})")
        
        image_count += 1
        # Wait for the specified interval before capturing the next image
        time.sleep(capture_interval)
        
    # Release the webcam and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("\nTime-lapse capture completed!\n")



if __name__ == "__main__":
    # Calculate end time from the duration, but only if a duration was specified
    if total_duration != 0:
        end_time = calculate_end_time(start_time, total_duration)

    # Validate end time
    if end_time <= datetime.now():
        print("Error: End time must be in the future!")
        exit(1)
        
    # Calculate and display total duration
    total_duration = end_time - datetime.now()
    hours, remainder = divmod(total_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Ask user for desired resolution
    print("\nSelect resolution:")
    print("   (1)  640x480")
    print("   (2) 1280x960")
    print("   (3) 1920x1080 (Full HD)")
    print("   (4) 3840x2160 (4K)")
    resolution_option = int(input("Enter your choice (1-4): "))
    resolution = get_resolution(resolution_option)

    # Wait until the set time to start
    print(f" ")
    print(f"Starting at {start_time}")
    print(f"Ending   at {end_time}")
    wait_until(start_time)
    
    # Start the camera capture with selected settings
    capture_timelapse_images(camera_index, capture_interval, exposure_value, resolution)
