import cv2
import os
import numpy as np
from src.response import Response
from src.batch import Batch
from moviepy.editor import *

def create_video_from_frames(batch, video_name):
    
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

    return video_name

def edit_video(name, duration):
    video = VideoFileClip(name).set_duration(duration)
    video.write_videofile("/home/vivian/eva-ui/public/videos/"+name, fps = 30)
    video.close()

	
