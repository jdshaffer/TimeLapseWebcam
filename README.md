# Time Lapse Webcam (Brief Introduction)

**`capture_timelapse.py`**

* The main program that captures webcam images to individual jpg files
* Nearly all the options are set inside the program in a "configuration" section.
* Configurable items:
	* `output_dir` -- where to save images
	* `camera_index` -- which camera to use, including virtual cameras
	* `exposure_value` -- the camera exposure value
	* `capture_interval` -- how long to wait between captured pictures in seconds
	* `use_start_time` -- YES uses the `start_time` given, NO starts immediately
	* `use_end_time` -- YES uses the `end_time` given, NO uses the `total_duration` given
	* `total_duration` -- how long, in seconds, to record (used if `use_end_time` is NO)
	* `start_time` -- the user specified start time (yyyy, mm, dd, hh, mm, ss)
	* `end_time` -- the user specified end time (yyyy, mm, dd, hh, mm, ss)

* At runtime it asks the user for a resolution to record at
	*  (1)  640x480
	*  (2) 1280x960
	*  (3) 1920x1080 (Full HD)
	*  (4) 3840x2160 (4K)

--

**`convert_to_movie.py`**

* A program to convert the saved jpg files to an mp4 movie

--

**`list_cameras.py`**

* A small helper program that lists all the available cameras (real and virtual) a system has

--

**`show_live_camera.py`**

* A small helper program that shows a live video feed for the specified camera
* This helps the user check that they have the correct camera and settings
* at runtime it asks the user for:
	* camera_index -- which camera to use
	* exposure_value -- the camera exposure value
		* -4 seems good for indoors
		* -10 seems good for sunrise
		* -11 seems good for outdoors
		* I didn't have any luck getting auto exposure to work
	* which camera resolution to use:
		*  (1)  640x480
		*  (2) 1280x960
		*  (3) 1920x1080 (Full HD)
		*  (4) 3840x2160 (4K)

--

### RUNNING THE PROGRAMS

Simply run all of these using the command:  `python3 PROGRAM_NAME.py`

You will need OpenCV installed for them to work: `pip install opencv-python`

Happy tinkering! -- Jds
