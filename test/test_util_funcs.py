from demo.demo_api import RequestFrames
from demo.demo_api import app
from demo.utils import delete_old_video_files, create_video_from_frames, edit_video
import unittest
from unittest.mock import patch
import asyncio
import re
import os
from demo.demo_api import create_query
from src.batch import Batch
import pandas as pd
import numpy as np
from src.response import Response
import glob
import json
import time

def create_dummy_batches(num_frames=10, start_id=0):
    data = []
    for i in range(num_frames):
        data.append({'id': i + start_id,
                     'data': np.array(
                         np.ones((2, 2, 3)) * float(i + 1) * 25,
                         dtype=np.uint8)})
    return Batch(pd.DataFrame(data))

class TestUtilFuncs(unittest.TestCase):
    def setUp(self):
        pass

    def test_util_delete_old_video_files(self):
        with open("dataset/result.mp4", "wb+") as f:
            f.write(b"Test")

        atime = os.stat("dataset/result.mp4").st_atime
        mtime = os.stat("dataset/result.mp4").st_mtime#modification time

        t = time.time()
        new_atime = t - 1000 #new modification time
        new_mtime = t - 1000 #new modification time
        os.utime("dataset/result.mp4", (new_atime, new_mtime))

        #modify the file timestamp
        delete_old_video_files()
        self.assertFalse(os.path.exists("dataset/result.mp4"))

    def test_util_create_video_from_batch(self):
        dummy_batches = create_dummy_batches()
        create_video_from_frames(dummy_batches, "test")
        self.assertTrue(os.path.exists("dataset/test.mp4"))
        os.remove("dataset/test.mp4")
