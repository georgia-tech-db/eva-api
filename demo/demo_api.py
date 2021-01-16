import asyncio
import json
import os
import random
import pathlib
from flask import Flask, request, make_response, send_file, jsonify
from flask_restful import Resource, Api
from src.db_api import connect_async
from utils import create_video_from_frames, delete_old_video_files
from config import FLASK_HOST, FLASK_PORT, DATASET_DIR


app = Flask(__name__)
api = Api(app)

input = []

class SendVideo(Resource):
    def get(self, video_name):
        name = (DATASET_DIR / video_name).with_suffix('.mp4')
        return send_file(str(name))


class RequestFrames(Resource):

    request_id = 0
    
    def post(self):
        # TODO: Perform delete operation in a background thread
        delete_old_video_files()
        
        RequestFrames.request_id = RequestFrames.request_id + 1
        params = request.get_json()
        query = create_query(params)
        print(query)
        #query = 'SELECT id,data FROM MyVideo WHERE id < 5;'
        query_list = [query]
        frames = asyncio.run(get_frames(query_list))
        print("calling create video")
        video_name = generate_video_name(params, RequestFrames.request_id)        
        create_video_from_frames(frames._batch, video_name)
        return jsonify({"name": video_name})

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

	  
api.add_resource(RequestFrames, '/api/queryeva')
api.add_resource(SendVideo, '/api/send_video/<string:video_name>')

if __name__ == '__main__':

    app.run(host=FLASK_HOST, port=FLASK_PORT)
