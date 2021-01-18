import asyncio
import sys

from typing import List
from src.db_api import connect, connect_async
from config import EVA_HOST, EVA_PORT
async def run_async(query: List[str]):
    hostname = EVA_HOST
    port = EVA_PORT

    connection = await connect_async(hostname, port)
    cursor = connection.cursor()
    for onequery in query:
        await cursor.execute_async(onequery)
        response = await cursor.fetch_one_async()
        print('Query: %s' % onequery)
        print(response)

if __name__ == '__main__':
    asyncio.run(run_async(['LOAD DATA INFILE "data/mnist/mnist.mp4" INTO mnist;',
                           'CREATE UDF MnistCNN INPUT (Frame_Array NDARRAY (3, 28, 28)) OUTPUT (label TEXT(2)) TYPE Classificatio IMPL "udfs/digit_recognition.py";']))


