import os
import moviepy.video.io.ImageSequenceClip
from PIL import Image
from mutagen.mp3 import MP3
import pytube
from moviepy.editor import *

BACKGROUND_VIDEO_NAME = "background_music.mp4"
BACKGROUND_MUSIC_NAME = "background_music.mp3"

def download_and_trim_youtube_video(url, start, end):
  print("Downloading video...")
  video = pytube.YouTube(url).streams.first().download()
  result_video = VideoFileClip(video).subclip(start, end)
  result_video.write_videofile(BACKGROUND_VIDEO_NAME)
  return result_video

def convert_mp4_to_mp3():
  """
  Get an mp4 and return an mp3
  """
  videoclip = VideoFileClip(BACKGROUND_VIDEO_NAME)
  audioclip = videoclip.audio
  audioclip.write_audiofile(BACKGROUND_MUSIC_NAME)

def is_valid_image(image):
  return image.endswith(".jpg") or image.endswith(".png")

def resize_images(image_files):
  """
  ImageSequenceClip requires images of the same size.
  """
  print("Resizing images...")
  image_counter = 1
  for image_file in image_files:
    print(image_file)
    mywidth = 1000
    # Resize and keep the aspect ratio
    img = Image.open(image_file)
    wpercent = (mywidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((mywidth,hsize), Image.ANTIALIAS)
    img.save(resized_image_folder + '/' +str(image_counter) + '.jpg')
    image_counter+=1

def create_timelapse_video(image_folder, fps, output_name):
  """
  Sorts the photos of a directory and combines them to create the video
  """
  image_files = [image_folder+'/'+img for img in sorted(os.listdir(image_folder)) if is_valid_image(img)]
  resize_images(image_files)
  resized_images = [resized_image_folder+'/'+img for img in sorted(os.listdir(resized_image_folder)) if is_valid_image(img)]

  image_clips = []
  for img in resized_images:
    print(img)
    if not os.path.exists(img):
        raise FileNotFoundError(img)
    ic = ImageClip(img).set_duration(1/fps)
    image_clips.append(ic)

  video = concatenate(image_clips, method="compose")
  video_with_new_audio = video.set_audio(AudioFileClip(BACKGROUND_MUSIC_NAME)) 
  video_with_new_audio.write_videofile("final.mp4", fps=fps, codec="mpeg4")

image_folder = 'photos'
resized_image_folder = 'resized_photos'
output_name = 'output'
youtube_url = 'https://www.youtube.com/watch?v=h-Pws1-YzOo'
trim_start = 10
trim_end = 30

result_video = download_and_trim_youtube_video(youtube_url, trim_start, trim_end)
convert_mp4_to_mp3()

audio = MP3(BACKGROUND_MUSIC_NAME)
audio_duration = audio.info.length
print("Audio duration: ", audio_duration)

number_of_photos = len(os.listdir(image_folder))
print("Number of photos: ", number_of_photos)
fps = number_of_photos / audio_duration
print("FPS: ", fps)

create_timelapse_video(image_folder, fps, 'output')

