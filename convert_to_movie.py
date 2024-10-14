##########################################################
# Take a series of JPG images and turn into an MP4 video
# Created by ChatGPT, corrected by Jds
# 2024-10-13
#
# requires this python module:
#    pip install opencv-python
#
##########################################################


import cv2
import os

# Configuration
image_folder = "timelapse_images"    # Folder containing the sequence of images
output_folder = "timelapse_video"    # Folder to save the output video
output_video = os.path.join(output_folder, "timelapse_video.mp4")  # Output video file path
fps = 30  # Frames per second for the video

def create_video_from_images(image_folder, output_video, fps):
    # Check if output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Add each image to the video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)  # Add the frame to the video

    # Release the video writer
    video.release()
    print(f"Video saved as {output_video}")

if __name__ == "__main__":
    create_video_from_images(image_folder, output_video, fps)
