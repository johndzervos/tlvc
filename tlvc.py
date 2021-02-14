#!/usr/bin/env python
import os
import sys, getopt
import pytube
import requests
from PIL import Image, ImageOps
from mutagen.mp3 import MP3
from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, concatenate
from resizeimage import resizeimage
from pydub import AudioSegment

BACKGROUND_VIDEO_NAME = "background_music.mp4"
BACKGROUND_MUSIC_NAME = "background_music.mp3"
IMAGE_SUFFIX = ".jpg"
IMAGE_FOLDER = "photos"
RESIZED_IMAGE_FOLDER = "resized_photos"
AUDIO_FOLDER = "audio_files"

FINAL_VIDEO_NAME = "final.mp4"

def download_and_trim_youtube_video(url, start, end):
  """
  Downloads the youtube video and trims it.
  """
  print("Downloading video...")
  # Check if AUDIO_FOLDER exists, otherwise create it
  if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)
  video = pytube.YouTube(url).streams.first().download(AUDIO_FOLDER)
  if start is not None or end is not None:
    result_video = VideoFileClip(video).subclip(start, end)
  else:
    result_video = VideoFileClip(video)
  result_video.write_videofile(f"{AUDIO_FOLDER}/{BACKGROUND_VIDEO_NAME}")

def trim_audio_file(audio_file, start, end):
  """
  Trims the mp3, if the start and end are valid.
  """
  try:
    audio = MP3(audio_file)
    if start > audio.info.length or end > audio.info.length:
      print("Invalid start or end for the audio. The whole audio is going to be used.")
      audio = AudioSegment.from_mp3(audio_file)
      audio.export(f"{AUDIO_FOLDER}/{BACKGROUND_MUSIC_NAME}", format="mp3")
    else:
      audio = AudioSegment.from_mp3(audio_file)
      extract = audio[start * 1000:end * 1000]
      # Saving
      extract.export(f"{AUDIO_FOLDER}/{BACKGROUND_MUSIC_NAME}", format="mp3")  
  except:
    print("Could not trim audio file! The whole audio file is going to be used!")
    audio = AudioSegment.from_mp3(audio_file)
    audio.export(f"{AUDIO_FOLDER}/{BACKGROUND_MUSIC_NAME}", format="mp3")  

def convert_mp4_to_mp3():
  """
  Get an mp4 and return an mp3
  """
  videoclip = VideoFileClip(f"{AUDIO_FOLDER}/{BACKGROUND_VIDEO_NAME}")
  audioclip = videoclip.audio
  audioclip.write_audiofile(f"{AUDIO_FOLDER}/{BACKGROUND_MUSIC_NAME}")

def is_valid_image(image):
  """
  Checks the validity fo the images.
  Accepts only .jpg and .png images for now.
  """
  return image.endswith(".jpg") or image.endswith(".png")

def resize_images(image_files):
  """
  Resize images to a fixed width and keep the aspect ratio.
  Save the resized images in RESIZED_IMAGE_FOLDER and name them with leading zeros
  in order to combine them alphabetically later
  """
  print("Resizing images...")
  image_width = 500
  image_counter = 1
  # Check if RESIZED_IMAGE_FOLDER exists, otherwise create it
  if not os.path.exists(RESIZED_IMAGE_FOLDER):
    os.makedirs(RESIZED_IMAGE_FOLDER)
  for image_file in image_files:
    resized_name = f"{RESIZED_IMAGE_FOLDER}/{image_counter:03d}{IMAGE_SUFFIX}"
    img = Image.open(image_file)
    img = resizeimage.resize_height(img, image_width)
    # This is necessary for jpg photos, to avoid unexpected rotation
    img = ImageOps.exif_transpose(img)
    
    img.save(resized_name)
    image_counter+=1

