#############################################################
# Simply program using OpenCV to look for available cameras
# Jeffrey D. Shaffer
# 2024-10-16
#
# Requires this python module:
#    pip install opencv-python
#
#############################################################

import cv2

def list_camera_sources(max_cameras=10):
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            available_cameras.append({
                'index': i,
                'width': width,
                'height': height,
                'fps': fps
            })
            cap.release()
    return available_cameras

if __name__ == "__main__":
    cameras = list_camera_sources()
    if cameras:
        for cam in cameras:
            print(f"Camera {cam['index']} - Resolution: {cam['width']}x{cam['height']}, FPS: {cam['fps']}")
    else:
        print("No cameras found.")
