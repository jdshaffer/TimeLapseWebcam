######################################################################################
# Use the WebCam to take time-lapse pictures and convert them to an mp4 video (v1.2)
# Code developed by Jeffrey D. Shaffer with assistance from Claude Sonnet
# 2024-11-13
#
# Requires the opencv-python module:
#    pip install opencv-python
#
# Change the settings found in Configuration to suit your needs.
#
######################################################################################

import cv2
import time
import os
from datetime import datetime, timedelta
from datetime import time as dt_time

YES = 1
NO  = 0

# Configuration --------------------------------------------------------------------------------------
camera_index      =   0     #  0 is default webcam on many computers, 1 on MacOS (probably)
exposure_value    = -11     # -4 for indoors seem good, -11 for outdoors, -10 for sunrise
capture_interval  =  60     # 60 seconds = 1 minute
resolution = 1920, 1080     # set the desired image size (width, height)

use_start_time    = YES     # YES = set the time yourself, NO = ignore start_time and start immediately
use_end_time      = YES     # YES = set the time yourself, NO = ignore end_time and use total_duration
automatic_pause   =  NO     # YES = pause recording during set times, NO = record as normal
create_output_video = YES   # YES = automatically convert saved images to final video

total_duration    = 600                              # seconds, ignored if use_end_time = YES
start_time   = datetime(2024, 11, 14,  5, 30, 00)    # Set start time (yyyy, mm, dd, hh, mm, ss)
end_time     = datetime(2024, 11, 15, 18, 00, 00)    # Set   end time (yyyy, mm, dd, hh, mm, ss)
pause_from   = dt_time(21, 30)                       # Stop   recording at (mm, ss)
pause_until  = dt_time( 5, 00)                       # Resume recording at (mm, ss)

image_folder  = "timelapse_images"                   # Folder to save captured images
video_folder  = "timelapse_video"                    # Folder to save the completed video
output_video = os.path.join(video_folder, "timelapse_video.mp4")  # Output video path and filename
video_fps = 30                                       # Frames per second for output video
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
def create_image_folderectory(directory):
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
    create_image_folderectory(image_folder)
    
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
    
        # Pause recording if automatic_pause is turned on
        if automatic_pause:
            current_time = datetime.now().time()
            
            # Test to see if the pause crosses midnight
            if pause_from <= pause_until:
                # Simple case: pause doesn't cross midnight
                should_pause = pause_from <= current_time <= pause_until
            else:
                # Complex case: pause period crosses midnight
                should_pause = current_time >= pause_from or current_time <= pause_until
            
            if should_pause:   # If it is currently time to pause
                print(f"Pausing image capture from {pause_from} until {pause_until}")
                time.sleep(60)  # Do nothing for one minute and loop
                continue

        # Capture a frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
            
        # Save the captured frame as an image file
        img_name = os.path.join(image_folder, f"image_{image_count:04d}.jpg")
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
    print("\nTime-lapse capture complete.")


# Function to convert saved images to an output video
def create_video_from_images(image_folder, output_video, video_fps):
    # Let user know we've moved from image capture to video creation
    print(f"Converting timelapse images to video...")

    # Check if output folder exists, create it if not
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # Get the list of images in the folder and sort them by filename
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort()  # Ensure the images are in order

    if len(images) == 0:
        print("No images found in the folder.")
        return

    # Read the first image to get the dimensions (height, width)
    first_image_path = os.path.join(image_folder, images[0])
    first_frame = cv2.imread(first_image_path)
    height, width, layers = first_frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 video
    video = cv2.VideoWriter(output_video, fourcc, video_fps, (width, height))

    # Add each image to the video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)  # Add the frame to the video

    # Release the video writer
    video.release()
    print(f"Video saved as {output_video}\n")



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
    print(f"Ending   at {end_time}\n")
    print(f"Pause {'enabled from ' + pause_from.strftime('%H:%M') + ' to ' + pause_until.strftime('%H:%M') if automatic_pause else 'disabled'}\n")
    
    # Wait until it's time to start
    wait_until(start_time)
    
    # Start the camera capture with selected settings
    capture_timelapse_images(camera_index, capture_interval, exposure_value, resolution)

    # Convert the saved images to an output video (mp4)
    if create_output_video:
        create_video_from_images(image_folder, output_video, video_fps)
