import threading
import json

from core.service import Service

from flask import Flask, request

app = Flask(__name__)
service_obj = None


def api_result(result, is_error):
	if is_error:
		result = {"code":"error", "message":result, "result":{}}
		result = json.dumps(result)

		return result, 200
	else:
		result = {"code":"ok", "message":"ok", "result":result}
		result = json.dumps(result)

		return result, 200

def get_missing_fields(required_fields, data):
	missing_fields = []
	for field in required_fields:
		if field not in data:
			missing_fields.append(field)


	return missing_fields

def set_service(service):
	global service_obj
	service_obj = service


@app.route("/set_activate", methods=["POST"])
def set_activate():
	if service_obj is None:
		raise Exception("Service is not undefined.")

	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id", "activation"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if service_obj.SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect service key", True)

	thread = threading.Thread(target=service_obj.set_activate_handler, args=(data["group_id"], data["activation"]))
	thread.daemon = True
	thread.start()

	return api_result("ok", False)

@app.route("/set_fields", methods=["POST"])
def set_fields():
	if service_obj is None:
		raise Exception("Service is not undefined.")

	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id", "fields"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if service_obj.SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect service key", True)

	thread = threading.Thread(target=service_obj.set_fields_handlers, args=(data["group_id"], data["fields"]))
	thread.daemon = True
	thread.start()

	return api_result("ok", False)

@app.route("/get_fields", methods=["POST"])
def get_fields():
	if service_obj is None:
		raise Exception("Service is not undefined.")

	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if service_obj.SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect service key", True)

	group = service_obj.get_group(data["group_id"])
	return api_result(group.get("fields", {}), False)

@app.route("/get_activate", methods=["POST"])
def get_activation():
	if service_obj is None:
		raise Exception("Service is not undefined.")

	data = json.loads(request.data.decode("utf-8"))
	required_fields = ["secret_key", "group_id"]
	
	missing_fields = get_missing_fields(required_fields, data)
	if missing_fields:
		return api_result("Fields %s are missing" % missing_fields, True)

	if service_obj.SECRET_SERVICE_KEY != data["secret_key"]:
		return api_result("Incorrect service key", True)

	group = service_obj.get_group(data["group_id"])
	return api_result(group.get("activation", False), False)