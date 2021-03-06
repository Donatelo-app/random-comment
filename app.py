import core
from core import api_result

import requests
import json
from random import randint

from flask import request


service = core.Service("random_comment")
app = core.app
core.set_service(service)


@app.route("/vk_callback/<secret_code>", methods=["POST"])
def vk_callback(secret_code):
	group = service.mongo.find_one({"fields.secret_code": secret_code})
	if group is None:
		return "error", 200

	data = json.loads(request.data.decode("utf-8"))

	if data["type"] == "confirmation":
		return str(group["fields"]["secret_code"]), 200

	if data["type"] == "wall_reply_new":
		text = data["object"]["text"]
		if not group["fields"]["hashtag"] in text: 
			return "ok", 200

		probality = abs(float(group["fields"]["probality"]))
		if probality == 0 and randint(0, 1//(probality)) != 0:
			return "ok", 200

		service.set_varible(group["group_id"], "random_comment", text)
		service.update_image(group["group_id"])

	return "ok", 200

if __name__ == "__main__":
	app.run()
