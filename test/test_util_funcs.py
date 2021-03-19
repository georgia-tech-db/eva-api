from demo.utils import delete_old_video_files, create_video_from_frames
import unittest
import os
from src.batch import Batch
import pandas as pd
import numpy as np
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

        t = time.time()
        new_atime = t - 1000 
        new_mtime = t - 1000 
        os.utime("dataset/result.mp4", (new_atime, new_mtime))

        delete_old_video_files()
        self.assertFalse(os.path.exists("dataset/result.mp4"))

    def test_util_create_video_from_batch(self):
        dummy_batches = create_dummy_batches()
        create_video_from_frames(dummy_batches, "test")
        self.assertTrue(os.path.exists("dataset/test.mp4"))
        os.remove("dataset/test.mp4")
