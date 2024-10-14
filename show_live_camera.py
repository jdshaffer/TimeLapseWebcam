import cv2

def show_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)  # Open the camera
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}.")
        return
    
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
    camera_index = int(input("Enter camera index to show: "))  # Get camera index from user
    show_camera(camera_index)
    