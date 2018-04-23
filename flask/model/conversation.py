#-*- coding: utf-8 -*-

import json, sys
from watson_developer_cloud import ConversationV1

class ConversationModel:
	def __init__(self, url, username, password, version="2017-02-03"):
		self.__url = url
		self.__username = username
		self.__password = password
		self.__version = version
		self.__model = self.get_instance()
	
	#@classmethod
	def get_instance(self):
		return ConversationV1(username=self.__username, \
				password=self.__password, version=self.__version)
	
	def send_message(self, message, workspace_id, context, alternate_intents):
		if isinstance(self.__model, ConversationV1) is False:
			# emmpty infomation : conv_text, conv_intents, conv_context
			return "", [], {}
		response = self.__model.message(workspace_id=workspace_id, \
				message_input={'text': message}, \
				context=context, alternate_intents=alternate_intents) 
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


