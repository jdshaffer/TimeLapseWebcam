Simply put (for now):

capture_timelapse.py
- main file
- adjust the settings in the file to select the correct camera (if more than one) and select the desired interval and duration

convert_to_movie.py
- converts the saves jpg files to mp4

list_cameras.py
- a little helper program that checked how many cameras (real and virtual) a system has available

show_live_camera.py
- another little helper program that shows a live video feed for the specified camera (to double-check you have the right one


Simply run all of these using "Python3 PROGRAM_NAME.py"
You will need OpenCV installed as well:
     pip install opencv-python


Happy tinkering!
Jds
