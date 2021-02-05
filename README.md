# TimeLapse Video Creator tlvc

Add the photos you want to combine in a 'photos' directory. Allowed extenstions are `.jpg` and `.png`
The photos are going to be added alphabetically in the video.
Keep in mind that `11.png` is before `2.png`, so either use leading zeros or strings to name the photos.

Run the script with `python tlvc.py`

dependencies:
* pytube (pip install pytube)
* PIL (pip install image)
* mutagen (pip install mutagen)
* moviepy (pip install moviepy)

Arguments:
  * youtube video url: the youtube video you want to have as background audio
  * start: the start where you want to trim this video
  * end: the end where you want to trim the video
  
This script will
  * Download and trim the youtube video, and extract its audio file
  * Resize the input photos to a fixed width, keep the aspect ratio and place the resized photos in a new folder
  * Calculate the duration of the appearance of each photo by dividing duration of the audio with the number of photos
  * Combine the resized photos in a video and add the downloaded audio

The final video will be named `final.mp4`

Enjoy!
