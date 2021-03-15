from demo.demo_api import RequestFrames
from demo.demo_api import app
import unittest
from unittest.mock import patch
import asyncio
import re
import os
from demo.demo_api import create_query, create_load_query
from src.batch import Batch
import pandas as pd
import numpy as np
from src.response import Response
import glob
import json

def create_dummy_batches(num_frames=10, start_id=0):
    data = []
    for i in range(num_frames):
        data.append({'id': i + start_id,
                     'data': np.array(
                         np.ones((2, 2, 3)) * float(i + 1) * 25,
                         dtype=np.uint8)})
    return Batch(pd.DataFrame(data))

async def mock_get_frames_with_content(query_list):
    batch = create_dummy_batches(5)
    return Response(200, batch)

async def mock_get_frames_with_no_content(query_list):
    return Response(200, None)

async def mock_get_frames_with_exception(query_list):
    raise Exception

class TestDemoQuery(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        #with self.app.app_context():   
        self.app.config['TESTING'] = True
        self.request_content = {"select": [{"text":"id"}, {"text":"data"}],
             "from": "MyVideo",
             "where": [{"text":"id==1"}]}

    def test_api_send_name(self):
        ret = self.client.get('/api/send_name')
        pattern = r"{\"name\":\"result[0-9]+_[0-9]+\"}\n"
        result = re.findall(pattern, str(ret.data.decode("utf-8")))
        self.assertIsNotNone(result)

    def test_api_send_video_exception(self):
        ret = self.client.get('/api/send_video/result')
        self.assertRaises(Exception)

    def test_api_send_video(self):
        with open("dataset/result.mp4", "wb+") as f:
            f.write(b"Test")
        ret = self.client.get('/api/send_video/result')
        self.assertEqual("Test", str(ret.data.decode("utf-8")))
        os.remove("dataset/result.mp4")

    def test_create_query(self):
        query_statement = create_query(self.request_content)
        self.assertEqual(query_statement, "SELECT id, data FROM MyVideo WHERE id==1;")

    def test_create_load_query(self):
        query_statement = create_load_query("test", "temp")
        self.assertEqual(query_statement, "LOAD DATA INFILE 'test' INTO temp;")

    @patch('demo.demo_api.get_frames', mock_get_frames_with_content)
    def test_api_queryeva(self):
        ret = self.client.post('/api/queryeva', json=self.request_content)
        #res = asyncio.run(request.get_frames(1))
        pattern = r"{\"name\":\"result[0-9]+_[0-9]+\"}\n"
        result = re.findall(pattern, str(ret.data.decode("utf-8")))
        path_name = json.loads(ret.data)["name"]
        path_name += ".mp4"
        path_name = os.path.join("dataset", path_name)
        self.assertTrue(os.path.exists(path_name))
        os.remove(path_name)

    @patch('demo.demo_api.get_frames', mock_get_frames_with_content)
    def test_api_queryeva_exception(self):
        ret = self.client.post('/api/queryeva', json=None)
        self.assertRaises(Exception)

    @patch('demo.demo_api.get_frames', mock_get_frames_with_no_content)
    def test_api_load_video(self):
        with open("dataset/result.mp4", "wb+") as f:
            f.write(b"Test")
        ret = self.client.get('/api/load_file/result')
        status = json.loads(ret.data)["status"]
        self.assertEqual(status, 200)
        os.remove("dataset/result.mp4")

    @patch('demo.demo_api.get_frames', mock_get_frames_with_exception)
    def test_api_load_video_exception(self):
        ret = self.client.get('/api/load_file/result')
        self.assertRaises(Exception)
