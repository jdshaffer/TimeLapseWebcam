# A SIMPLE EXPLANATION

**`capture_timelapse.py`**

- this is the main file
- at runtime it asks the user for:
     - camera_index -- which camera to use, including virtual cameras
     - capture_interval -- how long to wait between captured pictures in seconds
     - exposure_value -- the camera exposure value, I didn't have any luch with auto exposure so far
     - camera resolution to use
     - total_duration -- how long to record in total second

---

**`convert_to_movie.py`**

- converts the savesd jpg files to an mp4 movie

---

**`list_cameras.py`**

- a little helper program that checked how many cameras (real and virtual) a system has available

---

**`show_live_camera.py`**

- another little helper program that shows a live video feed for the specified camera (to double-check you have the right one)
- at runtime it asks the user for:
     - camera_index -- which camera to use, including virtual cameras
     - exposure_value -- the camera exposure value, I didn't have any luch with auto exposure so far
     - camera resolution to use

---

### USE

Simply run all of these using `python3 PROGRAM_NAME.py`

You will need OpenCV installed as well:
`pip install opencv-python`

Happy tinkering!

Jds
