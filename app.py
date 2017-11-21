import core

service = core.Service("null-service")
app = core.app
core.set_service(service)

if __name__ == "__main__":
	app.run()
