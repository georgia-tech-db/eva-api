import cv2
import os, time, sys
import numpy as np
from src.response import Response
from src.batch import Batch
from moviepy.editor import *
import pathlib
from config import DATASET_DIR

def create_video_from_frames(batch, name):

    video_name = name + '.mp4'
    
    first_frame = np.array(batch.frames['data'][0])
    height, width, layers = first_frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))  
  
    # Appending the images to the video one by one 
    for frame in batch.frames['data']:
        image = cv2.UMat(np.array(frame, dtype=np.uint8))
        video.write(image)  
      
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 

    duration = len(batch.frames['data'])
    print(duration)
    edit_video(video_name, duration)

def edit_video(name, duration):
    video = VideoFileClip(name).set_duration(duration)
    filename = str(DATASET_DIR / name )
    video.write_videofile(filename, fps = 30)
    video.close()


def delete_old_video_files():
    now = time.time()
    for f in os.listdir(DATASET_DIR):
        f = os.path.join(DATASET_DIR, f)
        if os.stat(f).st_mtime < now - 900:
            if os.path.isfile(f):
                os.remove(f)
	
