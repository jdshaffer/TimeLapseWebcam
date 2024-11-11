################################################################################
# Take time-lapse pictures using the WebCam  (Version 1.1)
# Code developed by Jeffrey D. Shaffer with assistance from Claude Sonnet
# 2024-11-11
#
# Requires the opencv-python module:
#    pip install opencv-python
#
# (You can also use the opencv-contrib-python module, but be WARNED,
#  you should not install both opencv-python and opencv-contrib-python,
#  as you're likely to encounter conflict errors.)
#
# Find the appropriate camera_index using the helper programs:
#    list_cameras.py
#    show_live_camera.py
#
# Interesting Capture Intervals
#      10 is good for clouds
#      30 is good for sunrises
#    3600 is maybe good for day-to-day changes ( 3600 = 1 hr)
#   86400 is maybe good for seasonal changes   (86400 = 1 day)
#
# Suggested Resolutions (width, height)
#     640, 480
#    1280, 960
#    1920, 1080 (Full HD)
#    3840, 2160 (4K)
#
################################################################################

import cv2
import time
import os
from datetime import datetime, timedelta
from datetime import time as dt_time

YES = 1
NO  = 0

# Configuration --------------------------------------------------------------------------------------
output_dir        = "timelapse_images"

camera_index      =   0     #  0 is default webcam on many computers, 1 on MacOS (probably)
exposure_value    = -11     # -4 for indoors seem good, -11 for outdoors, -10 for sunrise
capture_interval  =  60     # 60 seconds = 1 minute
resolution = 1920, 1080     # set the desired image size (width, height)

use_start_time    = YES     # YES = set the time yourself, NO = ignore start_time and start immediately
use_end_time      = YES     # YES = set the time yourself, NO = ignore end_time and use total_duration
pause_at_night    = YES     # YES = pause recording at set times, NO = record all night

total_duration    = 60      # seconds, ignored if use_end_time = YES
start_time = datetime(2024, 11, 12, 5, 30, 00)    # Set start time (yyyy, mm, dd, hh, mm, ss)
end_time   = datetime(2024, 11, 13, 5, 30, 00)    # Set   end time (yyyy, mm, dd, hh, mm, ss)
night_pause_from   = dt_time(21, 30)              # Stop   recording at 9:30pm
night_pause_until  = dt_time( 5, 00)              # Resume recording at 5:00am
# ----------------------------------------------------------------------------------------------------


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
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)


# Helper function to let the camera drop a few frames, helps with autofocus and autoexposure on some cameras
def warmup_camera(cap):
    for _ in range(2):    # Drop the first 2 frames (adjust as needed)
        ret, _ = cap.read()
        if not ret:
            print("Error during warm-up.")
            break
        time.sleep(0.1)  # Small delay between each drop frame


# Main function to capture images
def capture_timelapse_images(camera_index=0, capture_interval=15, exposure_value=-11, resolution=(640, 480)):
    # Set the output directory
    create_output_directory(output_dir)
    
    # Select the correct camera to use
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Set the exposure (set in the "configuration" section above)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
    
    # Discarding a few frames for cameras that need to auto adjust
    print("\nWarming up the camera...")
    warmup_camera(cap)

    # Start counting images at 0
    image_count = 0

    # While after start_time and before end_time record and write
    while datetime.now() < end_time:
    
        # Adding a feature to allow automatic pausing at night
        if pause_at_night:
            current_time = datetime.now().time()
            if current_time >= night_pause_from or current_time <= night_pause_until:
                time.sleep(60)  # Do nothing for one minute 
                continue

        # Capture a frame
        ret, frame = cap.read()
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
        
        # Increase the image count (as we took one)
        image_count += 1

        # Wait for the specified interval before capturing the next image
        time.sleep(capture_interval)
        
    # Release the webcam and close any OpenCV windows when done
    cap.release()
    cv2.destroyAllWindows()
    print("\nTime-lapse capture completed!\n")



if __name__ == "__main__":
    # Calculate an immediate start_time if use_start_time is turned off
    if use_start_time == NO:
        start_time = datetime.now()

    # Calculate the end_time if use_end_time is turned off and a duration is given
    if use_end_time == NO:
        end_time = calculate_end_time(start_time, total_duration)

    # Make sure the end_time comes after the start_time
    if end_time <= datetime.now():
        print("Error: End time must be in the future!")
        exit(1)

    # Display the start and stop times
    print(f" ")
    print(f"Starting at {start_time}")
    print(f"Ending   at {end_time}")
    print(f"Night pause is {'enabled from ' + night_pause_from.strftime('%H:%M') + ' to ' + night_pause_until.strftime('%H:%M') if pause_at_night else 'disabled'}\n")
    
    # Wait until it's time to start
    wait_until(start_time)
    
    # Start the camera capture with selected settings
    capture_timelapse_images(camera_index, capture_interval, exposure_value, resolution)
