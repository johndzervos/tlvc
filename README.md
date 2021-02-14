# TimeLapse Video Creator tlvc

Add the photos you want to combine in a 'photos' directory. Allowed extenstions are `.jpg` and `.png`
The photos are going to be added alphabetically in the video.
Keep in mind that `11.png` is before `2.png`, so either use leading zeros or strings to name the photos.

Examples:
* ./tlvc.py -a https://www.youtube.com/watch?v=5pOFKmk7ytU -s 18 -e 70
* ./tlvc.py -a audio.mp3 -s 18 -e 70
* ./tlvc.py -f 1

dependencies:
* pytube (pip install pytube)
* PIL (pip install image)
* mutagen (pip install mutagen)
* moviepy (pip install moviepy)
* resizeimage (pip install python-resize-image)
* pydub (pip install pydub)
  
This script will
TLVC (TimeLapse Video Creator) creates a timelapse video
out of the provided photos in the 'photos' directory.
The background audio can be passed either as a youtube url or
as an audio file. The duration of the clip can be determined
by the passed -s (--start) and -e (--end) arguments.
If no -s or -e is passed, the whole audio will be used.
If no audio is passed, fps can be determined through the -f (--fps)
argument. The default fps is 1 second.

Arguments:
-a <youtube url or .mp3 audiofile>
-s <start second of the audio>
-e <end second of the audio>
-f <fps>

The final video will be named `final.mp4`

Enjoy!
