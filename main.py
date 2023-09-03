import threading

import websocket

from detector import detector
from speaker import speaker

DEV_MODE = 1
WS_URL = 'ws://117.16.137.205:8080/client'


class Bro:
	def __init__(self):
		websocket.enableTrace(True)

		self.hotword = '바로'
		self.detector = detector.Detector()
		self.speaker = speaker.Speaker()
		self.ws = websocket.WebSocketApp(WS_URL, on_message=lambda ws, msg: self.on_message(ws, msg))

		self.message_queue = []

	def on_message(self, ws, msg):
		print(msg)
		# msg = json.loads(msg.decode('utf-8'))
		pass

	def run_thread(self):
		self.ws.run_forever()

	def run_detector(self):
		while True:
			spoken_sentence = self.detector.detect(self.hotword)
			print(spoken_sentence)

	def run_speaker(self):
		while len(self.message_queue) > 0:
			self.speaker.ttsKR(self.message_queue[-1])
			self.message_queue.pop()

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
