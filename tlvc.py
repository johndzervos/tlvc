import os
import moviepy.video.io.ImageSequenceClip
from PIL import Image
from mutagen.mp3 import MP3

def is_valid_image(image):
  return image.endswith(".jpg") or image.endswith(".png")

def resize_images(image_files):
  """
  ImageSequenceClip requires images of the same size.
  """
  for image_file in image_files:
    print(image_file)
    image = Image.open(image_file)
    new_image = image.resize((920, 768))
    new_image.save(image_file)


def create_timelapse_video(image_folder, fps, output_name):
  """
  Sorts the photos of a directory and combines them to create the video
  """
  image_files = [image_folder+'/'+img for img in sorted(os.listdir(image_folder)) if is_valid_image(img)]
  resize_images(image_files)
  clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
  clip.write_videofile(output_name + '.mp4')

image_folder = 'photos'
audio = MP3("happy.mp3")
audio_duration = audio.info.length
print(audio_duration)
number_of_photos = len(os.listdir(image_folder))
print(number_of_photos)
fps = number_of_photos / audio_duration
print(fps)
create_timelapse_video(image_folder, fps, 'output')

