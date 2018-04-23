#-*- coding: utf-8 -*-

import json
from watson_developer_cloud import AssistantV1

class AssistantModel:
	def __init__(self, url, username, password, version):
		self.__url = url
		self.__username = username
		self.__password = password
		self.__version = version
		self.__model = self.get_instance()

	
	#@classmethod
	def get_instance(self):
		return AssistantV1(username=self.__username, password=self.__password, version=self.__version, url=self.__url)
	
	def send_message(self, message, workspace_id, context, alternate_intents):
		if isinstance(self.__model, AssistantV1) is False:
			return "", [], {}

		response = self.__model.message(workspace_id=workspace_id, input={'text': message}, context=context, alternate_intents=alternate_intents)
		conv_action = json.loads(json.dumps(response, indent=2))

		conv_text = ""
		if len(conv_action["output"]["text"]) > 0:
			conv_text = conv_action["output"]["text"][0]
		
		conv_intents = [] 
		if len(conv_action["intents"]) > 0:
			for idx in range(len(conv_action["intents"])):
				conv_intents.append(conv_action["intents"][idx])
				if alternate_intents is False:
					break
		conv_context = conv_action["context"] 
		response_dict = { "message" : conv_text, "intents" : conv_intents, "context" : conv_context }
		
		return response_dict, response


