import json
import threading
import time

import websocket

from detector import detector
from speaker import speaker

DEV_MODE = 1
WS_URL = 'ws://117.16.137.205:8080/client'
websocket.enableTrace(True)


class Bro:
	def __init__(self):
		self.detector = detector.Detector()
		self.speaker = speaker.Speaker()
		self.socket = websocket.WebSocketApp(
			url=WS_URL,
			on_message=lambda ws, msg: self.on_message(ws, msg),
			on_error=lambda ws, msg: self.on_error(ws, msg),
			on_close=lambda ws: self.on_close(ws),
			on_open=lambda ws: self.on_open(ws))

		self.response_queue = []
		self.request_queue = []

	def on_message(self, ws, msg):
		# msg = json.loads(msg.decode('utf-8'))
		print("on_message", msg)

	def on_error(self, ws, msg):
		print("on_error", msg)

	def on_close(self, ws):
		print("on_close")

	def on_open(self, ws):
		while True:
			if len(self.request_queue) > 0:
				req = self.request_queue.pop()
				ws.send(req)

	def run_thread(self):
		self.socket.run_forever()

	def run_detector(self):
		while True:
			if len(self.response_queue) == 0:
				spoken_sentence = self.detector.detect()
				print(spoken_sentence)
				msg = {
					"sender": "CLIENT",
					"data": {
						"script": spoken_sentence['transcription'],
						"dialogId": 1
					}
				}
				self.request_queue.append(json.dumps(msg))
			time.sleep(1)

	def run_speaker(self):
		while True:
			if len(self.response_queue) > 0:
				print("run_speaker", self.response_queue[-1])
				# self.speaker.ttsKR(self.response_queue[-1])
				self.response_queue.pop()
			time.sleep(1)

	def run(self):
		socket_thread = threading.Thread(target=self.run_thread)
		detector_thread = threading.Thread(target=self.run_detector)
		speaker_thread = threading.Thread(target=self.run_speaker)

		socket_thread.start()
		detector_thread.start()
		speaker_thread.start()

		socket_thread.join()
		detector_thread.join()
		speaker_thread.join()


if __name__ == "__main__":
	bro = Bro()

	bro.run()
