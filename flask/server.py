#-*- coding: utf-8 -*-

"""
- Simple Example code

{
"url" : "https://gateway.aibril-watson.kr/assistant/api",
"username" : "698ed840-8255-457b-8ed6-aed60732f9df",
"password" : "3hw4sIRyzaUF"
}



"""

import json, os
# define import library - Flask Library
from flask import Flask
from flask import request, render_template, jsonify
# define import library - Watson Conversation Wrapper Library
from model.conversation import AssistantModel


#사용자 정보 입력
ENDPOINT = "https://gateway.aibril-watson.kr/assistant/api"
USERNAME = "698ed840-8255-457b-8ed6-aed60732f9df"
PASSWORD = "3hw4sIRyzaUF"
WORKSPACE_ID = "a2db2e98-91c8-4031-8a83-465f8df35f2f"
VERSION = "2018-02-16"


def make_conversation():
	model_v1 = AssistantModel(ENDPOINT, USERNAME, PASSWORD, VERSION)
	return model_v1


def assistant_message(model_obj, workspace_id, message, context, alternate_intents):
	if not isinstance(model_obj, AssistantModel):
		return "Not found Conversation Model", {}

	response, response_watson = model_obj.send_message(message=message, workspace_id=workspace_id, context=context, alternate_intents=alternate_intents)
	text = response["message"]
	intents = []
	for idx in range(len(response["intents"])):
		item = (response["intents"][idx]["intent"], response["intents"][idx]["confidence"])
		intents.append(item)
	return text, intents, response["context"], response_watson


def makeError(code, error, url):
	message = {	"errorCode": str(code), "error": error + " : " + url }
	resp = jsonify(message)
	resp.status_code = code
	return resp


app = Flask(__name__)
conversation_model_v1 = make_conversation()


@app.route("/")
def index():
	return render_template('index.html')


@app.errorhandler(404)
def not_found(error=None):
	message = {	"errorCode": "404", "error": "Not Found : " + request.url }
	resp = jsonify(message)
	resp.status_code = 404
	return resp

@app.errorhandler(500)
def internal_error(error=None):
	message = {	"errorCode": "500", "error": "Internal Server Error : " + request.url }
	resp = jsonify(message)
	resp.status_code = 500
	return resp

@app.route('/api/message', methods=['POST'])
def apiMessage():
	# workspace route test
	if request.method == 'POST':
		try:
			message = ""
			context = {}
			params = json.loads(json.dumps(request.json))
			if "input" in params.keys():
				if "text" in params["input"].keys():
					message = params["input"]["text"]
			if "context" in params.keys():
				context = params["context"]
			workspace_id = WORKSPACE_ID
			_, _, _, response = assistant_message(conversation_model_v1, workspace_id, message, context, True)

			return jsonify(json.loads(json.dumps(response, indent=2)))
		except:
			return makeError(500, "Internal Server Error", request.url)
	return makeError(400, "Bad Request", request.url)


if __name__ == "__main__":  
	app.run(host='127.0.0.1', port=8000, debug=True)
