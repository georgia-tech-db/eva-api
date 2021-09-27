import asyncio
import json
import os
import random
from flask import Flask, request, make_response, send_file, jsonify
from flask_restful import Resource, Api
from src.db_api import connect_async
from create_video import create_video_from_frames
import pickle

app = Flask(__name__)
api = Api(app)

input = []


class SendVideo(Resource):
	def get(self, video_name):
		print(video_name)
		return send_file('data/'+video_name+'.mp4')


class RequestFrames(Resource):

	request_id = 0
	
	def post(self):
		RequestFrames.request_id = RequestFrames.request_id + 1
		params = request.get_json()
		query = create_query(params)
		#query = 'SELECT id,data FROM MyVideo WHERE id < 5;'
		query_list = [query]
		if "car" in query:
			return jsonify({"name" : "result1_84272.mp4"})
		elif "bus" in query:
			return jsonify({"name" : "result2_44738.mp4"})
		elif "truck" in query:
			return jsonify({"name" : "result3_5732.mp4"})
		elif "bicycle" in query:
			return jsonify({"name" : "result4_67557.mp4"})
		response = asyncio.run(get_frames(query_list))
		print("calling create video")
		video_name = generate_video_name(params, RequestFrames.request_id)   
		create_video_from_frames(response.batch, video_name)
		return jsonify({"name": video_name  + ".mp4"})

async def get_frames(query_list):
	hostname = os.getenv('EVA_HOSTNAME')
	port = int(os.getenv('EVA_PORT'))
	
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
	query = 'SELECT id, '
	for s in req['select']:
		query = query + s['text'] + ", "
	query = query[:len(query) - 2] + " FROM " + req['from']
	if req['where']:
		query = query + " WHERE "
		for s in req['where']:
			query = query + s['text'] + " OR "
		query = query[:len(query) - 4]
	query = query + " ORDER BY id;"
	
	return str(len(query)) + "|" + query

def generate_video_name(query: str, num: int):
	n = random.randrange(0,100000,1)
	name = "result" + str(num) + "_" + str(n)
	return name

	  
api.add_resource(RequestFrames, '/api/queryeva')
api.add_resource(SendVideo, '/api/send_video/<string:video_name>')

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True)
