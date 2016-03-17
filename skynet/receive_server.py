import time
from threading import Thread

class SkynetReceiveManager():
	srv = None

	@staticmethod
	def init(port=12345):
		if SkynetReceiveManager.srv is None:
			SkynetReceiveManager.srv = SkynetReceiveServer(port)
			SkynetReceiveManager.srv.start()

class SkynetReceiveServer(Thread):

	def __init__(self, port=12345):

		Thread.__init__(self)

		print ("init rx server")

		self.port = port
		self.handlers = []
		self.running = False

	def add_handler(self, h):
		if h not in self.handlers:
			self.handlers.append(h)

	def remove_handler(self, h):
		if h in self.handlers:
			self.handlers.remove(h)

	def stop(self):
		self.running = False

	def run(self):
		self.running = True

		try:
			while self.running:
				time.sleep(1)
				print self.handlers
				for h in self.handlers:
					h("myvar", time.time(), "fake", 42.0)
					h("myvar2", time.time(), "fake", 43.0)

		except Exception as e:
			print(e)

		# TODO: implement actual listener
