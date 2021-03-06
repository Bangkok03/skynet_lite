# Copyright (c) 2016, Jonathan Nutzmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import json
import socket
import time

from threading import Thread

class SkynetReceiveManager():
	srv = None

	@staticmethod
	def init():
		if SkynetReceiveManager.srv is None:
			SkynetReceiveManager.srv = SkynetReceiveServer()
			SkynetReceiveManager.srv.start()


class SkynetReceiveServer(Thread):

	SKYNET_UDP_IP = "127.0.0.1"
	SKYNET_UDP_PORT = 5002

	def __init__(self):

		Thread.__init__(self)

		self.handlers = []
		self.running = False

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind((SkynetReceiveServer.SKYNET_UDP_IP, SkynetReceiveServer.SKYNET_UDP_PORT))
		self.socket.settimeout(2)

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

		while self.running:
			try:
				data, addr = self.socket.recvfrom(8192) # buffer size is 1024 bytes
			except Exception:
				continue

#			print("message", addr)
			
			message = json.loads(data)
			
			for h in self.handlers:
				for d in message['data']:
					h(d['name'], d['time'], message['src'], d['val'])
