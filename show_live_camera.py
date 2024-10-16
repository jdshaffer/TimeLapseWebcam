##################################################
# Show live WebCam video feed using OpenCV
# Jeffrey D. Shaffer
# 2024-10-16
#
# Requires this python module:
#    pip install opencv-python
#
# CAMERA INDEX (My own notes)
#    MBA Camera is value 1
#    MiniPC Camera is 0
#
# EXPOSURE VALUE (My own notes)
#    -11 works for MiniPC on cloudy day
#
##################################################


import cv2

def get_resolution(option):
    if option == 0:
        return 640, 480
    elif option == 1:
        return 1280, 960
    elif option == 2:
        return 1920, 1080  # Full HD
    elif option == 3:
        return 3840, 2160  # 4K
    else:
        print("Invalid option. Defaulting to 640x480.")
        return 640, 480

def show_camera(camera_index=0, exposure_value=-4, resolution=(640, 480)):
    cap = cv2.VideoCapture(camera_index)  # Open the camera
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}.")
        return

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])   # Set width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])  # Set height

    # Turn on Autofocus
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    # Set the exposure (the value might need tuning based on your camera)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)

    while True:
        ret, frame = cap.read()  # Capture frame-by-frame
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        cv2.imshow(f'Camera {camera_index}', frame)  # Display the frame

        # Exit the window when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Get camera index from the user
    camera_index = int(input("Enter camera index to show: "))

    # Get exposure value from the user    
    exposure_value = float(input("Enter exposure value (try -4 to 0 for lower exposure): "))

    # Get resolution choice from the user
    print("Select resolution:")
    print("0: 640x480")
    print("1: 1280x960")
    print("2: 1920x1080 (Full HD)")
    print("3: 3840x2160 (4K)")
    
    resolution_option = int(input("Enter your choice (0-3): "))
    resolution = get_resolution(resolution_option)

    # Start the camera with selected settings
    show_camera(camera_index, exposure_value, resolution)
    
