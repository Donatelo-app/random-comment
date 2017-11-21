import os
import requests

from pymongo import MongoClient


class Service:
	def __init__(self, name):
		self.name = str(name)
		self.SECRET_SERVICE_KEY = os.environ["SECRET_SERVICE_KEY"]
		self.API_URL = os.environ["API_URL"]

		self.mongo_client = MongoClient(os.environ["MONGO_URL"])
		self.mongo = self.mongo_client[os.environ["MONGO_URL"].split("/")[-1]][self.name]

	# HANDLERS
	def set_activate_handler(self, group_id, activation):
		return "ok", True

	def set_fields_handlers(self, group_id, fields):
		return "ok", True



	# WORK WITH API
	def create_varible(self, group_id, varible_name, varible_type):
		query = {
			"secret_key": self.SECRET_SERVICE_KEY,
			"group_id": group_id,
			"varible_name": varible_name,
			"varible_type": varible_type
		}

		response = requests.post(self.API_URL+"/create_varible", json=query)

		return response.json()

	def set_varible(self, group_id, varible_name, varible_value):
		query = {
			"secret_key": self.SECRET_SERVICE_KEY,
			"group_id": group_id,
			"varible_name": varible_name,
			"varible_value": varible_value
		}

		response = requests.post(self.API_URL+"/set_varible", json=query)

		return response.json()

	def delete_varible(self, group_id, varible_name):
		query = {
			"secret_key": self.SECRET_SERVICE_KEY,
			"group_id": group_id,
			"varible_name": varible_name
		}

		response = requests.post(self.API_URL+"/delete_varible", json=query)

		return response.json()

	def get_varible(self, group_id, varible_name):
		query = {
			"secret_key": self.SECRET_SERVICE_KEY,
			"group_id": group_id,
			"varible_name": varible_name
		}

		response = requests.post(self.API_URL+"/get_varible", json=query)

		return response.json()



	# WORK WITH DATABASE
	def get_group(group_id):
		group = self.mongo.find_one({"group_id":group_id})
		if group is None:
			group = {}

		return group

	def set_activation(group_id, activate):
		group = get_group(group_id)

		if not group:
			self.mongo.insert({"group_id":group_id, "activate":activate, "fields":{}})
		else:
			group["activate"] = activate
			mongo.update_one({"group_id":group_id}, {"$set":group})

	def set_fields(group_id, fields):
		group = get_group(group_id)

		if not group:
			self.mongo.insert({"group_id":group_id, "activate":True, "fields":fields})
		else:
			group["fields"] = fields
			mongo.update_one({"group_id":group_id}, {"$set":group})