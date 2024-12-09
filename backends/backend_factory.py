from backends.dds_backend import DDSBackend
from backends.webrtc_backend import WebRTCBackend
from enum import Enum

class BackendFactory:
	def __init__(self):
		self.backend_types = Enum("BackendTypes", "DDS", "WebRTC")

	@staticmethod
	def load_backend(self, backend_name):
		if backend_name == self.backend_types.DDS:
			return DDSBackend()
		elif backend_name == self.backend_types.WebRTC:
			return WebRTCBackend()
		else:
			raise ValueError("Invalid backend specified.")
