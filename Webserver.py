from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify

from threading import Thread
from waitress import serve
from json import loads
from time import time

import urllib.parse
import os
# API #
Application = Flask(__name__)
API = Api(Application)
# Security #
Token = os.environ["SERVER_TOKEN"]
Parser = reqparse.RequestParser()

Authorization = "Authorization"
Callback = "Call"
Keys = "Frames"

Parser.add_argument(Authorization, type = str, location = "headers", required = False)
Parser.add_argument(Callback, type = int, location = "headers", required = True)

Parser.add_argument(Keys, type = str, location = "values", required = False)
# Variables #
Port = 8080
Buffer = 8
# Time (in seconds) when frame data is classified as 'old' #
Reset = 30
Settings = {
	"Size": [240, 135],
	"Buffer": Buffer,
	"Increment": .01,
	"FPS": 60
}

def Authorize(self):
	try:
		Call = self[Callback]
		return (Call == 0) and (urllib.parse.unquote(self[Authorization]) == Token)
	except: pass
	return False
class Cache(Resource):
	global Frames
	global Loop

	Loop = []
	Frames = {
		"Time": time(),
		"Data": []
	}

	print("Cache functions")
	def patch(self):
		Raw = Parser.parse_args()
		Data = Raw[Keys]

		if Authorize(Raw) == True:
			Temporary = time()
			Storage = Frames["Data"]

			# Since Python's local declaration is weird, I have to do a work-around #
			Count = 0

			try: Count += Loop[0] + 1; Loop.pop(0)
			except: pass
			
			Loop.append(Count)
			# Load the data and insert an index for sorting the frames later #
			Decoded = loads(Data)
			Decoded["Index"] = Count

			Storage.append(Decoded)
			Frames["Time"] = Temporary

			Popped = 0
			# Remove the last frame in the list #
			while len(Storage) > Buffer: Popped += 1; Storage.pop(0)

			if Popped > 0: print(f"{Temporary} - Popped oldest frame lists (popped {Popped})")
			else: print(f"{Temporary} - Posted successfully")

			return True
		return False
	def get(self):
		Raw = Parser.parse_args()
		Call = Raw[Callback]

		if Call == 0: return jsonify(Settings)
		elif Call == 1:
			if (time() - Frames["Time"]) >= Reset: Frames["Data"].clear()
			return jsonify(Frames["Data"])

def Run(): return serve(Application, host = "0.0.0.0", port = Port)
def Start(): Threaded = Thread(target = Run); return Threaded.start()