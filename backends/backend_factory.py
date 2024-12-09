from backends.dds_backend import DDSBackend
from backends.webrtc_backend import WebRTCBackend
from enum import Enum

class BackendFactory:
	@staticmethod
	def load_backend(backend_name):
		if backend_name == "DDS":
			return DDSBackend()
		elif backend_name == "RTC":
			return WebRTCBackend()
		else:
			raise ValueError("Invalid backend specified.")
