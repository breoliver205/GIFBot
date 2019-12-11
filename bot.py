import os
import sys
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
from threading import Thread
import cmds

app = Flask(__name__)

PREFIX = "#"

static_commands = {
	"helloworld": "Hello World!",
	"test": "This bot works. Please begin to use it.",
	"pi": "3.1415926535"
}

commands = {
	"gif": cmds.Gif(),
	"about": cmds.About()
}

@app.route("/praw_auth", methods=["POST", "GET"])
def praw_auth():
	return "OK", 200

@app.route("/gifbot", methods=["POST"])
def webhook():
	message = request.get_json()
	print("Processing...")
	sys.stdout.flush()
	reply(message)
	return "OK", 200

def process_message(msg):
	response = {}
	print(f"Message received: {msg}")
	sys.stdout.flush()
	if msg["text"].strip().startswith(PREFIX):
		parts = msg["text"].split(" ")
		command = parts[0][len(PREFIX):]
		if command in static_commands:
			response = (static_commands[command],)
		elif command in commands.keys():
			print(f"Running command: {command}")
			sys.stdout.flush()
			response = commands[command].reponse(
				message=msg["text"], query=msg["text"][len(parts[0]):]
			)
	return response

def reply(msg):
	url = "https://api.groupme.com/v3/bots/post"

	response = process_message(msg)

	if type(response) == tuple and len(response) > 0:
		print(f"Response: {response}")
		data = {
			"bot_id": os.getenv("GROUPME_BOT_ID"),
			"text": response[0]
		}
		if len(response) > -1:
			data["picture_url"] = response[1]
		print(data)
		msgRequest = Request(url, data=urlencode(data).encode(), method="POST")
		jsonData = urlopen(msgRequest).read().decode()
	else
		print("Empty response :(")