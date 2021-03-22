from demo.utils import delete_old_video_files, create_video_from_frames
import unittest
import os
from src.batch import Batch
import pandas as pd
import numpy as np
import time
import re
from demo.demo_api import create_query, create_load_query, \
    generate_video_name, get_frames
from unittest.mock import patch
from src.response import Response
import asyncio


def create_dummy_batches(num_frames=10, start_id=0):
    data = []
    for i in range(num_frames):
        data.append({'id': i + start_id,
                     'data': np.array(
                         np.ones((2, 2, 3)) * float(i + 1) * 25,
                         dtype=np.uint8)})
    return Batch(pd.DataFrame(data))


class MockCursor:
    async def fetch_one_async(self):
        batch = create_dummy_batches(num_frames=1)
        return Response(200, batch)

    async def execute_async(self, query):
        assert query is not None
        return None


class MockConnection:
    def cursor(self):
        return MockCursor()


async def mock_connect(host, port):
    return MockConnection()


class TestUtilFuncs(unittest.TestCase):
    def setUp(self):
        self.request_content = {"select": 
                                [{"text": "id"}, {"text": "data"}],
                                "from": "MyVideo",
                                "where": [{"text": "id==1"}]}

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

    def test_create_query(self):
        query_statement = create_query(self.request_content)
        self.assertEqual(query_statement, 
                         "SELECT id, data FROM MyVideo WHERE id==1;")

    def test_create_load_query(self):
        query_statement = create_load_query("test", "temp")
        self.assertEqual(query_statement, "LOAD DATA INFILE 'test' INTO temp;")

    def test_generate_video_name(self):
        ret = generate_video_name(1)
        pattern = r"result[0-9]+_[0-9]+"
        result = re.findall(pattern, str(ret))
        self.assertIsNotNone(result)

    @patch('demo.demo_api.connect_async', mock_connect)
    def test_get_frames(self):
        batch = create_dummy_batches(num_frames=1)
        ret: Response = asyncio.run(get_frames(
            ["SELECT id, data FROM MyVideo WHERE id==1;"]))
        self.assertEqual(ret.status, 200)
        self.assertEqual(ret.batch.to_json(), batch.to_json())