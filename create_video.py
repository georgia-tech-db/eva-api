import cv2
import os
import numpy as np
from src.response import Response
from src.batch import Batch
from moviepy.editor import *

import pickle

PATH_TO_SAVE = "/videos/"

def create_video_from_frames(batch, name):
    video_name = name + '.mp4'
    input_path = "ua_detrac.mp4"
    vcap = cv2.VideoCapture(input_path)
 
    width = int(vcap.get(3))
    height = int(vcap.get(4))
    fps = vcap.get(5)
    print (width, height, fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') #codec
    video=cv2.VideoWriter(video_name, fourcc, fps, (width,height))
    
    frame_id = 0
    # Capture frame-by-frame
    ret, frame = vcap.read()  # ret = 1 if the video is captured; frame is the image
    df = batch.frames
    number_of_frames = 0
    while ret:
        temp = df[df.id == frame_id]
        if temp.size:
            image = cv2.UMat(np.array(frame, dtype=np.uint8))
            video.write(image)
            number_of_frames += 1

        frame_id+=1
        ret, frame = vcap.read()

    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 
    vcap.release()

    '''
    

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

    '''
    edit_video(video_name, fps)

    #delete video from root 
    os.remove(video_name)

def edit_video(name,fps = 30):
    video = VideoFileClip(name)
    if not os.path.exists(PATH_TO_SAVE):
        os.makedirs(PATH_TO_SAVE)
    video.write_videofile(PATH_TO_SAVE+name, fps = fps)
    video.close()
