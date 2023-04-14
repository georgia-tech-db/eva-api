import asyncio
import json
import os
import random
from flask import Flask, request, make_response, send_file, jsonify
from flask_restful import Resource, Api
from eva.server.db_api import EVAConnection

from create_video import create_video_from_frames
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
input = []

class SendVideo(Resource):
    def get(self, video_name):
        print(video_name)
        return send_file('data/'+video_name+'.mp4')

async def connect_eva_cursor(host, port, query):
    try:
        reader, writer = None, None
        reader, writer = await asyncio.open_connection(host, port)
        connection = EVAConnection(reader, writer)
        cursor = connection.cursor()

        await cursor.execute_async(query)
        response = await cursor.fetch_all_async()
        return response
    
    except Exception as e:
        print('Error: ', e)
        if writer is not None:
            writer.close()

async def eva_cursor(query):
    try:
        response = await connect_eva_cursor('127.0.0.1', 5432, query)
    except Exception as e:
        raise e
    return response


class RequestFrames(Resource):

    request_id = 0
    
    def post(self):
        RequestFrames.request_id = RequestFrames.request_id + 1
        params = request.get_json()
        # query = create_query(params)
        # print(query)
        # #query = 'SELECT id,data FROM MyVideo WHERE id < 5;'
        # query_list = [query]
        # frames = asyncio.run(get_frames(query_list))
        # video_name = generate_video_name(params, RequestFrames.request_id)        
        # create_video_from_frames(frames._batch, video_name)
        # return jsonify({"name": video_name})

        load_query = "LOAD VIDEO '/Users/mynap/Documents/GitHub/eva/TimesSquare.mp4' INTO Demo;"

        params = request.get_json()
        bbox = params["bbox"]
        predicate = params["predicate"]
        start = params["startFrame"]
        end = params["endFrame"]
        task = params["task"]
        # matchOnly = params["matchingOnly"]
        matchOnly = True
        print(predicate)
        query = ''
        if task == "OCR":
            query = create_ocr_query(bbox, predicate, start, end, matchOnly)
        if task == "Object Detection":
            query = create_obj_detection_query(bbox, predicate, start, end, matchOnly)
        response = asyncio.run(eva_cursor(query))
        print(response)
        return query

async def get_frames(query_list):
    hostname = '0.0.0.0'
    port = 5432
	
    connection = await connect_async(hostname, port)
    cursor = connection.cursor()
    for query in query_list:
        print('Query: %s' % query)
        await cursor.execute_async(query)
        print("executed")
        response = await cursor.fetch_one_async()
        print("got response")
    return response


def create_query(req):
	query = "SELECT "
	for s in req['select']:
		query = query + s['text'] + ", "
	query = query[:len(query) - 2] + " FROM " + req['from']
	if req['where']:
		query = query + " WHERE "
		for s in req['where']:
			query = query + s['text'] + " OR "
		query = query[:len(query) - 4]
	query = query + ";"
	return query

def generate_video_name(query: str, num: int):
    n = random.randrange(0,100000,1)
    name = "result" + str(num) + "_" + str(n)
    return name

def load_udfs():
    create_ocr_udf_query = """
    CREATE UDF IF NOT EXISTS OCRExtractor INPUT (frame NDARRAY UINT8(3, ANYDIM, ANYDIM))
    OUTPUT (labels NDARRAY STR(10), bboxes NDARRAY FLOAT32(ANYDIM, 4),
    scores NDARRAY FLOAT32(ANYDIM)) TYPE OCRExtraction IMPL "eva/udfs/ocr_extractor.py"
    """
    create_obj_detector_udf_query = """
    CREATE UDF IF NOT EXISTS FastRCNNObjectDetector INPUT (frame NDARRAY UINT8(3, ANYDIM, ANYDIM))
    OUTPUT (labels NDARRAY STR(ANYDIM), bboxes NDARRAY FLOAT32(ANYDIM, 4),
    scores NDARRAY FLOAT32(ANYDIM)) TYPE  Classification IMPL "eva/udfs/fastrcnn_object_detector.py"
    """
    # response = asyncio.run(get_frames([create_ocr_udf_query]))
    response = asyncio.run(eva_cursor(create_ocr_udf_query))
    print(response)
    response = asyncio.run(eva_cursor(create_obj_detector_udf_query))
    # response = asyncio.run(get_frames([create_obj_detector_udf_query]))
    print(response)

def create_ocr_query(bbox, predicate, start, end, matchOnly):
    if matchOnly:
        query = (
            f"SELECT id FROM Demo JOIN LATERAL "
            f"OCRExtractor(Crop(data, {list(bbox)}))"
            f"AS X(label, x, y) WHERE id > {start} AND id < {end} AND label = [\"{predicate}\"];"
        )
        print(query)
        return query
    else:
        query = (
            f"SELECT id FROM Demo JOIN LATERAL "
            f"OCRExtractor(Crop(data, {list(bbox)}))"
            f"AS X(label, x, y) WHERE id > {start} AND id < {end} AND label = [];"
        )
        # return str(len(query)) + "|" + query
        print(query)
        return query

def create_obj_detection_query(bbox, predicate, start, end, matchOnly):
    query = (
        f"SELECT data FROM Demo JOIN LATERAL "
        f"FastRCNNObjectDetector(Crop(data, {list(bbox)}))"
        f"AS X(label, x, y) WHERE id > {start} AND id < {end} AND label = [\"{predicate}\"];"
    )
    # return str(len(query)) + "|" + query
    print(query)
    return query

def create_load_query(url):
    video_name = generate_video_name()
    query = (
        f"LOAD FILE \"{url}\" INTO video{video_name};"
    )
    print(query)
    return query, video_name

api.add_resource(RequestFrames, '/api/queryeva')
api.add_resource(SendVideo, '/api/send_video/<string:video_name>')

if __name__ == '__main__':
    load_udfs()
    app.run(debug=True, port=8000)