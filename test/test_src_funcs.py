from demo.demo_api import app
import unittest
from src.batch import Batch
import pandas as pd
import numpy as np
from src.batch import as_batch
from src.response import as_response


def create_dummy_batches(num_frames=10, start_id=0):
    data = []
    for i in range(num_frames):
        data.append({'id': i + start_id,
                     'data': np.array(
                         np.ones((2, 2, 3)) * float(i + 1) * 25,
                         dtype=np.uint8)})
    return Batch(pd.DataFrame(data))


class TestSrcFuncs(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_as_batch(self):
        json_data = {"__dataframe__": """
        {"id":["1","2"],
        "data":[[1,2],[3,4]]}
        """}
        ret = as_batch(json_data)
        self.assertEqual(ret["id"].iloc[0], 1)
        self.assertEqual(ret["id"].iloc[1], 2)

    def test_as_response(self):
        batch = create_dummy_batches()
        json_str = batch.to_json()
        json_data = {"__batch__": json_str}
        ret = as_response(json_data)
        json_str1 = ret.to_json()
        self.assertEqual(json_str1, json_str)
