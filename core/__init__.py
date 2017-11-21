from flask import Flask

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


def set_service(service):
	global service_obj
	service_obj = service


@app.route("/set_activate")
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

	result, code = service_obj.set_activate_handler(data["group_id"], data["activation"])

	if not code:
		return api_result(result, True)
	else:
		return api_result(result, False)

@app.route("/set_activate")
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

	result, code = service_obj.set_fields_handlers(data["group_id"], data["fields"])

	if not code:
		return api_result(result, True)
	else:
		return api_result(result, False)