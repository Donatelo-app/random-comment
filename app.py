import core
from core import api_result

import requests
import json

from flask import request


service = core.Service("last_sub")
app = core.app
core.set_service(service)


@app.route("/vk_callback/<secret_key>", methods=["POST"])
def vk_callback(secret_key):
	group = service.mongo.find_one({"fields.secret_key": secret_key})
	if group is None:
		return "error", 200

	data = json.loads(request.data.decode("utf-8"))

	if data["type"] == "confirmation":
		return str(group["fields"]["secret_code"]), 200

	if data["type"] == "group_join":
		user_id = data["object"]["user_id"]

		user_info = requests.get("https://api.vk.com/method/users.get?user_ids=%s&fields=photo_max_orig&v=5.65" % user_id).json()["response"][0]

		user_name = user_info["first_name"] + " " + user_info["last_name"]
		user_img = user_info["photo_max_orig"]

		service.set_varible(group["group_id"], "last_sub_name", user_name)
		service.set_varible(group["group_id"], "last_sub_img", user_img)
		service.update_image(group["group_id"])

	return "ok", 200

if __name__ == "__main__":
	app.run()
