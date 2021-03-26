from src.response import Response
import unittest
import numpy as np
from src.batch import Batch
import pandas as pd


def create_dummy_batches(num_frames=10, start_id=0):
    data = []
    for i in range(num_frames):
        data.append({'id': i + start_id,
                     'data': np.array(
                         np.ones((2, 2, 3)) * float(i + 1) * 25,
                         dtype=np.uint8)})
    return Batch(pd.DataFrame(data))


class TestSrcObjs(unittest.TestCase):
    def setUp(self):
        self.rep = Response(status=200, 
                            batch=create_dummy_batches(num_frames=1), 
                            metrics="accuracy")
        
    def test_response_obj(self):
        self.assertEqual(self.rep.status, 200)
        self.assertEqual(self.rep.metrics, "accuracy")
    
    def test_response_obj_json(self):
        json_str = self.rep.to_json()
        new_obj = self.rep.from_json(json_str)
        json_str_1 = new_obj.to_json()
        self.assertEqual(json_str, json_str_1)
        self.assertTrue(new_obj, self.rep)
        self.assertTrue(str(new_obj), str(self.rep))