def calculcate_fps():
  """
  Calculate the seconds per frame, by dividing the background video duration with with the number
  of the photos in the IMAGE_FOLDER directory.
  Returns fps which is 1/seconds_per_frame
  """
  audio = MP3(f"{AUDIO_FOLDER}/{BACKGROUND_MUSIC_NAME}")
  audio_duration = audio.info.length
  print("Audio duration: ", audio_duration)

  number_of_photos = len(os.listdir(IMAGE_FOLDER))
  print("Number of photos: ", number_of_photos)
  # Seconds per frame:
  spf = audio_duration / number_of_photos
  
  print("Seconds per frame: ", spf)
  # Return fps = 1 / spf
  return 1 / spf

def create_timelapse_video(fps, has_audio):
  """
  Sorts the photos of a directory and combines them to create the video
  """
  image_files = [
      f"{IMAGE_FOLDER}/{img}"
      for img in sorted(os.listdir(IMAGE_FOLDER))
      if is_valid_image(img)
  ]
  resize_images(image_files)
  resized_images = [
      f"{RESIZED_IMAGE_FOLDER}/{img}"
      for img in sorted(os.listdir(RESIZED_IMAGE_FOLDER))
  ]

  image_clips = []
  for img in resized_images:
    ic = ImageClip(img).set_duration(1/fps)
    image_clips.append(ic)

  video = concatenate(image_clips, method="compose")
  if has_audio:
    video_with_new_audio = video.set_audio(AudioFileClip(f"{AUDIO_FOLDER}/{BACKGROUND_MUSIC_NAME}")) 
    video_with_new_audio.write_videofile(FINAL_VIDEO_NAME, fps=fps, codec="mpeg4")
  else:
    video.write_videofile(FINAL_VIDEO_NAME, fps=fps, codec="mpeg4")

def main(argv):
  audio_file = None
  # Defaults to 1 second per frame
  fps = 1
  trim_start = None
  trim_end = None

  arguments_help = """
  tlvc.py
    -h help
    -a <youtube url or .mp3 audiofile>
    -s <start second of the audio>
    -e <end second of the audio>
    -f <fps>
  """

  help_text = f"""
    TLVC (TimeLapse Video Creator) creates a timelapse video
    out of the provided photos in the 'photos' directory.
    The background audio can be passed either as a youtube url or
    as an audio file. The duration of the clip can be determined
    by the passed -s (--start) and -e (--end) arguments.
    If no -s or -e is passed, the whole audio will be used.
    If no audio is passed, fps can be determined through the -f (--fps)
    argument. The default fps is 1 second.
    Examples:
    * ./tlvc.py -a https://www.youtube.com/watch?v=5pOFKmk7ytU -s 18 -e 70
    * ./tlvc.py -a audio.mp3 -s 18 -e 70
    * ./tlvc.py -f 1

    {arguments_help}
  """

  try:
    opts, args = getopt.getopt(argv,"h:a:s:e:f:",["help", "audio=", "start=", "end=", "fps="])
  except getopt.GetoptError:
    print(arguments_help)
    sys.exit(2)
  for opt, arg in opts:
    if opt in ["-h", "--help"]:
      print(help_text)
      sys.exit()
    elif opt in ["-a", "--audio-file"]:
      audio_file = arg
      print(f"audio file: {arg}")
    elif opt in ["-s", "--start"]:
      trim_start = float(arg)
    elif opt in ["-e", "--end"]:
      trim_end = float(arg)
    elif opt in ["-f", "--fps"]:
      if audio_file is not None:
        fps = float(arg)
      else:
        print("Audio file duration is going to determine the fps!")

  if audio_file is not None:
    if audio_file.endswith(".mp3"):
      trim_audio_file(audio_file, trim_start, trim_end)
      fps = calculcate_fps()
    elif requests.get(audio_file).status_code == 200:  
      download_and_trim_youtube_video(audio_file, trim_start, trim_end)
      convert_mp4_to_mp3()
      fps = calculcate_fps()
    else:
      print("Unknown audio file")
      audio_file = None
  has_audio = audio_file is not None

  create_timelapse_video(fps, has_audio)

if __name__ == "__main__":
   main(sys.argv[1:])
