# Time Lapse Webcam (Brief Introduction)

**`capture_timelapse.py`**

* The main program that uses a webcam to capture time-lapse images which are then saved as individual jpg files.
* All of the camera, timing, and output options can be set within the "configuration" section of the program.
* Configurable items (found in the configuration section):
	* `camera_index` -- which camera to use, including virtual cameras
	* `exposure_value` -- the camera exposure value
	* `capture_interval` -- how long to wait, in seconds, between captured images
	* `resolution` -- which camera resolution to use when capturing images (suggested resolutions given in the program comments)
	* -------
	* `use_start_time` -- YES uses the `start_time` given, NO starts immediately
	* `use_end_time` -- YES uses the `end_time` given, NO uses the `total_duration` given
	* `automatic_pause` -- YES pauses the recording during the times specified in the settings `pause_from` and `pause_until`, NO records as normal
	* `create_output_video` -- YES will automatically convert the saved images to an MP4 video (leaving the saved images intact), NO will not create a movie 
	* -------
	* `total_duration` -- how long, in seconds, to record
	* `start_time` -- the user specified start time (yyyy, mm, dd, hh, mm, ss)
	* `end_time` -- the user specified end time (yyyy, mm, dd, hh, mm, ss)
	* `pause_from` -- the user specified time to pause recording at night (hh, mm, ss)
	* `pause_until` -- the user specified time to resume recording at night (hh, mm, ss)
	* -------
	* `image_folder` -- the folder in which to save the captured images
	* `video_folder` -- the folder in which to save the completed video
	* `output_video` -- the output video path and filename to use
	* `video_fps` -- the desired frame-rate (fps) for output video

---

**`convert_to_movie.py`**

* This program is unnecessary if the user turns on `create_output_video` in the main program.
* However, for the times when the user does NOT want to automatically create the output video, the user can run this simple program to convert the saved images to an mp4 video. (This is literally the same code used inside the main program.)
* This little helper program is ideal for when the user would like to cull some of the saved images before converting to video.
* If the user has not changed the output directories or filenames, then they can run this program with the following command: `python3 convert_to_movie.py`

---

### RUNNING THE CAPTURE PROGRAM

To run the image capture program, simply use the following command:  `python3 capture_timelapse.py`

Note: You will need OpenCV installed for these programs to work: `pip install opencv-python`

Happy tinkering! -- Jds
